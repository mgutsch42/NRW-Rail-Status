import aiohttp
import random
import string
from datetime import datetime
from html import unescape
import re


BASE_URL = "https://www.zuginfo.nrw/gate/"


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

        payload = {
            "svcReqL": [
                {
                    "req": {
                        "him": {
                            "mot": "ALL",
                            "prod": "ALL",
                            "region": "NRW"
                        }
                    },
                    "meth": "HimSearch"
                }
            ],
            "client": {
                "id": "WEB",
                "type": "WEB",
                "name": "zuginfo-web",
                "l": "de"
            },
            "ver": "1.24",
            "auth": {
                "aid": "23lkjh63l456oisplergn"
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with self.session.post(BASE_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                raise RuntimeError(f"API returned status {resp.status}")

            data = await resp.json()

        try:
            res = data["svcResL"][0]["res"]
        except (KeyError, IndexError):
            raise RuntimeError("Unexpected API structure")

        common = res.get("common", {})
        msg_list = res.get("msgL", [])

        messages = [NRWMessage(m, common) for m in msg_list]
        return messages
