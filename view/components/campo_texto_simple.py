"""
Componente de campo de texto simplificado.
Responsabilidad: Manejar entrada de texto básica.
"""

import pygame
from typing import Tuple, Optional, Callable


class CampoTextoSimple:
    """
    Campo de texto simplificado.
    """

    def __init__(self, x: int, y: int, ancho: int, alto: int = 28, 
                 placeholder: str = "", validador: Optional[Callable] = None):
        """
        Inicializa el campo de texto.

        Args:
            x, y (int): Posición del campo
            ancho, alto (int): Dimensiones del campo
            placeholder (str): Texto de placeholder
            validador (Callable): Función para validar el texto
        """
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.placeholder = placeholder
        self.validador = validador
        self.texto = ""
        self.activo = False
        self.hover = False
        self.valido = True

    def dibujar(self, screen) -> None:
        """Dibuja el campo de texto."""
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
        
        # Indicar si es inválido
        if not self.valido:
            color_borde = (255, 100, 100)
        
        # Fondo del campo
        campo_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        screen.draw.filled_rect(campo_rect, color_fondo)
        screen.draw.rect(campo_rect, color_borde)
        
        # Texto del campo
        if self.texto:
            color_texto = (30, 30, 30) if self.activo else (100, 100, 100)
            screen.draw.text(self.texto, (self.x + 10, self.y + 7), 
                           fontsize=12, color=color_texto)
        elif not self.activo:
            # Placeholder
            screen.draw.text(self.placeholder, (self.x + 10, self.y + 7), 
                           fontsize=11, color=(150, 150, 150))
        
        # Cursor si está activo
        if self.activo:
            cursor_x = self.x + 10 + len(self.texto) * 7
            screen.draw.line((cursor_x, self.y + 6), (cursor_x, self.y + 22), 
                           (100, 180, 255))

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

    def agregar_caracter(self, caracter: str) -> None:
        """Agrega un carácter al texto."""
        if self.activo:
            self.texto += caracter
            self.validar()

    def borrar_caracter(self) -> None:
        """Borra el último carácter del texto."""
        if self.activo and self.texto:
            self.texto = self.texto[:-1]
            self.validar()

    def limpiar(self) -> None:
        """Limpia el texto del campo."""
        self.texto = ""
        self.valido = True

    def obtener_texto(self) -> str:
        """Obtiene el texto actual."""
        return self.texto

    def establecer_texto(self, texto: str) -> None:
        """Establece el texto del campo."""
        self.texto = texto
        self.validar()

    def validar(self) -> None:
        """Valida el texto usando el validador."""
        if self.validador:
            self.valido = self.validador(self.texto)
        else:
            self.valido = True

    def actualizar_hover(self, pos: Tuple[int, int]) -> None:
        """Actualiza el estado de hover."""
        self.hover = self.verificar_clic(pos)
