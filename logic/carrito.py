"""
Clase que representa el carrito del jugador.
Responsabilidad: Gestionar posición, movimiento, estado y colisiones del carrito.
"""

from enum import Enum


class EstadoCarrito(Enum):
    """Estados posibles del carrito durante el juego."""

    NORMAL = "normal"
    SALTANDO = "saltando"
    COLISIONANDO = "colisionando"
    INVULNERABLE = "invulnerable"


class Carrito:
    """
    Representa el carrito controlado por el jugador.
    Maneja movimiento automático en X y control manual en Y.
    """

    def __init__(
        self,
        x_inicial: int = 50,
        y_inicial: int = 2,  # Comenzar en el carril 2 (centro-abajo)
        energia_maxima: int = 100,
    ) -> None:
        """
        Inicializa el carrito en la posición especificada.

        Args:
            x_inicial (int): Posición X inicial
            y_inicial (int): Carril inicial (0-5: 0,1,2=carriles inferiores; 3,4,5=carriles superiores)
            energia_maxima (int): Energía máxima del carrito
        """
        self.x: int = x_inicial
        self.y: int = y_inicial
        self.energia_actual: int = energia_maxima
        self.energia_maxima: int = energia_maxima
        self.estado: EstadoCarrito = EstadoCarrito.NORMAL

        # Configuración de movimiento
        self.velocidad_x: int = 5  # metros por frame
        self.velocidad_y: int = 0  # velocidad vertical actual
        self.altura_salto: int = 50  # altura máxima del salto
        self.tiempo_salto: int = 0  # tiempo actual de salto
        self.duracion_salto: int = 20  # frames que dura el salto

        # Configuración visual
        self.ancho: int = 40
        self.alto: int = 30
        self.color_normal: str = "azul"
        self.color_saltando: str = "amarillo"
        self.color_actual: str = self.color_normal

    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado del carrito cada frame.

        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        self.mover_automaticamente()
        if self.estado == EstadoCarrito.SALTANDO:
            self.actualizar_salto()
            
        # Consumir energía gradualmente mientras avanza
        # Consumo proporcional a la velocidad (ajustado para ser equilibrado)
        consumo_energia = 0.01 * self.velocidad_x  # Reducido a 1/5 del valor anterior
        self.energia_actual = max(0, self.energia_actual - consumo_energia)
        
        # Imprimir información de depuración cada 100 frames aproximadamente
        if int(self.x) % 100 == 0:
            print(f"Energía actual: {self.energia_actual:.2f}, Consumo: {consumo_energia:.4f}, Velocidad: {self.velocidad_x}")

    def mover_automaticamente(self) -> None:
        """
        Mueve el carrito automáticamente hacia adelante en el eje X.
        """
        self.x += self.velocidad_x

    def mover_arriba(self) -> None:
        """
        Mueve el carrito un carril hacia arriba (si es posible).
        """
        if self.y < 5:  # 0=abajo, 5=arriba (6 carriles totales: 0,1,2,3,4,5)
            self.y += 1

    def mover_abajo(self) -> None:
        """
        Mueve el carrito un carril hacia abajo (si es posible).
        """
        if self.y > 0:  # 0=abajo, 5=arriba (6 carriles totales: 0,1,2,3,4,5)
            self.y -= 1

    def saltar(self) -> None:
        """
        Inicia el salto del carrito si no está ya saltando.
        """
        if self.estado != EstadoCarrito.SALTANDO:
            self.estado = EstadoCarrito.SALTANDO
            self.tiempo_salto = 0
            self.color_actual = self.color_saltando

    def actualizar_salto(self) -> None:
        """
        Actualiza la lógica del salto (altura y duración).
        """
        self.tiempo_salto += 1

        # Calcular altura del salto (parábola invertida)
        progreso = self.tiempo_salto / self.duracion_salto
        # Usar una parábola que va de 0 a altura máxima y luego baja a 0
        altura_actual = int(self.altura_salto * 4 * progreso * (1 - progreso))
        
        # Calcular velocidad basada en la diferencia de altura
        if self.tiempo_salto == 0:
            self.velocidad_y = 0
        else:
            # Velocidad es la diferencia de altura entre frames
            altura_anterior = int(self.altura_salto * 4 * (progreso - 1/self.duracion_salto) * (1 - (progreso - 1/self.duracion_salto)))
            self.velocidad_y = altura_actual - altura_anterior

        # Terminar salto
        if self.tiempo_salto >= self.duracion_salto:
            self.estado = EstadoCarrito.NORMAL
            self.velocidad_y = 0
            self.color_actual = self.color_normal

    def recibir_daño(self, cantidad_daño: int) -> bool:
        """
        Reduce la energía del carrito por una colisión.

        Args:
            cantidad_daño (int): Cantidad de energía a reducir

        Returns:
            bool: True si el carrito sigue vivo, False si se quedó sin energía
        """
        # Solo aplicar daño si es positivo
        if cantidad_daño > 0:
            self.energia_actual = max(0, self.energia_actual - cantidad_daño)
        return self.energia_actual > 0
 
    def obtener_rectangulo_colision(self) -> dict:
        """
        Obtiene el rectángulo de colisión actual del carrito.

        Returns:
            dict: Diccionario con 'x', 'y', 'ancho', 'alto'
        """
        return {"x": self.x, "y": self.y, "ancho": self.ancho, "alto": self.alto}
        
    def get_hitbox(self) -> 'pygame.Rect':
        """Alias para obtener_rectangulo_colision que devuelve pygame.Rect."""
        import pygame
        rect_data = self.obtener_rectangulo_colision()
        return pygame.Rect(rect_data["x"], rect_data["y"], rect_data["ancho"], rect_data["alto"])

    def colisiona_con(self, obstaculo) -> bool:
        """
        Verifica si el carrito está colisionando con un obstáculo.

        Args:
            obstaculo: Obstáculo a verificar

        Returns:
            bool: True si hay colisión
        """
        carrito_rect = self.obtener_rectangulo_colision()
        obstaculo_rect = obstaculo.obtener_rectangulo_colision()

        # Verificar colisión en X
        colision_x = (
            carrito_rect["x"] < obstaculo_rect["x"] + obstaculo_rect["ancho"]
            and carrito_rect["x"] + carrito_rect["ancho"] > obstaculo_rect["x"]
        )

        # Verificar colisión en Y
        colision_y = (
            carrito_rect["y"] == obstaculo_rect["y"]  # Usar igualdad para comparar carriles
        )

        colision = colision_x and colision_y
        
        # Información de depuración en caso de colisión
        if colision:
            print(f"¡COLISIÓN! con {obstaculo}")
            print(f"Carrito: {carrito_rect}")
            print(f"Obstáculo: {obstaculo_rect}")
        
        return colision

    def esta_saltando(self) -> bool:
        """
        Verifica si el carrito está en estado de salto.

        Returns:
            bool: True si está saltando
        """
        return self.estado == EstadoCarrito.SALTANDO

    def esta_vivo(self) -> bool:
        """
        Verifica si el carrito tiene energía suficiente para continuar.

        Returns:
            bool: True si tiene energía > 0
        """
        return self.energia_actual > 0

    def obtener_porcentaje_energia(self) -> float:
        """
        Obtiene el porcentaje actual de energía.

        Returns:
            float: Porcentaje de energía (0.0 a 1.0)
        """
        return (
            self.energia_actual / self.energia_maxima
            if self.energia_maxima > 0
            else 0.0
        )

    def reiniciar(self, x_inicial: int = 50, y_inicial: int = 2) -> None:
        """
        Reinicia el carrito a su estado inicial.

        Args:
            x_inicial (int): Nueva posición X inicial
            y_inicial (int): Nuevo carril inicial (0-5)
        """
        self.x = x_inicial
        self.y = y_inicial
        self.energia_actual = self.energia_maxima
        self.estado = EstadoCarrito.NORMAL
        self.velocidad_y = 0
        self.tiempo_salto = 0
        self.color_actual = self.color_normal

    def obtener_sprite_nombre(self) -> str:
        """
        Obtiene el nombre del sprite actual según el estado.

        Returns:
            str: Nombre del archivo de sprite
        """
        if self.estado == EstadoCarrito.SALTANDO:
            return "carrito_saltando"
        elif self.estado == EstadoCarrito.COLISIONANDO:
            return "carrito_dañado"
        else:
            return "carrito_normal"

    def __str__(self) -> str:
        """
        Representación en string del carrito para debugging.

        Returns:
            str: Información del estado actual
        """
        return f"Carrito(pos: ({self.x}, {self.y}), energia: {self.energia_actual}/{self.energia_maxima}, estado: {self.estado.value})"
