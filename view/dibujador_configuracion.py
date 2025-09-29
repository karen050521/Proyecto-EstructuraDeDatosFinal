"""
Módulo para dibujar la pantalla de configuración.
Responsabilidad: Manejar todo el dibujo visual de la pantalla.
"""

import pygame
from typing import Tuple


class DibujadorConfiguracion:
    """
    Clase responsable de dibujar la pantalla de configuración.
    """

    def __init__(self, ancho: int, alto: int):
        """
        Inicializa el dibujador.

        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto

    def dibujar_fondo(self, screen) -> None:
        """Dibuja el fondo de la pantalla."""
        # Fondo principal más atractivo
        screen.draw.filled_rect(pygame.Rect(0, 0, self.ancho, self.alto), (25, 30, 50))
        
        # Patrón de fondo sutil
        for i in range(0, self.alto, 40):
            color = (35, 40, 65)
            screen.draw.filled_rect(pygame.Rect(0, i, self.ancho, 20), color)

    def dibujar_titulo(self, screen) -> None:
        """Dibuja el título principal."""
        # Título principal simplificado
        titulo_rect = pygame.Rect(self.ancho // 2 - 200, 10, 400, 50)
        
        # Sombra
        sombra_rect = pygame.Rect(titulo_rect.x + 3, titulo_rect.y + 3, titulo_rect.width, titulo_rect.height)
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 100))
        
        # Fondo del título
        screen.draw.filled_rect(titulo_rect, (50, 70, 120))
        screen.draw.rect(titulo_rect, (120, 160, 220))
        
        # Título principal
        screen.draw.text(
            "🎮 CONFIGURACIÓN DEL JUEGO",
            (self.ancho // 2 - 150, 25),
            fontsize=20,
            color=(255, 255, 255),
        )

        # Subtítulo
        screen.draw.text(
            "🌳 Árbol AVL de Obstáculos",
            (self.ancho // 2 - 120, 45),
            fontsize=12,
            color=(200, 220, 255),
        )

    def dibujar_area_arbol(self, screen, area_arbol: pygame.Rect) -> None:
        """Dibuja el área del árbol."""
        # Sombra
        sombra_rect = pygame.Rect(
            area_arbol.x + 4,
            area_arbol.y + 4,
            area_arbol.width,
            area_arbol.height,
        )
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))

        # Fondo simplificado
        screen.draw.filled_rect(area_arbol, (40, 50, 80))
        screen.draw.rect(area_arbol, (100, 140, 200))

        # Etiqueta
        label_rect = pygame.Rect(area_arbol.x + 5, area_arbol.y - 30, 150, 25)
        screen.draw.filled_rect(label_rect, (60, 60, 60))
        screen.draw.text(
            "🌳 Vista del Árbol AVL",
            (area_arbol.x + 10, area_arbol.y - 25),
            fontsize=14,
            color=(255, 255, 255),
        )

    def dibujar_area_controles(self, screen, area_controles: pygame.Rect) -> None:
        """Dibuja el área de controles."""
        # Sombra
        sombra_rect = pygame.Rect(
            area_controles.x + 4,
            area_controles.y + 4,
            area_controles.width,
            area_controles.height,
        )
        screen.draw.filled_rect(sombra_rect, (0, 0, 0, 80))

        # Fondo simplificado
        screen.draw.filled_rect(area_controles, (45, 60, 100))
        screen.draw.rect(area_controles, (110, 150, 220))

        # Etiqueta
        label_rect = pygame.Rect(
            area_controles.x + 5, area_controles.y - 30, 120, 25
        )
        screen.draw.filled_rect(label_rect, (60, 60, 60))
        screen.draw.text(
            "⚙️ Controles",
            (area_controles.x + 10, area_controles.y - 25),
            fontsize=14,
            color=(255, 255, 255),
        )

    def dibujar_titulo_seccion(self, screen, texto: str, x: int, y: int) -> None:
        """Dibuja un título de sección."""
        screen.draw.filled_rect(
            pygame.Rect(x - 5, y - 5, len(texto) * 8 + 10, 25), (45, 45, 45)
        )
        screen.draw.text(texto, (x, y), fontsize=12, color=(255, 255, 255))

    def dibujar_info_arbol(self, screen, x: int, y: int, gestor_juego) -> None:
        """Dibuja información sobre el árbol."""
        if gestor_juego and gestor_juego.arbol_obstaculos:
            total = gestor_juego.arbol_obstaculos.obtener_total_obstaculos()
            altura = gestor_juego.arbol_obstaculos.obtener_altura(
                gestor_juego.arbol_obstaculos.raiz
            )
            info_texto = f"Obstáculos: {total} | Altura: {altura}"
            screen.draw.text(info_texto, (x, y), fontsize=10, color=(150, 150, 150))
        else:
            screen.draw.text("Árbol vacío", (x, y), fontsize=10, color=(150, 150, 150))

    def dibujar_instrucciones(self, screen, x: int, y: int) -> None:
        """Dibuja las instrucciones de uso."""
        instrucciones = [
            "💡 INSTRUCCIONES:",
            "• Usa +/- para cambiar valores",
            "• Haz clic en campos para escribir",
            "• Presiona Enter para confirmar",
            "• Usa Escape para cancelar",
        ]

        for i, instruccion in enumerate(instrucciones):
            color = (200, 200, 200) if i == 0 else (150, 150, 150)
            screen.draw.text(instruccion, (x, y + i * 15), fontsize=9, color=color)
