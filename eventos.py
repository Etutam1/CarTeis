import locale
import os.path
import shutil
import xlwt
import xlrd
from PyQt6 import QtWidgets, QtCore, QtSql
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import *
from PyQt6.uic.properties import QtGui
import conexion
import drivers, clientes
import eventos
import facturas
import var
from datetime import *
import locale
import re
import zipfile
from geopy.distance import geodesic


from dialogReport import Ui_dialogReports
from slider import Ui_SliderWidget

import main
from PyQt6.QtWidgets import QSlider

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')


class Eventos():
    """
    Clase que define diversos eventos y funcionalidades de la interfaz de usuario.
    """
    current_hovered_row = -1

    @staticmethod
    def ventanaAviso(aviso, icono):
        """
        Muestra una ventana de aviso con un mensaje y un icono especificados.

        :param aviso: Mensaje a mostrar en la ventana de aviso.
        :param icono: Icono a mostrar en la ventana de aviso.
        """
        try:
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setWindowIcon(QIcon(':/img/img/coche2.png'))
            msg.setIcon(icono)
            msg.setText(aviso)
            if not var.main.modoOscuro:
                msg.setStyleSheet('''
                                                                QPushButton{ 
                                                                            background-color: #51007A;
                                                                          color: white;
                                                                          border-radius:10px;
                                                                          padding:5px 10px;}
        
                                                             QPushButton:hover {
                                                             background-color: #7E4EAA;
                                                              }
        
                                                             QPushButton:pressed {
                                                             background-color: #330046;
                                                              }
                                                             ''')
            else:
                msg.setStyleSheet('''QMessageBox { background-color: rgb(96,96,96); } QLabel{color:white;}
                                                                               QPushButton{ 
                                                                                           background-color: #51007A;
                                                                                         color: white;
                                                                                         border-radius:10px;
                                                                                         padding:5px 10px;}

                                                                            QPushButton:hover {
                                                                            background-color: #7E4EAA;
                                                                             }

                                                                            QPushButton:pressed {
                                                                            background-color: #330046;
                                                                             }
                                                                            ''')
            msg.exec()
        except Exception as error:
            print('Error al mostrar ventana aviso', error)

    @staticmethod
    def ventanaConfirmacion(aviso, icono):
        """
        Muestra una ventana de confirmación con un mensaje y un icono especificados.

        :param aviso: Mensaje a mostrar en la ventana de confirmación.
        :param icono: Icono a mostrar en la ventana de confirmación.
        :return: El resultado de la ejecución de la ventana de confirmación.
        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle('Aviso')
            mbox.setWindowIcon(QIcon(':/img/img/coche2.png'))
            mbox.setIcon(icono)
            mbox.setText(aviso)
            if not var.main.modoOscuro:
                mbox.setStyleSheet('''
                                                                           QPushButton{ 
                                                                                       background-color: #51007A;
                                                                                     color: white;
                                                                                     border-radius:10px;
                                                                                     padding:5px 10px;}

                                                                        QPushButton:hover {
                                                                        background-color: #7E4EAA;
                                                                         }

                                                                        QPushButton:pressed {
                                                                        background-color: #330046;
                                                                         }
                                                                        ''')
            else:
                mbox.setStyleSheet('''QMessageBox { background-color: rgb(96,96,96); } QLabel{color:white;}
                                                                                          QPushButton{ 
                                                                                                      background-color: #51007A;
                                                                                                    color: white;
                                                                                                    border-radius:10px;
                                                                                                    padding:5px 10px;}

                                                                                       QPushButton:hover {
                                                                                       background-color: #7E4EAA;
                                                                                        }

                                                                                       QPushButton:pressed {
                                                                                       background-color: #330046;
                                                                                        }
                                                                                       ''')
            btn_yes = QPushButton("Sí")
            btn_no = QPushButton("No")

            mbox.addButton(btn_yes, QMessageBox.ButtonRole.YesRole)
            mbox.addButton(btn_no, QMessageBox.ButtonRole.NoRole)

            return mbox.exec()
        except Exception as error:
            print('Error al mostrar aviso confirmacion', error)

    @staticmethod
    def abrirCalendar(self):
        """
        Abre el calendario en la interfaz.

        :param self: Instancia de la clase.
        """

        try:
            var.calendar.show()
        except Exception as error:
            print('error en abrir calendar ', error)

    @staticmethod
    def abrirDlgSalir():
        """
        Abre el diálogo para salir de la aplicación.
        """
        try:
            var.salir.show()
        except Exception as error:
            print('error en abrir ventana salir ', error)

    @staticmethod
    def abrirDlgAcercaDe():
        """
        Abre el diálogo "Acerca de" en la interfaz.
        """
        try:
            var.about.show()
        except Exception as error:
            print("error en abrir ventana acerca de", error)

    def cargarStatusBar(self):
        """
        Carga la barra de estado con la fecha y la versión de la aplicación.

        :param self: Instancia de la clase.
        """
        try:
            fecha = datetime.now().strftime("%A  -  " + "%d/%m/%y %H:%M")
            self.labelstatus = QtWidgets.QLabel(fecha.capitalize(), self)
            self.labelstatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            var.ui.statusbar.addPermanentWidget(self.labelstatus, 1)
            self.labelstatusversion = QtWidgets.QLabel(var.version, self)
            self.labelstatusversion.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            var.ui.statusbar.addPermanentWidget(self.labelstatusversion, 0)

        except Exception as error:
            print('Error al cargar el statusbar: ', error)

    def cargarSlider(self):
        """
        Carga el slider en la barra de herramientas de la interfaz.
        """
        var.slider = Ui_SliderWidget()
        var.slider.setupUi(var.ui.toolBar)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        var.ui.toolBar.addWidget(spacer)
        var.ui.toolBar.addWidget(var.slider.horizontalLayoutWidget)

    def selEstado(self):
        """
        Selecciona el estado de los conductores según la opción elegida en la interfaz.
        """
        drivers.Drivers.limpiarPanel()
        if var.ui.rbtTodos.isChecked():
            conexion.Conexion.mostrardrivers(self)
        elif var.ui.rbtAlta.isChecked():
            conexion.Conexion.mostrardriversAlta(self)
        elif var.ui.rbtBaja.isChecked():
            conexion.Conexion.mostrardriversBaja(self)
        var.ui.tabDrivers.clearSelection()
        eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers)

    @staticmethod
    def selEstadoCli():
        """
        Selecciona el estado de los clientes según la opción elegida en la interfaz.
        """
        clientes.Clientes.limpiarPanelCli()
        if var.ui.rbtTodos_2.isChecked():
            conexion.Conexion.mostrarclientes()
        elif var.ui.rbtAlta_2.isChecked():
            conexion.Conexion.mostrarclisAlta()
        elif var.ui.rbtBaja_2.isChecked():
            conexion.Conexion.mostrarclisBaja()
        var.ui.tabDrivers_2.clearSelection()
        eventos.Eventos.cambiarEstiloTabla(var.ui.tabDrivers_2)

    @staticmethod
    def selEstadoTarifa():
        """
        Selecciona el estado de la tarifa según la opción elegida en la interfaz.
        """
        try:
            if facturas.Facturas.checkcmb():
                if var.ui.cmbProvO.currentText() != var.ui.cmbProvD.currentText():
                    var.ui.rbtNac.setChecked(True)
                elif var.ui.cmbMuniO.currentText() != var.ui.cmbMuniD.currentText():
                    var.ui.rbtProv.setChecked(True)
                else:
                    var.ui.rbtLocal.setChecked(True)
                if var.ui.cmbMuniD.hasFocus() or var.ui.cmbMuniO.hasFocus():
                    if not conexion.Conexion.comprobarConexion():
                        eventos.Eventos.ventanaAviso('Error de conexión al calcular la distancia', QtWidgets.QMessageBox.Icon.Warning)
                        var.ui.txtKms.clear()
                        var.ui.txtKms.setFocus()
                        var.ui.txtKms.setEnabled(True)
                    else:
                        if var.ui.cmbMuniO.currentText() != '' and var.ui.cmbMuniD.currentText() != '':
                            distancia = Eventos.calcularDistancia(var.ui.cmbMuniO.currentText(), var.ui.cmbMuniD.currentText())
                            var.ui.txtKms.setText(str(distancia))
                            var.ui.txtKms.setEnabled(False)
                        else:
                            var.ui.txtKms.clear()
                            print('vaciar')
        except Exception as error:
            print('Error al seleccionar Tarifa', error)

    @staticmethod
    def calcularDistancia(loc1, loc2):
        """
        Calcula la distancia entre dos ubicaciones geográficas.

        :param loc1: Primera ubicación.
        :param loc2: Segunda ubicación.
        :return: La distancia entre las dos ubicaciones en kilómetros.
        """
        try:
            if loc1.strip != '' and loc2.strip != '':
                location1 = var.nominatim.geocode(loc1).raw
                location2 = var.nominatim.geocode(loc2).raw
                distancia = str(geodesic((location1["lat"], location1["lon"]), (location2["lat"], location2["lon"]))).replace('km', '')
                return round(float(distancia), 2)
        except Exception as e:
                print('Error al calcular distancia localidadesd', {e})
                eventos.Eventos.ventanaAviso('Error al calcular la distancia',
                                             QtWidgets.QMessageBox.Icon.Warning)
                var.ui.txtKms.setText('')
                var.ui.txtKms.setFocus()
                var.ui.txtKms.setEnabled(True)

    @staticmethod
    def resizeTabFac(tabla):
        """
        Ajusta el tamaño de las columnas de la tabla de facturas.

        :param tabla: La tabla de facturas.
        """
        try:
            header = tabla.horizontalHeader()
            for i in range(tabla.columnCount()):
                # if i == 0 or i == 3 or i == 4:
                #     header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                if i == 1 or i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Fixed)

                tabla.setColumnWidth(2, 30)

        except Exception as error:
            print('Error al resize tabfac', error)

    @staticmethod
    def resizeTab(tabla):
        """
        Ajusta el tamaño de las columnas de la tabla de conductores.

        :param tabla: La tabla de conductores.
        """
        try:
            header = tabla.horizontalHeader()
            for i in range(tabla.columnCount()):
                if i == 0 or i == 3 or i == 4 or i == 6:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                elif i == 1 or i == 2 or i == 6:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        except Exception as error:
            print('Error al resize tabdrivers', error)

    def formatCajaTexto(self=None):
        """
        Formatea el texto de las cajas de texto en la interfaz.
        """
        try:
            var.ui.txtApel.setText(var.ui.txtApel.text().title())
            var.ui.txtNombre.setText(var.ui.txtNombre.text().title())
            var.ui.txtSalario.setText(str(locale.currency(float(var.ui.txtSalario.text()))))
        except Exception as error:
            print('Error al formatear cajas de texto', error)

    def comprobarMovilCli(self=None):
        """
        Comprueba el formato del número de móvil del cliente.
        """
        try:
            movil = var.ui.txtMovil_2.text()
            patron = r'^\d{9}$'

            if not re.match(patron, movil):
                eventos.Eventos.ventanaAviso("Móvil no válido", QtWidgets.QMessageBox.Icon.Warning)
                var.ui.txtMovil_2.setText("")
        except Exception as error:
            print('Error al comprobar movil', error)

            """	msg = QtWidgets.QMessageBox()
                   msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msg.setText('Valor de Salario incorrect (00000000.00)')
                    msg.exec()
                    var.ui.txtSalario.setText("")"""

    def comprobarMovil(self=None):
        """
        Comprueba el formato del número de móvil del conductor.
        """
        try:
            movil = var.ui.txtMovilDriver.text()
            patron = r'^\d{9}$'

            if not re.match(patron, movil):
                eventos.Eventos.ventanaAviso("Móvil no válido", QtWidgets.QMessageBox.Icon.Warning)
                var.ui.txtMovilDriver.setText("")
        except Exception as error:
            print('Error al comprobar movil', error)

    def comprobarSalario(self=None):
        """
        Comprueba el formato del salario ingresado.
        """
        try:
            salario = var.ui.txtSalario.text()
            patron = r'^\d+\,\d{2} €$'

            if not re.match(patron, salario):
                eventos.Eventos.ventanaAviso("Salario no válido", QtWidgets.QMessageBox.Icon.Warning)
                var.ui.txtSalario.setText(None)

        except Exception as error:
            print('Error al comprobar salario', error)

    @staticmethod
    def resizeFrame(frame, button):
        """
        Ajusta el tamaño del marco según el botón de expansión.

        :param frame: El marco a ajustar.
        :param button: El botón de expansión asociado.
        """
        try:
            if frame.isVisible():
                # animation = QPropertyAnimation(frame)
                # animation.setDuration(2000)  # Duration of the animation in milliseconds
                # animation.setStartValue(1.0)  # Initial opacity
                # animation.setEndValue(0.0)  # Final opacity
                # animation.finished.connect(frame.hide)
                # animation.start()
                frame.hide()
                button.setIcon(QIcon(':/img/img/chevron-derecho.png'))
            else:
                frame.show()
                button.setIcon(QIcon(':/img/img/chevron-izquierdo.png'))
        except Exception as error:
            print('error al resize frameInfo', error)

    def crearbackup(self):
        """
        Crea una copia de seguridad de la base de datos.
        """
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            copia = str(fecha) + '_backup.zip'
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar copia de seguridad', copia, '.zip')

            if var.dlgabrir.accept and filename:
                fichzip = zipfile.ZipFile(copia, 'w')
                fichzip.write(var.bbdd, os.path.basename(var.bbdd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))
                eventos.Eventos.ventanaAviso("Copia de seguridad creada", QtWidgets.QMessageBox.Icon.Information)


        except Exception as error:
            eventos.Eventos.ventanaAviso('Error en copia de seguridad', QtWidgets.QMessageBox.Icon.Warning)

    def restaurarbackup(self):
        """
        Restaura una copia de seguridad de la base de datos.
        """
        try:
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar copia de seguridad', '', '*.zip;;All Files(*)')
            if filename[1]:
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                Eventos.selEstado(self)
                Eventos.selEstadoCli()
                eventos.Eventos.ventanaAviso("Copia de seguridad restaurada", QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            eventos.Eventos.ventanaAviso("'Error al restaurar la Copia de seguridad'", QtWidgets.QMessageBox.Icon.Warning)

    def exportardatosxls(self):
        """
        Exporta los datos de los conductores a un archivo XLS.
        """
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_datos.xls')
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar Datos en XLS', file, '.xls')
            if var.dlgabrir.accept and filename:
                wb = xlwt.Workbook()
                sheet1 = wb.add_sheet('Conductores')
                sheet1.write(0, 0, 'ID')
                sheet1.write(0, 1, 'DNI')
                sheet1.write(0, 2, 'Fecha Alta')
                sheet1.write(0, 3, 'Apellidos')
                sheet1.write(0, 4, 'Nombre')
                sheet1.write(0, 5, 'Dirección')
                sheet1.write(0, 6, 'Provincia')
                sheet1.write(0, 7, 'Municipio')
                sheet1.write(0, 8, 'Móvil')
                sheet1.write(0, 9, 'Salario')
                sheet1.write(0, 10, 'Carnet')

                registros = conexion.Conexion.selectDriversTodos()

                for fila, registro in enumerate(registros, 1):
                    for col, valor in enumerate(registro[:-1]):
                        sheet1.write(fila, col, str(valor))
                wb.save(directorio)
                eventos.Eventos.ventanaAviso('Expotación de datos realizada', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            eventos.Eventos.ventanaAviso('Error al exportar datos xls'+error, QtWidgets.QMessageBox.Icon.Warning)

    def exportarsxlsCli(self):
        """
        Exporta los datos de los clientes a un archivo XLS.
        """
        try:
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_datos.xls')
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar Datos en XLS', file, '.xls')
            if var.dlgabrir.accept and filename:
                wb = xlwt.Workbook()
                sheet1 = wb.add_sheet('Clientes')
                sheet1.write(0, 0, 'ID')
                sheet1.write(0, 1, 'DNI')
                sheet1.write(0, 2, 'Razon Social')
                sheet1.write(0, 3, 'Telefono')
                sheet1.write(0, 4, 'Direccion')
                sheet1.write(0, 5, 'Provincia')
                sheet1.write(0, 6, 'Municipio')
                sheet1.write(0, 7, 'Baja')

                registros = conexion.Conexion.selectClientesTodos()

                for fila, registro in enumerate(registros, 1):
                    for col, valor in enumerate(registro):
                        sheet1.write(fila, col, str(valor))
                wb.save(directorio)
                eventos.Eventos.ventanaAviso('Exportación de datos realizada', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            eventos.Eventos.ventanaAviso(error, QtWidgets.QMessageBox.Icon.Warning)

    def importardatosxls(self):
        """
        Importa datos de conductores desde un archivo XLS.
        """
        dniInvalido = False
        try:
            filename, _ = var.dlgabrir.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files(*)')
            if filename:
                file = filename
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols
                for i in range(filas):
                    if i == 0:
                        pass
                    else:
                        new = []
                        for j in range(columnas):
                            if j == 1:
                                dato = xlrd.xldate_as_datetime(datos.cell_value(i, j), documento.datemode)
                                # print(dato)
                                dato = dato.strftime('%d/%m/%Y')
                                # print(dato)
                                new.append(str(dato))
                            else:
                                new.append(str(datos.cell_value(i, j)))
                        if drivers.Drivers.validarDNI(new[0]):
                            conexion.Conexion.guardardri(new)
                        else:
                            dniInvalido = True
                    if i == filas - 1:
                        if dniInvalido:
                            eventos.Eventos.ventanaAviso('Se han encontrado DNIs inválidos y solo se han importado aquellos válidos', QtWidgets.QMessageBox.Icon.Warning)
                        eventos.Eventos.ventanaAviso('Importación de datos realizada', QtWidgets.QMessageBox.Icon.Warning)
                eventos.Eventos.selEstado(self)

        except Exception as error:
            eventos.Eventos.ventanaAviso(error, QtWidgets.QMessageBox.Icon.Warning)

    def importardatosxlsCli(self):
        """
        Importa datos de clientes desde un archivo XLS.
        """
        dniInvalido = False
        try:
            filename, _ = var.dlgabrir.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files(*)')
            if filename:
                file = filename
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols
                for i in range(filas):
                    if i == 0:
                        print('n')
                        pass
                    else:
                        new = []
                        for j in range(columnas):
                            new.append(str(datos.cell_value(i, j)))
                            print(new)
                        if drivers.Drivers.validarDNICli(new[0]):
                            conexion.Conexion.guardarCli(new)
                        else:
                            dniInvalido = True
                    if i == filas - 1:
                        if dniInvalido:
                            eventos.Eventos.ventanaAviso('Se han encontrado DNIs inválidos y solo se han importado aquellos válidos', QtWidgets.QMessageBox.Icon.Warning)
                        eventos.Eventos.ventanaAviso('Importación de datos realizada', QtWidgets.QMessageBox.Icon.Warning)
                eventos.Eventos.selEstadoCli()

        except Exception as error:
           eventos.Eventos.ventanaAviso(error, QtWidgets.QMessageBox.Icon.Warning)

    @staticmethod
    def ocultarFiltro():
        """
        Oculta o muestra el filtro de búsqueda en la interfaz.
        """
        try:
            var.ui.txtFiltro.clear()
            if var.ui.chkFiltrar.isChecked():
                var.ui.frameFiltrar.show()
            else:
                var.ui.frameFiltrar.hide()

        except Exception as e:
            print('Error al ocultar filtro', {e})

    @staticmethod
    def cargarDiaglosReport():
        """
        Carga los diálogos de reporte en la interfaz.
        """
        var.dialogReport = Ui_dialogReports()
        var.dialogReport.setupUi(QtWidgets.QDialog)

    @staticmethod
    def setRowBackground(tabla, row, color):
        """
        Establece el fondo de una fila específica en una tabla.

        :param tabla: La tabla en la que se establecerá el fondo.
        :param row: La fila para la que se establecerá el fondo.
        :param color: El color del fondo.
        """
        try:
            for column in range(tabla.columnCount()):
                item = tabla.item(row, column)
                if item is not None:
                    item.setBackground(color)
                    item.setForeground(Qt.GlobalColor.white)

        except Exception as e:
            print('Error al cambiar fondo de ', tabla.objectName(), e)

    @staticmethod
    def onCellEntered(tabla, row):
        """
        Maneja el evento de entrada a una celda en una tabla.

        :param tabla: La tabla en la que se ha ingresado una celda.
        :param row: La fila en la que se ha ingresado la celda.
        """
        try:

            eventos.Eventos.clearRowBackground(tabla, eventos.Eventos.current_hovered_row)
            if var.main.modoOscuro:
                color = "#8d58b3"
            else:
                color = "#747476"
            eventos.Eventos.setRowBackground(tabla, row, QColor(color))
            Eventos.current_hovered_row = row
        except Exception as e:
            print('Error on cell entered ', tabla.objectName(), e)

    @staticmethod
    def clearRowBackground(tabla, row):
        """
        Limpia el fondo de una fila específica en una tabla.

        :param tabla: La tabla en la que se limpiará el fondo.
        :param row: La fila para la que se limpiará el fondo.
        """
        try:
            if row != -1:
                for col in range(tabla.columnCount()):
                    item = tabla.item(row, col)
                    if item is not None:
                        if not var.main.modoOscuro:
                            if row % 2 == 0:
                                item.setBackground(QColor("#ffffff"))
                            else:
                                item.setBackground(QColor("#f5f5f5"))
                            item.setForeground(QColor(149, 149, 149))
                        else:
                            if row % 2 == 0:
                                item.setBackground(QColor(96, 96, 96))
                            else:
                                item.setBackground(Qt.GlobalColor.darkGray)
                            item.setForeground(Qt.GlobalColor.white)
        except Exception as e:
            print('Error al limpiar fondo ', tabla.objectName(), e)

    @staticmethod
    def cambiarEstiloTabla(tabla):
        """
        Cambia el estilo de una tabla según el modo de visualización.

        :param tabla: La tabla cuyo estilo se cambiará.
        """
        try:
            for row in range(tabla.rowCount()):
                for col in range(tabla.columnCount()):
                    item = tabla.item(row, col)
                    widget = tabla.cellWidget(row, col)
                    if item is None:
                        item = QTableWidgetItem()
                        tabla.setItem(row, col, item)
                    if var.main.modoOscuro:
                        if row % 2 == 0:
                            item.setBackground(QColor(96, 96, 96))
                        else:
                            item.setBackground(Qt.GlobalColor.darkGray)
                        item.setForeground(Qt.GlobalColor.white)
                    else:
                        if row % 2 == 0:
                            item.setBackground(QColor("#ffffff"))
                        else:
                            item.setBackground(QColor("#f5f5f5"))
                        item.setForeground(QColor(149, 149, 149))

        except Exception as e:
            print('error al cambiar estilo tabla',e)

    @staticmethod
    def comprobarFilas():
        """
        Comprueba el estado de las filas en una tabla para habilitar o deshabilitar ciertos botones.
        """
        try:
            if var.ui.tabViajes.rowCount() > 0 and var.ui.lblCodFac.text() != '':
                var.ui.btnFac.setEnabled(True)
            else:
                var.ui.btnFac.setEnabled(False)
        except Exception as e:
            print('error al comprobar filas', e)

