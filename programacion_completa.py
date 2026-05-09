"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación 213023 - UNAD
Fase 4 - Prácticas simuladas
Versión: Alternativa para aporte de compañero

Descripción general:
Este programa desarrolla una aplicación orientada a objetos para gestionar
clientes, servicios y reservas de la empresa Software FJ, sin utilizar bases
de datos. La información se maneja mediante objetos, listas internas y archivo
de logs para registrar eventos y errores.

La versión presenta una interfaz gráfica diferente, con colores verdes y una
organización visual distinta, manteniendo los requisitos principales del problema:
abstracción, herencia, polimorfismo, encapsulación, validaciones, excepciones
personalizadas, bloques try/except/else/finally, encadenamiento de excepciones
y registro de errores en archivo de logs.
"""

# Importa ABC y abstractmethod para construir clases abstractas.
from abc import ABC, abstractmethod
# Importa datetime para registrar fecha y hora de las operaciones.
from datetime import datetime
# Importa singledispatchmethod para simular sobrecarga de métodos.
from functools import singledispatchmethod
# Importa logging para registrar eventos y errores del sistema.
import logging
# Importa RotatingFileHandler para manejar archivos de logs con respaldo automático.
from logging.handlers import RotatingFileHandler
# Importa re para validar correos y nombres mediante expresiones regulares.
import re
# Importa tkinter para crear la interfaz gráfica.
import tkinter as tk
# Importa ttk y messagebox para widgets modernos y mensajes emergentes.
from tkinter import ttk, messagebox


# ==========================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================================

# Define el nombre del archivo donde se guardarán los eventos y errores.
ARCHIVO_LOG = "software_fj_companero.log"

# Crea un logger propio para esta versión del sistema.
logger = logging.getLogger("SoftwareFJCompanero")

# Define que el sistema guardará mensajes informativos, advertencias y errores.
logger.setLevel(logging.INFO)

# Evita que los logs se dupliquen si el programa se ejecuta varias veces.
logger.propagate = False

# Verifica que no existan manejadores previos para evitar registros repetidos.
if not logger.handlers:
    # Crea un manejador de logs con límite de tamaño y respaldo automático.
    manejador = RotatingFileHandler(ARCHIVO_LOG, maxBytes=250000, backupCount=2, encoding="utf-8")
    # Define el formato de cada registro dentro del archivo log.
    formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # Aplica el formato configurado al manejador.
    manejador.setFormatter(formato)
    # Agrega el manejador al logger principal.
    logger.addHandler(manejador)


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


class ErrorReserva(ErrorSoftwareFJ):
    """Excepción usada cuando una reserva no puede ser procesada."""


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Excepción usada cuando una acción no es permitida por el estado actual."""


class ErrorCalculo(ErrorSoftwareFJ):
    """Excepción usada cuando un cálculo produce un resultado incorrecto."""


# ==========================================================
# CLASE ABSTRACTA GENERAL
# ==========================================================

class ElementoSistema(ABC):
    """Clase abstracta que representa cualquier elemento general del sistema."""

    # Contador compartido para crear identificadores únicos.
    contador = 1

    def __init__(self):
        """Inicializa el identificador y la fecha de creación del elemento."""
        # Asigna un identificador único al objeto creado.
        self._codigo = ElementoSistema.contador
        # Incrementa el contador para el siguiente objeto.
        ElementoSistema.contador += 1
        # Guarda la fecha y hora de creación del objeto.
        self._fecha_registro = datetime.now()

    @property
    def codigo(self):
        """Devuelve el código único del elemento."""
        return self._codigo

    @property
    def fecha_registro(self):
        """Devuelve la fecha de registro del elemento."""
        return self._fecha_registro

    @abstractmethod
    def obtener_detalle(self):
        """Método obligatorio para entregar la información principal del objeto."""


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(ElementoSistema):
    """Clase que representa un cliente con datos protegidos y validados."""

    # Patrón usado para validar el formato del correo electrónico.
    PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")

    def __init__(self, nombre, correo, telefono):
        """Construye un cliente validando nombre, correo y teléfono."""
        # Llama el constructor de la clase abstracta para asignar código y fecha.
        super().__init__()
        # Inicializa el nombre privado del cliente.
        self.__nombre = ""
        # Inicializa el correo privado del cliente.
        self.__correo = ""
        # Inicializa el teléfono privado del cliente.
        self.__telefono = ""
        # Valida y asigna el nombre recibido mediante el setter.
        self.nombre = nombre
        # Valida y asigna el correo recibido mediante el setter.
        self.correo = correo
        # Valida y asigna el teléfono recibido mediante el setter.
        self.telefono = telefono

    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida y guarda el nombre del cliente."""
        if not valor:
            raise ErrorCampoObligatorio("El nombre del cliente es obligatorio.")
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ErrorDatoInvalido("El nombre debe tener mínimo 3 caracteres.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            raise ErrorDatoInvalido("El nombre solo puede contener letras y espacios.")
        self.__nombre = valor.title()

    @property
    def correo(self):
        """Devuelve el correo del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        """Valida y guarda el correo del cliente."""
        if not valor:
            raise ErrorCampoObligatorio("El correo del cliente es obligatorio.")
        valor = str(valor).strip().lower()
        if not Cliente.PATRON_EMAIL.match(valor):
            raise ErrorDatoInvalido("El correo ingresado no tiene un formato válido.")
        self.__correo = valor

    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        """Valida y guarda el teléfono del cliente."""
        if not valor:
            raise ErrorCampoObligatorio("El teléfono del cliente es obligatorio.")
        valor = str(valor).strip()
        if not valor.isdigit():
            raise ErrorDatoInvalido("El teléfono solo debe contener números.")
        if len(valor) < 7 or len(valor) > 10:
            raise ErrorDatoInvalido("El teléfono debe tener entre 7 y 10 dígitos.")
        self.__telefono = valor

    def obtener_detalle(self):
        """Entrega un resumen general del cliente."""
        return f"Cliente {self.codigo}: {self.nombre} | {self.correo} | {self.telefono}"

    def __str__(self):
        """Convierte el cliente en texto legible."""
        return self.obtener_detalle()


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ElementoSistema, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, nombre, valor_base, activo=True):
        """Inicializa los datos comunes de un servicio."""
        super().__init__()
        if not nombre:
            raise ErrorCampoObligatorio("El servicio debe tener un nombre.")
        if float(valor_base) <= 0:
            raise ErrorDatoInvalido("El valor base del servicio debe ser mayor que cero.")
        if not isinstance(activo, bool):
            raise ErrorDatoInvalido("La disponibilidad debe indicarse como True o False.")
        self.nombre = str(nombre).strip().title()
        self.valor_base = float(valor_base)
        self.activo = activo

    @abstractmethod
    def calcular_valor(self, horas):
        """Calcula el valor del servicio según la cantidad de horas."""

    @abstractmethod
    def descripcion(self):
        """Entrega una descripción particular del servicio."""

    @abstractmethod
    def validar(self):
        """Valida las características internas del servicio."""

    def obtener_detalle(self):
        """Entrega un resumen general del servicio."""
        estado = "Disponible" if self.activo else "No disponible"
        return f"Servicio {self.codigo}: {self.nombre} | Base: ${self.valor_base:,.0f} | {estado}"

    @singledispatchmethod
    def valor_con_ajuste(self, parametro):
        """Método base para simular sobrecarga en el cálculo del costo."""
        raise ErrorDatoInvalido("Tipo de parámetro no permitido para el cálculo.")

    @valor_con_ajuste.register
    def _(self, descuento: float):
        """Calcula el valor aplicando un porcentaje de descuento."""
        if descuento < 0 or descuento > 0.5:
            raise ErrorDatoInvalido("El descuento debe estar entre 0% y 50%.")
        return self.valor_base * (1 - descuento)

    @valor_con_ajuste.register
    def _(self, impuesto: int):
        """Calcula el valor aplicando un porcentaje entero de impuesto."""
        if impuesto < 0 or impuesto > 30:
            raise ErrorDatoInvalido("El impuesto debe estar entre 0% y 30%.")
        return self.valor_base * (1 + impuesto / 100)


# ==========================================================
# SERVICIO 1: RESERVA DE SALA
# ==========================================================

class ReservaSala(Servicio):
    """Servicio especializado para reservar salas de trabajo o reuniones."""

    def __init__(self, nombre, valor_base, capacidad, video_beam=True):
        """Inicializa una sala con capacidad y disponibilidad de video beam."""
        super().__init__(nombre, valor_base)
        self.capacidad = int(capacidad)
        self.video_beam = bool(video_beam)
        self.validar()

    def validar(self):
        """Valida que la sala tenga una capacidad permitida."""
        if self.capacidad < 2 or self.capacidad > 80:
            raise ErrorDatoInvalido("La capacidad de la sala debe estar entre 2 y 80 personas.")

    def calcular_valor(self, horas):
        """Calcula el valor de reservar la sala por cierta cantidad de horas."""
        if horas <= 0:
            raise ErrorDatoInvalido("La duración debe ser mayor que cero.")
        adicional = 25000 if self.video_beam else 0
        total = (self.valor_base + adicional) * horas
        if total <= 0:
            raise ErrorCalculo("El valor calculado para la sala no es válido.")
        return total

    def descripcion(self):
        """Describe las características de la sala."""
        equipo = "con video beam" if self.video_beam else "sin video beam"
        return f"Reserva de sala para {self.capacidad} personas, {equipo}."


# ==========================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# ==========================================================

class AlquilerEquipo(Servicio):
    """Servicio especializado para alquilar equipos tecnológicos."""

    def __init__(self, nombre, valor_base, tipo_equipo, unidades):
        """Inicializa el alquiler con tipo de equipo y unidades solicitadas."""
        super().__init__(nombre, valor_base)
        self.tipo_equipo = str(tipo_equipo).strip().title()
        self.unidades = int(unidades)
        self.validar()

    def validar(self):
        """Valida el tipo de equipo y la cantidad de unidades."""
        if not self.tipo_equipo:
            raise ErrorCampoObligatorio("Debe indicar el tipo de equipo a alquilar.")
        if self.unidades < 1 or self.unidades > 20:
            raise ErrorDatoInvalido("Las unidades de equipos deben estar entre 1 y 20.")

    def calcular_valor(self, horas):
        """Calcula el valor del alquiler según horas y unidades."""
        if horas <= 0:
            raise ErrorDatoInvalido("La duración debe ser mayor que cero.")
        total = self.valor_base * self.unidades * horas
        if total <= 0:
            raise ErrorCalculo("El cálculo del alquiler de equipos no es válido.")
        return total

    def descripcion(self):
        """Describe el alquiler de equipos solicitado."""
        return f"Alquiler de {self.unidades} unidad(es) de {self.tipo_equipo}."


# ==========================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ==========================================================

class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías profesionales."""

    def __init__(self, nombre, valor_base, area, nivel):
        """Inicializa la asesoría con área y nivel de especialización."""
        super().__init__(nombre, valor_base)
        self.area = str(area).strip().title()
        self.nivel = str(nivel).strip().lower()
        self.validar()

    def validar(self):
        """Valida el área y nivel de la asesoría."""
        niveles_validos = ["basico", "intermedio", "avanzado"]
        if not self.area:
            raise ErrorCampoObligatorio("Debe indicar el área de asesoría.")
        if self.nivel not in niveles_validos:
            raise ErrorDatoInvalido("El nivel debe ser basico, intermedio o avanzado.")

    def calcular_valor(self, horas):
        """Calcula el valor de la asesoría según el nivel seleccionado."""
        if horas <= 0:
            raise ErrorDatoInvalido("La duración debe ser mayor que cero.")
        multiplicador = {"basico": 1.0, "intermedio": 1.25, "avanzado": 1.55}[self.nivel]
        total = self.valor_base * multiplicador * horas
        if total <= 0:
            raise ErrorCalculo("El cálculo de la asesoría no es válido.")
        return total

    def descripcion(self):
        """Describe la asesoría especializada."""
        return f"Asesoría en {self.area}, nivel {self.nivel}."


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva(ElementoSistema):
    """Clase que integra cliente, servicio, duración, estado y costo."""

    def __init__(self, cliente, servicio, duracion):
        """Crea una reserva validando cliente, servicio y duración."""
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("La reserva debe tener un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("La reserva debe tener un servicio válido.")
        if not servicio.activo:
            raise ErrorServicioNoDisponible("El servicio seleccionado no está disponible.")
        if int(duracion) <= 0:
            raise ErrorReserva("La duración de la reserva debe ser mayor que cero.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = int(duracion)
        self.estado = "Pendiente"
        self.total = 0

    def confirmar(self):
        """Confirma la reserva si aún se encuentra pendiente."""
        if self.estado != "Pendiente":
            raise ErrorOperacionNoPermitida("Solo se pueden confirmar reservas pendientes.")
        self.total = self.servicio.calcular_valor(self.duracion)
        self.estado = "Confirmada"
        logger.info("Reserva confirmada: %s", self.obtener_detalle())

    def cancelar(self):
        """Cancela la reserva si no ha sido finalizada previamente."""
        if self.estado == "Finalizada":
            raise ErrorOperacionNoPermitida("No se puede cancelar una reserva finalizada.")
        self.estado = "Cancelada"
        logger.info("Reserva cancelada: %s", self.obtener_detalle())

    def procesar(self):
        """Procesa la reserva usando try/except/else/finally."""
        try:
            self.confirmar()
        except ErrorSoftwareFJ as error:
            logger.error("Error procesando reserva: %s", error)
            raise ErrorReserva("No fue posible procesar la reserva.") from error
        else:
            logger.info("Procesamiento exitoso de la reserva %s", self.codigo)
            self.estado = "Finalizada"
        finally:
            logger.info("Proceso de reserva terminado para el código %s", self.codigo)

    def obtener_detalle(self):
        """Entrega un resumen completo de la reserva."""
        return (
            f"Reserva {self.codigo}: {self.cliente.nombre} | "
            f"{self.servicio.nombre} | {self.duracion} hora(s) | "
            f"Estado: {self.estado} | Total: ${self.total:,.0f}"
        )


# ==========================================================
# CLASE CONTROLADORA DEL SISTEMA
# ==========================================================

class SistemaGestion:
    """Clase encargada de administrar clientes, servicios y reservas."""

    def __init__(self):
        """Inicializa las listas internas del sistema."""
        self.clientes = []
        self.servicios = []
        self.reservas = []
        logger.info("Sistema de gestión iniciado correctamente.")

    def registrar_cliente(self, nombre, correo, telefono):
        """Registra un cliente y lo almacena en la lista interna."""
        try:
            cliente = Cliente(nombre, correo, telefono)
        except ErrorSoftwareFJ as error:
            logger.error("Error registrando cliente: %s", error)
            raise
        else:
            self.clientes.append(cliente)
            logger.info("Cliente registrado: %s", cliente.obtener_detalle())
            return cliente
        finally:
            logger.info("Finalizó intento de registro de cliente.")

    def agregar_servicio(self, servicio):
        """Agrega un servicio validado a la lista interna."""
        if not isinstance(servicio, Servicio):
            raise ErrorDatoInvalido("El objeto agregado no corresponde a un servicio válido.")
        self.servicios.append(servicio)
        logger.info("Servicio agregado: %s", servicio.obtener_detalle())
        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        """Crea y procesa una reserva dentro del sistema."""
        try:
            reserva = Reserva(cliente, servicio, duracion)
            reserva.procesar()
        except ErrorSoftwareFJ as error:
            logger.error("No se pudo crear la reserva: %s", error)
            raise
        else:
            self.reservas.append(reserva)
            return reserva
        finally:
            logger.info("Finalizó intento de creación de reserva.")

    def resumen_general(self):
        """Devuelve un resumen de la cantidad de registros del sistema."""
        return f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | Reservas: {len(self.reservas)}"


# ==========================================================
# INTERFAZ GRÁFICA DIFERENTE PARA EL COMPAÑERO
# ==========================================================

class InterfazSoftwareFJ:
    """Interfaz gráfica alternativa con estilo verde y distribución diferente."""

    def __init__(self, raiz):
        """Construye la ventana principal de la aplicación."""
        self.raiz = raiz
        self.sistema = SistemaGestion()
        self.raiz.title("Software FJ | Gestión Integral - Versión Compañero")
        self.raiz.geometry("1180x720")
        self.raiz.minsize(1050, 650)
        self.color_fondo = "#eef7f1"
        self.color_panel = "#dcefe3"
        self.color_principal = "#146c43"
        self.color_secundario = "#0f5132"
        self.color_texto = "#1f2d24"
        self.raiz.configure(bg=self.color_fondo)
        self.configurar_estilos()
        self.crear_widgets()
        self.cargar_servicios_base()

    def configurar_estilos(self):
        """Configura el estilo visual de los widgets ttk."""
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", background=self.color_principal, foreground="white", font=("Segoe UI", 18, "bold"), padding=12)
        estilo.configure("Panel.TLabelframe", background=self.color_panel, foreground=self.color_secundario, font=("Segoe UI", 10, "bold"))
        estilo.configure("Panel.TLabelframe.Label", background=self.color_panel, foreground=self.color_secundario, font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabel", background=self.color_panel, foreground=self.color_texto, font=("Segoe UI", 10))
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        estilo.configure("Accent.TButton", background=self.color_principal, foreground="white")
        estilo.map("Accent.TButton", background=[("active", self.color_secundario)])

    def crear_widgets(self):
        """Crea y organiza los elementos visuales de la ventana."""
        titulo = ttk.Label(self.raiz, text="Sistema Integral de Clientes, Servicios y Reservas - Software FJ", style="Titulo.TLabel")
        titulo.pack(fill="x")

        contenedor = tk.Frame(self.raiz, bg=self.color_fondo)
        contenedor.pack(fill="both", expand=True, padx=12, pady=12)

        izquierda = tk.Frame(contenedor, bg=self.color_fondo)
        izquierda.pack(side="left", fill="both", expand=True, padx=(0, 8))

        derecha = tk.Frame(contenedor, bg=self.color_fondo)
        derecha.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self.crear_panel_cliente(izquierda)
        self.crear_panel_servicio(izquierda)
        self.crear_panel_reserva(izquierda)
        self.crear_panel_resultados(derecha)

    def crear_panel_cliente(self, padre):
        """Crea el panel para registrar clientes."""
        marco = ttk.LabelFrame(padre, text="1. Registro de cliente", style="Panel.TLabelframe")
        marco.pack(fill="x", pady=6)
        self.entry_nombre = self.crear_entrada(marco, "Nombre completo:", 0)
        self.entry_correo = self.crear_entrada(marco, "Correo electrónico:", 1)
        self.entry_telefono = self.crear_entrada(marco, "Teléfono:", 2)
        ttk.Button(marco, text="Registrar cliente", style="Accent.TButton", command=self.registrar_cliente_gui).grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

    def crear_panel_servicio(self, padre):
        """Crea el panel para agregar servicios."""
        marco = ttk.LabelFrame(padre, text="2. Creación de servicios", style="Panel.TLabelframe")
        marco.pack(fill="x", pady=6)
        ttk.Label(marco, text="Tipo de servicio:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        self.combo_tipo = ttk.Combobox(marco, values=["Reserva de sala", "Alquiler de equipo", "Asesoría especializada"], state="readonly")
        self.combo_tipo.grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        self.combo_tipo.current(0)
        self.entry_servicio = self.crear_entrada(marco, "Nombre del servicio:", 1)
        self.entry_valor = self.crear_entrada(marco, "Valor base:", 2)
        self.entry_extra1 = self.crear_entrada(marco, "Dato 1: capacidad / equipo / área:", 3)
        self.entry_extra2 = self.crear_entrada(marco, "Dato 2: video beam / unidades / nivel:", 4)
        marco.columnconfigure(1, weight=1)
        ttk.Button(marco, text="Agregar servicio", style="Accent.TButton", command=self.agregar_servicio_gui).grid(row=5, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

    def crear_panel_reserva(self, padre):
        """Crea el panel para generar reservas."""
        marco = ttk.LabelFrame(padre, text="3. Procesamiento de reserva", style="Panel.TLabelframe")
        marco.pack(fill="x", pady=6)
        ttk.Label(marco, text="Cliente:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        self.combo_cliente = ttk.Combobox(marco, state="readonly")
        self.combo_cliente.grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        ttk.Label(marco, text="Servicio:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.combo_servicio = ttk.Combobox(marco, state="readonly")
        self.combo_servicio.grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        self.entry_duracion = self.crear_entrada(marco, "Duración en horas:", 2)
        marco.columnconfigure(1, weight=1)
        ttk.Button(marco, text="Crear reserva", style="Accent.TButton", command=self.crear_reserva_gui).grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

    def crear_panel_resultados(self, padre):
        """Crea el panel derecho donde se muestran los resultados."""
        marco = ttk.LabelFrame(padre, text="Consola de eventos del sistema", style="Panel.TLabelframe")
        marco.pack(fill="both", expand=True)
        self.txt_resultado = tk.Text(marco, bg="#f8fff9", fg="#113b24", font=("Consolas", 10), wrap="word", relief="flat")
        self.txt_resultado.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scroll = ttk.Scrollbar(marco, command=self.txt_resultado.yview)
        scroll.pack(side="right", fill="y")
        self.txt_resultado.config(yscrollcommand=scroll.set)
        self.escribir("Bienvenido al sistema alternativo de Software FJ.\n")

    def crear_entrada(self, marco, etiqueta, fila):
        """Crea una etiqueta y una caja de texto en una fila determinada."""
        ttk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=8, pady=4)
        entrada = ttk.Entry(marco)
        entrada.grid(row=fila, column=1, sticky="ew", padx=8, pady=4)
        marco.columnconfigure(1, weight=1)
        return entrada

    def escribir(self, mensaje):
        """Escribe mensajes dentro de la consola visual."""
        self.txt_resultado.insert("end", mensaje + "\n")
        self.txt_resultado.see("end")

    def actualizar_combos(self):
        """Actualiza las listas desplegables de clientes y servicios."""
        self.combo_cliente["values"] = [f"{i} - {c.nombre}" for i, c in enumerate(self.sistema.clientes)]
        self.combo_servicio["values"] = [f"{i} - {s.nombre}" for i, s in enumerate(self.sistema.servicios)]

    def registrar_cliente_gui(self):
        """Registra un cliente desde la interfaz gráfica."""
        try:
            cliente = self.sistema.registrar_cliente(self.entry_nombre.get(), self.entry_correo.get(), self.entry_telefono.get())
        except ErrorSoftwareFJ as error:
            self.escribir(f"ERROR CLIENTE: {error}")
            messagebox.showerror("Error de cliente", str(error))
        else:
            self.escribir(f"CLIENTE REGISTRADO: {cliente.obtener_detalle()}")
            self.actualizar_combos()
        finally:
            logger.info("Operación gráfica de cliente finalizada.")

    def agregar_servicio_gui(self):
        """Agrega un servicio desde la interfaz gráfica."""
        try:
            tipo = self.combo_tipo.get()
            nombre = self.entry_servicio.get()
            valor = float(self.entry_valor.get())
            extra1 = self.entry_extra1.get()
            extra2 = self.entry_extra2.get()
            if tipo == "Reserva de sala":
                video = str(extra2).strip().lower() in ["si", "sí", "true", "1", "con"]
                servicio = ReservaSala(nombre, valor, int(extra1), video)
            elif tipo == "Alquiler de equipo":
                servicio = AlquilerEquipo(nombre, valor, extra1, int(extra2))
            else:
                servicio = AsesoriaEspecializada(nombre, valor, extra1, extra2)
            self.sistema.agregar_servicio(servicio)
        except ValueError as error:
            logger.error("Error de conversión creando servicio: %s", error)
            self.escribir("ERROR SERVICIO: revise valores numéricos y campos obligatorios.")
            messagebox.showerror("Error de servicio", "Revise valores numéricos y campos obligatorios.")
        except ErrorSoftwareFJ as error:
            self.escribir(f"ERROR SERVICIO: {error}")
            messagebox.showerror("Error de servicio", str(error))
        else:
            self.escribir(f"SERVICIO AGREGADO: {servicio.obtener_detalle()}")
            self.escribir(f"DESCRIPCIÓN: {servicio.descripcion()}")
            self.actualizar_combos()
        finally:
            logger.info("Operación gráfica de servicio finalizada.")

    def crear_reserva_gui(self):
        """Crea una reserva desde la interfaz gráfica."""
        try:
            if self.combo_cliente.current() < 0 or self.combo_servicio.current() < 0:
                raise ErrorCampoObligatorio("Debe seleccionar un cliente y un servicio.")
            cliente = self.sistema.clientes[self.combo_cliente.current()]
            servicio = self.sistema.servicios[self.combo_servicio.current()]
            duracion = int(self.entry_duracion.get())
            reserva = self.sistema.crear_reserva(cliente, servicio, duracion)
        except ValueError as error:
            logger.error("Error de conversión creando reserva: %s", error)
            self.escribir("ERROR RESERVA: la duración debe ser un número entero.")
            messagebox.showerror("Error de reserva", "La duración debe ser un número entero.")
        except ErrorSoftwareFJ as error:
            self.escribir(f"ERROR RESERVA: {error}")
            messagebox.showerror("Error de reserva", str(error))
        else:
            self.escribir(f"RESERVA CREADA: {reserva.obtener_detalle()}")
            self.escribir(self.sistema.resumen_general())
        finally:
            logger.info("Operación gráfica de reserva finalizada.")

    def cargar_servicios_base(self):
        """Carga servicios iniciales para facilitar las pruebas del sistema."""
        try:
            self.sistema.agregar_servicio(ReservaSala("Sala Ejecutiva", 45000, 15, True))
            self.sistema.agregar_servicio(AlquilerEquipo("Alquiler Portátil", 30000, "Portátil", 2))
            self.sistema.agregar_servicio(AsesoriaEspecializada("Asesoría Técnica", 60000, "Desarrollo de Software", "intermedio"))
        except ErrorSoftwareFJ as error:
            logger.error("Error cargando servicios base: %s", error)
        else:
            self.escribir("Servicios base cargados correctamente.")
            self.actualizar_combos()
        finally:
            logger.info("Carga inicial de servicios finalizada.")


# ==========================================================
# SIMULACIÓN DE OPERACIONES PARA VALIDAR EL SISTEMA
# ==========================================================

def simulacion_operaciones():
    """Ejecuta operaciones válidas e inválidas para probar estabilidad del sistema."""
    sistema = SistemaGestion()
    pruebas = []
    try:
        c1 = sistema.registrar_cliente("Victor Jaraba", "victor.jaraba@gmail.com", "3004567890")
        c2 = sistema.registrar_cliente("Husman Gomes", "husman.gomes@gmail.com", "3015557799")
        pruebas.append("Cliente válido 1 registrado")
        pruebas.append("Cliente válido 2 registrado")
        s1 = sistema.agregar_servicio(ReservaSala("Sala Principal", 50000, 25, True))
        s2 = sistema.agregar_servicio(AlquilerEquipo("Alquiler Computadores", 28000, "Computador", 4))
        s3 = sistema.agregar_servicio(AsesoriaEspecializada("Asesoría Avanzada", 75000, "Ciberseguridad", "avanzado"))
        pruebas.append("Tres servicios especializados creados")
        sistema.crear_reserva(c1, s1, 2)
        sistema.crear_reserva(c2, s2, 3)
        sistema.crear_reserva(c1, s3, 1)
        pruebas.append("Tres reservas válidas procesadas")
    except ErrorSoftwareFJ as error:
        logger.error("Error inesperado en simulación válida: %s", error)

    operaciones_invalidas = [
        lambda: sistema.registrar_cliente("12", "correo", "abc"),
        lambda: ReservaSala("Sala error", -1000, 20, True),
        lambda: AlquilerEquipo("Equipo error", 20000, "", 0),
        lambda: AsesoriaEspecializada("Asesoría error", 50000, "Redes", "experto"),
        lambda: sistema.crear_reserva("cliente falso", sistema.servicios[0], 1),
        lambda: sistema.crear_reserva(sistema.clientes[0], sistema.servicios[0], 0),
        lambda: sistema.servicios[0].valor_con_ajuste(0.9),
    ]

    for operacion in operaciones_invalidas:
        try:
            operacion()
        except ErrorSoftwareFJ as error:
            logger.error("Prueba inválida controlada: %s", error)
            pruebas.append(f"Error controlado: {error}")
        except Exception as error:
            logger.error("Error general encadenado: %s", error)
            pruebas.append(f"Error general controlado: {error}")
        finally:
            logger.info("Prueba de simulación finalizada.")
    return pruebas


# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================================

if __name__ == "__main__":
    # Ejecuta una simulación previa para demostrar más de 10 operaciones controladas.
    simulacion_operaciones()
    # Crea la ventana principal de Tkinter.
    ventana = tk.Tk()
    # Crea la aplicación gráfica con la ventana principal.
    app = InterfazSoftwareFJ(ventana)
    # Inicia el ciclo de ejecución de la interfaz.
    ventana.mainloop()
