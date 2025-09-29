"""
Componente de campo numérico simple.
Responsabilidad: Manejar entrada de números básica.
"""

import pygame
from typing import Tuple, Optional, Callable


class CampoSimple:
    """
    Campo numérico simple con validación.
    """

    def __init__(self, x: int, y: int, ancho: int, alto: int = 28, 
                 valor_inicial: int = 0, valor_min: int = 0, valor_max: int = 9999):
        """
        Inicializa el campo numérico.

        Args:
            x, y (int): Posición del campo
            ancho, alto (int): Dimensiones del campo
            valor_inicial (int): Valor inicial
            valor_min, valor_max (int): Rango de valores permitidos
        """
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.valor = valor_inicial
        self.valor_min = valor_min
        self.valor_max = valor_max
        self.activo = False
        self.hover = False
        self.valido = True

    def dibujar(self, screen) -> None:
        """Dibuja el campo numérico."""
        # Sombra
        sombra_rect = pygame.Rect(self.x + 2, self.y + 2, self.ancho, self.alto)
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))
        
        # Colores según estado
        if self.activo:
            color_fondo = (255, 255, 255)
            color_borde = (100, 180, 255)
        elif self.hover:
            color_fondo = (250, 250, 255)
            color_borde = (140, 160, 200)
        else:
            color_fondo = (240, 245, 250)
            color_borde = (160, 170, 180)
        
        # Fondo del campo
        campo_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        screen.draw.filled_rect(campo_rect, color_fondo)
        screen.draw.rect(campo_rect, color_borde)
        
        # Texto del valor
        texto_valor = str(self.valor)
        color_texto = (30, 30, 30) if self.activo else (100, 100, 100)
        screen.draw.text(texto_valor, (self.x + 10, self.y + 7), 
                       fontsize=12, color=color_texto)

    def verificar_clic(self, pos: Tuple[int, int]) -> bool:
        """Verifica si el clic está dentro del campo."""
        x, y = pos
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)

    def manejar_clic(self, pos: Tuple[int, int]) -> bool:
        """Maneja el clic en el campo."""
        if self.verificar_clic(pos):
            self.activo = True
            return True
        return False

    def activar(self) -> None:
        """Activa el campo."""
        self.activo = True

    def desactivar(self) -> None:
        """Desactiva el campo."""
        self.activo = False

    def establecer_valor(self, valor: int) -> None:
        """Establece el valor del campo."""
        self.valor = max(self.valor_min, min(self.valor_max, valor))

    def obtener_valor(self) -> int:
        """Obtiene el valor actual."""
        return self.valor

    def incrementar(self) -> None:
        """Incrementa el valor."""
        if self.valor < self.valor_max:
            self.valor += 1

    def decrementar(self) -> None:
        """Decrementa el valor."""
        if self.valor > self.valor_min:
            self.valor -= 1

    def actualizar_hover(self, pos: Tuple[int, int]) -> None:
        """Actualiza el estado de hover."""
        self.hover = self.verificar_clic(pos)
