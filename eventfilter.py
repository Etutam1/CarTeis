from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QComboBox

import conexion
import var


class EventFilter(QObject):
    """
    Clase para filtrar eventos de la interfaz gráfica.
    """
    def eventFilter(self, obj, event):
        """
        Filtra los eventos de la interfaz gráfica.

        :param obj: El objeto que emitió el evento.
        :param event: El evento que se está filtrando.
        :return: True si el evento ha sido filtrado, False si no.
        """
        if obj is var.ui.cmbDriverFac and event.type() == QEvent.Type.MouseButtonPress:
            conexion.Conexion.cargarDrivers()
        return super().eventFilter(obj, event)
