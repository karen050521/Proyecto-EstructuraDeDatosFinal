"""
Componente de botón moderno para la interfaz.
Responsabilidad: Renderizar botones con diseño moderno y manejar estados.
"""

import pygame
from typing import Tuple, Optional, Callable


class BotonModerno:
    """
    Botón con diseño moderno y efectos visuales.
    """

    def __init__(self, texto: str, x: int, y: int, ancho: int, alto: int, 
                 color: Tuple[int, int, int], accion: Optional[Callable] = None):
        """
        Inicializa el botón.

        Args:
            texto (str): Texto del botón
            x, y (int): Posición del botón
            ancho, alto (int): Dimensiones del botón
            color (tuple): Color RGB del botón
            accion (Callable): Función a ejecutar al hacer clic
        """
        self.texto = texto
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.accion = accion
        self.hover = False
        self.presionado = False

    def dibujar(self, screen) -> None:
        """
        Dibuja el botón en la pantalla.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Ajustar color según estado
        color_actual = self.color
        if self.presionado:
            color_actual = tuple(max(0, c - 30) for c in self.color)
        elif self.hover:
            color_actual = tuple(min(255, c + 20) for c in self.color)

        # Sombra del botón
        sombra_rect = pygame.Rect(self.x + 3, self.y + 3, self.ancho, self.alto)
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 120))
        
        # Fondo del botón
        boton_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        screen.draw.filled_rect(boton_rect, color_actual)
        
        # Borde exterior brillante
        screen.draw.rect(boton_rect, (255, 255, 255, 200))
        
        # Borde interno
        borde_interno = pygame.Rect(self.x + 2, self.y + 2, self.ancho - 4, self.alto - 4)
        screen.draw.rect(borde_interno, (0, 0, 0, 100))
        
        # Efecto de gradiente
        gradiente_rect = pygame.Rect(self.x + 3, self.y + 3, self.ancho - 6, self.alto // 2)
        screen.draw.filled_rect(gradiente_rect, (255, 255, 255, 30))
        
        # Texto centrado con sombra
        texto_x = self.x + (self.ancho - len(self.texto) * 6) // 2
        texto_y = self.y + (self.alto - 12) // 2
        
        # Sombra del texto
        screen.draw.text(self.texto, (texto_x + 1, texto_y + 1), 
                        fontsize=11, color=(0, 0, 0, 150))
        
        # Texto principal
        screen.draw.text(self.texto, (texto_x, texto_y), 
                        fontsize=11, color=(255, 255, 255))

    def verificar_clic(self, pos: Tuple[int, int]) -> bool:
        """
        Verifica si el clic está dentro del botón.

        Args:
            pos (tuple): Posición del clic (x, y)

        Returns:
            bool: True si el clic está dentro del botón
        """
        x, y = pos
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)

    def manejar_clic(self, pos: Tuple[int, int]) -> bool:
        """
        Maneja el clic en el botón.

        Args:
            pos (tuple): Posición del clic

        Returns:
            bool: True si se ejecutó la acción
        """
        if self.verificar_clic(pos):
            print(f"Clic en botón: {self.texto}")
            if self.accion:
                resultado = self.accion()
                print(f"Resultado de la acción del botón: {resultado}")
            else:
                print("Este botón no tiene acción definida")
            return True
        return False

    def actualizar_hover(self, pos: Tuple[int, int]) -> None:
        """
        Actualiza el estado de hover del botón.

        Args:
            pos (tuple): Posición del mouse
        """
        self.hover = self.verificar_clic(pos)
