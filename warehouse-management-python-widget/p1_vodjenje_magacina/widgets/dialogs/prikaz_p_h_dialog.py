from PySide2 import QtWidgets, QtCore, QtGui
import csv

class PrikazPHalaDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, path=None):

        super().__init__(parent)
        self.setWindowTitle("Prikaz Hala")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.n_hale = QtWidgets.QComboBox(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        #ucitavanje naziva iz CSV fajla
        naziviHala = []
        with open(path, "r", encoding="utf-8") as fp:
            h_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
        if not h_podaci: #ako je prazna lista
            naziviHala = []
        else: #postoje podaci u CSV-u
            for hala in h_podaci:
                naziviHala.append(hala[0])

        ####################

        self.n_hale.addItems(naziviHala)

        self.form_layout.addRow("Izaberite halu:", self.n_hale)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        self.accept()

    def get_data(self):
        return {
        "n_h" : self.n_hale.currentText()
        }
