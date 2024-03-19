import conexion
from datetime import datetime
from PyQt6 import QtWidgets, QtCore, QtSql

import eventos
import var
from windowaux import *


class Clientes():
    """
    Clase para gestionar la información de los clientes.
    """
    def limpiarPanelCli(self=None):
        try:
            """
                   Limpia los widgets del panel de clientes.

                   :param self: Referencia a la instancia de la clase.
                   """
            listawidgets = [var.ui.lblCodeBD_2, var.ui.txtDni_2, var.ui.txtRazon, var.ui.txtMovil_2, var.ui.txtDirDriver_2, var.ui.lblValidardni_2]

            for widget in listawidgets:
                if widget.objectName() == "lblValidardni_2":
                    widget.hide()

                else:
                    widget.setText(None)

            var.ui.cmbProv_2.setCurrentText('')
            var.ui.cmbMuni_2.setCurrentText('')

        except Exception as error:
            print('error en limpiar panel cli', error)

    @staticmethod
    def obtenerCamposCli():
        """
            Obtiene los campos del cliente.

            :return: Lista con los campos del cliente.
            :rtype: list
            """
        try:
            cliente = [var.ui.txtDni_2, var.ui.txtRazon, var.ui.txtMovil_2, var.ui.txtDirDriver_2]
            newcliente = []
            for i in cliente:
                newcliente.append(i.text().title())

            newcliente.insert(4, var.ui.cmbProv_2.currentText())
            newcliente.insert(5, var.ui.cmbMuni_2.currentText())
            return newcliente
        except Exception as error:
            print("error alta clientes", error)

    def altaCli(self):
        """
        Da de alta un cliente.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            if len(var.ui.tabDrivers_2.selectedItems()) > 0 or var.ui.lblCodeBD_2.text() != '':  # si selecciono o busco un cliente que existe
                if var.cliente[7] != '':  # comprueba si está de baja
                    resultado = eventos.Eventos.ventanaConfirmacion('El cliente está dado de baja, quiere darlo de alta?', QtWidgets.QMessageBox.Icon.Warning)
                    if resultado == 0:
                        if drivers.Drivers.modificarFechaBajaCli(None):  # se da de alta
                            eventos.Eventos.ventanaAviso('El cliente ha sido dado de alta', QtWidgets.QMessageBox.Icon.Information)
                            var.ui.rbtAlta_2.setChecked(True)
                            eventos.Eventos.selEstadoCli()
                            Clientes.buscarCliTabla(var.cliente[0])
                            Clientes.cargarCli(self)
                else:
                    eventos.Eventos.ventanaAviso('El cliente ya está de alta', QtWidgets.QMessageBox.Icon.Warning)
            else:
                if not len(var.ui.tabDrivers_2.selectedItems()) > 0 and var.ui.txtDni_2.text() == '':
                    eventos.Eventos.ventanaAviso('Por favor, seleccione un cliente', QtWidgets.QMessageBox.Icon.Warning)
                else:
                    newcli = Clientes.obtenerCamposCli()

                    if drivers.Drivers.validarDNICli(newcli[0]):
                        if conexion.Conexion.guardarCli(newcli):
                            eventos.Eventos.ventanaAviso('Cliente dado de alta',
                                                         QtWidgets.QMessageBox.Icon.Information)
                            eventos.Eventos.selEstadoCli()
                    else:
                        eventos.Eventos.ventanaAviso('DNI inválido aseguúrese de corregirlo',
                                                     QtWidgets.QMessageBox.Icon.Information)

        except Exception as error:
            print("error alta cli", error)

    def cargartablacli(registros):
        """
        Carga registros en la tabla de clientes.

        :param registros: Lista de registros de clientes.
        """
        try:
            index = 0
            for registro in registros:
                var.ui.tabDrivers_2.setRowCount(index + 1)
                var.ui.tabDrivers_2.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabDrivers_2.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabDrivers_2.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabDrivers_2.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabDrivers_2.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))

                var.ui.tabDrivers_2.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers_2.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers_2.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers_2.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1

        except Exception as error:
            print('Error al cargar en tabla cli', error)

    def cargarCamposCli(registro):
        """
        Carga los campos de un cliente.

        :param registro: Lista que contiene los datos del cliente.
        """
        try:
            Clientes.limpiarPanelCli()
            datos = [var.ui.lblCodeBD_2, var.ui.txtDni_2, var.ui.txtRazon, var.ui.txtMovil_2, var.ui.txtDirDriver_2,
                     var.ui.cmbProv_2, var.ui.cmbMuni_2]

            for i, widget in enumerate(datos):
                if isinstance(widget, QtWidgets.QComboBox):
                    widget.setCurrentText(registro[i])
                else:
                    widget.setText(str(registro[i]))

        except Exception as error:
            print('Error al cargar datos de 1 cli', error)

    def cargarCli(self):
        """
        Carga un cliente.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            codigo = var.ui.tabDrivers_2.item(var.ui.tabDrivers_2.currentRow(), 0).text()
            registro = conexion.Conexion.onecli(codigo)
            var.cliente = registro
            Clientes.cargarCamposCli(var.cliente)
            var.ui.txtCifFac.setText(var.cliente[1])
            var.ui.txtFiltro.clear()
            if var.ui.rbtCliente.isChecked():
                var.ui.txtFiltro.setText(var.cliente[1])
        except Exception as error:
            print('error al conseguir registro cli', error)

    def buscarCliTabla(codigo):
        """
        Busca un cliente en la tabla.

        :param codigo: Código del cliente a buscar.
        """
        try:
            tabla = var.ui.tabDrivers_2
            for fila in range(tabla.rowCount()):
                celda = tabla.item(fila, 0)
                codigoCelda = celda.text()
                if codigoCelda == str(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(celda)
        except Exception as error:
            print('No se ha podido seleccionar al cliente en la tabla', error)

    @staticmethod
    def buscarCli(dni):
        """
        Busca un cliente por su DNI.

        :param dni: DNI del cliente a buscar.
        """
        try:
            if dni == '':
                eventos.Eventos.ventanaAviso('Por favor, introduce un DNI', QtWidgets.QMessageBox.Icon.Warning)
                return False
            else:
                registro = conexion.Conexion.codCli(dni)

                if registro is None:
                    eventos.Eventos.ventanaAviso('El cliente no existe', QtWidgets.QMessageBox.Icon.Warning)
                    Clientes.limpiarPanelCli()
                    return False
                else:
                    var.cliente = registro
                    if registro[7] != "":
                        var.ui.rbtBaja_2.setChecked(True)
                    else:
                        var.ui.rbtAlta_2.setChecked(True)

                    eventos.Eventos.selEstadoCli()
                    Clientes.buscarCliTabla(registro[0])
                    Clientes.cargarCamposCli(var.cliente)
                    return True

            # var.ui.frameForm.hide()
        except Exception as error:
            print('Error al buscar cliente', error)

    def bajaCli(self):
        """
        Da de baja un cliente.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            if len(var.ui.tabDrivers_2.selectedItems()) > 0:
                fecha = var.ui.tabDrivers_2.item(var.ui.tabDrivers_2.currentRow(), 4).text()
                if fecha is None or fecha == '':
                    resultado = eventos.Eventos.ventanaConfirmacion('El cliente está dado de alta, quiere darlo de baja?', QtWidgets.QMessageBox.Icon.Information)

                    if resultado == 0:
                        codigo = var.ui.lblCodeBD_2.text()
                        conexion.Conexion.bajaCli(codigo)
                        var.ui.rbtBaja_2.setChecked(True)
                        eventos.Eventos.selEstadoCli()
                        Clientes.cargarCli(self)
                        Clientes.buscarCliTabla(codigo)
                else:
                    eventos.Eventos.ventanaAviso('El cliente ya está de baja', QtWidgets.QMessageBox.Icon.Warning)
            else:
                eventos.Eventos.ventanaAviso('Por favor, selecciona un cliente', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            print('Error al dar de baja un cliente', error)

    def modificarCli(self):
        """
        Modifica un cliente.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            if len(var.ui.tabDrivers_2.selectedItems()) > 0 or var.ui.lblCodeBD_2.text() != '':  # Comprueba driver seleccionado o buscado
                cli = Clientes.obtenerCamposCli()  # Obtiene registro con los datos despues de pulsar modificar
                codigo = var.ui.lblCodeBD_2.text()
                print('obtener campos', cli)
                print('varcli', var.cliente[1:7])
                if var.cliente[1:7] == cli:  # compara los campos guardados en var.driver antes de modificar y los campos despues de pulsar modificar
                    eventos.Eventos.ventanaAviso('No hay datos que modificar', QtWidgets.QMessageBox.Icon.Information)
                else:
                    conexion.Conexion.modificarCli(cli)
                    Clientes.cargarCli(self=None)
                    eventos.Eventos.selEstadoCli()  # actualizar la tabla con los nuevos datos modificados

                if var.cliente[7] != '':  # si tiene fecha de baja
                    resultado = eventos.Eventos.ventanaConfirmacion(
                        'El cliente está dado de baja, quiere modificar la fecha de la baja?', QtWidgets.QMessageBox.Icon.Information)

                    if resultado == 0:
                        var.calendar.modificarBaja = True
                        var.calendar.show()
            else:

                eventos.Eventos.ventanaAviso('Por favor, selecciona un cliente', QtWidgets.QMessageBox.Icon.Information)

        except Exception as error:
            print('No se ha podido modificar cliente', error)

    def modificarFechaBajaCli(fecha):
        """
        Modifica la fecha de baja de un cliente.

        :param fecha: Nueva fecha de baja del cliente.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set baja= :fechabaja where codigo = :cod')
            query.bindValue(':fechabaja', fecha)
            query.bindValue(':cod', var.cliente[0])
            if query.exec():
                return True
        except Exception as error:
            print('error al modificar fecha baja cli', error)
