from PySide2 import QtWidgets, QtCore, QtGui
import csv
import os

class UkloniHaluDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, path=None , path2=None):

        super().__init__(parent)
        self.putanja = path
        self.putanja_do_csv = path2
        self.setWindowTitle("Ukloni Hala")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.n_hale = QtWidgets.QComboBox(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        #ucitavanje naziva iz CSV fajla
        self.lista_hala = []
        naziviHala = []
        with open(self.putanja, "r", encoding="utf-8") as fp:
            h_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
        if not h_podaci: #ako je prazna lista
            naziviHala = []
            self.lista_hala = []
        else: #postoje podaci u CSV-u
            for hala in h_podaci:
                naziviHala.append(hala[0])
                self.lista_hala.append(hala)

        ####################

        self.n_hale.addItems(naziviHala)

        self.form_layout.addRow("Izaberite halu:", self.n_hale)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):

        with open(self.putanja, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for hala in self.lista_hala:
                if hala[0] == self.n_hale.currentText():
                    continue;
                else:
                    writer.writerow(hala)
        putanja_do_hale_csv = self.putanja_do_csv + self.n_hale.currentText() +".csv"
        if (os.path.exists(putanja_do_hale_csv) ):
            os.remove(putanja_do_hale_csv)

        self.accept()

    def get_data(self):
        return {}
