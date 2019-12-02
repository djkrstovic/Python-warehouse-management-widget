from PySide2 import QtWidgets, QtCore, QtGui
import csv
import os

class UkloniProizvodHalaDialog(QtWidgets.QDialog):

        def __init__(self, parent=None , path1=None, path2=None, path3=None):

            super().__init__(parent)
            self.putanjaProizvoda = path1
            self.putanjaHala = path2
            self.putanjaDoHala = path3
            ################## proizvodi
            #ucitavanje naziva iz CSV fajla
            self.lista_p = []
            naziviP = []
            with open(self.putanjaProizvoda, "r", encoding="utf-8") as fp:
                p_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
            if not p_podaci: #ako je prazna lista
                naziviP = []
                self.lista_p = []
            else: #postoje podaci u CSV-u
                for pro in p_podaci:
                    naziviP.append(pro[0] + "   " + pro[1] )
                    self.lista_p.append(pro)

            #################### HALE
            #ucitavanje naziva iz CSV fajla
            self.lista_hala = []
            naziviHala = []
            with open(self.putanjaHala, "r", encoding="utf-8") as fp:
                h_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
            if not h_podaci: #ako je prazna lista
                naziviHala = []
                self.lista_hala = []
            else: #postoje podaci u CSV-u
                for hala in h_podaci:
                    naziviHala.append(hala[0])
                    self.lista_hala.append(hala)

            ####################
            self.setWindowTitle("UKLONI proizvod iz hale")
            self.vbox_layout = QtWidgets.QVBoxLayout()
            self.form_layout = QtWidgets.QFormLayout()

            self.proizvodi_in = QtWidgets.QComboBox(self)
            self.proizvodi_in.addItems(naziviP)

            self.hale_in = QtWidgets.QComboBox(self)
            self.hale_in.addItems(naziviHala)

            self.kolicna_in = QtWidgets.QLineEdit(self)

            self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                | QtWidgets.QDialogButtonBox.Cancel, parent=self)

            self.form_layout.addRow("Proizvod:", self.proizvodi_in)
            self.form_layout.addRow("Hala:", self.hale_in)
            self.form_layout.addRow("Kolicina:", self.kolicna_in)

            self.vbox_layout.addLayout(self.form_layout)
            self.vbox_layout.addWidget(self.button_box)

            self.button_box.accepted.connect(self._on_accept)
            self.button_box.rejected.connect(self.reject)

            self.setLayout(self.vbox_layout)

        def _on_accept(self):
            #proveri da li je kolicina =< od kolicine u hali!

            if self.kolicna_in.text().strip() == "":
                QtWidgets.QMessageBox.warning(self,
                "Količina Proizvoda GREŠKA UNOSA", "Polje količina proizvoda treba da sadrži količinu, a ne da bude prazno!", QtWidgets.QMessageBox.Ok)
                return
            #provera da li je kolicina brokcana vrednost
            number = self.kolicna_in.text().strip()
            try:
                val = int(number)
            except ValueError:
                QtWidgets.QMessageBox.warning(self,
                "Količina GREŠKA UNOSA", "Polje količina mora biti brojčana vrednost!", QtWidgets.QMessageBox.Ok)
                return

            #postoji proizvod u hali? Kolicina je ok? -PRIJAVI GRESKU
            # Ako se uklanja cela kolicina izbrisi proizvod u suprotnom smanji kolicinu
            #smanji broj slobodnih mesta u odredjenoj hali

            path = self.putanjaDoHala + self.lista_hala[self.hale_in.currentIndex()][0] + ".csv"
            nova_kol = -1
            nova_lista_proizvoda = []
            tempV = True
            nova_ukupna_kolicina = 0
            izabranProizvod = self.lista_p[self.proizvodi_in.currentIndex()]
            if (os.path.exists(path) ):
                with open(path, "r", encoding="utf-8") as fp:
                    p_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
                    if not p_podaci: #ako je prazna lista
                        QtWidgets.QMessageBox.warning(self,
                        "Proizvod GREŠKA", "Ova hala nema nijedan proizvod u njoj!", QtWidgets.QMessageBox.Ok)
                        return
                    else: #postoje podaci u CSV-u
                        for pro in p_podaci:
                            if pro[0] == izabranProizvod[3] :
                                tempV = False
                                kol = int(self.kolicna_in.text().strip())
                                if (int(pro[1]) - kol < 0):
                                    QtWidgets.QMessageBox.warning(self,
                                    "Količina GREŠKA", "Uneta količina je veća od količine proizvoda u hali!", QtWidgets.QMessageBox.Ok)
                                    return
                                else:
                                    nova_kol = int(pro[1]) - kol
                                    nova_ukupna_kolicina += nova_kol
                                    if nova_kol != 0:
                                        nova_lista_proizvoda.append([pro[0], nova_kol])
                            else:
                                nova_lista_proizvoda.append(pro)
                                nova_ukupna_kolicina += int(pro[1])

                if tempV:
                    QtWidgets.QMessageBox.warning(self,
                    "Proizvod GREŠKA", "Ova hala nema izabran proizvod u njoj!", QtWidgets.QMessageBox.Ok)
                    return

                with open(path, "w", encoding="utf-8") as fp:
                    writer = csv.writer(fp, dialect=csv.unix_dialect)
                    for pro in nova_lista_proizvoda:
                        writer.writerow(pro)
            else:
                QtWidgets.QMessageBox.warning(self,
                "Proizvod GREŠKA", "Ova hala nema nijedan proizvod u njoj!", QtWidgets.QMessageBox.Ok)
                return

            if (nova_kol != -1):
                self.lista_hala[self.hale_in.currentIndex()][3] = str(nova_ukupna_kolicina)
                with open(self.putanjaHala, "w", encoding="utf-8") as fp:
                    writer = csv.writer(fp, dialect=csv.unix_dialect)
                    for row in self.lista_hala:
                        writer.writerow(row)
            self.accept()

        def get_data(self):
            path = self.putanjaDoHala + self.lista_hala[self.hale_in.currentIndex()][0] + ".csv"
            return {
            "path" : path
            }
