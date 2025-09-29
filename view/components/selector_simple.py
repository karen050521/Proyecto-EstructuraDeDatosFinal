"""
Componente selector simple que alterna entre opciones.
Responsabilidad: Permitir seleccionar entre opciones con clics simples.
"""

import pygame
from typing import List, Tuple


class SelectorSimple:
    """
    Selector simple que alterna entre opciones con cada clic.
    """

    def __init__(self, x: int, y: int, ancho: int, alto: int, 
                 opciones: List[str], opcion_inicial: str = None):
        """
        Inicializa el selector.

        Args:
            x, y (int): Posición del selector
            ancho, alto (int): Dimensiones del selector
            opciones (List[str]): Lista de opciones disponibles
            opcion_inicial (str): Opción seleccionada inicialmente
        """
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.opciones = opciones
        self.opcion_actual = opcion_inicial or opciones[0]
        self.hover = False

    def dibujar(self, screen) -> None:
        """Dibuja el selector."""
        # Sombra del selector
        sombra_rect = pygame.Rect(self.x + 2, self.y + 2, self.ancho, self.alto)
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))
        
        # Fondo del selector
        color_fondo = (250, 250, 255) if self.hover else (240, 245, 250)
        selector_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        screen.draw.filled_rect(selector_rect, color_fondo)
        
        # Borde
        color_borde = (100, 180, 255) if self.hover else (160, 170, 180)
        screen.draw.rect(selector_rect, color_borde)
        
        # Borde interno
        borde_interno = pygame.Rect(self.x + 2, self.y + 2, self.ancho - 4, self.alto - 4)
        screen.draw.rect(borde_interno, (120, 130, 140))
        
        # Texto de la opción actual
        screen.draw.text(self.opcion_actual.upper(), (self.x + 10, self.y + 7), 
                        fontsize=11, color=(50, 50, 50))
        
        # Flecha indicadora
        flecha_x = self.x + self.ancho - 20
        flecha_y = self.y + 7
        screen.draw.text("▼", (flecha_x, flecha_y), fontsize=10, color=(100, 100, 100))

    def verificar_clic(self, pos: Tuple[int, int]) -> bool:
        """Verifica si el clic está dentro del selector."""
        x, y = pos
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)

    def manejar_clic(self, pos: Tuple[int, int]) -> bool:
        """Maneja el clic en el selector - alterna a la siguiente opción."""
        if not self.verificar_clic(pos):
            return False
        
        # Encontrar el índice de la opción actual
        indice_actual = self.opciones.index(self.opcion_actual)
        
        # Ir a la siguiente opción (circular)
        siguiente_indice = (indice_actual + 1) % len(self.opciones)
        self.opcion_actual = self.opciones[siguiente_indice]
        
        return True

    def obtener_opcion_actual(self) -> str:
        """Obtiene la opción actualmente seleccionada."""
        return self.opcion_actual

    def establecer_opcion(self, opcion: str) -> None:
        """Establece la opción seleccionada."""
        if opcion in self.opciones:
            self.opcion_actual = opcion

    def actualizar_hover(self, pos: Tuple[int, int]) -> None:
        """Actualiza el estado de hover."""
        self.hover = self.verificar_clic(pos)
