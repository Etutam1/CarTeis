from PyQt6 import QtWidgets, QtCore, QtSql
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QMainWindow, QTableWidgetItem

import clientes
import conexion
import drivers
import eventos
import facturas
import main
import var


class Facturas():
    """
    Clase que define operaciones relacionadas con la gestión de facturas.
    """

    @staticmethod
    def limpiarViaje():
        """
        Limpia los widgets relacionados con los datos de un viaje en la interfaz.
        """
        try:
            widgets = [var.ui.cmbProvD,
                       var.ui.cmbProvO,
                       var.ui.cmbMuniD,
                       var.ui.cmbMuniO,
                       var.ui.txtKms,
                       var.ui.rbtNac]

            for widget in widgets:
                if isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText("")
                elif isinstance(widget, QtWidgets.QRadioButton):
                    widget.setChecked(True)
                else:
                    # widget.setCurrentText("")
                    widget.setCurrentIndex(-1)
            var.ui.tabViajes.clearSelection()
        except Exception as e:
            print('Error al limpair panel viaje', e)

    @staticmethod
    def limpiarFac():
        try:
            widgets = [var.ui.lblCodFac,
                       var.ui.txtCifFac,
                       var.ui.cmbDriverFac,
                       var.ui.txtFechaFac,
                       var.ui.txtSubTotalFac,
                       var.ui.txtIva,
                       var.ui.txtTotalFac
                       ]

            for widget in widgets:
                if isinstance(widget, QtWidgets.QLineEdit) or isinstance(widget, QtWidgets.QLabel):
                    widget.setText("")
                else:
                    widget.setItemText(0, '')
                    widget.setCurrentText('')

            var.ui.tabFac.clearSelection()
            var.ui.tabViajes.setRowCount(0)
        except Exception as e:
            print('error al limpiar panel factura', e)

    @staticmethod
    def limpiarPanelFac():
        """
        Limpia los campos del panel de facturas en la interfaz.
        """
        try:
            campos = [var.ui.lblCodFac, var.ui.txtCifFac, var.ui.cmbDriverFac, var.ui.txtFechaFac, var.ui.cmbProvD,
                      var.ui.cmbProvO, var.ui.cmbMuniD, var.ui.cmbMuniO, var.ui.txtKms, var.ui.tabViajes, var.ui.tabFac,
                      var.ui.rbtNac,
                      var.ui.txtTotalFac, var.ui.txtSubTotalFac, var.ui.txtIva, var.ui.txtFiltro]

            for widget in campos:
                if isinstance(widget, QtWidgets.QComboBox):
                    # widget.setItemText(0, '')
                    # widget.setCurrentText('')
                    widget.setCurrentIndex(-1)
                elif isinstance(widget, QtWidgets.QTableWidget):
                    if widget.objectName() == 'tabFac':
                        var.ui.chkFiltrar.setChecked(False)
                        conexion.Conexion.cargarFacturas()
                    else:
                        widget.setRowCount(0)
                elif isinstance(widget, QtWidgets.QRadioButton):
                    widget.setChecked(True)
                else:
                    widget.setText(None)
        except Exception as error:
            print('Error al limpiar panel facturas', error)

    @staticmethod
    def facturar():
        """
        Crea una factura en la interfaz y en la base de datos si los campos son válidos.
        """
        try:
            if var.ui.lblCodFac.text() == '':
                codFac = conexion.Conexion.guardarFac()

                if codFac != '':
                    conexion.Conexion.cargarFacturas()
                    # facturas.Facturas.limpiarPanelFac()
                    var.ui.tabFac.clearSelection()
                    Facturas.buscarFacTabla(codFac)
                    facturas.Facturas.cargarFactura()
                    conexion.Conexion.guardarViajes()
                    eventos.Eventos.ventanaAviso('Factura creada con éxito', QtWidgets.QMessageBox.Icon.Information)

        except Exception as error:
            print('Error al crear factura', error)
            eventos.Eventos.ventanaAviso(error, QtWidgets.QMessageBox.Icon.Information)

    @staticmethod
    def buscarFacTabla(codigo):
        """
        Busca y selecciona una factura en la tabla de facturas según su código.

        :param codigo: El código de la factura a buscar.
        """
        try:
            tabla = var.ui.tabFac
            for fila in range(tabla.rowCount()):
                celda = tabla.item(fila, 0)
                codigoCelda = celda.text()
                if codigoCelda == str(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(celda)
        except Exception as error:
            print('No se ha podido seleccionar factura en la tabla', error)

    @staticmethod
    def checkCampos(campos):
        """
        Verifica si los campos de una factura son válidos.

        :param campos: Lista de campos a verificar.
        :return: True si los campos son válidos, False en caso contrario.
        """
        try:
            for campo in campos:
                if isinstance(campo, QtWidgets.QComboBox):
                    if campo.currentText() == '':
                        eventos.Eventos.ventanaAviso('Por favor, seleccione un conductor',
                                                     QtWidgets.QMessageBox.Icon.Warning)
                        return False
                elif campo.objectName() == 'txtCifFac':
                    if not Facturas.checkCIF(campo.text()):
                        return False
                elif campo.objectName() == 'txtFechaFac':
                    if campo.text() == '':
                        eventos.Eventos.ventanaAviso('Por favor, indique una fecha de alta',
                                                     QtWidgets.QMessageBox.Icon.Warning)
                        return False
            return True
        except Exception as error:
            print('Error al comprobar campos factura', error)

    @staticmethod
    def buscarCliFac(cif):
        """
        Busca un cliente en la interfaz y lo muestra si existe.

        :param cif: El CIF del cliente a buscar.
        """
        try:
            if clientes.Clientes.buscarCli(cif):
                var.ui.panelPrincipal.setCurrentIndex(1)

        except Exception as error:
            print('Error al buscarCliFac', error)

    @staticmethod
    def checkCIF(cif):
        """
        Verifica si un CIF dado es válido.

        :param cif: El CIF a verificar.
        :return: True si el CIF es válido, False en caso contrario.
        """
        try:
            if cif == '':
                eventos.Eventos.ventanaAviso('Por favor, indique un CIF', QtWidgets.QMessageBox.Icon.Warning)
                return False
            else:
                cli = conexion.Conexion.codCli(cif.upper())
                if cli is None:
                    eventos.Eventos.ventanaAviso('El cliente no existe', QtWidgets.QMessageBox.Icon.Warning)
                    return False
                elif cli[7] != '':
                    eventos.Eventos.ventanaAviso('El cliente está de baja', QtWidgets.QMessageBox.Icon.Warning)
                    return False
            return True
        except Exception as error:
            print('Error al comprobar CIF', error)

    @staticmethod
    def cargarTablaFac(registros):
        """
        Carga datos en la tabla de facturas en la interfaz.

        :param registros: Los datos a cargar en la tabla.
        """
        try:
            for fila, registro in enumerate(registros):
                var.ui.tabFac.setRowCount(fila + 1)
                var.ui.tabFac.setItem(fila, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabFac.setItem(fila, 1, QtWidgets.QTableWidgetItem(str(registro[1])))

                var.ui.tabFac.item(fila, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabFac.item(fila, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                widget_contenedor = facturas.Facturas.botonEliminarFac(fila)
                var.ui.tabFac.setCellWidget(fila, 2, widget_contenedor)

        except Exception as error:
            print('Error al cargar en tabla fac', error)

    @staticmethod
    def cargarTablaViajes(registros):
        """
        Carga datos en la tabla de viajes en la interfaz.

        :param registros: Los datos a cargar en la tabla.
        """
        try:
            for fila, registro in enumerate(registros):
                var.ui.tabViajes.setRowCount(fila + 1)
                for columna, dato in enumerate(registro):

                    if isinstance(dato, QtWidgets.QWidget):
                        var.ui.tabViajes.setCellWidget(fila, columna, dato)
                    else:
                        var.ui.tabViajes.setItem(fila, columna, QtWidgets.QTableWidgetItem(str(registro[columna])))
                        if columna == 1 or columna == 2:
                            var.ui.tabViajes.item(fila, columna).setTextAlignment(
                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                        elif columna == 5:
                            var.ui.tabViajes.item(fila, columna).setTextAlignment(
                                QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
                        else:
                            var.ui.tabViajes.item(fila, columna).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                widget_contenedor = facturas.Facturas.botonesTabViaje(fila)
                var.ui.tabViajes.setCellWidget(fila, 6, widget_contenedor)


        except Exception as error:
            print('Error al cargar en tabla viajes', error)

    @staticmethod
    def cargarViajeTabla(viaje):
        """
        Carga un viaje en la tabla de viajes en la interfaz.

        :param viaje: Los datos del viaje a cargar.
        """
        try:
            fila = var.ui.tabViajes.rowCount()
            var.ui.tabViajes.insertRow(fila)

            for columna, dato in enumerate(viaje):
                var.ui.tabViajes.setItem(fila, columna, QtWidgets.QTableWidgetItem(str(viaje[columna])))
                if columna == 1 or columna == 2:
                    var.ui.tabViajes.item(fila, columna).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
                elif columna == 5:
                    var.ui.tabViajes.item(fila, columna).setTextAlignment(
                        QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
                else:
                    var.ui.tabViajes.item(fila, columna).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            widget_contenedor = facturas.Facturas.botonesTabViaje(fila)
            var.ui.tabViajes.setCellWidget(fila, 6, widget_contenedor)

        except Exception as error:
            print('Error al cargar en tabla viajes', error)

    @staticmethod
    def cargarFactura():
        """
        Carga los datos de una factura seleccionada en la interfaz.
        """
        try:
            numFac = var.ui.tabFac.item(var.ui.tabFac.currentRow(), 0).text()
            factura = conexion.Conexion.onefac(numFac)
            Facturas.cargarCamposFac(factura)
            # conexion.Conexion.cargarViajes(numFac)
            # Facturas.cargarTotalFactura()
            var.ui.tabViajes.clearSelection()
        except Exception as error:
            print('Error al cargar factura', error)

    @staticmethod
    def cargarCamposFac(factura):
        """
        Carga los campos de una factura en la interfaz.

        :param factura: Los datos de la factura a cargar.
        """
        try:
            driver = conexion.Conexion.onedriver(factura[3])

            var.ui.lblCodFac.setText(factura[0])
            var.ui.txtCifFac.setText(factura[1])
            var.ui.txtFechaFac.setText(factura[2])

            var.ui.cmbDriverFac.setItemText(0, driver[0] + '.' + driver[3])
            var.ui.cmbDriverFac.setCurrentIndex(0)

        except Exception as error:
            print('Error al cargar campos factura', error)

    @staticmethod
    def cargarCamposViaje(viaje):
        """
        Carga los campos de un viaje en la interfaz.

        :param viaje: Los datos del viaje a cargar.
        """
        var.ui.cmbProvO.setCurrentText(viaje[1].split('-')[1])
        var.ui.cmbMuniO.setCurrentText(viaje[1].split('-')[0])
        var.ui.cmbProvD.setCurrentText(viaje[2].split('-')[1])
        var.ui.cmbMuniD.setCurrentText(viaje[2].split('-')[0])
        var.ui.txtKms.setText(viaje[3])
        eventos.Eventos.selEstadoTarifa()

    @staticmethod
    def cargarViaje():
        """
        Carga los datos de un viaje seleccionado en la interfaz.
        """
        try:
            viaje = []

            for col in range(var.ui.tabViajes.columnCount() - 2):
                celda = var.ui.tabViajes.item(var.ui.tabViajes.currentRow(), col)
                viaje.append(celda.text())

            Facturas.cargarCamposViaje(viaje)

        except Exception as error:
            print('error al cargar viaje', error)

    @staticmethod
    def grabarViaje():
        """
        Guarda un nuevo viaje en la interfaz y en la base de datos si es válido.
        """
        try:
            if var.ui.lblCodFac.text() == '':
                if Facturas.checkcmb() and var.ui.txtKms.text() != '':
                    viaje = []
                    fila = var.ui.tabViajes.rowCount()
                    viaje.append(str(fila + 1))
                    viaje.append(var.ui.cmbMuniO.currentText() + '-' + var.ui.cmbProvO.currentText())
                    viaje.append(var.ui.cmbMuniD.currentText() + '-' + var.ui.cmbProvD.currentText())
                    viaje.append(var.ui.txtKms.text())
                    tarifa = facturas.Facturas.checkTarifa()
                    viaje.append(tarifa)
                    total = float(var.ui.txtKms.text()) * float(tarifa)
                    viaje.append(round(total, 2))
                    facturas.Facturas.cargarViajeTabla(viaje)
                    eventos.Eventos.cambiarEstiloTabla(var.ui.tabViajes)
                else:
                    eventos.Eventos.ventanaAviso('Por favor cubra todos los campos', QtWidgets.QMessageBox.Icon.Warning)
            elif Facturas.checkcmb() and var.ui.txtKms.text() != '':
                idViaje = conexion.Conexion.guardarViaje()
                if idViaje != '':
                    conexion.Conexion.cargarViajes(var.ui.lblCodFac.text())
                    Facturas.buscarViajeTabla(idViaje)
            else:
                eventos.Eventos.ventanaAviso('Por favor cubra todos los campos', QtWidgets.QMessageBox.Icon.Warning)
        except Exception as error:
            print('error al grabar viaje', error)

    @staticmethod
    def buscarViajeTabla(codigo):
        """
        Busca y selecciona un viaje en la tabla de viajes según su código.

        :param codigo: El código del viaje a buscar.
        """
        try:
            tabla = var.ui.tabViajes
            for fila in range(tabla.rowCount()):
                celda = tabla.item(fila, 0)
                codigoCelda = celda.text()
                if codigoCelda == str(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(celda)
        except Exception as error:
            print('No se ha podido seleccionar viaje en la tabla', error)

    @staticmethod
    def borrarViaje(fila):
        """
        Borra un viaje de la interfaz y de la base de datos.

        :param fila: La fila del viaje a borrar en la tabla de viajes.
        """
        try:
            var.ui.tabViajes.selectRow(fila)
            idViaje = var.ui.tabViajes.item(var.ui.tabViajes.currentRow(), 0).text()
            resultado = eventos.Eventos.ventanaConfirmacion('Quiere eliminar el viaje?',
                                                            QtWidgets.QMessageBox.Icon.Question)
            if resultado == 0 and var.ui.lblCodFac.text() != '':
                if conexion.Conexion.eliminarViaje(idViaje):
                    numFac = var.ui.tabFac.item(var.ui.tabFac.currentRow(), 0).text()
                    conexion.Conexion.cargarViajes(numFac)
                    var.ui.tabViajes.clearSelection()
                    facturas.Facturas.cargarTotalFactura()
            elif resultado == 0 and var.ui.lblCodFac.text() == '':
                selected_row = var.ui.tabViajes.currentRow()
                if selected_row != -1:
                    var.ui.tabViajes.removeRow(selected_row)

            facturas.Facturas.limpiarViaje()
        except Exception as error:
            print('Error al borrar viaje', error)

    @staticmethod
    def modificarViaje(fila):
        """
        Modifica un viaje en la interfaz y en la base de datos si es válido.

        :param fila: La fila del viaje a modificar en la tabla de viajes.
        """

        try:
            if not len(var.ui.tabViajes.selectedItems()) > 0:
                eventos.Eventos.ventanaAviso("Por favor selecciona el viaje", QtWidgets.QMessageBox.Icon.Warning)

            elif fila == var.ui.tabViajes.currentRow():
                resultado = eventos.Eventos.ventanaConfirmacion('Quiere modificar el viaje?',
                                                                QtWidgets.QMessageBox.Icon.Question)
                if resultado == 0:
                    numviaje = var.ui.tabViajes.item(var.ui.tabViajes.currentRow(), 0).text()

                    viaje = Facturas.obtenerCamposViaje()

                    viajeTabla = Facturas.obtenerViajeTabla()

                    if viaje != viajeTabla:
                        if var.ui.lblCodFac.text() != '':
                            if conexion.Conexion.modificarViaje(viaje):
                                numFac = var.ui.tabFac.item(var.ui.tabFac.currentRow(), 0).text()
                                conexion.Conexion.cargarViajes(numFac)

                        else:
                            Facturas.modificarViajeTabla(viaje)
                        facturas.Facturas.cargarTotalFactura()

                    else:
                        eventos.Eventos.ventanaAviso("No hay datos que modificar",
                                                     QtWidgets.QMessageBox.Icon.Information)

        except Exception as e:
            print('Error al modificar viaje', e)

    @staticmethod
    def obtenerViajeTabla():
        """
        Obtiene los datos de un viaje de la tabla de viajes.

        :return: Una lista con los datos del viaje.
        """
        try:
            viajeTabla = []

            for col in range(1, var.ui.tabViajes.columnCount() - 2):
                celda = var.ui.tabViajes.item(var.ui.tabViajes.currentRow(), col)

                if col == 1 or col == 2:
                    viajeTabla.append(celda.text().split("-")[0])
                    viajeTabla.append(celda.text().split("-")[1])
                else:
                    viajeTabla.append(celda.text())

            return viajeTabla

        except Exception as e:
            print("Error al obtejer viaje tabla", e)

    @staticmethod
    def cargarTotalFactura():
        """
        Calcula y carga el total de la factura en la interfaz.
        """

        try:
            if var.ui.tabViajes.rowCount() > 0:
                precio = 0

                for i in range(var.ui.tabViajes.rowCount()):
                    precio += float(var.ui.tabViajes.item(i, 5).text())

                var.ui.txtSubTotalFac.setText(str(round(precio, 2)) + " €")
                iva = precio * 0.21
                var.ui.txtIva.setText(str(round(iva, 2)) + " €")
                var.ui.txtTotalFac.setText(str(round(precio + iva, 2)) + " €")
            else:
                var.ui.txtSubTotalFac.clear()
                var.ui.txtIva.clear()
                var.ui.txtTotalFac.clear()
        except Exception as e:
            print('Error al cargarTotalfFactura', e)

    @staticmethod
    def checkcmb():
        """
        Comprueba si los campos de los combos están seleccionados.

        :return: True si todos los combos tienen selección, False en caso contrario.
        """
        try:
            combos = [var.ui.cmbMuniO, var.ui.cmbMuniD, var.ui.cmbProvO, var.ui.cmbProvD]
            for combo in combos:
                if combo.currentText() == '':
                    return False
            return True
        except Exception as error:
            print('Error al comprobar cmbs', error)

    @staticmethod
    def checkTarifa():
        """
        Comprueba la tarifa seleccionada.

        :return: El valor de la tarifa seleccionada.
        """
        try:
            if var.ui.rbtNac.isChecked():
                return 0.8
            elif var.ui.rbtProv.isChecked():
                return 0.4
            else:
                return 0.2
        except Exception as error:
            print('error al checkear tarifa', error)

    @staticmethod
    def Filtrar():
        """
        Filtra las facturas según la opción seleccionada en la interfaz.
        """

        try:
            if var.ui.rbtCliente.isChecked():
                if Facturas.checkCIF(var.ui.txtFiltro.text()):
                    conexion.Conexion.cargarFacturas()
            elif var.ui.rbtConductor.isChecked():

                if not var.ui.txtFiltro.text().strip():
                    eventos.Eventos.ventanaAviso("Por favor indique un DNI", QtWidgets.QMessageBox.Icon.Warning)
                else:
                    driver = conexion.Conexion.codDri(var.ui.txtFiltro.text())
                    if not driver:
                        eventos.Eventos.ventanaAviso("El conductor no existe", QtWidgets.QMessageBox.Icon.Warning)
                    else:
                        conexion.Conexion.cargarFacturas()
            elif var.ui.rbtNum.isChecked():
                if not var.ui.txtFiltro.text().strip():
                    eventos.Eventos.ventanaAviso("Por favor indique un número de factura", QtWidgets.QMessageBox.Icon.Warning)
                else:
                    fac = conexion.Conexion.onefac(var.ui.txtFiltro.text())
                    if not fac:
                        eventos.Eventos.ventanaAviso("La factura no existe", QtWidgets.QMessageBox.Icon.Warning)
                    else:
                        facturas.Facturas.buscarFacTabla(fac[0])


        except Exception as e:
            print('Error al filtrar facturas', {e})

    @staticmethod
    def botonesTabViaje(fila):
        """
        Crea los botones de acción para una fila de la tabla de viajes.

        :param fila: Índice de la fila en la tabla de viajes.
        :return: El contenedor de widgets con los botones de acción.
        """
        try:
            widget_contenedor = QWidget()
            layout_contenedor = QHBoxLayout(widget_contenedor)
            boton = QtWidgets.QPushButton()
            boton.setFixedSize(24, 24)
            boton.setIcon(QIcon(':/img/img/bin.png'))
            boton.clicked.connect(lambda _, r=fila: facturas.Facturas.borrarViaje(r))

            botonlapiz = QtWidgets.QPushButton()
            botonlapiz.setFixedSize(24, 24)
            botonlapiz.setIcon(QIcon(':/img/img/edit_.png'))
            botonlapiz.clicked.connect(lambda _, r=fila: facturas.Facturas.modificarViaje(r))
            layout_contenedor.addWidget(boton)
            layout_contenedor.addWidget(botonlapiz)
            layout_contenedor.setContentsMargins(10, 0, 10, 0)
            return widget_contenedor
        except Exception as e:
            print('Error al crear botones', e)

    @staticmethod
    def botonEliminarFac(fila):
        try:
            widget_contenedor = QWidget()
            layout_contenedor = QHBoxLayout(widget_contenedor)
            boton = QtWidgets.QPushButton()
            boton.setFixedSize(24, 24)
            boton.setIcon(QIcon(':/img/img/bin.png'))
            boton.clicked.connect(lambda _, r=fila: facturas.Facturas.borrarFac(r))

            layout_contenedor.addWidget(boton)
            layout_contenedor.setContentsMargins(10, 0, 10, 0)
            return widget_contenedor

        except Exception as e:
            print('Error al crear botones', e)

    @staticmethod
    def obtenerCamposViaje():
        """
        Obtiene los campos de entrada del viaje desde la interfaz.

        :return: Una lista con los datos del viaje.
        """
        try:
            viaje = []
            campos = [var.ui.cmbMuniO, var.ui.cmbProvO, var.ui.cmbMuniD, var.ui.cmbProvD, var.ui.txtKms]
            for campo in campos:
                if isinstance(campo, QtWidgets.QLineEdit):
                    viaje.append(campo.text())
                else:
                    viaje.append(campo.currentText())
            viaje.append(str(Facturas.checkTarifa()))
            return viaje
        except Exception as e:
            print('Error al obtener campos viaje', e)

    @staticmethod
    def modificarViajeTabla(viaje):
        """
        Modifica los datos de un viaje en la tabla de viajes.

        :param viaje: Lista con los datos del viaje a modificar.
        """
        try:
            print(viaje)
            var.ui.tabViajes.setItem(var.ui.tabViajes.currentRow(), 1, QTableWidgetItem(f"{viaje[0]}-{viaje[1]}"))
            var.ui.tabViajes.setItem(var.ui.tabViajes.currentRow(), 2, QTableWidgetItem(f"{viaje[2]}-{viaje[3]}"))
            var.ui.tabViajes.setItem(var.ui.tabViajes.currentRow(), 3, QTableWidgetItem(str(viaje[4])))
            var.ui.tabViajes.setItem(var.ui.tabViajes.currentRow(), 4, QTableWidgetItem(str(viaje[5])))
            total = float(viaje[4]) * float(viaje[5])
            var.ui.tabViajes.setItem(var.ui.tabViajes.currentRow(), 5, QTableWidgetItem(str(round(total, 2))))
        except Exception as e:
            print('Error al modificar viaje tabla', e)

    @staticmethod
    def borrarFac(fila):
        try:
            var.ui.tabFac.selectRow(fila)
            idFac = var.ui.tabFac.item(fila, 0).text()
            resultado = eventos.Eventos.ventanaConfirmacion('Quiere eliminar la factura?',
                                                            QtWidgets.QMessageBox.Icon.Question)
            if resultado == 0:
                if conexion.Conexion.eliminarFac(idFac):
                    conexion.Conexion.cargarFacturas()
                    var.ui.tabViajes.setRowCount(0)
                    var.ui.tabFac.clearSelection()
                Facturas.limpiarPanelFac()
        except Exception as e:
            print('error al borrar factura', e)

    @staticmethod
    def limpiarFiltroFac():
        try:
            var.ui.chkFiltrar.setChecked(False)
            conexion.Conexion.cargarFacturas()
            var.ui.tabFac.clearSelection()
            Facturas.limpiarPanelFac()
        except Exception as e:
            print('error al limpiar filtro fac', e)
