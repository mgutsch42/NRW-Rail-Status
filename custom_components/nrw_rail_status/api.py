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


def _random_request_id(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _html_to_markdown(html: str) -> str:
    if not html:
        return ""
    text = unescape(html)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


class NRWMessage:
    """Einzelne HIM-Meldung als Python-Objekt mit Referenzauflösung."""

    def __init__(self, raw, common):
        self.raw = raw
        self.common = common

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

        self.category_refs = raw.get("catRefL", [])
        self.edge_refs = raw.get("edgeRefL", [])
        self.event_refs = raw.get("eventRefL", [])
        self.prod_refs = raw.get("affProdRefL", [])

        self.locations = self._resolve_locations()
        self.products = self._resolve_products()
        self.edges = self._resolve_edges()
        self.events = self._resolve_events()

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


class NRWHimApi:
    """Client für die HAFAS-HIM-API von Zuginfo.nrw."""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_messages(self):
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

        async with self.session.post(
            BASE_URL,
            json=payload,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "de-DE,de;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Origin": "https://www.zuginfo.nrw",
                "Referer": "https://www.zuginfo.nrw/",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Connection": "keep-alive",
            },
        ) as resp:

            if resp.status != 200:
                raise Exception(f"HAFAS returned HTTP {resp.status}")

            data = await resp.json()

        svc = data["svcResL"][0]["res"]
        raw_messages = svc.get("msgL", [])
        common = svc.get("common", {})

        return [NRWMessage(msg, common) for msg in raw_messages]
