# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings
from builtins import super

import PyQt6
from PyQt6.QtGui import QFocusEvent, QMouseEvent
from PyQt6.QtWidgets import QComboBox
from geopy.geocoders import Nominatim

import clientes
import conexion
import drivers
import eventfilter
import eventos
import facturas
import informes
import main
import windowaux
from mainWindow import *
import sys
import var
from about import *
# Establecer la configuración regional en español
import locale
from PyQt6.QtCore import Qt, QMargins, QObject, QEvent
import resources

# Form implementation generated from reading ui file '.\templates\main.py'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')


class Main(QtWidgets.QMainWindow):
    """
    Clase principal que representa la ventana principal de la aplicación.
    """
    def __init__(self):
        """
        Método de inicialización de la clase Main.
        """
        super(Main, self).__init__()
        self.modoOscuro = False
        var.main = self
        var.ui = Ui_MainWindow()
        # self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        var.ui.setupUi(self)  # encargado de generar la interfaz
        var.calendar = windowaux.Calendar()
        var.salir = windowaux.Salir()
        var.about = windowaux.AcercaDe()
        var.dlgabrir = windowaux.FileDialogAbrir()
        var.dialogReport = windowaux.DialogReport()
        var.nominatim = Nominatim(user_agent="tycgis")
        conexion.Conexion.conexion()
        conexion.Conexion.cargaprov()
        eventos.Eventos.selEstado(self)
        eventos.Eventos.selEstadoCli()
        self.estiloClaro = self.leerFileTemaClaro()
        self.estiloOscuro = self.leerFileTemaOscuro()
        self.estiloClaroCalendar = self.leerFileTemaClaroCalendar()
        self.estiloOscuroCalendar = self.leerFileTemaOscuroCalendar()
        self.setStyleSheet(self.estiloClaro)
        var.calendar.setStyleSheet(self.estiloClaroCalendar)
        var.about.setStyleSheet(self.estiloClaro)
        var.salir.setStyleSheet(self.estiloClaro)
        var.dialogReport.setStyleSheet(self.estiloClaro)

        conexion.Conexion.cargarDrivers()
        conexion.Conexion.cargarFacturas()
        var.ui.frameFiltrar.hide()

        ''' funciones usadas'''
        eventos.Eventos.cargarStatusBar(self)
        eventos.Eventos.cargarSlider(self)


        ''' zona de eventos del menubar'''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.abrirDlgSalir)
        var.ui.actionAcerca_de.triggered.connect(eventos.Eventos.abrirDlgAcercaDe)
        var.ui.actionCrear_copia_de_seguridad.triggered.connect(eventos.Eventos.crearbackup)
        var.ui.actionRestaurar_copia_de_seguridad.triggered.connect(eventos.Eventos.restaurarbackup)
        var.ui.actionExportar_datos_Excel.triggered.connect(eventos.Eventos.exportardatosxls)
        var.ui.actionImportar_datos_Excel.triggered.connect(eventos.Eventos.importardatosxls)
        var.ui.actionImportar_Clientes_xls.triggered.connect(eventos.Eventos.importardatosxlsCli)
        var.ui.actionExportar_clientes_xls.triggered.connect(eventos.Eventos.exportarsxlsCli)
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.reportclientes2)
        var.ui.actionListado_Conductores.triggered.connect(informes.Informes.reportdrivers)
        var.ui.actionListado_Viajes.triggered.connect(lambda: informes.Informes.reportviajes())


        '''eventos del toolbar'''
        var.ui.actionlimpiarPanel.triggered.connect(drivers.Drivers.limpiarPanel)
        var.ui.actionlimpiarPanel.triggered.connect(clientes.Clientes.limpiarPanelCli)
        var.ui.actionlimpiarPanel.triggered.connect(facturas.Facturas.limpiarPanelFac)
        var.ui.actionlimpiarPanel.triggered.connect(var.ui.tabDrivers.clearSelection)
        var.ui.actionlimpiarPanel.triggered.connect(var.ui.tabDrivers_2.clearSelection)
        var.ui.actionlimpiarPanel.triggered.connect(var.ui.tabFac.clearSelection)
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.abrirDlgSalir)
        var.ui.actionbarReport.triggered.connect(var.dialogReport.show)
        var.ui.crearBackup.triggered.connect(eventos.Eventos.crearbackup)
        var.ui.restoreDB.triggered.connect(eventos.Eventos.restaurarbackup)
        var.slider.horizontalSlider.valueChanged.connect(self.cambiarTema)


        ''' zona de eventos cajas de texto'''
        var.ui.txtDni.editingFinished.connect(lambda: var.ui.txtDni.setText(var.ui.txtDni.text().upper()))
        var.ui.txtDni.editingFinished.connect(lambda: drivers.Drivers.validarDNI(var.ui.txtDni.text()))
        var.ui.txtNombre.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtApel.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtSalario.editingFinished.connect(eventos.Eventos.formatCajaTexto)
        var.ui.txtMovilDriver.editingFinished.connect(eventos.Eventos.comprobarMovil)
        var.ui.txtSalario.editingFinished.connect(eventos.Eventos.comprobarSalario)

        var.ui.txtDni_2.editingFinished.connect(lambda: var.ui.txtDni_2.setText(var.ui.txtDni_2.text().upper()))
        var.ui.txtDni_2.editingFinished.connect(lambda: drivers.Drivers.validarDNICli(var.ui.txtDni_2.text()))
        var.ui.txtMovil_2.editingFinished.connect(eventos.Eventos.comprobarMovilCli)

        var.ui.txtFiltro.editingFinished.connect(lambda : var.ui.txtFiltro.setText(var.ui.txtFiltro.text().upper()))
        var.ui.txtCifFac.editingFinished.connect(lambda : var.ui.txtCifFac.setText(var.ui.txtCifFac.text().upper()))

        '''zona de eventos de botones'''
        var.ui.btnCalendar.clicked.connect(eventos.Eventos.abrirCalendar)
        var.ui.btnAltaDriver.clicked.connect(drivers.Drivers.altadriver)
        var.ui.btnBuscar.clicked.connect(drivers.Drivers.buscarDriver)
        var.ui.btnBajaDriver.clicked.connect(drivers.Drivers.bajaDriver)
        var.ui.btnModDriver.clicked.connect(drivers.Drivers.modificarDriver)
        var.ui.btnFlecha.clicked.connect(lambda: eventos.Eventos.resizeFrame(var.ui.frameForm, var.ui.btnFlecha))

        var.ui.btnFlecha_2.clicked.connect(lambda: eventos.Eventos.resizeFrame(var.ui.frameForm_2, var.ui.btnFlecha_2))
        var.ui.btnAltaDriver_2.clicked.connect(clientes.Clientes.altaCli)
        var.ui.btnBajaDriver_2.clicked.connect(clientes.Clientes.bajaCli)
        var.ui.btnBuscar_2.clicked.connect(lambda: clientes.Clientes.buscarCli(var.ui.txtDni_2.text()))
        var.ui.btnModDriver_2.clicked.connect(clientes.Clientes.modificarCli)

        var.ui.btnCalendarFac.clicked.connect(eventos.Eventos.abrirCalendar)
        var.ui.btnBuscarFac.clicked.connect(lambda: facturas.Facturas.buscarCliFac(var.ui.txtCifFac.text()))
        var.ui.btnFac.clicked.connect(facturas.Facturas.facturar)
        var.ui.btnViaje.clicked.connect(facturas.Facturas.grabarViaje)
        var.ui.btnViaje.clicked.connect(facturas.Facturas.cargarTotalFactura)
        var.ui.btnFiltrar.clicked.connect(facturas.Facturas.Filtrar)

        var.ui.btnLimpiarViaje.clicked.connect(facturas.Facturas.limpiarViaje)
        var.ui.btnLimpiarFactura.clicked.connect(facturas.Facturas.limpiarFac)
        var.ui.btnLimpiarFiltroFac.clicked.connect(facturas.Facturas.limpiarFiltroFac)



        '''eventos de tablas'''
        eventos.Eventos.resizeTab(var.ui.tabDrivers)
        eventos.Eventos.resizeTab(var.ui.tabDrivers_2)
        eventos.Eventos.resizeTabFac(var.ui.tabFac)
        eventos.Eventos.resizeTab(var.ui.tabViajes)

        var.ui.tabDrivers.clicked.connect(drivers.Drivers.cargarDriver)
        var.ui.tabDrivers_2.clicked.connect(clientes.Clientes.cargarCli)
        var.ui.tabFac.clicked.connect(facturas.Facturas.cargarFactura)
        var.ui.tabFac.clicked.connect(lambda: conexion.Conexion.cargarViajes(var.ui.tabFac.item(var.ui.tabFac.currentRow(), 0).text()))
        var.ui.tabFac.clicked.connect(lambda: facturas.Facturas.cargarTotalFactura())
        var.ui.tabViajes.clicked.connect(facturas.Facturas.cargarViaje)
        var.ui.tabFac.clicked.connect(facturas.Facturas.limpiarViaje)

        var.ui.tabDrivers.cellEntered.connect(lambda row, column: eventos.Eventos.onCellEntered(var.ui.tabDrivers, row))
        var.ui.tabDrivers_2.cellEntered.connect(lambda row, column: eventos.Eventos.onCellEntered(var.ui.tabDrivers_2, row))
        var.ui.tabFac.cellEntered.connect(lambda row, column: eventos.Eventos.onCellEntered(var.ui.tabFac, row))
        var.ui.tabViajes.cellEntered.connect(lambda row, column: eventos.Eventos.onCellEntered(var.ui.tabViajes, row))

        var.ui.tabDrivers.leaveEvent = lambda event: eventos.Eventos.clearRowBackground(var.ui.tabDrivers, eventos.Eventos.current_hovered_row)
        var.ui.tabDrivers_2.leaveEvent = lambda event: eventos.Eventos.clearRowBackground(var.ui.tabDrivers_2, eventos.Eventos.current_hovered_row)
        var.ui.tabFac.leaveEvent = lambda event: eventos.Eventos.clearRowBackground(var.ui.tabFac, eventos.Eventos.current_hovered_row)
        var.ui.tabViajes.leaveEvent = lambda event: eventos.Eventos.clearRowBackground(var.ui.tabViajes, eventos.Eventos.current_hovered_row)




        '''eventos combobox'''
        var.ui.cmbProv.currentIndexChanged.connect(lambda: conexion.Conexion.selMuni(var.ui.cmbProv, var.ui.cmbMuni))
        var.ui.cmbProv_2.currentIndexChanged.connect(lambda: conexion.Conexion.selMuni(var.ui.cmbProv_2, var.ui.cmbMuni_2))
        var.ui.cmbProvO.currentIndexChanged.connect(lambda: conexion.Conexion.selMuni(var.ui.cmbProvO, var.ui.cmbMuniO))
        var.ui.cmbProvD.currentIndexChanged.connect(lambda: conexion.Conexion.selMuni(var.ui.cmbProvD, var.ui.cmbMuniD))
        var.ui.cmbMuniD.activated.connect(lambda: eventos.Eventos.selEstadoTarifa())
        var.ui.cmbMuniO.activated.connect(lambda: eventos.Eventos.selEstadoTarifa())


        '''zona eventos radiobuttons'''
        var.ui.buttonGroup.buttonClicked.connect(eventos.Eventos.selEstado)
        var.ui.buttonGroup_2.buttonClicked.connect(eventos.Eventos.selEstadoCli)

        '''zona eventos checkbox'''
        var.ui.chkFiltrar.stateChanged.connect(eventos.Eventos.ocultarFiltro)

    def leerFileTemaOscuro(self):
        """
        Método para leer el archivo de estilo para el tema oscuro.

        :returns: El contenido del archivo de estilo para el tema oscuro.
        :rtype: str
        """
        with open('style/temaOscuro.qss', 'r') as fileOscuro:
            estiloOscuro = fileOscuro.read()
        return estiloOscuro

    def leerFileTemaClaro(self):
        with open('style/temaClaro.qss', 'r') as fileClaro:
            estiloClaro = fileClaro.read()
            return estiloClaro
    def leerFileTemaClaroCalendar(self):
        with open('style/temaClaroCalendar.qss', 'r') as fileClaro:
            estiloClaro = fileClaro.read()
            return estiloClaro

    def leerFileTemaOscuroCalendar(self):
        with open('style/temaOscuroCalendar.qss', 'r') as fileOscuro:
            estiloOscuro = fileOscuro.read()
        return estiloOscuro


    def cambiarTema(self):
        """
        Método para cambiar el tema de la aplicación.
        """
        try:
            if var.slider.horizontalSlider.value() == var.slider.horizontalSlider.minimum():
                self.modoOscuro = False
                self.setStyleSheet(self.estiloClaro)
                var.calendar.setStyleSheet(self.estiloClaroCalendar)
                var.about.setStyleSheet(self.estiloClaro)
                var.salir.setStyleSheet(self.estiloClaro)
                var.dialogReport.setStyleSheet(self.estiloClaro)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers_2)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabFac)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabViajes)

            elif var.slider.horizontalSlider.value() == var.slider.horizontalSlider.maximum():
                self.modoOscuro = True
                self.setStyleSheet(self.estiloOscuro)
                var.calendar.setStyleSheet(self.estiloOscuroCalendar)
                var.about.setStyleSheet(self.estiloOscuro)
                var.salir.setStyleSheet(self.estiloOscuro)
                var.dialogReport.setStyleSheet(self.estiloOscuro)

                eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers_2)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabFac)
                eventos.Eventos.cambiarEstiloTabla(var.ui.tabViajes)

        except Exception as error:
            print('Error al cambiar el tema', error)

    def closeEvent(self, event):
        """
        Método llamado cuando se cierra la ventana principal.

        :param event: Evento de cierre.
        :type event: QCloseEvent
        """
        mbox = eventos.Eventos.ventanaConfirmacion('Estás seguro de que quieres salir?', QtWidgets.QMessageBox.Icon.Information)

        if mbox == 0:
            app.quit()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    event_filter = eventfilter.EventFilter()
    var.ui.cmbDriverFac.installEventFilter(event_filter)
    window.showNormal()
    sys.exit(app.exec())


