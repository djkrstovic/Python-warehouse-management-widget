from PySide2 import QtWidgets, QtCore, QtGui
import csv
import os

class DodajProizvodHalaDialog(QtWidgets.QDialog):

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
            self.setWindowTitle("Dodaj proizvod u halu")
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
            #temp p odgovara temp hali?? PROVERI

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
                "Količina temperatura GREŠKA UNOSA", "Polje količina mora biti brojčana vrednost!", QtWidgets.QMessageBox.Ok)
                return

            trenutnoSlobodnihMesta = self.lista_hala[self.hale_in.currentIndex()][3]
            ukupnoMestaUHali = self.lista_hala[self.hale_in.currentIndex()][2]
            tipHale = self.lista_hala[self.hale_in.currentIndex()][1]
            temperaturaProizvoda = self.lista_p[self.proizvodi_in.currentIndex()][2]
            temperaturaProizvoda = int(temperaturaProizvoda)

            if (int(number) + int(trenutnoSlobodnihMesta) > int(ukupnoMestaUHali) ):
                QtWidgets.QMessageBox.warning(self,
                "Nema Slobodnih Mesta", "Hala nema dovoljno mesta za odabranu količinu", QtWidgets.QMessageBox.Ok)
                return

            if (tipHale == "za čuvanje proizvoda na sobnoj temperaturi"):
                if not (19 <= temperaturaProizvoda <= 25):
                    QtWidgets.QMessageBox.warning(self,
                    "Proizvod temperatura", "Temperatura proizvoda ne odgovara temperaturi hale!", QtWidgets.QMessageBox.Ok)
                    return

                elif (tipHale == "rashladne hale"):
                    if not (1 <= temperaturaProizvoda <= 18):
                        QtWidgets.QMessageBox.warning(self,
                        "Proizvod temperatura", "Temperatura proizvoda ne odgovara temperaturi hale!", QtWidgets.QMessageBox.Ok)
                        return

                elif (tipHale == "hale za zamrzavanje"):
                    if not (-10 <= temperaturaProizvoda <= 0) :
                        QtWidgets.QMessageBox.warning(self,
                        "Proizvod temperatura", "Temperatura proizvoda ne odgovara temperaturi hale!", QtWidgets.QMessageBox.Ok)
                        return

            self.accept()
        def get_data(self):
            path = self.putanjaDoHala + self.lista_hala[self.hale_in.currentIndex()][0] + ".csv"
            #prolazak kroz fajl i trazi ako postiji proizvod
            # ako postoji proizvod on samo nadodaje kolicinu
            # u suprotnom postavlja novi proizvod
            tempV = True
            nova_lista_proizvoda = []
            nova_kolicina = -1
            nova_ukupna_kolicina = 0
            izabranProizvod = self.lista_p[self.proizvodi_in.currentIndex()]
            if (os.path.exists(path) ):
                with open(path, "r", encoding="utf-8") as fp:
                    p_podaci = list(csv.reader(fp, dialect=csv.unix_dialect))
                    if not p_podaci: #ako je prazna lista
                        nova_ukupna_kolicina = int(self.kolicna_in.text().strip())
                    else: #postoje podaci u CSV-u
                        for pro in p_podaci:
                            if pro[0] == izabranProizvod[3] :
                                nova_kolicina = int(pro[1]) + int(self.kolicna_in.text().strip())
                                nova_lista_proizvoda.append([izabranProizvod[3] , nova_kolicina])
                                tempV = False
                                nova_ukupna_kolicina += nova_kolicina
                            else:
                                nova_lista_proizvoda.append(pro)
                                nova_ukupna_kolicina += int(pro[1])


            if tempV:
                nov_proizvod = [izabranProizvod[3] , self.kolicna_in.text().strip()]
                nova_lista_proizvoda.append(nov_proizvod)
                nova_kolicina = int(self.kolicna_in.text().strip())
                nova_ukupna_kolicina += nova_kolicina

            with open(path, "w", encoding="utf-8") as fp:
                writer = csv.writer(fp, dialect=csv.unix_dialect)
                for pro in nova_lista_proizvoda:
                    writer.writerow(pro)

            if (nova_kolicina != -1):
                self.lista_hala[self.hale_in.currentIndex()][3] = str(nova_ukupna_kolicina)
                with open(self.putanjaHala, "w", encoding="utf-8") as fp:
                    writer = csv.writer(fp, dialect=csv.unix_dialect)
                    for row in self.lista_hala:
                        writer.writerow(row)

            return {
            "path" : path
            }
