import warnings

import flet as ft

from model.model import toMillisec


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, warning=None):
        try:
            durata = int(self._view._txtInDurata.value)
        except ValueError:
            warning.warn_explicit(message="duration not integer", category=TypeError, filename="controller.py", lineno=15)

        self._model.buildGraph(toMillisec(durata))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        nodes, edges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nodes} nodi e {edges} archi"))

        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(text=n.Title, data=n, on_click=self.getSelectedAlbum))

        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._selectedAlbum = None
        else:
            self._selectedAlbum = e.control.data

        print(f"Selected -- {self._selectedAlbum}")

    def handleAnalisiComponente(self, e):
        sizeConnessa, totDurata = self._model.getConnessaDetails(self._selectedAlbum)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che include {self._selectedAlbum} ha dimensione {sizeConnessa} e durata totale {totDurata}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        try:
            dTot = int(self._view._txtSoglia.value)
        except ValueError:
            warnings.warn("Soglia not integer")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Soglia inserita non valida - inserire un inetro"))
            return

        if self._selectedAlbum is None:
            warnings.warn("Attenzione, album non selezionato")
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Album non inserito - inserire un album"))
            return

        setAlbum = self._model.getSetAlbum(self._selectedAlbum, dTot)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Set di album ottimo trovato:"))
        for album in setAlbum:
            self._view.txt_result.controls.append(ft.Text(f"{album}"))

        self._view.update_page()