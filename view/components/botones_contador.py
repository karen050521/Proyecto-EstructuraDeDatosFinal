"""
Componente de botones de incremento/decremento.
Responsabilidad: Manejar botones +/- para campos numéricos.
"""

import pygame
from typing import Tuple, Callable
from .boton_moderno import BotonModerno


class BotonesContador:
    """
    Par de botones para incrementar/decrementar valores.
    """

    def __init__(self, x: int, y: int, alto: int, 
                 on_incrementar: Callable, on_decrementar: Callable):
        """
        Inicializa los botones contador.

        Args:
            x, y (int): Posición de los botones
            alto (int): Alto de los botones
            on_incrementar (Callable): Función para incrementar
            on_decrementar (Callable): Función para decrementar
        """
        self.boton_decrementar = BotonModerno(
            "-", x, y, 25, alto, (200, 100, 100), on_decrementar
        )
        
        self.boton_incrementar = BotonModerno(
            "+", x + 30, y, 25, alto, (100, 200, 100), on_incrementar
        )

    def dibujar(self, screen) -> None:
        """Dibuja ambos botones."""
        self.boton_decrementar.dibujar(screen)
        self.boton_incrementar.dibujar(screen)

    def manejar_clic(self, pos: Tuple[int, int]) -> bool:
        """Maneja clics en cualquiera de los botones."""
        if self.boton_decrementar.manejar_clic(pos):
            return True
        if self.boton_incrementar.manejar_clic(pos):
            return True
        return False

    def actualizar_hover(self, pos: Tuple[int, int]) -> None:
        """Actualiza el estado de hover de ambos botones."""
        self.boton_decrementar.actualizar_hover(pos)
        self.boton_incrementar.actualizar_hover(pos)
