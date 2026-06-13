"""API client for NRW Rail Status (Zuginfo.nrw / HAFAS HIM)."""

from __future__ import annotations

import aiohttp
import logging
import random
import string
import re
from html import unescape

BASE_URL = "https://zuginfo.nrw/him/HimSearch"
_LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def _random_request_id(length=8):
    """Erzeugt eine zufällige Request-ID wie im Browser."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _html_to_markdown(html: str) -> str:
    """Sehr einfache HTML→Markdown-Konvertierung."""
    if not html:
        return ""

    text = unescape(html)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


# ---------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------

class NRWMessage:
    """Einzelne HIM-Meldung als Python-Objekt mit Referenzauflösung."""

    def __init__(self, raw, common):
        self.raw = raw
        self.common = common

        # Grunddaten
        self.id = raw.get("hid")
        self.title = raw.get("head")
        self.text_html = raw.get("text")
        self.text = _html_to_markdown(self.text_html)

        self.active = raw.get("act", False)
        self.priority = raw.get("prio")
        self.product = raw.get("prod")
        self.comp = raw.get("comp")

        self.start_date = raw.get("sDate")
        self.start_time = raw.get("sTime")
        self.end_date = raw.get("eDate")
        self.end_time = raw.get("eTime")

        # Referenzen
        self.category_refs = raw.get("catRefL", [])
        self.edge_refs = raw.get("edgeRefL", [])
        self.event_refs = raw.get("eventRefL", [])
        self.prod_refs = raw.get("affProdRefL", [])

        # Aufgelöste Daten
        self.locations = self._resolve_locations()
        self.products = self._resolve_products()
        self.edges = self._resolve_edges()
        self.events = self._resolve_events()

    # ---------------------------------------------------------
    # Referenzauflösung
    # ---------------------------------------------------------

    def _resolve_locations(self):
        locL = self.common.get("locL", [])
        result = []

        for edge in self._resolve_edges():
            for loc_idx in [edge.get("from"), edge.get("to")]:
                if loc_idx is not None and 0 <= loc_idx < len(locL):
                    loc = locL[loc_idx]
                    result.append({
                        "name": loc.get("name"),
                        "id": loc.get("extId"),
                        "type": loc.get("type"),
                        "lat": loc.get("crd", {}).get("y"),
                        "lon": loc.get("crd", {}).get("x"),
                    })

        return result

    def _resolve_products(self):
        prodL = self.common.get("prodL", [])
        result = []

        for idx in self.prod_refs:
            if 0 <= idx < len(prodL):
                prod = prodL[idx]
                result.append({
                    "name": prod.get("name"),
                    "line": prod.get("line"),
                    "number": prod.get("number"),
                    "operator": prod.get("oprX"),
                })

        return result

    def _resolve_edges(self):
        edges = self.common.get("himMsgEdgeL", [])
        result = []

        for idx in self.edge_refs:
            if 0 <= idx < len(edges):
                edge = edges[idx]
                result.append({
                    "from": edge.get("fLocX"),
                    "to": edge.get("tLocX"),
                    "dir": edge.get("dir"),
                })

        return result

    def _resolve_events(self):
        events = self.common.get("himMsgEventL", [])
        result = []

        for idx in self.event_refs:
            if 0 <= idx < len(events):
                ev = events[idx]
                result.append({
                    "type": ev.get("type"),
                    "text": ev.get("txt"),
                    "time": ev.get("t"),
                })

        return result

    def __repr__(self):
        return f"<NRWMessage {self.id} {self.title}>"


# ---------------------------------------------------------
# API-Client
# ---------------------------------------------------------

class NRWHimApi:
    """Client für die HAFAS-HIM-API von Zuginfo.nrw."""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_messages(self):
        """Ruft die HIM-Meldungen ab und gibt eine Liste von NRWMessage zurück."""

        payload = {
            "req": {
                "ver": "1.24",
                "lang": "de",
                "auth": {"type": "AID", "aid": "hafas-nrw-app"},
                "client": {"id": "NRW", "type": "WEB", "name": "webapp"},
                "svcReqL": [{
                    "req": {
                        "himFltrL": [{"type": "PROD", "mode": "INC", "value": "0"}],
                        "getEdges": True,
                        "getEvents": True,
                        "getProds": True,
                        "getCats": True,
                    },
                    "meth": "HimSearch"
                }],
            },
            "id": _random_request_id(),
        }

        async with self.session.post(BASE_URL, json=payload) as resp:
            if resp.status != 200:
                raise Exception(f"HAFAS returned HTTP {resp.status}")

            data = await resp.json()

        try:
            svc = data["svcResL"][0]["res"]
            raw_messages = svc.get("msgL", [])
            common = svc.get("common", {})
        except Exception as err:
            raise Exception(f"Invalid HAFAS response: {err}")

        return [NRWMessage(msg, common) for msg in raw_messages]
