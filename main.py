# -*- coding: utf-8 -*-
"""
Punto de entrada principal del juego de carrito con obstaculos dinamicos.
Configurado para ejecutarse con pygame-zero.
"""


import pygame
from pgzero.constants import keys
from logic.gestor_juego import GestorJuego, EstadoJuego
from view.pantalla_configuracion import PantallaConfiguracion
from view.pantalla_juego import PantallaJuego

# Configuración de pygame-zero
WIDTH = 800
HEIGHT = 600
TITLE = "Carrito con Obstaculos Dinamicos - Arbol AVL"

# Centrar la ventana
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Instancias globales para pygame-zero
gestor_juego = None
pantalla_configuracion = None
pantalla_juego = None


def inicializar_juego():
    """
    Inicializa todos los componentes del juego.
    """
    global gestor_juego, pantalla_configuracion, pantalla_juego

    # Crear el gestor principal
    gestor_juego = GestorJuego()
    gestor_juego.cargar_configuracion()

    # Crear las pantallas
    pantalla_configuracion = PantallaConfiguracion(WIDTH, HEIGHT)
    pantalla_configuracion.gestor_juego = gestor_juego

    pantalla_juego = PantallaJuego(WIDTH, HEIGHT)
    pantalla_juego.gestor_juego = gestor_juego

    # Cambiar directamente a configuracion
    gestor_juego.cambiar_estado(EstadoJuego.CONFIGURACION)

    print("Juego inicializado correctamente")
    print("Estado inicial: Configuracion")
    print("Arbol AVL listo para recibir obstaculos")


def draw():
    """
    Función de dibujo principal llamada por pygame-zero.
    """
    if gestor_juego is None:
        inicializar_juego()
        return

    # Limpiar pantalla
    screen.fill((50, 50, 100))  # Azul oscuro

    # Dibujar según el estado actual
    if gestor_juego.estado_actual == EstadoJuego.CONFIGURACION:
        pantalla_configuracion.dibujar(screen)
    elif gestor_juego.estado_actual == EstadoJuego.JUGANDO:
        pantalla_juego.dibujar(screen)
    elif gestor_juego.estado_actual == EstadoJuego.PAUSADO:
        pantalla_juego.dibujar(screen)
        # Dibujar overlay de pausa
        # Crear overlay semitransparente
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negro con transparencia
        screen.blit(overlay, (0, 0))
        
        # Texto de PAUSA
        screen.draw.text(
            "PAUSA",
            center=(WIDTH//2, HEIGHT//2 - 50),
            fontsize=48,
            color="white"
        )
        
        # Instrucciones
        screen.draw.text(
            "Presiona P para continuar",
            center=(WIDTH//2, HEIGHT//2 + 20),
            fontsize=20,
            color="yellow"
        )
    elif gestor_juego.estado_actual == EstadoJuego.JUEGO_TERMINADO:
        pantalla_juego.dibujar(screen)
        # Dibujar overlay de fin de juego
        # Crear overlay semitransparente
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Negro con transparencia más oscura
        screen.blit(overlay, (0, 0))
        
        # Obtener estadísticas del juego
        stats = gestor_juego.obtener_estadisticas()
        
        # Título de FIN DE JUEGO
        screen.draw.text(
            "JUEGO TERMINADO",
            center=(WIDTH//2, HEIGHT//2 - 80),
            fontsize=40,
            color="red"
        )
        
        # Mostrar razón del fin del juego
        if gestor_juego.carrito and not gestor_juego.carrito.esta_vivo():
            reason = "Sin energía"
        elif gestor_juego.distancia_recorrida >= gestor_juego.distancia_total:
            reason = "¡Meta alcanzada!"
        else:
            reason = "Juego terminado"
            
        screen.draw.text(
            reason,
            center=(WIDTH//2, HEIGHT//2 - 40),
            fontsize=24,
            color="yellow"
        )
        
        # Estadísticas finales
        screen.draw.text(
            f"Puntuación final: {int(stats['puntuacion'])}",
            center=(WIDTH//2, HEIGHT//2 - 5),
            fontsize=20,
            color="white"
        )
        
        screen.draw.text(
            f"Distancia recorrida: {int(stats['distancia_recorrida'])} m",
            center=(WIDTH//2, HEIGHT//2 + 20),
            fontsize=20,
            color="white"
        )
        
        screen.draw.text(
            f"Tiempo jugado: {stats['tiempo_juego']:.1f} seg",
            center=(WIDTH//2, HEIGHT//2 + 45),
            fontsize=20,
            color="white"
        )
        
        # Instrucciones para reiniciar
        screen.draw.text(
            "Presiona R para reiniciar",
            center=(WIDTH//2, HEIGHT//2 + 80),
            fontsize=18,
            color="lime"
        )
        
        screen.draw.text(
            "Presiona ESC para configurar",
            center=(WIDTH//2, HEIGHT//2 + 105),
            fontsize=18,
            color="cyan"
        )

    # Dibujar información de debug (temporal)
    screen.draw.text(
        f"Estado: {gestor_juego.estado_actual.value}",
        (10, 10),
        fontsize=20,
        color="white",
    )

    if gestor_juego.arbol_obstaculos:
        screen.draw.text(
            f"Obstáculos en árbol: {gestor_juego.arbol_obstaculos.obtener_total_obstaculos()}",
            (10, 35),
            fontsize=16,
            color="white",
        )


def update(dt):
    """
    Función de actualización llamada por pygame-zero.

    Args:
        dt (float): Delta time desde el último frame
    """
    if gestor_juego is None:
        return

    # Actualizar el gestor principal
    gestor_juego.actualizar(dt)


def on_key_down(key):
    """
    Maneja las teclas presionadas.

    Args:
        key: Tecla presionada
    """
    if gestor_juego is None:
        return

    # Teclas globales
    if key == keys.ESCAPE:
        # Cambiar entre configuración y juego
        if gestor_juego.estado_actual == EstadoJuego.CONFIGURACION:
            print("Saliendo del juego...")
            exit()
        else:
            gestor_juego.cambiar_estado(EstadoJuego.CONFIGURACION)

    # Delegar a la pantalla actual
    if gestor_juego.estado_actual == EstadoJuego.CONFIGURACION:
        resultado = pantalla_configuracion.manejar_tecla(key)
        print(f"Resultado de la tecla en configuración: {resultado}")
        if resultado == "iniciar_juego":
            print("¡Iniciando juego desde teclado!")
            gestor_juego.cambiar_estado(EstadoJuego.JUGANDO)
            gestor_juego.inicializar_juego()

    elif gestor_juego.estado_actual == EstadoJuego.JUGANDO:
        # Controles del juego (corregidos para no estar invertidos)
        if key == keys.UP:
            gestor_juego.carrito.mover_abajo()
        elif key == keys.DOWN:
            gestor_juego.carrito.mover_arriba()
        elif key == keys.SPACE:
            gestor_juego.carrito.saltar()
        elif key == keys.P:
            gestor_juego.pausar_juego()
        elif key == keys.T:
            pantalla_juego.mostrar_arbol = not pantalla_juego.mostrar_arbol
        elif key == keys.H:  # Mostrar/ocultar hitboxes (modo debug)
            pantalla_juego.mostrar_hitbox = not pantalla_juego.mostrar_hitbox
        elif key == keys.B:  # Mostrar recorrido en anchura
            if pantalla_juego.visualizador_arbol and pantalla_juego.mostrar_arbol:
                pantalla_juego.visualizador_arbol.iniciar_recorrido_anchura(gestor_juego.arbol_obstaculos)
        elif key == keys.D:  # Mostrar recorrido en profundidad
            if pantalla_juego.visualizador_arbol and pantalla_juego.mostrar_arbol:
                pantalla_juego.visualizador_arbol.iniciar_recorrido_profundidad(gestor_juego.arbol_obstaculos)

    elif gestor_juego.estado_actual == EstadoJuego.PAUSADO:
        # Controles cuando el juego está pausado
        if key == keys.P:
            gestor_juego.pausar_juego()  # Despausa el juego
        elif key == keys.T:
            pantalla_juego.mostrar_arbol = not pantalla_juego.mostrar_arbol
        elif key == keys.H:  # Mostrar/ocultar hitboxes (modo debug)
            pantalla_juego.mostrar_hitbox = not pantalla_juego.mostrar_hitbox
    
    elif gestor_juego.estado_actual == EstadoJuego.JUEGO_TERMINADO:
        # Controles cuando el juego ha terminado
        if key == keys.R:
            print("¡Reiniciando juego!")
            gestor_juego.reiniciar_juego()
        elif key == keys.SPACE:
            print("¡Reiniciando juego con ESPACIO!")
            gestor_juego.reiniciar_juego()
        # ESC ya está manejado en las teclas globales


def on_mouse_down(pos):
    """
    Maneja los clics del mouse.

    Args:
        pos: Posición del clic
    """
    if gestor_juego is None:
        return

    # Delegar a la pantalla actual
    if gestor_juego.estado_actual == EstadoJuego.CONFIGURACION:
        resultado = pantalla_configuracion.manejar_clic_mouse(pos)
        print(f"Resultado del clic en configuración: {resultado}")
        if resultado == "iniciar_juego":
            print("¡Iniciando juego desde clic del mouse!")
            gestor_juego.cambiar_estado(EstadoJuego.JUGANDO)
            gestor_juego.inicializar_juego()


def main():
    """
    Función principal para ejecutar sin pygame-zero.
    """
    print("Iniciando Juego de Carrito con Obstaculos Dinamicos")
    print("Estructura de datos: Arbol AVL")
    print("Para ejecutar: uv run pgzrun main.py")
    print("O alternativamente: uv run python main.py")


if __name__ == "__main__":
    main()
