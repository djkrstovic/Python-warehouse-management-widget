from PySide2 import QtWidgets
from PySide2 import QtGui
from ..magacin_model import MagacinModel
from ..p_model import PModel
from ..p_hala_model import PHModel
from .dialogs.add_hala_dialog import AddHalaDialog
from .dialogs.dodaj_p_dialog import DodajProizvodDialog
from .dialogs.ukloni_p_dialog import UkloniProizvodDialog
from .dialogs.dodaj_p_hala_dialog import DodajProizvodHalaDialog
from .dialogs.ukloni_p_hala_dialog import UkloniProizvodHalaDialog
from .dialogs.prikaz_p_h_dialog import PrikazPHalaDialog
from .dialogs.ukloni_halu_dialog import UkloniHaluDialog


class MagacinWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        self.putanja_csv_fajla_lista_hala = "plugins/p1_vodjenje_magacina/CSV/lista_hala.csv" #prva inicijalizacija putanje fajla
        self.putanja_csv_fajla_lista_proizvoda = "plugins/p1_vodjenje_magacina/CSV/lista_proizvoda.csv"
        self.putanja_csv_fajlova_hale = "plugins/p1_vodjenje_magacina/CSV/hale_proizvodi/"
        #path="plugins/p1_vodjenje_magacina/CSV/lista_hala.csv"

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout1 = QtWidgets.QHBoxLayout()
        self.hbox_layout2 = QtWidgets.QHBoxLayout()
        self.prikaz_h = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/books-brown.png"), "Prikaz Hala", self)
        self.add_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj Halu", self)
        self.remove_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Obriši Halu", self)

        self.hbox_layout1.addWidget(self.prikaz_h)
        self.hbox_layout1.addWidget(self.add_hala)
        self.hbox_layout1.addWidget(self.remove_hala)

        self.dodaj_p = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/block--plus.png"), "Dodaj proizvod", self)
        self.ukloni_p = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/block--minus.png"), "Obriši proizvod", self)
        self.prikaz_p = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/block-share.png"), "Prikaz proizvoda", self)

        self.dodaj_p_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/database--plus.png"), "Dodaj proizvod u halu", self)
        self.ukloni_p_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/database-delete.png"), "Obriši proizvod iz hale", self)
        self.prikaz_p_hala = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/database-share.png"), "Prikaz proizvoda izabrane hale", self)

        self.hbox_layout2.addWidget(self.dodaj_p)
        self.hbox_layout2.addWidget(self.ukloni_p)
        self.hbox_layout2.addWidget(self.prikaz_p)
        self.hbox_layout2.addWidget(self.dodaj_p_hala)
        self.hbox_layout2.addWidget(self.ukloni_p_hala)
        self.hbox_layout2.addWidget(self.prikaz_p_hala)

        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.dodaj_p.clicked.connect(self._on_dodaj_p)
        self.ukloni_p.clicked.connect(self._on_ukloni_p)
        self.prikaz_p.clicked.connect(self._on_prikaz_p)
        self.dodaj_p_hala.clicked.connect(self._on_dodaj_p_hala)
        self.ukloni_p_hala.clicked.connect(self._on_ukloni_p_hala)
        self.prikaz_p_hala.clicked.connect(self._on_prikaz_p_hala)

        self.prikaz_h.clicked.connect(self._on_prikaz_h)
        self.add_hala.clicked.connect(self._on_add_hala)
        self.remove_hala.clicked.connect(self._on_remove_hala)

        self.vbox_layout.addLayout(self.hbox_layout2)
        self.vbox_layout.addLayout(self.hbox_layout1)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

    def set_model(self, model):
        self.table_view.setModel(model)

    def _on_prikaz_h(self):
        self.set_model(MagacinModel(self.putanja_csv_fajla_lista_hala))
        return

    def _on_add_hala(self):
        dialog = AddHalaDialog(self.parent() , self.putanja_csv_fajla_lista_hala)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()
            self._on_prikaz_h()

    def _on_remove_hala(self):
        dialog = UkloniHaluDialog(self.parent() , self.putanja_csv_fajla_lista_hala , self.putanja_csv_fajlova_hale)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()
            self._on_prikaz_h()

    def _on_dodaj_p(self):
        dialog = DodajProizvodDialog(self.parent(), self.putanja_csv_fajla_lista_proizvoda)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()
            self._on_prikaz_p()

    def _on_ukloni_p(self):
        dialog = UkloniProizvodDialog(self.parent() , self.putanja_csv_fajla_lista_proizvoda)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dialog.get_data()
            self._on_prikaz_p()

    def _on_prikaz_p(self):
        self.set_model(PModel(self.putanja_csv_fajla_lista_proizvoda))
        return

    def _on_dodaj_p_hala(self):
        dialog = DodajProizvodHalaDialog(self.parent(), self.putanja_csv_fajla_lista_proizvoda, self.putanja_csv_fajla_lista_hala , self.putanja_csv_fajlova_hale)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            putanja = dialog.get_data()
            self._postavi_prikaz_p_hala_model(putanja['path'])

    def _on_ukloni_p_hala(self):
        dialog = UkloniProizvodHalaDialog(self.parent() , self.putanja_csv_fajla_lista_proizvoda, self.putanja_csv_fajla_lista_hala  , self.putanja_csv_fajlova_hale)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            putanja = dialog.get_data()
            self._postavi_prikaz_p_hala_model(putanja['path'])

    def _on_prikaz_p_hala(self):
        dialog = PrikazPHalaDialog(self.parent() , self.putanja_csv_fajla_lista_hala)
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            nazivF = dialog.get_data()
            self.set_model(PHModel(self.putanja_csv_fajlova_hale + nazivF["n_h"] + ".csv" , self.putanja_csv_fajla_lista_proizvoda))
        return

    def _postavi_prikaz_p_hala_model(self , putanjaDoFajla):
        self.set_model(PHModel(putanjaDoFajla, self.putanja_csv_fajla_lista_proizvoda))
