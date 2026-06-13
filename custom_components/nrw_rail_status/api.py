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
        """Löst alle Bahnhofsreferenzen aus locL auf."""
        locL = self.common.get("locL", [])
        result = []

        for edge in self._resolve_edges():
            for loc_idx in [edge.get("fLocX"), edge.get("tLocX")]:
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
        """Löst Linien/Produkte aus prodL auf."""
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
        """Löst Streckenabschnitte aus himMsgEdgeL auf."""
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
        """Löst Ereignisse aus himMsgEventL auf."""
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
