from PySide2 import QtCore
import csv
import os


class PHModel(QtCore.QAbstractTableModel):
    """
    Klasa koja predstavlja specijalizaciju QAbstractTableModel-a.
    Koristimo tabelarni model, jer cemo podatke posmatrati kao tabelu, i u tabeli ih prikazivati.
    Svaki tabelarni model ima redove i kolone. Red je jedan korisnik u imeniku, a kolone predstavalju
    korisnikove pojedinacne podatke, poput imena, prezimena itd.
    Datoteka na osnovu koje se populise model je CSV datoteka, gde su redovi modela zapravo redovi
    iz datoteke, a kolone modela, su podaci koji su u redu u datoteci odvojeni separatorom (zarezom).
    """
    def __init__(self ,path1=None , path2=None):
        #path1 : hale
        #path2 : proizvodi
        """
        Inicijalizator modela za kontakte.
        Pri inicijalizaciji se na osnovu datoteke sa putanje path ucitavaju i populise se model.

        :param path: putanja do datoteke u kojoj su smesteni podaci.
        :type path: str
        """
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._data = []
        self.load_data(path1,path2)

    def rowCount(self, index):
        """
        Vraca broj redova u modelu.

        :param index: putanja do datoteke u kojoj su smesteni podaci.
        :type index: QModelIndex
        :returns: int -- broj redova modela.
        """
        return len(self._data)

    def columnCount(self, index):
        """
        Vraca broj kolona u modelu. Posto znamo da nas korisnik iz imenika je opisan sa pet
        podataka, vracamo fiksni broj kolona na osnovu datoteke.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: int -- broj kolona modela.
        """
        return 4

    def data(self, index, role):
        """
        Vraca podatak smesten na datom indeksu sa datom ulogom.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :param role: putanja do datoteke u kojoj su smesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: object -- podatak koji se nalazi na zadatom indeksu sa zadatom ulogom.
        """
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):
        """
        Vraca podatak koji ce popuniti sekciju zaglavlja tabele.

        :param section: sekcija koja u zavisnosti od orijentacije predstavlja redni broj kolone ili reda.
        :type section: int
        :param orientation: odredjuje polozaj zaglavlja.
        :type orientation: QtCore.Qt.Vertical ili QtCore.Qt.Horizontal
        :param role: putanja do datoteke u kojoj su smesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: str -- naziv sekcije zaglavlja.
        """
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "Naziv"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Rok Upotrebe"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Temperatura"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Količina u hali"


    def get_element(self, index : QtCore.QModelIndex):
        """
        Dobavlja podatak smesten na zadatom indeksu, ako je indeks validan.
        Pomocna metoda nase klase.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- vrednost na indeksu.
        """
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def load_data(self, path1="" , path2=""):
        """
        Ucitava podatke iz CSV datoteke na zadatoj path putanji uz pomoc CSV reader-a.
        Pomocna metoda nase klase.

        :param path: putanja do CSV datoteke.
        :type path: str
        """
        if not (os.path.exists(path2) ): #putanja proizvoda ne valja
            return False
        lista_proizvoda = []
        with open(path2, "r", encoding="utf-8") as fp:
            lista_proizvoda = list(csv.reader(fp, dialect=csv.unix_dialect))

        lista_u_hali = []
        if (os.path.exists(path1) ):
            with open(path1, "r", encoding="utf-8") as fp:
                lista_u_hali = list(csv.reader(fp, dialect=csv.unix_dialect))
        else:
            open(path1, 'w+', encoding="utf-8") #kreira fajl ako ne postoji w+

        data_list = []
        for p_u_hali in lista_u_hali:
            for pro in lista_proizvoda:
                if p_u_hali[0] == pro[3]:
                    data_list.append([pro[0] , pro[1], pro[2] ,p_u_hali[1]])

        self._data = data_list
