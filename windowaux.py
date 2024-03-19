# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt6.QtGui import QIcon

import informes
from dialogReport import Ui_dialogReports
from mainWindow import *
import drivers
import sys
import var
import eventos
from datetime import datetime
from dlgcalendar import *
from salir import *
from about import *
from mainWindow import *

class Salir(QtWidgets.QDialog):
    """
    Clase para mostrar un diálogo de confirmación para salir de la aplicación.

    """
    def __init__(self):
        """
        Constructor de la clase Salir.
        """
        super(Salir, self).__init__()
        var.salir = Ui_dlgSalir()
        var.salir.setupUi(self)

        '''zona eventos botones'''
        var.salir.btnAceptarSalir.clicked.connect(sys.exit)
        var.salir.btnCancelarSalir.clicked.connect(self.hide)


class AcercaDe(QtWidgets.QDialog):
    """
    Clase para mostrar un diálogo con información acerca de la aplicación.

    """
    def __init__(self):
        """
        Constructor de la clase AcercaDe.
        """
        super(AcercaDe, self).__init__()
        var.about = Ui_dlgAbout()
        var.about.setupUi(self)

        '''zona eventos botones'''
        var.about.btnCerrarAbout.clicked.connect(self.hide)
        var.about.label_2.setText(var.version)


class Calendar(QtWidgets.QDialog):
    """
    Clase para mostrar un calendario.

    """
    def __init__(self):
        """
        Constructor de la clase Calendar.
        """
        super(Calendar, self).__init__()
        var.calendar = Ui_dlgCalendar()
        var.calendar.setupUi(self)
        self.modificarBaja = False
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        var.calendar.Calendar.setSelectedDate(QtCore.QDate(ano, mes, dia))
        var.calendar.Calendar.clicked.connect(drivers.Drivers.cargarFecha)


class FileDialogAbrir(QtWidgets.QFileDialog):
    """
    Clase para mostrar un cuadro de diálogo para abrir archivos.

    """
    def __init__(self):
        """
        Constructor de la clase FileDialogAbrir.
        """
        super(FileDialogAbrir, self).__init__()
        self.setWindowIcon(QIcon('img/coche2.png'))

class DialogReport(QtWidgets.QDialog):
    """
    Clase para mostrar un diálogo de generación de informes.

    """
    def __init__(self):
        """
        Constructor de la clase DialogReport.
        """
        super(DialogReport, self).__init__()
        self.ui = Ui_dialogReports()
        self.ui.setupUi(self)

        self.ui.btnOK.clicked.connect(self.checkRbt)
        self.ui.btnCancel.clicked.connect(self.hide)

    def checkRbt(self):
        """
        Método para comprobar qué opción de informe ha sido seleccionada y generar el informe correspondiente.

        """
        try:
            if self.ui.rbtFac.isChecked():
                informes.Informes.reportviajes()
            elif self.ui.rbtClientes.isChecked():
                informes.Informes.reportclientes2()
            elif self.ui.rbtDrivers.isChecked():
                informes.Informes.reportdrivers()

        except Exception as e:
            print('Error al comprobar rbt dialog report', {e})
        finally:
            self.hide()