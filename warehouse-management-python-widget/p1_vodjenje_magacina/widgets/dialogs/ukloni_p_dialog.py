from PySide2 import QtWidgets, QtCore, QtGui
import csv

class UkloniProizvodDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, path=None):

        super().__init__(parent)
        self.putanja = path
        self.setWindowTitle("Ukloni Proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.proizvodi_in = QtWidgets.QComboBox(self)

        #ucitavanje naziva iz CSV fajla
        self.lista_p = []
        naziviP = []
        with open(self.putanja, "r", encoding="utf-8") as fp:
            p_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
        if not p_podaci: #ako je prazna lista
            naziviP = []
            self.lista_p = []
        else: #postoje podaci u CSV-u
            for pro in p_podaci:
                naziviP.append(pro[0] + "   " + pro[1] )
                self.lista_p.append(pro)

        ####################
        #testing = naziviP[1].split("   ")
        #print(testing)

        self.proizvodi_in.addItems(naziviP)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("Proizvod:", self.proizvodi_in)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        str_spliter = self.proizvodi_in.currentText().split("   ")
        with open(self.putanja, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for pro in self.lista_p:
                if pro[0] == str_spliter[0] and pro[1] == str_spliter[1] :
                    continue;
                else:
                    writer.writerow(pro)
        self.accept()

    def get_data(self):
        return {}
