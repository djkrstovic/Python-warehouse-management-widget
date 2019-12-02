from PySide2 import QtWidgets, QtCore, QtGui
import csv

class AddHalaDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje novog kontakta u imenik.
    """
    def __init__(self, parent=None ,path=None):
        """
        Inicijalizator dijaloga za dodavanje novog kontakta u imenik.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.putanja = path
        self.setWindowTitle("Dodaj Halu u Magacin")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.hala_naziv = QtWidgets.QLineEdit(self)
        self.tip_h = QtWidgets.QComboBox(self)
        self.brMesta = QtWidgets.QLineEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.tip_h.addItems(["za čuvanje proizvoda na sobnoj temperaturi" , "rashladne hale" , "hale za zamrzavanje"])

        self.form_layout.addRow("Hala:", self.hala_naziv)
        self.form_layout.addRow("Tip:", self.tip_h)
        self.form_layout.addRow("Broj Mesta:", self.brMesta)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):

        if self.hala_naziv.text().strip() == "":
            QtWidgets.QMessageBox.warning(self,
            "Naziv Hale GREŠKA UNOSA", "Polje hala treba da sadrži ime, a ne da bude prazno!", QtWidgets.QMessageBox.Ok)
            return

        if self.brMesta.text().strip() == "":
            QtWidgets.QMessageBox.warning(self,
            "Naziv broj mesta GREŠKA UNOSA", "Polje broj mesta treba imati vrednost!", QtWidgets.QMessageBox.Ok)
            return

        number = self.brMesta.text().strip()
        try:
            val = int(number)
            if val <= 0:  # if not a positive int print message and ask for input again
                QtWidgets.QMessageBox.warning(self,
                "Naziv broj mesta GREŠKA UNOSA", "Polje mora biti veće ili jednako broju 1!", QtWidgets.QMessageBox.Ok)
                return
        except ValueError:
            QtWidgets.QMessageBox.warning(self,
            "Naziv broj mesta GREŠKA UNOSA", "Polje mora biti brojčana vrednost!", QtWidgets.QMessageBox.Ok)
            return
        #provera da li hala sa datim nazivom postoji

        with open(self.putanja, "r", encoding="utf-8") as fp:
            h_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
        if len(h_podaci) > 0:  #postoje hale u CSV - fajlu
            for hala in h_podaci:
                if hala[0] == self.hala_naziv.text().strip():
                    QtWidgets.QMessageBox.warning(self,
                    "Hala Postoji", "Data Hala postoji u magacinu, molimo vas promenite ime hale!", QtWidgets.QMessageBox.Ok)
                    return

        self.accept()
    def get_data(self):
        with open(self.putanja,'a' , encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            myCsvRow = [self.hala_naziv.text().strip() , self.tip_h.currentText() , int(self.brMesta.text().strip()) , 0]
            writer.writerow(myCsvRow)
        return {}
