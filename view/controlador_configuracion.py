"""
Módulo para manejar eventos de la pantalla de configuración.
Responsabilidad: Manejar clics y teclas de la pantalla.
"""

from typing import Tuple, Optional


class ControladorConfiguracion:
    """
    Clase responsable de manejar eventos de la pantalla de configuración.
    """

    def __init__(self, pantalla):
        """
        Inicializa el controlador.

        Args:
            pantalla: Referencia a la pantalla de configuración
        """
        self.pantalla = pantalla

    def manejar_clic_mouse(self, pos: Tuple[int, int]) -> Optional[str]:
        """
        Maneja los clics del mouse.

        Args:
            pos (tuple): Posición del clic

        Returns:
            str: Acción a realizar o None
        """
        x, y = pos

        # Verificar clic en área del árbol
        if self.pantalla.area_arbol.collidepoint(x, y):
            if (self.pantalla.gestor_juego and 
                self.pantalla.gestor_juego.arbol_obstaculos):
                nodo = self.pantalla.visualizador.obtener_nodo_en_posicion(
                    self.pantalla.gestor_juego.arbol_obstaculos,
                    x - self.pantalla.area_arbol.x,
                    y - self.pantalla.area_arbol.y,
                )
                if nodo:
                    self.pantalla.visualizador.establecer_nodo_seleccionado(nodo)
                    return "seleccionar_nodo"

        # Verificar clic en controles
        if self.pantalla.area_controles.collidepoint(x, y):
            resultado = self._manejar_clic_controles(pos)
            print(f"🔍 RESULTADO DE _manejar_clic_controles(): {resultado}")
            return resultado

        return None

    def _manejar_clic_controles(self, pos: Tuple[int, int]) -> Optional[str]:
        """Maneja clics en el área de controles."""
        # Verificar primero el botón de iniciar juego ya que es prioritario
        print(f"Verificando clic en botón iniciar juego en posición: {pos}")
        if self.pantalla.boton_iniciar.verificar_clic(pos):
            print("¡Clic detectado en el botón iniciar juego!")
            resultado = self.pantalla._iniciar_juego()
            print(f"🔍 RESULTADO DE _iniciar_juego(): {resultado}")
            return resultado

        # Resto de componentes
        if self.pantalla.campo_x.verificar_clic(pos):
            self.pantalla.campo_x.activar()
            self.pantalla.campo_y.desactivar()
            return None

        if self.pantalla.campo_y.verificar_clic(pos):
            self.pantalla.campo_y.activar()
            self.pantalla.campo_x.desactivar()
            return None

        if self.pantalla.selector_tipo.manejar_clic(pos):
            return None

        if self.pantalla.campo_x.manejar_clic(pos):
            return None

        if self.pantalla.campo_y.manejar_clic(pos):
            return None

        if self.pantalla.botones_x.manejar_clic(pos):
            return None

        if self.pantalla.botones_y.manejar_clic(pos):
            return None

        if self.pantalla.boton_agregar.manejar_clic(pos):
            return None

        if self.pantalla.boton_anchura.manejar_clic(pos):
            return None

        if self.pantalla.boton_profundidad.manejar_clic(pos):
            return None

        # Desactivar campos si se hace clic fuera
        self.pantalla.campo_x.desactivar()
        self.pantalla.campo_y.desactivar()

        return None

        # Desactivar campos si se hace clic fuera
        self.pantalla.campo_x.desactivar()
        self.pantalla.campo_y.desactivar()

        return None

    def manejar_tecla(self, tecla) -> Optional[str]:
        """
        Maneja las teclas presionadas.

        Args:
            tecla: Tecla presionada

        Returns:
            str: Acción a realizar o None
        """
        # Manejar entrada de texto
        if self.pantalla.campo_x.activo or self.pantalla.campo_y.activo:
            campo_activo = (
                self.pantalla.campo_x if self.pantalla.campo_x.activo 
                else self.pantalla.campo_y
            )

            if tecla == "backspace":
                campo_activo.borrar_caracter()
            elif tecla == "return":
                if self.pantalla.campo_x.activo:
                    self.pantalla.campo_x.desactivar()
                    self.pantalla.campo_y.activar()
                else:
                    self.pantalla._agregar_obstaculo()
                    self.pantalla.campo_x.desactivar()
                    self.pantalla.campo_y.desactivar()
            elif tecla == "escape":
                self.pantalla.campo_x.desactivar()
                self.pantalla.campo_y.desactivar()
            else:
                # Manejar diferentes tipos de entrada
                if hasattr(tecla, "name"):
                    if tecla.name.isdigit():
                        campo_activo.agregar_caracter(tecla.name)
                    elif tecla.name == "minus":
                        campo_activo.agregar_caracter("-")
                    elif tecla.name == "period":
                        campo_activo.agregar_caracter(".")
                elif isinstance(tecla, str):
                    # Manejar teclas como strings
                    if tecla.isdigit():
                        campo_activo.agregar_caracter(tecla)
                    elif tecla == "-":
                        campo_activo.agregar_caracter("-")
                    elif tecla == ".":
                        campo_activo.agregar_caracter(".")

        # Teclas especiales
        if tecla == "enter":
            return "iniciar_juego"

        return None
