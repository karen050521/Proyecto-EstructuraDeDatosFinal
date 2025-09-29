"""
Pantalla de configuración del juego refactorizada.
Responsabilidad: Coordinar la interfaz de configuración usando componentes UI.
"""

import pygame
from typing import Optional, Tuple
from .visualizador_arbol import VisualizadorArbol
from .components import BotonModerno, CampoTextoSimple, CampoSimple, BotonesContador, SelectorSimple
from .dibujador_configuracion import DibujadorConfiguracion
from .controlador_configuracion import ControladorConfiguracion


class PantallaConfiguracion:
    """
    Pantalla que permite configurar el árbol de obstáculos antes de jugar.
    """

    def __init__(self, ancho=800, alto=600):
        """
        Inicializa la pantalla de configuración.

        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        self.gestor_juego = None

        # Áreas de la interfaz
        self.area_arbol = pygame.Rect(50, 100, 400, 400)
        self.area_controles = pygame.Rect(500, 100, 250, 500)

        # Visualizador del árbol
        self.visualizador = VisualizadorArbol(400, 400)
        
        # Módulos auxiliares
        self.dibujador = DibujadorConfiguracion(ancho, alto)
        self.controlador = ControladorConfiguracion(self)

        # Componentes UI
        self._crear_componentes_ui()

    def _crear_componentes_ui(self):
        """Crea todos los componentes UI."""
        x = self.area_controles.x + 15
        y = self.area_controles.y + 20

        # Campos numéricos
        self.campo_x = CampoSimple(x + 20, y + 60, 80, 28, 0, 0, 9999)
        self.campo_y = CampoSimple(x + 20, y + 110, 80, 28, 0, 0, 2)
        
        # Botones contador
        self.botones_x = BotonesContador(
            x + 110, y + 60, 28, 
            self.campo_x.incrementar, self.campo_x.decrementar
        )
        
        self.botones_y = BotonesContador(
            x + 110, y + 110, 28, 
            self.campo_y.incrementar, self.campo_y.decrementar
        )

        # Selector de tipo
        tipos = ["roca", "cono", "hueco", "aceite", "barrera"]
        self.selector_tipo = SelectorSimple(x + 20, y + 160, 120, 28, tipos, "roca")


        # Botones principales
        self.boton_agregar = BotonModerno(
            "➕ AGREGAR", x, y + 220, 120, 35, (76, 175, 80), self._agregar_obstaculo
        )

        self.boton_anchura = BotonModerno(
            "🔍 RECORRIDO ANCHURA",
            x,
            y + 320,
            180,
            30,
            (33, 150, 243),
            self._mostrar_recorrido_anchura,
        )

        self.boton_profundidad = BotonModerno(
            "🔍 RECORRIDO PROFUNDIDAD",
            x,
            y + 360,
            180,
            30,
            (33, 150, 243),
            self._mostrar_recorrido_profundidad,
        )

        self.boton_iniciar = BotonModerno(
            "🚀 INICIAR JUEGO", x, y + 380, 150, 40, (255, 152, 0), self._iniciar_juego
        )

    def _validar_coordenada_x(self, valor: int) -> bool:
        """Valida la coordenada X."""
        return valor >= 0

    def _validar_coordenada_y(self, valor: int) -> bool:
        """Valida la coordenada Y."""
        return 0 <= valor <= 2

    def _agregar_obstaculo(self):
        """Agrega un obstáculo al árbol."""
        if not self.gestor_juego:
            print("Error: No hay gestor de juego")
            return

        if not self.campo_x.valido or not self.campo_y.valido:
            print("Error: Campos inválidos")
            return

        try:
            x = self.campo_x.obtener_valor()
            y = self.campo_y.obtener_valor()
            tipo_str = self.selector_tipo.obtener_opcion_actual()

            from logic.obstaculo import TipoObstaculo

            tipo = TipoObstaculo(tipo_str)

            if self.gestor_juego.agregar_obstaculo(x, y, tipo):
                print(f"Obstáculo agregado: ({x}, {y}) tipo {tipo_str}")
                # Resetear a valores por defecto
                self.campo_x.establecer_valor(0)
                self.campo_y.establecer_valor(0)
            else:
                print(f"Error: Ya existe un obstáculo en ({x}, {y})")

        except Exception as e:
            print(f"Error al agregar obstáculo: {e}")

    def _mostrar_recorrido_anchura(self):
        """Muestra el recorrido en anchura."""
        if self.gestor_juego and not self.gestor_juego.arbol_obstaculos.esta_vacio():
            recorrido = self.gestor_juego.obtener_recorrido_anchura()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            print("Recorrido en anchura iniciado")

    def _mostrar_recorrido_profundidad(self):
        """Muestra el recorrido en profundidad."""
        if self.gestor_juego and not self.gestor_juego.arbol_obstaculos.esta_vacio():
            recorrido = self.gestor_juego.obtener_recorrido_profundidad()
            self.visualizador.iniciar_animacion_recorrido(recorrido)
            print("Recorrido en profundidad iniciado")

    def _iniciar_juego(self):
        """Inicia el juego."""
        print("🚀 ¡INICIANDO JUEGO DESDE PANTALLA DE CONFIGURACIÓN!")
        return "iniciar_juego"


    def dibujar(self, screen):
        """
        Dibuja toda la pantalla de configuración.

        Args:
            screen: Superficie de pygame donde dibujar
        """
        self.dibujador.dibujar_fondo(screen)
        self.dibujador.dibujar_titulo(screen)
        self.dibujador.dibujar_area_arbol(screen, self.area_arbol)
        self.dibujador.dibujar_area_controles(screen, self.area_controles)
        self._dibujar_arbol(screen)
        self._dibujar_controles(screen)


    def _dibujar_arbol(self, screen):
        """Dibuja la visualización del árbol."""
        if self.gestor_juego and self.gestor_juego.arbol_obstaculos:
            self.visualizador.dibujar_arbol(
                screen,
                self.gestor_juego.arbol_obstaculos,
                self.area_arbol.x,
                self.area_arbol.y,
            )

    def _dibujar_controles(self, screen):
        """Dibuja todos los controles."""
        x = self.area_controles.x + 15
        y = self.area_controles.y + 20

        # Títulos de sección
        self.dibujador.dibujar_titulo_seccion(screen, "AGREGAR OBSTÁCULO", x, y)
        y += 40

        # Etiquetas
        screen.draw.text("Posición X:", (x, y), fontsize=11, color=(200, 200, 200))
        screen.draw.text(
            "Carril Y (0-2):", (x, y + 50), fontsize=11, color=(200, 200, 200)
        )
        screen.draw.text(
            "Tipo de obstáculo:", (x, y + 100), fontsize=11, color=(200, 200, 200)
        )

        # Componentes
        self.campo_x.dibujar(screen)
        self.campo_y.dibujar(screen)
        self.selector_tipo.dibujar(screen)
        
        # Botones contador
        self.botones_x.dibujar(screen)
        self.botones_y.dibujar(screen)

        # Botón principal
        self.boton_agregar.dibujar(screen)

        # Separador
        y += 120
        screen.draw.line((x, y), (x + 200, y), (100, 100, 100))
        y += 20

        # Recorridos
        self.dibujador.dibujar_titulo_seccion(screen, "RECORRIDOS DEL ÁRBOL", x, y)
        y += 35

        self.boton_anchura.dibujar(screen)
        self.boton_profundidad.dibujar(screen)

        # Separador
        y += 80
        screen.draw.line((x, y), (x + 200, y), (100, 100, 100))
        y += 20

        # Iniciar juego
        self.boton_iniciar.dibujar(screen)

        # Información del árbol
        y += 60
        self.dibujador.dibujar_info_arbol(screen, x, y, self.gestor_juego)

        # Instrucciones de uso
        y += 30
        self.dibujador.dibujar_instrucciones(screen, x, y)


    def manejar_clic_mouse(self, pos):
        """
        Maneja los clics del mouse.

        Args:
            pos (tuple): Posición del clic

        Returns:
            str: Acción a realizar o None
        """
        resultado = self.controlador.manejar_clic_mouse(pos)
        print(f"🔍 RESULTADO DE controlador.manejar_clic_mouse(): {resultado}")
        return resultado


    def manejar_tecla(self, tecla):
        """
        Maneja las teclas presionadas.

        Args:
            tecla: Tecla presionada
        
        Returns:
            str: Acción a realizar o None
        """
        return self.controlador.manejar_tecla(tecla)

