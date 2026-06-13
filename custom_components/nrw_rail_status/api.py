import aiohttp
import random
import string
from datetime import datetime
from html import unescape
import re
import logging

from .const import (
    BASE_URL,
    HAFAS_VERSION,
    HAFAS_CLIENT_ID,
    HAFAS_CLIENT_TYPE,
    HAFAS_CLIENT_NAME,
    HAFAS_CLIENT_LABEL,
    HAFAS_CLIENT_VERSION,
    HAFAS_AID,
    HAFAS_EXT,
    HAFAS_LANG,
)


_LOGGER = logging.getLogger(__name__)


def _random_request_id(length=16):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def _html_to_markdown(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text)
    text = re.sub(r"<i>(.*?)</i>", r"*\1*", text)
    text = re.sub(r"<.*?>", "", text)
    return text.strip()


class NRWMessage:
    """Einzelne HIM-Meldung als Python-Objekt."""

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

    def __repr__(self):
        return f"<NRWMessage {self.id} {self.title}>"


class NRWHimApi:
    """API-Klasse für Zuginfo.nrw HIM-Störungsdaten."""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_messages(self):
        """Holt alle HIM-Meldungen und gibt sie als NRWMessage-Liste zurück."""

        request_id = _random_request_id()

        url = (
            f"{BASE_URL}"
            f"?requestId={request_id}"
            f"&hciMethod=HimSearch"
            f"&hciVersion={HAFAS_VERSION}"
            f"&hciClientType={HAFAS_CLIENT_TYPE}"
            f"&hciClientVersion={HAFAS_CLIENT_VERSION}"
            f"&aid={HAFAS_AID}"
            f"&rnd={int(datetime.now().timestamp() * 1000)}"
        )

        payload = {
            "id": request_id,
            "ver": HAFAS_VERSION,
            "lang": HAFAS_LANG,
            "auth": {
                "type": "AID",
                "aid": HAFAS_AID
            },
            "client": {
                "id": HAFAS_CLIENT_ID,
                "type": HAFAS_CLIENT_TYPE,
                "name": HAFAS_CLIENT_NAME,
                "l": HAFAS_CLIENT_LABEL,
                "v": HAFAS_CLIENT_VERSION
            },
            "ext": HAFAS_EXT,
            "formatted": False,
            "svcReqL": [
                {
                    "meth": "HimSearch",
                    "req": {
                        "him": {
                            "mot": "ALL",
                            "prod": "ALL",
                            "region": "NRW"
                        }
                    }
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Origin": "https://www.zuginfo.nrw",
            "Referer": "https://www.zuginfo.nrw/",
            "User-Agent": "Mozilla/5.0"
        }

        async with self.session.post(url, json=payload, headers=headers) as resp:
            raw_text = await resp.text()
            _LOGGER.debug("RAW API RESPONSE: %s", raw_text)

            if resp.status != 200:
                raise RuntimeError(f"API returned status {resp.status}")

            data = await resp.json()

        try:
            res = data["svcResL"][0]["res"]
        except (KeyError, IndexError):
            raise RuntimeError("Unexpected API structure")

        common = res.get("common", {})
        msg_list = res.get("msgL", [])

        return [NRWMessage(m, common) for m in msg_list]
