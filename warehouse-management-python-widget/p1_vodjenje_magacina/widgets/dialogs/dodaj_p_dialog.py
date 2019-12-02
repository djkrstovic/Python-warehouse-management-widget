from PySide2 import QtWidgets, QtCore, QtGui
import csv
import random
import string

class DodajProizvodDialog(QtWidgets.QDialog):

    def __init__(self, parent=None , path=None):

        super().__init__(parent)
        self.putanja = path
        self.setWindowTitle("Dodaj proizvod")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.naziv_p = QtWidgets.QLineEdit(self)
        self.temperatura_in = QtWidgets.QLineEdit(self)
        self.rok_u = QtWidgets.QDateEdit(self)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.rok_u.setDate(QtCore.QDate.currentDate())
        self.rok_u.setCalendarPopup(True)


        self.form_layout.addRow("Naziv Proizvoda:", self.naziv_p)
        self.form_layout.addRow("Rok Upotrebe:", self.rok_u)
        self.form_layout.addRow("Temperatura:", self.temperatura_in)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        if self.naziv_p.text().strip() == "":
            QtWidgets.QMessageBox.warning(self,
            "Naziv Proizvoda GREŠKA UNOSA", "Polje naziv proizvoda treba da sadrži naziv, a ne da bude prazno!", QtWidgets.QMessageBox.Ok)
            return

        if self.temperatura_in.text().strip() == "":
            QtWidgets.QMessageBox.warning(self,
            "Temperatura Proizvoda GREŠKA UNOSA", "Polje temperatura proizvoda treba da sadrži temperaturu, a ne da bude prazno!", QtWidgets.QMessageBox.Ok)
            return
        #provera da li je temperatura brokcana vrednost
        number = self.temperatura_in.text().strip()
        try:
            val = int(number)
        except ValueError:
            QtWidgets.QMessageBox.warning(self,
            "Naziv temperatura GREŠKA UNOSA", "Polje temperatura mora biti brojčana vrednost!", QtWidgets.QMessageBox.Ok)
            return
        #provera da li postoji proizvod
        with open(self.putanja, "r", encoding="utf-8") as fp:
            p_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
        if len(p_podaci) > 0:  #postoje hale u CSV - fajlu
            for proizvod in p_podaci:
                if proizvod[0] == self.naziv_p.text().strip() and proizvod[1] == self.rok_u.text().strip():
                    QtWidgets.QMessageBox.warning(self,
                    "Proizvod Postoji", "Dati proizvod postoji!", QtWidgets.QMessageBox.Ok)
                    return
        ################################

        self.accept()
    def get_data(self):
        with open(self.putanja,'a' , encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            rStr = self.randomStringDigits()
            myCsvRow = [self.naziv_p.text().strip() , self.rok_u.text().strip() , int(self.temperatura_in.text().strip()) , rStr]
            writer.writerow(myCsvRow)
        return {
        "Naziv" : self.naziv_p.text().strip(),
        "rok" : self.rok_u.text().strip() ,
        "temperatura" : int(self.temperatura_in.text().strip())
        }

    def randomStringDigits(self, stringLength=10):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
