# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS NECESARIAS
# ==========================================================

# Importa ABC y abstractmethod para construir clases abstractas.
from abc import ABC, abstractmethod

# Importa datetime para registrar fecha y hora de las operaciones.
from datetime import datetime

# ==========================================================
# EXCEPCIONES PERSONALIZADAS DEL SISTEMA
# ==========================================================

class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores controlados de la aplicación."""


class ErrorDatoInvalido(ErrorSoftwareFJ):
    """Excepción usada cuando un dato ingresado no cumple las reglas."""


class ErrorCampoObligatorio(ErrorSoftwareFJ):
    """Excepción usada cuando falta un dato obligatorio."""


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Excepción usada cuando un servicio no se encuentra disponible."""


# ==========================================================
# CLASE ABSTRACTA BASE DEL SISTEMA
# ==========================================================

class ElementoSistema(ABC):
    """Clase abstracta base para los elementos del sistema."""

    contador = 1

    def __init__(self):
        """Asigna un código consecutivo automático."""
        self._codigo = ElementoSistema.contador
        ElementoSistema.contador += 1

    @property
    def codigo(self):
        """Retorna el código interno del objeto."""
        return self._codigo


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(ElementoSistema):
    """Representa un cliente dentro del sistema."""

    def __init__(self, nombre, correo, telefono):
        """Inicializa los datos básicos del cliente."""
        super().__init__()
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def obtener_detalle(self):
        """Retorna un resumen del cliente."""
        return f"{self.nombre} | {self.correo} | {self.telefono}"


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ElementoSistema, ABC):
    """Clase abstracta para todos los servicios."""

    def __init__(self, nombre, valor_base):
        """Inicializa nombre y valor base."""
        super().__init__()
        self.nombre = nombre
        self.valor_base = valor_base

    @abstractmethod
    def calcular_valor(self, horas):
        """Método abstracto para calcular el valor."""
        pass


# ==========================================================
# SERVICIO DE RESERVA DE SALA
# ==========================================================

class ReservaSala(Servicio):
    """Servicio especializado para reservas de salas."""

    def __init__(self, nombre, valor_base, capacidad, video):
        """Inicializa datos específicos de la sala."""
        super().__init__(nombre, valor_base)
        self.capacidad = capacidad
        self.video = video

    def calcular_valor(self, horas):
        """Calcula el valor total de la reserva."""
        return self.valor_base * horas


# ==========================================================
# SERVICIO DE ALQUILER DE EQUIPO
# ==========================================================

class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos."""

    def __init__(self, nombre, valor_base, tipo, unidades):
        """Inicializa datos del equipo."""
        super().__init__(nombre, valor_base)
        self.tipo = tipo
        self.unidades = unidades

    def calcular_valor(self, horas):
        """Calcula el valor del alquiler."""
        return (self.valor_base * horas) * 1.05


# ==========================================================
# SERVICIO DE ASESORÍA ESPECIALIZADA
# ==========================================================

class AsesoriaEspecializada(Servicio):
    """Servicio especializado de asesorías."""

    def __init__(self, nombre, valor_base, area, nivel):
        """Inicializa el área y nivel."""
        super().__init__(nombre, valor_base)
        self.area = area
        self.nivel = nivel

    def calcular_valor(self, horas):
        """Calcula el valor de la asesoría."""
        return (self.valor_base * horas) * 1.10


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva(ElementoSistema):
    """Clase encargada de administrar las reservas."""

    def __init__(self, cliente, servicio, duracion):
        """Inicializa una reserva."""
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.fecha = datetime.now()

    def procesar(self):
        """Procesa el valor total de la reserva."""
        self.estado = "Procesada"
        return self.servicio.calcular_valor(self.duracion)
