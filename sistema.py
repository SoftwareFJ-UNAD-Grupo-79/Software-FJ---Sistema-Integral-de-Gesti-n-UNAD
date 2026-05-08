# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

# Importa logging para registrar eventos y errores.
import logging

# Importa clases principales desde modelos.py
from modelos import Cliente, Reserva


# ==========================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================================

logging.basicConfig(
    filename="software_fj_companero.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# CLASE CONTROLADORA DEL SISTEMA
# ==========================================================

class SistemaGestion:
    """Clase encargada de administrar clientes, servicios y reservas."""

    def _init_(self):
        """Inicializa listas internas."""
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, correo, telefono):
        """Registra un cliente en el sistema."""

        cliente = Cliente(nombre, correo, telefono)

        self.clientes.append(cliente)

        logging.info(f"Cliente registrado: {cliente.obtener_detalle()}")

        return cliente

    def agregar_servicio(self, servicio):
        """Agrega un servicio a la lista interna."""

        self.servicios.append(servicio)

        logging.info(f"Servicio agregado: {servicio.nombre}")

        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        """Crea una reserva y la almacena."""

        reserva = Reserva(cliente, servicio, duracion)

        self.reservas.append(reserva)

        logging.info("Reserva creada correctamente")

        return reserva

    def resumen_general(self):
        """Retorna resumen del sistema."""

        return (
            f"Clientes: {len(self.clientes)} | "
            f"Servicios: {len(self.servicios)} | "
            f"Reservas: {len(self.reservas)}"
        )
        