from __future__ import annotations

import aiohttp
import logging
import random
import string
import re
from html import unescape

BASE_URL = "https://www.zuginfo.nrw/him/HimSearch"
PRE_URL = "https://www.zuginfo.nrw/webapp/"

_LOGGER = logging.getLogger(__name__)
# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def _random_request_id(length=8):
    """Erzeugt eine zufällige Request-ID wie ein Browser."""
    import random
    import string
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def _html_to_markdown(html: str) -> str:
    """Konvertiert HTML aus HIM-Meldungen in reinen Text."""
    if not html:
        return ""
    from html import unescape
    import re

    text = unescape(html)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()
# ---------------------------------------------------------
# Datenmodell: NRWMessage
# ---------------------------------------------------------

class NRWMessage:
    """Repräsentiert eine einzelne HIM-Meldung aus Zuginfo.nrw."""

    def __init__(self, raw, common):
        self.raw = raw
        self.common = common

        # Basisdaten
        self.id = raw.get("hid")
        self.title = raw.get("head")
        self.text_html = raw.get("text")
        self.text = _html_to_markdown(self.text_html)

        # Status / Metadaten
        self.active = raw.get("act", False)
        self.priority = raw.get("prio")
        self.product = raw.get("prod")
        self.comp = raw.get("comp")

        # Zeitliche Angaben
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

    # -----------------------------------------------------
    # Auflösung von Referenzen
    # -----------------------------------------------------

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
# ---------------------------------------------------------
# API-Client: NRWHimApi (Teil 1)
# ---------------------------------------------------------

class NRWHimApi:
    """Client für die HAFAS-HIM-API von Zuginfo.nrw."""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def _prepare_session(self):
        """Lädt die Web-App wie ein Browser, um Session-Cookies zu erhalten."""

        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Accept-Encoding": "gzip, deflate, br, zstd",

            "Sec-CH-UA": "\"Microsoft Edge\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
            "Sec-CH-UA-Mobile": "?1",
            "Sec-CH-UA-Platform": "\"Android\"",

            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",

            "Priority": "u=1, i",

            "Origin": "https://www.zuginfo.nrw",
            "Referer": "https://www.zuginfo.nrw/",
        }

        async with self.session.get(PRE_URL, headers=headers) as resp:
            _LOGGER.debug("PRE_URL status: %s", resp.status)


    async def fetch_messages(self):
        """Holt HIM-Meldungen von Zuginfo.nrw."""

        # Schritt 1: PRE-Request (Cookies holen)
        await self._prepare_session()

        # Schritt 2: Request-Payload wie im Browser
        request_id = _random_request_id()

        payload = {
            "id": request_id,
            "ver": "1.24",
            "lang": "deu",
            "auth": {
                "type": "AID",
                "aid": "23lkjh63l456oisplergn",
            },
            "client": {
                "id": "HAFAS",
                "type": "WEB",
                "name": "webapp",
                "l": "vs_webapp",
                "v": 10107,
            },
            "formatted": False,
            "ext": "VRR.1",
            "svcReqL": [
                {
                    "meth": "HimSearch",
                    "req": {
                        "maxNum": 500,
                        "dateB": "20251214",
                        "timeB": "000000",
                        "dateE": "20261212",
                        "timeE": "235959",
                        "himFltrL": [
                            {"type": "CH", "mode": "INC", "value": "MESSAGELIST_CUSTOMER"},
                            {"type": "HIMCAT", "mode": "INC", "value": 0},
                            {"type": "HIMCAT", "mode": "INC", "value": 4},
                            {"type": "HIMCAT", "mode": "INC", "value": 2},
                            {"type": "HIMCAT", "mode": "INC", "value": 3},
                        ],
                        "sortL": ["LMOD_DESC"],
                        "getParent": True,
                        "getChildren": True,
                    },
                    "id": "1|1|",
                }
            ],
        }


        # Cookie-Debug
        _LOGGER.error("Cookies after PRE_URL: %s",
                      self.session.cookie_jar.filter_cookies(PRE_URL))

        # Schritt 3: POST-Request an die HIM-API
        rnd = random.randint(10**12, 10**13 - 1)

        url = (
            f"{BASE_URL}"
            f"?requestId={request_id}"
            f"&hciMethod=HimSearch"
            f"&hciVersion=1.24"
            f"&hciClientType=WEB"
            f"&hciClientVersion=10107"
            f"&aid=23lkjh63l456oisplergn"
            f"&rnd={rnd}"
        )

        async with self.session.post(
            url,   # <--- NEU: die URL aus Schritt 4
            json=payload,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36",

                "Accept": "*/*",
                "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Accept-Encoding": "gzip, deflate, br, zstd",

                "Sec-CH-UA": "\"Microsoft Edge\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
                "Sec-CH-UA-Mobile": "?1",
                "Sec-CH-UA-Platform": "\"Android\"",

                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",

                "Priority": "u=1, i",

                "Origin": "https://www.zuginfo.nrw",
                "Referer": "https://www.zuginfo.nrw/",

                "Content-Type": "application/json",
            },
        ) as resp:
            raw_text = await resp.text()

        # Schritt 3b: Cookie-Debug nach POST
        _LOGGER.debug("RAW POST RESPONSE: %s", raw_text)
        _LOGGER.error("Cookies after POST: %s",
                      self.session.cookie_jar.filter_cookies(BASE_URL))

        # Wenn der Server HTML statt JSON liefert → Hinweis ausgeben
        if "html" in resp.headers.get("Content-Type", "").lower():
            _LOGGER.error("Server lieferte HTML statt JSON. Vermutlich fehlende Session.")
            _LOGGER.error("Erste 500 Zeichen HTML: %s", raw_text[:500])
            return []
 
        # Schritt 4: JSON-Antwort parsen
        try:
            data = await resp.json(content_type=None)
        except Exception as e:
            _LOGGER.error("Konnte JSON nicht parsen: %s", e)
            _LOGGER.error("Antwort war: %s", raw_text)
            return []

        # Schritt 5: Struktur prüfen
        try:
            svc = data["svcResL"][0]["res"]
        except Exception as e:
            _LOGGER.error("Unerwartete JSON-Struktur: %s", e)
            _LOGGER.error("Antwort war: %s", raw_text)
            return []

        common = svc.get("common", {})
        msgL = svc.get("himL", [])

        # Schritt 6: NRWMessage-Objekte erzeugen
        messages = []
        for msg in msgL:
            try:
                messages.append(NRWMessage(msg, common))
            except Exception as e:
                _LOGGER.error("Fehler beim Erstellen einer NRWMessage: %s", e)

        return messages
