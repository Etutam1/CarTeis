import conexion, clientes
from datetime import datetime
from PyQt6 import QtWidgets, QtCore, QtSql

import eventos
import var
from windowaux import *


class Drivers():
    """
    Clase para gestionar la información de los conductores.
    """

    @staticmethod
    def validarDNI(dni):
        """
        Valida un número de DNI español.

        :param dni: El número de DNI a validar.
        :return: True si el DNI es válido, False si no lo es.
        """
        try:
            tabla = "TRWAGMYFPDXBNJCSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"

            if len(dni) == 9:  # compruebo que son 9
                dig_control = dni[8]  # tomo la letra del dni
                dni = dni[:8]  # tomo los numeros del dni
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    if var.ui.txtNombre.hasFocus():
                        var.ui.lblValidardni.setPixmap(QIcon(":/img/img/valido.png").pixmap(30, 50))
                        var.ui.lblValidardni.show()
                    return True

                else:
                    if var.ui.txtNombre.hasFocus():
                        var.ui.lblValidardni.setPixmap(QIcon(":/img/img/invalido.png").pixmap(30, 50))
                        var.ui.lblValidardni.show()
                    return False
            else:
                if var.ui.txtNombre.hasFocus():
                    var.ui.lblValidardni.setPixmap(QIcon(":/img/img/invalido.png").pixmap(30, 50))
                    var.ui.lblValidardni.show()
                return False

        except Exception as error:
            print("error en validar dni ", error)

    @staticmethod
    def validarDNICli(dni):
        """
        Valida un número de DNI para un cliente.

        :param dni: El número de DNI a validar.
        :return: True si el DNI es válido, False si no lo es.
        """
        try:
            tabla = "TRWAGMYFPDXBNJCSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"

            if len(dni) == 9:  # compruebo que son 9
                dig_control = dni[8]  # tomo la letra del dni
                dni = dni[:8]  # tomo los numeros del dni
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:

                    if var.ui.txtRazon.hasFocus():
                        var.ui.lblValidardni_2.setPixmap(QIcon(":/img/img/valido.png").pixmap(30, 50))
                        var.ui.lblValidardni_2.show()
                    return True
                else:
                    if var.ui.txtRazon.hasFocus():
                        var.ui.lblValidardni_2.setPixmap(QIcon(":/img/img/invalido.png").pixmap(30, 50))
                        var.ui.lblValidardni_2.show()
                    return False
            else:
                if var.ui.txtRazon.hasFocus():
                    var.ui.lblValidardni_2.setPixmap(QIcon(":/img/img/invalido.png").pixmap(30, 50))
                    var.ui.lblValidardni_2.show()
                return False

        except Exception as error:
            print("error en validar dni ", error)

    def cargarFecha(qDate):
        """
        Carga una fecha en un campo de texto en la interfaz gráfica.

        :param qDate: La fecha en formato QDate.
        :return: None
        """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if not var.calendar.modificarBaja:
                if var.ui.panelPrincipal.currentIndex() == 0:
                    var.ui.txtFechaAlta.setText(str(data))
                elif var.ui.panelPrincipal.currentIndex() == 2:
                    var.ui.txtFechaFac.setText(str(data))
            else:
                if var.ui.panelPrincipal.currentIndex() == 0:
                    if drivers.Drivers.modificarFechaBaja(data):
                        eventos.Eventos.ventanaAviso('Se ha modificado la fecha de baja', QtWidgets.QMessageBox.Icon.Information)
                        eventos.Eventos.selEstado(self=None)
                        Drivers.buscarDriverTabla(var.driver[0])
                        var.calendar.modificarBaja = False
                elif var.ui.panelPrincipal.currentIndex() == 1:
                    if drivers.Drivers.modificarFechaBajaCli(data):
                        eventos.Eventos.ventanaAviso('Se ha modificado la fecha de baja', QtWidgets.QMessageBox.Icon.Information)
                        eventos.Eventos.selEstadoCli()
                        clientes.Clientes.buscarCliTabla(var.cliente[0])
                        var.calendar.modificarBaja = False
            var.calendar.hide()
        except Exception as error:
            print('error en cargar fecha', error)

    def limpiarPanel(self=None):
        """
        Limpia los campos del panel de información de conductor en la interfaz gráfica.

        :return: None
        """
        try:
            listawidgets = [var.ui.lblCodeBD, var.ui.txtDni, var.ui.txtFechaAlta, var.ui.txtApel, var.ui.txtNombre,
                            var.ui.txtDirDriver,
                            var.ui.txtMovilDriver, var.ui.txtSalario, var.ui.lblValidardni]

            for widget in listawidgets:
                if widget.objectName() == "lblValidardni":
                    widget.hide()

                else:
                    widget.setText(None)

            chklicencia = [var.ui.chkA, var.ui.chkB, var.ui.chkC, var.ui.chkD]
            for i in chklicencia:
                i.setChecked(False)

            var.ui.cmbProv.setCurrentText('')
            var.ui.cmbMuni.setCurrentText('')

        except Exception as error:
            print('error en limpiar panel', error)


    def altadriver(self):
        """
        Realiza el alta de un nuevo conductor en la base de datos.

        :return: None
        """
        try:
            if len(var.ui.tabDrivers.selectedItems()) > 0 or var.ui.lblCodeBD.text() != '': # si selecciono o busco un driver que existe
                if var.driver[11] != '':  # comprueba si está de baja

                    resultado = eventos.Eventos.ventanaConfirmacion('El conductor está dado de baja, quiere darlo de alta?', QtWidgets.QMessageBox.Icon.Information)

                    if resultado == 0:
                        if drivers.Drivers.modificarFechaBaja(None): #se da de alta
                            eventos.Eventos.ventanaAviso('El conductor ha sido dado de alta', QtWidgets.QMessageBox.Icon.Information)
                            var.ui.rbtAlta.setChecked(True)
                            eventos.Eventos.selEstado(self)
                            drivers.Drivers.buscarDriverTabla(var.driver[0])
                            drivers.Drivers.cargarDriver(self)
                else:
                    eventos.Eventos.ventanaAviso('El conductor ya está dado de alta',QtWidgets.QMessageBox.Icon.Information)

            else:
                if not len(var.ui.tabDrivers.selectedItems()) > 0 and var.ui.txtDni.text() == '':
                    eventos.Eventos.ventanaAviso('Por favor, selecciona un conductor', QtWidgets.QMessageBox.Icon.Information)
                else:
                    newdriver = Drivers.obtenerDatosCampos(self)
                    if drivers.Drivers.validarDNI(newdriver[0]):
                        if conexion.Conexion.guardardri(newdriver):
                            eventos.Eventos.ventanaAviso('El conductor ha sido dado de alta',
                                                         QtWidgets.QMessageBox.Icon.Information)
                            eventos.Eventos.selEstado(self)
                    else:
                        eventos.Eventos.ventanaAviso('DNI inválido, asegurese de corregirlo',
                                                     QtWidgets.QMessageBox.Icon.Warning)
        except Exception as error:
            print("error alta clientes", error)

    def obtenerDatosCampos(self):
        """
        Obtiene los datos ingresados en los campos del formulario de conductor.

        :return: Una lista con los datos del conductor.
        """
        driver = [var.ui.txtDni, var.ui.txtFechaAlta, var.ui.txtApel, var.ui.txtNombre, var.ui.txtDirDriver,
                  var.ui.txtMovilDriver, var.ui.txtSalario]
        newDriver = []
        for i in driver:
            newDriver.append(i.text().title())
        newDriver.insert(5, var.ui.cmbProv.currentText())
        newDriver.insert(6, var.ui.cmbMuni.currentText())
        licencias = []
        chklicencia = [var.ui.chkA, var.ui.chkB, var.ui.chkC, var.ui.chkD]
        for i in chklicencia:
            if i.isChecked():
                licencias.append(i.text())
        newDriver.append('-'.join(licencias))
        return newDriver

    def cargartabladri(registros):
        """
        Carga los registros de conductores en la tabla de la interfaz gráfica.

        :param registros: Una lista de listas con los registros de conductores.
        :return: None
        """
        try:
            index = 0
            for registro in registros:
                var.ui.tabDrivers.setRowCount(index + 1)
                var.ui.tabDrivers.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabDrivers.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabDrivers.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabDrivers.setItem(index, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabDrivers.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
                var.ui.tabDrivers.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[5])))



                var.ui.tabDrivers.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabDrivers.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
        except Exception as error:
            print('Error al cargar en tabla dri', error)


    def comprobarLicencias(licencias):
        """
        Marca las licencias en el formulario según las licencias del conductor.

        :param licencias: Una cadena con las licencias del conductor.
        :return: None
        """
        try:
            if "A" in licencias:
                var.ui.chkA.setChecked(True)
            if "B" in licencias:
                var.ui.chkB.setChecked(True)
            if "C" in licencias:
                var.ui.chkC.setChecked(True)
            if "D" in licencias:
                var.ui.chkD.setChecked(True)
        except Exception as error:
            print('Error al comprobar licencias ', error)

    def cargarCamposDriver(registro):
        """
        Carga los datos del conductor en los campos del formulario.

        :param registro: Una lista con los datos del conductor.
        :return: None
        """
        try:
            drivers.Drivers.limpiarPanel()
            datos = [var.ui.lblCodeBD, var.ui.txtDni, var.ui.txtFechaAlta, var.ui.txtApel, var.ui.txtNombre,
                     var.ui.txtDirDriver, var.ui.cmbProv, var.ui.cmbMuni, var.ui.txtMovilDriver, var.ui.txtSalario]
            for i, widget in enumerate(datos):
                if isinstance(widget, QtWidgets.QComboBox):
                    widget.setCurrentText(registro[i])
                else:
                    widget.setText(str(registro[i]))

            Drivers.comprobarLicencias(registro[10])
        except Exception as error:
            print('Error al cargar datos de 1 driver', error)

    def cargarDriver(self):
        """
        Carga los datos del conductor seleccionado en la interfaz gráfica.

        :return: None
        """
        try:
            codigo = var.ui.tabDrivers.item(var.ui.tabDrivers.currentRow(), 0).text()
            registro = conexion.Conexion.onedriver(codigo)
            var.driver = registro
            Drivers.cargarCamposDriver(registro)
            var.ui.txtFiltro.clear()
            if var.ui.rbtConductor.isChecked():
                var.ui.txtFiltro.setText(var.driver[1])
        except Exception as error:
            print('error al conseguir registro driver', error)

    def buscarDriver(self):
        """
        Busca un conductor en la base de datos y carga sus datos en la interfaz gráfica.

        :return: None
        """
        try:
            dni = var.ui.txtDni.text()
            if dni == '':
                eventos.Eventos.ventanaAviso('Por favor, introduce un dni',
                                             QtWidgets.QMessageBox.Icon.Warning)

            else:
                registro = conexion.Conexion.codDri(dni)

                if registro is not None:
                    var.driver = registro
                    if registro[11] != "":
                        var.ui.rbtBaja.setChecked(True)
                    else:
                        var.ui.rbtAlta.setChecked(True)
                    Drivers.cargarCamposDriver(registro)
                    eventos.Eventos.selEstado(self)
                    Drivers.buscarDriverTabla(registro[0])
                else:
                    eventos.Eventos.ventanaAviso('El conductor no existe',
                                                 QtWidgets.QMessageBox.Icon.Warning)


                    Drivers.limpiarPanel()
            # var.ui.frameForm.hide()
        except Exception as error:
            print('Error al buscar driver', error)

    def buscarDriverTabla(codigo):
        """
        Selecciona un conductor en la tabla de conductores.

        :param codigo: El código del conductor a seleccionar.
        :return: None
        """

        try:
            tabla = var.ui.tabDrivers
            for fila in range(tabla.rowCount()):
                celda = tabla.item(fila, 0)
                codigoCelda = celda.text()
                if codigoCelda == str(codigo):
                    tabla.selectRow(fila)
                    tabla.scrollToItem(celda)
        except Exception as error:
            print('No se ha podido seleccionar al driver en la tabla', error)





    def bajaDriver(self):
        """
        Realiza la baja de un conductor en la base de datos.

        :return: None
        """
        try:
            if len(var.ui.tabDrivers.selectedItems()) > 0:
                fecha = var.ui.tabDrivers.item(var.ui.tabDrivers.currentRow(), 5).text()
                if fecha is None or fecha == '':
                    resultado = eventos.Eventos.ventanaConfirmacion(
                        'El conductor está dado de alta, quiere darlo de baja?', QtWidgets.QMessageBox.Icon.Information)

                    if resultado == 0:
                        codigo = var.ui.lblCodeBD.text()
                        conexion.Conexion.bajaDriver(codigo)
                        var.ui.rbtBaja.setChecked(True)
                        eventos.Eventos.selEstado(self)
                        drivers.Drivers.cargarDriver(self)
                        Drivers.buscarDriverTabla(codigo)

                else:
                    eventos.Eventos.ventanaAviso('El conductor ya está de baja',
                                                 QtWidgets.QMessageBox.Icon.Information)
            else:
                eventos.Eventos.ventanaAviso('Por favor, selecciona un conductor',
                                             QtWidgets.QMessageBox.Icon.Information)

        except Exception as error:
            print('Error al dar de baja un driver', error)




    def modificarDriver(self):
        """
        Modifica los datos de un conductor en la base de datos.

        :return: None
        """
        try:
            if len(var.ui.tabDrivers.selectedItems()) > 0 or var.ui.lblCodeBD.text() != '': # Comprueba driver seleccionado o buscado
                driver = Drivers.obtenerDatosCampos(self)  # Obtiene registro con los datos despues de pulsar modificar
                codigo = var.ui.lblCodeBD.text()

                if var.driver[1:11] == driver:  # compara los campos guardados en var.driver antes de modificar y los campos despues de pulsar modificar
                    eventos.Eventos.ventanaAviso('No hay datos que modificar',
                                                 QtWidgets.QMessageBox.Icon.Information)
                else:
                    conexion.Conexion.modificarDriver(driver)
                    drivers.Drivers.cargarDriver(self=None)
                    eventos.Eventos.selEstado(self=None)  #actualizar la tabla con los nuevos datos modificados

                if var.driver[11] != '':  # si tiene fecha de baja



                    resultado = eventos.Eventos.ventanaConfirmacion('El conductor está dado de baja, quiere modificar la fecha de la baja?', QtWidgets.QMessageBox.Icon.Information)

                    if resultado == 0:
                        var.calendar.modificarBaja = True
                        var.calendar.show()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Por favor, selecciona un conductor')
                mbox.exec()

        except Exception as error:
            print('No se ha podido modificar', error)

    @staticmethod
    def modificarFechaBaja(fecha):
        """
        Modifica la fecha de baja de un conductor en la base de datos.

        :param fecha: La nueva fecha de baja.
        :return: True si la modificación se realiza correctamente, False si no.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update drivers set bajadri= :fechabaja where codigo = :cod')
            query.bindValue(':fechabaja', fecha)
            query.bindValue(':cod', var.driver[0])
            if query.exec():
                return True
        except Exception as error:
            print('error al modificar fecha baja', error)

    def modificarFechaBajaCli(fecha):
        """
        Modifica la fecha de baja de un cliente en la base de datos.

        :param fecha: La nueva fecha de baja.
        :return: True si la modificación se realiza correctamente, False si no.
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
