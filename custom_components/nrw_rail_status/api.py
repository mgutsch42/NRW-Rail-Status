async def fetch_messages(self):
    request_id = _random_request_id()

    url = (
        f"https://www.zuginfo.nrw/gate/"
        f"?requestId={request_id}"
        f"&hciMethod=HimSearch"
        f"&hciVersion=1.24"
        f"&hciClientType=WEB"
        f"&hciClientVersion=10107"
        f"&aid=23lkjh63l456oisplergn"
        f"&rnd={int(datetime.now().timestamp() * 1000)}"
    )

    payload = {
        "id": request_id,
        "ver": "1.24",
        "lang": "deu",
        "auth": {
            "type": "AID",
            "aid": "23lkjh63l456oisplergn"
        },
        "client": {
            "id": "HAFAS",
            "type": "WEB",
            "name": "webapp",
            "l": "vs_webapp",
            "v": 10107
        },
        "ext": "VRR.1",
        "formatted": False,
        "svcReqL": [
            {
                "meth": "HimSearch",
                "req": {
                    # HIER kommt dein Filter rein
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
        text = await resp.text()
        logging.getLogger(__name__).warning("RAW API RESPONSE: %s", text)
        data = await resp.json()
