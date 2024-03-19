import os, var, shutil
from PIL import Image
from PyQt6 import QtSql, QtWidgets
from PyQt6.QtCore import QFile
from PyQt6.QtGui import QIcon, QImage, QPixmap
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime

import conexion
import eventos


class Informes:
    """
    Clase que define operaciones relacionadas con la generación de informes.
    """

    @staticmethod
    def crearTabla(header, style, col_widths, datos):
        """
        Crea una tabla para el informe.

        :param header: Encabezado de la tabla.
        :param style: Estilo de la tabla.
        :param col_widths: Ancho de las columnas.
        :param datos: Datos para llenar la tabla.
        :return: La tabla creada.
        """
        try:
            data = [header]

            for registro in datos:
                data.append(registro)

            table = Table(data, colWidths=col_widths)
            table.setStyle(style)
            return table

        except Exception as error:
         print('Error al crear tabla informe')

    @staticmethod
    def calculardimens(tabla):
        """
        Calcula las dimensiones de la tabla.

        :param tabla: La tabla de la que se calcularán las dimensiones.
        :return: Ancho y alto de la tabla.
        """
        table_width, table_height = tabla.wrapOn(var.report, 0, 0)
        return table_height, table_width

    @staticmethod
    def calcularposicion(height, table_height, table_width):
        """
        Calcula la posición para dibujar la tabla en el informe.

        :param height: Altura de la página.
        :param table_height: Altura de la tabla.
        :param table_width: Ancho de la tabla.
        :return: Coordenadas x, y para la posición de la tabla.
        """

        x = (475 - table_width) / 2 + 45
        y = (height - table_height) - 140

        return x, y

    @staticmethod
    def pintarTabla(tabla, x, y):
        """
        Dibuja la tabla en el informe.

        :param tabla: La tabla a dibujar.
        :param x: Coordenada x de la posición de la tabla.
        :param y: Coordenada y de la posición de la tabla.
        """
        try:
            tabla.drawOn(var.report, x, y)
        except Exception as e:
            print('error al pintar la tabla en informe', e)

    @staticmethod
    def reportclientes2():
        """
        Genera el informe de clientes.
        """
        try:
            clientes = conexion.Conexion.obtenerclientes()

            if len(clientes) > 0:
                var.ui.panelPrincipal.setCurrentIndex(1)
                fecha = datetime.today()
                fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')

                configTabla = {}
                nombre = fecha + '_listadoclientes.pdf'
                titulo = 'CLIENTES'
                header = ['CÓDIGO', 'DNI', 'RAZÓN SOCIAL', 'MUNICIPIO', 'TELÉFONO', 'FECHA BAJA']
                estilo_tabla = TableStyle([
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinea la primera fila al centro
                    ('ALIGN', (1, 1), (2, -1), 'LEFT'),
                    # Alinea la segunda y tercera columna a partir de la segunda fila a la izquierda
                    ('ALIGN', (3, 1), (3, -1), 'LEFT'),
                    ('ALIGN', (4, 1), (4, -1), 'CENTER'),
                    # Alinea la cuarta y quinta columna a partir de la segunda fila al centro
                    ('ALIGN', (5, 1), (5, -1), 'CENTER'),
                    # Alinea la última columna a partir de la segunda fila a la derecha

                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12)
                ])
                col_widths = [79, 79, 89, 89, 79, 79]
                max_registros_pag = 26

                configTabla['nombre'] = nombre
                configTabla['titulo'] = titulo
                configTabla['header'] = header
                configTabla['estilo'] = estilo_tabla
                configTabla['widths'] = col_widths
                configTabla['max'] = max_registros_pag

                Informes.crearInforme(clientes, configTabla)
                Informes.abrirInforme(nombre)
            else:
               eventos.Eventos.ventanaAviso('El registro de clientes está vacío', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            print('error al crear informe 2')

    def reportclientes(self):
        """
        Genera el informe de clientes.
        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            nombre = fecha + '_listadoclientes.pdf'
            var.report = canvas.Canvas('informes/' + nombre)
            titulo = 'LISTADO CLIENTES'

            Informes.topInforme(titulo)
            Informes.footInforme(titulo, 0)

            headers = ['CÓDIGO', 'DNI', 'RAZÓN SOCIAL', 'MUNICIPIO', 'TELÉFONO', 'FECHA BAJA']
            var.report.setFont('Helvetica-Bold', size=10)
            x_coords = [55, 120, 175, 290, 380, 455]

            for ind, header in enumerate(headers):
                var.report.drawString(x_coords[ind], 675, str(headers[ind]))

            var.report.line(50, 670, 525, 670)

            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, razon, municipio, telefono, baja from clientes order by razon')
            var.report.setFont('Helvetica', size=9)

            if query.exec():
                i = 75
                j = 655

                while query.next():

                    if j <= 80:
                        var.report.drawString(450, 60, 'Página siguiente...')
                        var.report.showPage()  # crea una nueva página
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, 0)
                        var.report.setFont('Helvetica-Bold', size=10)

                        for ind, header in enumerate(headers):
                            var.report.drawString(x_coords[ind], 675, str(headers[ind]))
                        var.report.line(50, 670, 525, 670)
                        j = 655

                    var.report.setFont('Helvetica', size=9)
                    var.report.drawCentredString(i, j, str(query.value(0)))

                    dni = query.value(1)
                    dnilist = list(dni)
                    dniModifStr = Informes.ocultarDni(dnilist)

                    var.report.drawString(i + 37, j, str(dniModifStr))

                    for value in range(2, query.record().count()):
                        var.report.drawString(x_coords[value]+5, j, str(query.value(value)))

                    j = j - 20

            var.report.save()
            self.abrirInforme(nombre)
        except Exception as error:
            print('Error report clientes :', error)

    @staticmethod
    def reportdrivers():
        """
        Genera el informe de conductores.
        """
        try:
            drivers = Informes.obtenerdrivers()

            if len(drivers) > 0:
                var.ui.panelPrincipal.setCurrentIndex(0)
                fecha = datetime.today()
                fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')

                configTabla = {}
                nombre = fecha + '_listadodrivers.pdf'
                titulo = 'CONDUCTORES'
                header = ['CÓDIGO', 'APELLIDOS', 'NOMBRE', 'TELÉFONO', 'CARNET', 'FECHA BAJA']
                estilo_tabla = TableStyle([
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinea la primera fila al centro
                    ('ALIGN', (1, 1), (2, -1), 'LEFT'),
                    # Alinea la segunda y tercera columna a partir de la segunda fila a la izquierda
                    ('ALIGN', (3, 1), (4, -1), 'CENTER'),
                    # Alinea la cuarta y quinta columna a partir de la segunda fila al centro
                    ('ALIGN', (5, 1), (5, -1), 'CENTER'),
                    # Alinea la última columna a partir de la segunda fila a la derecha

                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12)
                ])
                col_widths = [79, 79, 89, 89, 79, 79]
                max_registros_pag = 26

                configTabla['nombre'] = nombre
                configTabla['titulo'] = titulo
                configTabla['header'] = header
                configTabla['estilo'] = estilo_tabla
                configTabla['widths'] = col_widths
                configTabla['max'] = max_registros_pag

                Informes.crearInforme(drivers, configTabla)
                Informes.abrirInforme(nombre)

            else:
                eventos.Eventos.ventanaAviso('El registro de conductores está vacío', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            print('Error report drivers:', error)

    @staticmethod
    def abreviardato(dato):
        """
        Abrevia un dato si su longitud es mayor o igual a 18 caracteres.

        :param dato: El dato a abreviar.
        :return: El dato abreviado.
        """
        try:
            if len(dato) >= 18:
                dato_abreviado = list(dato)
                dato_abreviado[17] = '.'
                return ''.join(dato_abreviado[:18])
            else:
                return dato
        except Exception as error:
            print('Error al abreviar dato', error)

    @staticmethod
    def obtenerdrivers():
        """
        Obtiene la información de los conductores desde la base de datos.

        :return: Lista de conductores.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, apellidos, nombre, movildri, carnet, bajadri from drivers order by apellidos')
            drivers = []
            if query.exec():
                while query.next():
                    driver = [query.value(i) for i in range(query.record().count())]
                    drivers.append(driver)
            return drivers
        except Exception as error:
            print('Error al obtener Drivers', error)

    @staticmethod
    def crearInforme(datos, config):
        """
        Crea el informe.

        :param datos: Datos para llenar el informe.
        :param config: Configuración del informe.
        """
        try:
            var.report = canvas.Canvas('informes/' + config['nombre'])

            width_pag, height_pag = letter

            totalpags = Informes.calculartotalpag(datos, config['max'])

            Informes.topInforme(config['titulo'])
            Informes.footInforme(config['titulo'], totalpags)

            while len(datos) > config['max']:
                var.report.drawString(470, 60, 'Página siguiente...')
                tabla = Informes.crearTabla(config['header'], config['estilo'], config['widths'], datos[:config['max']])
                Informes.insertartabla(height_pag, tabla)
                var.report.showPage()
                Informes.topInforme(config['titulo'])
                Informes.footInforme(config['titulo'], totalpags)
                datos = datos[config['max']:]


            tabla = Informes.crearTabla(config['header'], config['estilo'], config['widths'], datos)
            Informes.insertartabla(height_pag, tabla)
            # if len(datos)


            var.report.save()

        except Exception as error:
            print('Error al crear Informe', error)

    @staticmethod
    def insertartabla(height, tabla):
        """
        Inserta una tabla en el informe.

        :param height: Altura de la página.
        :param tabla: Tabla a insertar.
        """
        table_height, table_width = Informes.calculardimens(tabla)
        x, y = Informes.calcularposicion(height, table_height, table_width)
        Informes.pintarTabla(tabla, x + 15, y)

    @staticmethod
    def calculartotalpag(datos, max_registros_pag):
        """
        Calcula el total de páginas del informe.

        :param datos: Datos del informe.
        :param max_registros_pag: Máximo de registros por página.
        :return: Total de páginas.
        """
        pags = 1
        while len(datos) > max_registros_pag:
            pags += 1
            datos = datos[max_registros_pag:]
        return pags

    @staticmethod
    def abrirInforme(nombre):
        """
        Abre el informe generado.

        :param nombre: Nombre del archivo del informe.
        """
        try:
            rootPath = '.\\informes'
            for file in os.listdir(rootPath):
                if file.endswith(nombre):
                    os.startfile('%s\\%s' % (rootPath, file))
        except Exception as error:
            print('Error al abrir informe', error)

    @staticmethod
    def ocultarDni(dnilist):
        """
        Oculta parte del DNI.

        :param dnilist: Lista con los caracteres del DNI.
        :return: DNI modificado.
        """
        for index, char in enumerate(dnilist):
            if index != 5 and index != 6:
                dnilist[index] = '*'
        dniModifStr = ''.join(dnilist)
        return dniModifStr

    @staticmethod
    def topInforme(titulo):
        """
        Agrega la cabecera al informe.

        :param titulo: Título del informe.
        """
        try:

            var.report.line(50, 830, 545, 830)
            var.report.setFont('Helvetica-Bold', size=14)
            var.report.drawString(55, 805, 'Transportes Teis')
            ancho_pagina, alto_pagina = var.report._pagesize
            ancho_texto, alto_texto = var.report.stringWidth(titulo, "Helvetica", 14), 14

            # Calcula las coordenadas para centrar el texto
            x = (ancho_pagina - ancho_texto) / 2


            # Dibuja el texto centrado
            var.report.drawString(x, 675, titulo)
            var.report.line(50, 670, 545, 670)

            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 785, 'CIF: A12345678')
            var.report.drawString(55, 770, 'Avda. Galicia - 101')
            var.report.drawString(55, 755, 'Vigo - 36216 - España')
            var.report.drawString(55, 740, 'Teléfono: 986 132 456')
            var.report.drawString(55, 725, 'e-mail: cartesteisr@mail.com')

            if var.ui.panelPrincipal.currentIndex() == 2:
                cliente = conexion.Conexion.codCli(var.ui.txtCifFac.text())
                var.report.setFont('Helvetica-Bold', size=11)
                var.report.drawString(290, 805, 'Número Factura: ' + var.ui.lblCodFac.text())
                var.report.drawString(415, 805, 'Fecha: ' + var.ui.txtFechaFac.text())
                var.report.setFont('Helvetica', size=9)
                var.report.drawString(290, 785, 'CLIENTE')
                var.report.drawString(290, 770, 'CIF: ' + cliente[1])
                var.report.drawString(290, 755, 'Razón Social: ' + cliente[2])
                var.report.drawString(290, 740, 'Dirección: ' + cliente[4])
                var.report.drawString(290, 725, 'Provincia: ' + cliente[5])
                var.report.drawString(360, 785, 'Teléfono: ' + cliente[3])

            # Dibuja la imagen en el informe
            ruta_recurso = ":/img/img/coche2.png"
            pixmap = QPixmap(ruta_recurso)
            ruta_temporal = "temp_image.png"

            # Guardar la imagen en un archivo temporal
            pixmap.save(ruta_temporal)
            # logo = Image.open(ruta_temporal)


            var.report.drawImage(ruta_temporal, 480, 755, width=40, height=40, mask='auto')
            os.remove(ruta_temporal)


        except Exception as error:
            print('Error en cabecera informe:', error)

    @staticmethod
    def footInforme(titulo, pages):
        """
        Agrega el pie al informe.

        :param titulo: Título del informe.
        :param pages: Total de páginas del informe.
        """
        try:
            var.report.line(50, 50, 545, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))

            ancho_pagina, alto_pagina = var.report._pagesize
            ancho_texto, alto_texto = var.report.stringWidth(titulo, "Helvetica", 7), 7

            # Calcula las coordenadas para centrar el texto
            x = (ancho_pagina - ancho_texto) / 2
            var.report.drawString(x, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()+'/'+str(pages)))

            if var.ui.panelPrincipal.currentIndex() == 2 and var.report.getPageNumber() == pages:
                Informes.footTotalFac()

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)

    @staticmethod
    def footTotalFac():
        """
        Agrega el pie para el total de la factura en el informe.
        """

        try:

            var.report.setFont('Helvetica-Bold', size=14)

            var.report.drawString(355, 130, 'Subtotal')
            var.report.drawString(455, 130, var.ui.txtSubTotalFac.text())

            var.report.drawString(355, 110, 'IVA 21.0%')
            var.report.drawString(455, 110, var.ui.txtIva.text())

            var.report.drawString(355, 90, 'TOTAL')
            var.report.drawString(455, 90, var.ui.txtTotalFac.text())

        except Exception as error:
            print('Error en pie total fac: ', error)

    @staticmethod
    def reportviajes():
        """
        Genera el informe de viajes.
        """
        try:
            var.ui.panelPrincipal.setCurrentIndex(2)
            numFactura = var.ui.lblCodFac.text()
            if numFactura == '':
                eventos.Eventos.ventanaAviso('Por favor, selecciona un factura', QtWidgets.QMessageBox.Icon.Warning)
            else:
                viajes = conexion.Conexion.obtenerViajes(numFactura)

                for viaje in viajes:
                    total = float(viaje[3]) * float(viaje[4])
                    viaje.append(str(round(total, 2))+' €')

                if len(viajes) > 0:
                    fecha = datetime.today()
                    fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')

                    configTabla = {}
                    nombre = fecha + '_factura_'+numFactura+'.pdf'
                    titulo = 'FACTURA'
                    header = ['VIAJE', 'ORIGEN', 'DESTINO', 'KMS', 'TARIFA', 'TOTAL']
                    estilo_tabla = TableStyle([
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinea la primera fila al centro
                        ('ALIGN', (1, 1), (2, -1), 'LEFT'),
                        # Alinea la segunda y tercera columna a partir de la segunda fila a la izquierda
                        ('ALIGN', (3, 1), (4, -1), 'CENTER'),
                        # Alinea la cuarta y quinta columna a partir de la segunda fila al centro
                        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
                        # Alinea la última columna a partir de la segunda fila a la derecha

                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12)
                    ])
                    col_widths = [59, 110, 110, 89, 59, 79]
                    max_registros_pag = 26

                    configTabla['nombre'] = nombre
                    configTabla['titulo'] = titulo
                    configTabla['header'] = header
                    configTabla['estilo'] = estilo_tabla
                    configTabla['widths'] = col_widths
                    configTabla['max'] = max_registros_pag


                    Informes.crearInforme(viajes, configTabla)
                    Informes.abrirInforme(nombre)

                else:
                   eventos.Eventos.ventanaAviso('El registro de viajes está vacío', QtWidgets.QMessageBox.Icon.Warning)

        except Exception as error:
            print('error al crear informe viajes', {error})
