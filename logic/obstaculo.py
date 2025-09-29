"""
Clase que representa un obstáculo en el juego.
Responsabilidad: Encapsular las propiedades y comportamiento de un obstáculo individual.
"""

from enum import Enum


class TipoObstaculo(Enum):
    """Tipos de obstáculos disponibles en el juego."""

    ROCA = "roca"
    CONO = "cono"
    HUECO = "hueco"
    ACEITE = "aceite"
    BARRERA = "barrera"


class Obstaculo:
    """
    Representa un obstáculo en el juego con posición, tipo y propiedades de daño.
    """

    # Configuración de daño por tipo de obstáculo
    DAÑO_POR_TIPO = {
        TipoObstaculo.ROCA: 20,
        TipoObstaculo.CONO: 10,
        TipoObstaculo.HUECO: 15,
        TipoObstaculo.ACEITE: 5,
        TipoObstaculo.BARRERA: 25,
    }

    def __init__(
        self,
        x: int,
        y: int,
        tipo: TipoObstaculo,
        ancho: int = 30,
        alto: int = 30,
    ) -> None:
        """
        Crea un nuevo obstáculo.

        Args:
            x (int): Posición X en la carretera (distancia)
            y (int): Posición Y (carril: 0-5, donde 0,1,2=carriles inferiores y 3,4,5=carriles superiores)
            tipo (TipoObstaculo): Tipo de obstáculo
            ancho (int): Ancho del obstáculo en píxeles
            alto (int): Alto del obstáculo en píxeles
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.ancho = ancho
        
        # Las barreras son más altas (ocupan 2 carriles de altura)
        if tipo == TipoObstaculo.BARRERA:
            self.alto = 100  # Doble altura para ocupar 2 carriles
        else:
            self.alto = alto
            
    def es_barrera(self) -> bool:
        """
        Verifica si este obstáculo es una barrera.
        
        Returns:
            bool: True si es una barrera
        """
        return self.tipo == TipoObstaculo.BARRERA
        
    def se_puede_saltar(self) -> bool:
        """
        Verifica si este obstáculo se puede evitar saltando.
        
        Returns:
            bool: True si se puede saltar (solo barreras)
        """
        return self.tipo == TipoObstaculo.BARRERA

    def obtener_daño(self) -> int:
        """
        Obtiene el daño que causa este obstáculo al carrito.

        Returns:
            int: Puntos de daño que causa este obstáculo
        """
        return self.DAÑO_POR_TIPO.get(self.tipo, 0)

    def obtener_rectangulo_colision(self) -> dict:
        """
        Obtiene el rectángulo de colisión del obstáculo.

        Returns:
            dict: Diccionario con 'x', 'y', 'ancho', 'alto' del rectángulo
        """
        return {"x": self.x, "y": self.y, "ancho": self.ancho, "alto": self.alto}
    
    def get_hitbox(self) -> 'pygame.Rect':
        """Alias para obtener_rectangulo_colision que devuelve pygame.Rect."""
        import pygame
        rect_data = self.obtener_rectangulo_colision()
        return pygame.Rect(rect_data["x"], rect_data["y"], rect_data["ancho"], rect_data["alto"])

    def esta_en_rango(self, x_min: int, x_max: int, y_min: int, y_max: int) -> bool:
        """
        Verifica si el obstáculo está dentro del rango especificado.

        Args:
            x_min (int): Límite inferior X
            x_max (int): Límite superior X
            y_min (int): Límite inferior Y (carril)
            y_max (int): Límite superior Y (carril)

        Returns:
            bool: True si está dentro del rango
        """
        en_rango_x = x_min <= self.x <= x_max
        en_rango_y = y_min <= self.y <= y_max
        
        # Debugging para ver si está en rango
        if en_rango_x and en_rango_y and (self.x - x_min < 100):  # Solo imprimir los que están cerca del límite
            print(f"Obstáculo en rango: {self} - X: {x_min} <= {self.x} <= {x_max}, Y: {y_min} <= {self.y} <= {y_max}")
            
        return en_rango_x and en_rango_y

    def obtener_sprite_nombre(self) -> str:
        """
        Obtiene el nombre del sprite asociado a este tipo de obstáculo.

        Returns:
            str: Nombre del archivo de sprite (sin extensión)
        """
        return self.tipo.value

    def __str__(self) -> str:
        """
        Representación en string del obstáculo.

        Returns:
            str: Información del obstáculo
        """
        return f"Obstaculo({self.tipo.value} en ({self.x}, {self.y}), daño: {self.obtener_daño()})"

    def __eq__(self, other: object) -> bool:
        """
        Compara dos obstáculos por coordenadas.

        Args:
            other (Obstaculo): Otro obstáculo a comparar

        Returns:
            bool: True si tienen las mismas coordenadas
        """
        if not isinstance(other, Obstaculo):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Hash del obstáculo basado en sus coordenadas.

        Returns:
            int: Hash del obstáculo
        """
        return hash((self.x, self.y))
