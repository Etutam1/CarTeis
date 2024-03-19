from PyQt6 import QtWidgets, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

import conexion
import drivers, clientes
import eventos
import facturas
import informes
import var
from PyQt6.QtGui import QIcon
import socket

class Conexion():
    """
       Clase para gestionar la conexión y operaciones con la base de datos.
       """
    @staticmethod
    def comprobarConexion():
        """
               Comprueba la conexión a internet intentando conectarse a un servidor externo.

               :return: True si la conexión es exitosa, False si hay un error.
               :rtype: bool
               """
        try:
            # Intenta conectar con un servidor de Google (puedes cambiarlo a otro servidor si lo prefieres)
            socket.create_connection(("www.google.com", 80))
            return True
        except Exception as e:
            print("Error al comprobar conexion", e)
            return False

    def conexion(self=None):
        """
               Establece la conexión con la base de datos.

               :param self: Referencia a la instancia de la clase.
               :return: True si la conexión se establece correctamente, False si hay un error.
               :rtype: bool
               """
        var.bbdd ='bbdd.sqlite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(var.bbdd)
        if not db.open():
            print('error de conexion')
            return False
        else:
            query = QtSql.QSqlQuery()
            query.exec("PRAGMA foreign_keys = ON;")
            print('base de datos conectada')
            return True

    def cargaprov(self=None):
        """
               Carga las provincias en los campos de selección correspondientes.

               :param self: Referencia a la instancia de la clase.
               """
        try:
            var.ui.cmbProvO.setPlaceholderText("Provincia")
            var.ui.cmbProvD.setPlaceholderText("Provincia")
            var.ui.cmbMuniO.setPlaceholderText("Municipio")
            var.ui.cmbMuniD.setPlaceholderText("Municipio")

            var.ui.cmbProv.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select provincia from provincias')
            if query.exec():
                var.ui.cmbProv.addItem('')
                var.ui.cmbProv_2.addItem('')
                var.ui.cmbProvO.addItem('')
                var.ui.cmbProvD.addItem('')
                while query.next():
                    var.ui.cmbProv.addItem(query.value(0))
                    var.ui.cmbProv_2.addItem(query.value(0))
                    var.ui.cmbProvO.addItem(query.value(0))
                    var.ui.cmbProvD.addItem(query.value(0))

        except Exception as error:
            print('Error al cargar las provincias', error)

    @staticmethod
    def selMuni(cmbProv, cmbLoc):
        """
               Selecciona los municipios correspondientes a una provincia dada.

               :param cmbProv: ComboBox que contiene las provincias.
               :param cmbLoc: ComboBox que contendrá los municipios.
               """
        try:
            cmbLoc.clear()
            id = 0
            prov = cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select idprov from provincias where provincia = :prov')
            query.bindValue(':prov', prov)

            if query.exec():
                while query.next():
                    id = query.value(0)

            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where idprov = :id')
            query1.bindValue(':id', int(id))

            if query1.exec():
                cmbLoc.addItem('')
                while query1.next():
                    cmbLoc.addItem(query1.value(0))

        except Exception as error:
            print("Error al cargar los municipios", error)


    def guardardri(newdriver):
        """
        Guarda los datos de un nuevo conductor en la base de datos.

        :param newdriver: Lista que contiene los datos del nuevo conductor.
        :return: True si se guarda correctamente, False si hay un error.
        :rtype: bool
        """
        try:
            if (newdriver[0].strip() == "" or newdriver[1].strip() == "" or newdriver[2].strip() == "" or newdriver[3].strip() == "" or newdriver[7].strip() == ""):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText('Debe completar los siguientes campos: Dni, Nombre, Apellidos, Fecha Alta y Móvil')
                mbox.exec()
                return False
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    'insert into drivers (dnidri,altadri,apellidos,nombre,direcciondri,provdri, munidri, movildri, salario, carnet) VALUES (:dni, :alta, :apel, :direccion, :nombre, :provincia, :municipio, :movil, :salario, :carnet)')
                query.bindValue(':dni', str(newdriver[0]))
                query.bindValue(':alta', str(newdriver[1]))
                query.bindValue(':apel', str(newdriver[2]))
                query.bindValue(':nombre', str(newdriver[4]))
                query.bindValue(':direccion', str(newdriver[3]))
                query.bindValue(':provincia', str(newdriver[5]))
                query.bindValue(':municipio', str(newdriver[6]))
                query.bindValue(':movil', str(newdriver[7]))
                query.bindValue(':salario', str(newdriver[8]))
                query.bindValue(':carnet', str(newdriver[9]))

                if query.exec():
                   return True
                else:
                    if var.ui.btnAltaDriver.hasFocus():
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('img/coche2.png'))
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setText('Asegurese de que el conductor no existe')
                        mbox.exec()
                    return False

        except Exception as error:
            print('Error en alta conductor', error)

    @staticmethod
    def guardarCli(newCli):
        """
        Guarda los datos de un nuevo cliente en la base de datos.

        :param newCli: Lista que contiene los datos del nuevo cliente.
        :return: True si se guarda correctamente, False si hay un error.
        :rtype: bool
        """
        try:
            if (newCli[0].strip() == "" or newCli[1].strip() == "" or newCli[2].strip() == ""):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText('Debe completar los siguientes campos: Dni, Razón, Telefono')
                mbox.exec()
                return False
            else:
                query = QtSql.QSqlQuery()
                query.prepare('insert into clientes (dni,razon,direccion,telefono,provincia, municipio) VALUES (:dni, :raz, :dir, :tel, :prov, :mun)')
                query.bindValue(':dni', str(newCli[0]))
                query.bindValue(':raz', str(newCli[1]))
                query.bindValue(':dir', str(newCli[3]))
                query.bindValue(':tel', str(newCli[2]))
                query.bindValue(':prov', str(newCli[4]))
                query.bindValue(':mun', str(newCli[5]))

                if query.exec():
                    return True
                else:
                    if var.ui.btnAltaDriver_2.hasFocus():
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle('Aviso')
                        mbox.setWindowIcon(QIcon('img/coche2.png'))
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setText('Asegurese de que el cliente no existe')
                        mbox.exec()
                    return False

            # select de los datos de conductores de la base de datos
            # drivers
        except Exception as error:
            print('Error en alta conductor', error)

    def mostrardrivers(self):
        """
        Muestra los datos de los conductores en la interfaz gráfica.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            registros = []
            query1 = QtSql.QSqlQuery()
            query1.prepare("select codigo, apellidos, nombre, movildri, carnet, bajadri from drivers")
            if query1.exec():
                while query1.next():
                    row = [query1.value(i) for i in range(query1.record().count())]
                    registros.append(row)
            if registros:
                drivers.Drivers.cargartabladri(registros)
            else:
                var.ui.tabDrivers.setRowCount(0)
        except Exception as error:
            print("Error al mostrar drivers", error)

    @staticmethod
    def mostrarclientes():
        """
        Muestra los datos de los clientes en la interfaz gráfica.
        """
        try:
            registros = []
            query1 = QtSql.QSqlQuery()
            query1.prepare("select codigo, razon, telefono, provincia, baja from clientes")
            if query1.exec():
                while query1.next():
                    row = [query1.value(i) for i in range(query1.record().count())]
                    registros.append(row)
            if registros:
                clientes.Clientes.cargartablacli(registros)
            else:
                var.ui.tabDrivers.setRowCount(0)
        except Exception as error:
            print("Error al mostrar clientes", error)

    @staticmethod
    def selectDriversTodos():
        """
        Selecciona todos los conductores de la base de datos.

        :return: Lista de registros de conductores.
        """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from drivers order by apellidos')
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range (query.record().count())]
                    registros.append(row)
            return registros
        except Exception as error:
            print('Error al devolver todos los drivers', error)

    @staticmethod
    def selectClientesTodos():
        """
        Selecciona todos los clientes de la base de datos.

        :return: Lista de registros de clientes.
        """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from clientes order by razon')
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            return registros
        except Exception as error:
            print('Error al devolver todos los clientes', error)

    def mostrardriversBaja(self):
        """
        Muestra los conductores dados de baja en la interfaz gráfica.

        :param self: Referencia a la instancia de la clase.
        """
        try:

            registros = []
            query = QtSql.QSqlQuery()
            query.prepare('SELECT CODIGO, APELLIDOS, NOMBRE, MOVILDRI, CARNET, BAJADRI FROM DRIVERS WHERE BAJADRI != ""')
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            if registros:
                drivers.Drivers.cargartabladri(registros)
            else:
                var.ui.tabDrivers.setRowCount(0)
        except Exception as error:
            print('Error al cargar drivers baja en la tabla', error)

    @staticmethod
    def mostrarclisBaja():
        """
        Muestra los clientes dados de baja en la interfaz gráfica.
        """
        try:

            registros = []
            query = QtSql.QSqlQuery()
            query.prepare(
                'select codigo, razon, telefono, provincia, baja from clientes WHERE BAJA != ""')
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            if registros:
                clientes.Clientes.cargartablacli(registros)
            else:
                var.ui.tabDrivers_2.setRowCount(0)
        except Exception as error:
            print('Error al cargar clientes baja en la tabla', error)

    def mostrardriversAlta(self):
        """
        Muestra los conductores dados de alta en la interfaz gráfica.

        :param self: Referencia a la instancia de la clase.
        """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare(
                'SELECT CODIGO, APELLIDOS, NOMBRE, MOVILDRI, CARNET, BAJADRI FROM DRIVERS WHERE BAJADRI IS NULL')
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            if registros:
                drivers.Drivers.cargartabladri(registros)

            else:
                # var.ui.tabDrivers.setRowCount(0)
             pass
        except Exception as error:
            print('Error al cargar drivers baja en la tabla', error)

    @staticmethod
    def mostrarclisAlta():
        """
        Muestra los clientes dados de alta en la interfaz gráfica.
        """
        try:
            registros = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "select codigo, razon, telefono, provincia, baja from clientes where baja is null")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
            if registros:
                clientes.Clientes.cargartablacli(registros)
            else:
                # var.ui.tabDrivers.setRowCount(0)
                pass
        except Exception as error:
            print('Error al cargar drivers baja en la tabla', error)

    def onedriver(codigo):
        """
        Obtiene los datos de un conductor dado su código.

        :param codigo: Código del conductor.
        :return: Lista con los datos del conductor.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from drivers where codigo= :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec():
                while query.next():
                    for i in range(12):
                        registro.append(str(query.value(i)))
            return registro

        except Exception as error:
            print('Error en fichero conexion datos de 1 driver: ', error)

    def onecli(codigo):
        """
        Obtiene los datos de un cliente dado su código.

        :param codigo: Código del cliente.
        :return: Lista con los datos del cliente.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from clientes where codigo= :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec():
                while query.next():
                    record = query.record()
                    for i in range(record.count()):
                        registro.append(str(query.value(i)))
            return registro

        except Exception as error:
            print('Error en fichero conexion datos de 1 cliente: ', error)

    def codDri(dni):
        """
        Obtiene el código de un conductor dado su DNI.

        :param dni: DNI del conductor.
        :return: Código del conductor.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, bajadri from drivers where dnidri= :dni')
            query.bindValue(':dni', str(dni))
            if query.exec():
                while query.next():
                    codigo = query.value(0)
                    registro = Conexion.onedriver(codigo)
                    return registro
        except Exception as error:
            print('Error al buscar driver', error)

    def codCli(dni):
        """
        Obtiene el código de un cliente dado su DNI.

        :param dni: DNI del cliente.
        :return: Código del cliente.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from clientes where dni=:dni')
            query.bindValue(':dni', str(dni))
            if query.exec():
                while query.next():
                    codigo = query.value(0)
                    registro = Conexion.onecli(codigo)
                    return registro
        except Exception as error:
            print('Error al buscar cliente', error)

    def bajaDriver(codigo):
        """
        Da de baja a un conductor.

        :param codigo: Código del conductor a dar de baja.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update drivers set bajadri = :fechabaja where codigo = :codigo')
            query.bindValue(':fechabaja', str(var.fechaActual))
            query.bindValue(':codigo', str(codigo))
            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('El conductor ha sido dado de baja')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('No se ha podido dar de baja a conductor')
                mbox.exec()
        except Exception as error:
            print('Error en baja driver', error)


    def bajaCli(codigo):
        """
        Da de baja a un cliente.

        :param codigo: Código del cliente a dar de baja.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set baja = :fechabaja where codigo = :codigo')
            query.bindValue(':fechabaja', str(var.fechaActual))
            query.bindValue(':codigo', str(codigo))
            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('El cliente ha sido dado de baja')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('No se ha podido dar de baja a cliente')
                mbox.exec()
        except Exception as error:
            print('Error en baja cliente', error)

    def modificarDriver(newdriver):
        """
        Modifica los datos de un conductor en la base de datos.

        :param newdriver: Lista con los nuevos datos del conductor.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update drivers set dnidri= :dni,altadri= :alta, apellidos=:apel, nombre=:nombre, direcciondri=:direccion,provdri=:provincia,'
                          'munidri=:municipio,movildri=:movil,salario=:salario,carnet=:carnet where dnidri = :dni')
            query.bindValue(':dni', str(newdriver[0]))
            query.bindValue(':alta', str(newdriver[1]))
            query.bindValue(':apel', str(newdriver[2]))
            query.bindValue(':nombre', str(newdriver[3]))
            query.bindValue(':direccion', str(newdriver[4]))
            query.bindValue(':provincia', str(newdriver[5]))
            query.bindValue(':municipio', str(newdriver[6]))
            query.bindValue(':movil', str(newdriver[7]))
            query.bindValue(':salario', str(newdriver[8]))
            query.bindValue(':carnet', str(newdriver[9]))

            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Los datos han sido modificados')
                mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('No se han podido modificar datos')
                mbox.exec()
        except Exception as error:
            print('Problema al modificar en la bd', error)

    def modificarCli(newCli):
        """
        Modifica los datos de un cliente en la base de datos.

        :param newCli: Lista con los nuevos datos del cliente.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set dni= :dni,razon= :raz, direccion=:dir, telefono=:tel, provincia=:prov, municipio=:mun where dni= :dni')
            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':raz', str(newCli[1]))
            query.bindValue(':dir', str(newCli[3]))
            query.bindValue(':tel', str(newCli[2]))
            query.bindValue(':prov', str(newCli[4]))
            query.bindValue(':mun', str(newCli[5]))

            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('Los datos han sido modificados')
                mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QIcon('img/coche2.png'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText('No se han podido modificar datos')
                mbox.exec()
        except Exception as error:
            print('Problema al modificar cli en la bd', error)

    @staticmethod
    def cargarDrivers():
        """
        Carga los conductores en un campo de selección.
        """
        try:
            var.ui.cmbDriverFac.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, apellidos from drivers where bajadri is null')

            if query.exec():
                var.ui.cmbDriverFac.addItem('')
                while query.next():
                    var.ui.cmbDriverFac.addItem(str(query.value(0))+'.'+str(query.value(2)))
        except Exception as error:
            print('Error al cargar drivers cmb', error)

    @staticmethod
    def obtenerclientes():
        """
        Obtiene los clientes de la base de datos.

        :return: Lista de clientes.
        """
        try:

            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, razon, municipio, telefono, baja from clientes order by razon')
            clientes = []

            if query.exec():

                while query.next():
                    cliente = [query.value(i) for i in range(query.record().count())]

                    cliente[1] = '*****' + list(cliente[1])[5] + list(cliente[1])[6] + '**'
                    cliente[2] = informes.Informes.abreviardato(cliente[2])

                    clientes.append(cliente)

            return clientes
        except Exception as error:
            print('Error al obtener Drivers', error)

    @staticmethod
    def cargarFacturas():
        """
        Carga las facturas desde la base de datos y las muestra en la interfaz gráfica.

        :return: None
        """
        try:
            query = QtSql.QSqlQuery()
            registros = []

            if not var.ui.chkFiltrar.isChecked():
                query.prepare('select numfac, dnicli from facturas')
            else:
                if var.ui.rbtCliente.isChecked():
                    query.prepare('select numfac, dnicli from facturas where dnicli = :cli')
                    query.bindValue(':cli', var.ui.txtFiltro.text())
                else:
                    query.prepare('select numfac, dnicli from facturas where driver = (select codigo from drivers where dnidri = :dri)')
                    query.bindValue(':dri', var.ui.txtFiltro.text())

            if query.exec():

                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    registros.append(row)
                if registros:
                    facturas.Facturas.cargarTablaFac(registros)
                else:
                    var.ui.tabDrivers.setRowCount(0)
            eventos.Eventos.cambiarEstiloTabla(var.ui.tabFac)

        except Exception as e:
            print('Error al cargar facturas', e)

    @staticmethod
    def cargarViajes(numFac):
        """
        Carga los viajes asociados a una factura específica y los muestra en la interfaz gráfica.

        :param numFac: El número de la factura para la cual se cargan los viajes.
        :return: None
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select viaje, origen, destino, km, tarifa from viajes where factura = :factura')
            query.bindValue(':factura', numFac)
            registros = []

            if query.exec():
                while query.next():

                    row = [query.value(i) for i in range(query.record().count())]
                    row[1] = row[1]+'-'+Conexion.getProv(row[1])
                    row[2] = row[2] + '-' + Conexion.getProv(row[2])
                    total = float(row[3])*float(row[4])
                    row.append(round(total, 2))
                    registros.append(row)

                if registros:
                    facturas.Facturas.cargarTablaViajes(registros)
                else:
                    var.ui.tabViajes.setRowCount(0)
            eventos.Eventos.cambiarEstiloTabla(var.ui.tabViajes)
        except Exception as error:
            print('Error al cargar viajes', error)

    @staticmethod
    def onefac(codigo):
        """
        Obtiene los detalles de una factura específica de la base de datos.

        :param codigo: El código de la factura a consultar.
        :return: Una lista con los detalles de la factura.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from facturas where numfac = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec():
                while query.next():
                    record = query.record()
                    for i in range(record.count()):
                        registro.append(str(query.value(i)))
            return registro
        except Exception as error:
            print('Error en consultar fac en bd', error)

    @staticmethod
    def guardarFac():
        """
        Guarda una nueva factura en la base de datos.

        :return: El código de la factura guardada.
        """
        try:
            campos = [var.ui.lblCodFac, var.ui.txtCifFac, var.ui.cmbDriverFac, var.ui.txtFechaFac]
            codFac = ''

            if facturas.Facturas.checkCampos(campos):
                query = QtSql.QSqlQuery()
                query.prepare(
                    'insert into facturas(numfac, dnicli, fecha, driver) values (null, :cif, :fecha, :driver)')
                query.bindValue(':cif', campos[1].text().upper())
                query.bindValue(':driver', campos[2].currentText().split('.')[0])
                query.bindValue(':fecha', campos[3].text())

                if query.exec():
                    query.exec("select last_insert_rowid()")
                    while query.next():
                        codFac = query.value(0)

            return codFac
        except Exception as error:
            print('Error al guardar factura', error)

    @staticmethod
    def guardarViaje():
        """
        Guarda un nuevo viaje en la base de datos.

        :return: El número del viaje guardado.
        """
        try:
            if var.ui.tabViajes.rowCount() == 0:
                viaje = var.ui.tabViajes.rowCount()+1
            else:
                viaje = int(var.ui.tabViajes.item(var.ui.tabViajes.rowCount()-1, 0).text()) +1
            print(viaje)
            query = QtSql.QSqlQuery()
            query.prepare('insert into viajes(viaje, factura, origen, destino, tarifa, km) values (:viaje, :fac, :o, :d, :tar, :km)')
            query.bindValue(':viaje', viaje)
            query.bindValue(':fac', var.ui.lblCodFac.text())
            query.bindValue(':o', var.ui.cmbMuniO.currentText())
            query.bindValue(':d', var.ui.cmbMuniD.currentText())
            tarifa = facturas.Facturas.checkTarifa()
            query.bindValue(':tar', tarifa)
            query.bindValue(':km', var.ui.txtKms.text())
            if query.exec():
                return viaje
        except Exception as error:
            print('Error al guardar viaje', error)

    @staticmethod
    def guardarViajeSinFactura(viaje):
        """
        Guarda un nuevo viaje en la base de datos sin asociarlo a una factura.

        :param viaje: Una lista que contiene los detalles del viaje a guardar.
        :return: El número del viaje guardado.
        """
        try:
            print(viaje)
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into viajes(viaje, factura, origen, destino, tarifa, km) values (:viaje, :fac, :o, :d, :tar, :km)')
            query.bindValue(':viaje', viaje[0])
            query.bindValue(':fac', var.ui.lblCodFac.text())
            query.bindValue(':o', viaje[1])
            query.bindValue(':d', viaje[2])
            query.bindValue(':tar', viaje[4])
            query.bindValue(':km', viaje[3])
            if query.exec():
                return viaje[0]
        except Exception as error:
            print('Error al guardar viaje', error)

    @staticmethod
    def guardarViajes():
        """
        Guarda múltiples viajes en la base de datos.

        :return: None
        """
        try:
            for fila in range(var.ui.tabViajes.rowCount()):
                viaje = []
                for columna in range(var.ui.tabViajes.columnCount()-2):
                    item = var.ui.tabViajes.item(fila, columna)
                    if columna == 1 or columna == 2:
                        viaje.append(item.text().split('-')[0])
                    else:
                        viaje.append(item.text())
                conexion.Conexion.guardarViajeSinFactura(viaje)
        except Exception as e:
            print('error al guardarViajes', e)

    @staticmethod
    def oneviaje(numViaje, fac):
        """
        Obtiene los detalles de un viaje específico de la base de datos.

        :param numViaje: El número del viaje a consultar.
        :param fac: El número de la factura asociada al viaje.
        :return: Una lista con los detalles del viaje.
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select * from viajes where viaje = :numViaje and factura = :fac' )
            query.bindValue(':numViaje', int(numViaje))
            query.bindValue(':fac', fac)
            if query.exec():
                while query.next():
                    record = query.record()
                    for i in range(record.count()):
                        registro.append(str(query.value(i)))
                        if i == 2 or i == 3:
                            registro.append(str(Conexion.getProv(registro[-1])))
            return registro
        except Exception as error:
            print('Error en consultar viaje en bd', error)

    @staticmethod
    def getProv(muni):
        """
        Obtiene el nombre de la provincia correspondiente a un municipio dado.

        :param muni: El nombre del municipio.
        :return: El nombre de la provincia.
        """
        try:
            query1 = QtSql.QSqlQuery()
            query1.prepare('select provincia from provincias where idprov=(select idprov from municipios where municipio = :muni)')
            query1.bindValue(':muni', muni)

            if query1.exec():
                while query1.next():
                    return query1.value(0)
        except Exception as error:
            print('Error al consultar prov', error)

    @staticmethod
    def eliminarViaje(idViaje):
        """
        Elimina un viaje de la base de datos.

        :param idViaje: El ID del viaje a eliminar.
        :return: True si se elimina correctamente, False en caso contrario.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from viajes where viaje = :viaje')
            query.bindValue(':viaje', idViaje)
            if query.exec():
                return True
            return False
        except Exception as error:
            print('Error al eliminar viaje bd', error)

    @staticmethod
    def obtenerViajes(numFac):
        """
        Obtiene todos los viajes asociados a una factura específica de la base de datos.

        :param numFac: El número de la factura.
        :return: Una lista de listas con los detalles de cada viaje.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select viaje, origen, destino, km, tarifa from viajes where factura = :factura')
            query.bindValue(':factura', numFac)
            registros = []

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    row[1] = row[1] + '-' + Conexion.getProv(row[1])
                    row[2] = row[2] + '-' + Conexion.getProv(row[2])
                    registros.append(row)
            return registros

        except Exception as error:
            print('Error al obtener viajes', error)

    @staticmethod
    def modificarViaje(viaje):
        """
        Modifica los detalles de un viaje en la base de datos.

        :param viaje: Una lista que contiene los nuevos detalles del viaje.
        :return: True si se modifica correctamente, False en caso contrario.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update viajes set origen= :og, destino= :dt, tarifa=:tar, km=:km where viaje = :viaj and factura= :fac')
            query.bindValue(':og', str(viaje[0]))
            query.bindValue(':dt', str(viaje[2]))
            query.bindValue(':tar', str(viaje[5]))
            query.bindValue(':km', str(viaje[4]))
            query.bindValue(':viaj', var.ui.tabViajes.item(var.ui.tabViajes.currentRow(), 0).text())
            query.bindValue(':fac', var.ui.lblCodFac.text())

            if query.exec():
                eventos.Eventos.ventanaAviso('Los datos han sido modificados', QtWidgets.QMessageBox.Icon.Information)
                return True

            else:
                eventos.Eventos.ventanaAviso('No se han podido modificar los datos', QtWidgets.QMessageBox.Icon.Information)
                return False

        except Exception as e:
            print("Error al modificar viaje en BBDD", e)

    @staticmethod
    def eliminarFac(numFac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where numfac = :num')
            query.bindValue(':num', numFac)
            if query.exec():
                return True
            return False
        except Exception as e:
            print('error al eliminar factura en bdd', e)
