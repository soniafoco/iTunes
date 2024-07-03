import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._durata = None
        self._selectedAlbum = None
        self._soglia = None

    def handleCreaGrafo(self, warning=None):
        self._view.txt_result.controls.clear()
        try:
            self._durata = float(self._view._txtInDurata.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico!"))
            self._view.update_page()
            return

        if self._durata < 0:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore maggiore di 0!"))
            self._view.update_page()
            return

        self._model.buildGrafo(self._durata)

        nodes, edges = self._model.getDettagli()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nodes} nodi e {edges} archi"))

        albums = self._model.getNodes()
        for album in albums:
            self._view._ddAlbum.options.append(ft.dropdown.Option(data=album, text=album.__str__(), on_click=self.readDDalbum))

        self._view.update_page()

    def readDDalbum(self, e):
        self._selectedAlbum = e.control.data

    def handleAnalisiComponente(self, e):
        self._view.txt_result.controls.clear()
        if self._selectedAlbum is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un album!"))
            self._view.update_page()
            return

        connessa, somma = self._model.getConnessa(self._selectedAlbum)
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa di {self._selectedAlbum}:"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione componente = {connessa}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata totale = {somma}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        self._view.txt_result.controls.clear()

        if self._selectedAlbum is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un album!"))
            self._view.update_page()
            return

        try:
            self._soglia = float(self._view._txtInSoglia.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico!"))
            self._view.update_page()
            return

        if self._soglia < 0:
            self._view.txt_result.controls.append(ft.Text("Inserire un valore maggiore di 0!"))
            self._view.update_page()
            return

        path, score = self._model.getSetAlbum(self._soglia, self._selectedAlbum)

