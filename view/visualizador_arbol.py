"""
Utilidad para visualizar gráficamente el árbol AVL.
Responsabilidad: Renderizar la estructura del árbol de forma comprensible.
"""

import pygame
import math
from typing import Optional, List, Tuple


class VisualizadorArbol:
    """
    Herramienta para visualizar gráficamente un árbol AVL.
    """

    def __init__(self, ancho=400, alto=400):
        """
        Inicializa el visualizador del árbol.

        Args:
            ancho (int): Ancho del área de visualización
            alto (int): Alto del área de visualización
        """
        self.ancho = ancho
        self.alto = alto

        # Configuración visual
        self.radio_nodo = 25
        self.espaciado_nivel = 60
        self.color_nodo = (100, 150, 255)
        self.color_nodo_seleccionado = (255, 100, 100)
        self.color_conexion = (50, 50, 50)
        self.color_texto = (255, 255, 255)
        self.color_recorrido = (255, 255, 0)

        # Estado del visualizador
        self.nodo_seleccionado = None
        self.recorrido_actual = []
        self.paso_recorrido_actual = 0
        self.animando_recorrido = False

    def dibujar_arbol(self, screen, arbol_avl, x_offset=0, y_offset=0):
        """
        Dibuja el árbol AVL completo.

        Args:
            screen: Superficie de pygame donde dibujar
            arbol_avl: Árbol AVL a visualizar
            x_offset (int): Desplazamiento X
            y_offset (int): Desplazamiento Y
        """
        if arbol_avl.raiz is None:
            # Dibujar mensaje de árbol vacío
            screen.draw.text(
                "Arbol vacio",
                (x_offset + self.ancho // 2 - 50, y_offset + self.alto // 2),
                fontsize=20,
                color=self.color_texto
            )
            return

        # Calcular posiciones de todos los nodos
        posiciones = self.calcular_posiciones_nodos(arbol_avl)
        
        # Dibujar conexiones primero (para que queden detrás de los nodos)
        self._dibujar_conexiones(screen, arbol_avl.raiz, posiciones, x_offset, y_offset)
        
        # Dibujar nodos
        self._dibujar_nodos(screen, arbol_avl.raiz, posiciones, x_offset, y_offset)

    def _dibujar_nodo_recursivo(self, screen, nodo, x, y, nivel, x_offset, y_offset):
        """
        Dibuja un nodo y sus hijos recursivamente.

        Args:
            screen: Superficie donde dibujar
            nodo: Nodo actual a dibujar
            x, y (int): Posición del nodo
            nivel (int): Nivel actual en el árbol
            x_offset, y_offset (int): Desplazamientos
        """
        pass

    def dibujar_nodo(self, screen, nodo, x, y, seleccionado=False, en_recorrido=False):
        """
        Dibuja un nodo individual.

        Args:
            screen: Superficie donde dibujar
            nodo: Nodo a dibujar
            x, y (int): Posición del nodo
            seleccionado (bool): Si el nodo está seleccionado
            en_recorrido (bool): Si el nodo está siendo recorrido
        """
        # Determinar color del nodo
        if seleccionado:
            color = self.color_nodo_seleccionado
        elif en_recorrido:
            color = self.color_recorrido
        else:
            color = self.color_nodo
        
        # Dibujar círculo del nodo
        screen.draw.filled_circle((x, y), self.radio_nodo, color)
        screen.draw.circle((x, y), self.radio_nodo, (255, 255, 255))  # Borde blanco
        
        # Dibujar texto del nodo
        self.dibujar_texto_nodo(screen, nodo, x, y)

    def dibujar_conexion(self, screen, x1, y1, x2, y2):
        """
        Dibuja una línea de conexión entre dos nodos.

        Args:
            screen: Superficie donde dibujar
            x1, y1 (int): Posición del nodo padre
            x2, y2 (int): Posición del nodo hijo
        """
        pass

    def dibujar_texto_nodo(self, screen, nodo, x, y):
        """
        Dibuja el texto dentro de un nodo (coordenadas del obstáculo).

        Args:
            screen: Superficie donde dibujar
            nodo: Nodo con la información a mostrar
            x, y (int): Posición del texto
        """
        # Obtener coordenadas del obstáculo
        obstaculo = nodo.obstaculo
        texto = f"({obstaculo.x},{obstaculo.y})"
        
        # Dibujar texto centrado en el nodo
        screen.draw.text(
            texto,
            (x - 20, y - 8),
            fontsize=12,
            color=self.color_texto
        )
        
        # Dibujar factor de balance
        factor_balance = nodo.obtener_factor_balance()
        color_balance = (255, 255, 255)  # Blanco por defecto
        
        # Color según factor de balance
        if factor_balance > 1 or factor_balance < -1:
            color_balance = (255, 50, 50)  # Rojo si está desbalanceado
        elif factor_balance == 0:
            color_balance = (50, 255, 50)  # Verde si está perfectamente balanceado
        else:
            color_balance = (255, 255, 50)  # Amarillo para balance +/-1
            
        screen.draw.text(
            f"FB:{factor_balance}",
            (x - 15, y + 5),
            fontsize=10,
            color=color_balance
        )

    def calcular_posiciones_nodos(self, arbol_avl):
        """
        Calcula las posiciones de todos los nodos para el dibujo.

        Args:
            arbol_avl: Árbol AVL a analizar

        Returns:
            dict: Diccionario con nodo como clave y (x, y) como valor
        """
        posiciones = {}
        if arbol_avl.raiz is None:
            return posiciones
        
        # Calcular altura del árbol
        altura = self._calcular_altura(arbol_avl.raiz)
        
        # Calcular posiciones recursivamente
        self._calcular_posicion_recursiva(arbol_avl.raiz, 0, 0, posiciones, altura)
        
        return posiciones
    
    def _calcular_altura(self, nodo):
        """Calcula la altura de un nodo."""
        if nodo is None:
            return 0
        return 1 + max(self._calcular_altura(nodo.izquierdo), self._calcular_altura(nodo.derecho))
    
    def _calcular_posicion_recursiva(self, nodo, nivel, indice, posiciones, altura_total):
        """Calcula recursivamente la posición de cada nodo."""
        if nodo is None:
            return
        
        # Usar un algoritmo más simple para posicionamiento
        # Calcular posición X basada en el índice en el nivel
        nodos_en_nivel = 2 ** nivel
        if nodos_en_nivel > 0:
            ancho_nivel = self.ancho - 100  # Margen
            x = 50 + (indice * ancho_nivel) // nodos_en_nivel + (ancho_nivel // nodos_en_nivel) // 2
        else:
            x = self.ancho // 2
        
        # Calcular posición Y basada en el nivel
        y = 50 + nivel * self.espaciado_nivel
        
        posiciones[nodo] = (x, y)
        
        # Calcular posiciones de los hijos
        if nodo.izquierdo is not None:
            self._calcular_posicion_recursiva(nodo.izquierdo, nivel + 1, indice * 2, posiciones, altura_total)
        if nodo.derecho is not None:
            self._calcular_posicion_recursiva(nodo.derecho, nivel + 1, indice * 2 + 1, posiciones, altura_total)

    def _dibujar_conexiones(self, screen, nodo, posiciones, x_offset, y_offset):
        """Dibuja las conexiones entre nodos."""
        if nodo is None:
            return
        
        nodo_x, nodo_y = posiciones[nodo]
        
        # Dibujar conexión al hijo izquierdo
        if nodo.izquierdo is not None:
            hijo_x, hijo_y = posiciones[nodo.izquierdo]
            screen.draw.line(
                (x_offset + nodo_x, y_offset + nodo_y),
                (x_offset + hijo_x, y_offset + hijo_y),
                self.color_conexion
            )
            self._dibujar_conexiones(screen, nodo.izquierdo, posiciones, x_offset, y_offset)
        
        # Dibujar conexión al hijo derecho
        if nodo.derecho is not None:
            hijo_x, hijo_y = posiciones[nodo.derecho]
            screen.draw.line(
                (x_offset + nodo_x, y_offset + nodo_y),
                (x_offset + hijo_x, y_offset + hijo_y),
                self.color_conexion
            )
            self._dibujar_conexiones(screen, nodo.derecho, posiciones, x_offset, y_offset)
    
    def _dibujar_nodos(self, screen, nodo, posiciones, x_offset, y_offset):
        """Dibuja todos los nodos del árbol."""
        if nodo is None:
            return
        
        nodo_x, nodo_y = posiciones[nodo]
        
        # Determinar si el nodo está en el recorrido actual
        # Comparar por coordenadas del obstáculo
        en_recorrido = False
        if self.recorrido_actual:
            for obstaculo in self.recorrido_actual:
                if (nodo.obstaculo.x == obstaculo.x and nodo.obstaculo.y == obstaculo.y):
                    en_recorrido = True
                    break
        
        seleccionado = nodo == self.nodo_seleccionado
        
        # Dibujar el nodo
        self.dibujar_nodo(screen, nodo, x_offset + nodo_x, y_offset + nodo_y, seleccionado, en_recorrido)
        
        # Dibujar nodos hijos recursivamente
        self._dibujar_nodos(screen, nodo.izquierdo, posiciones, x_offset, y_offset)
        self._dibujar_nodos(screen, nodo.derecho, posiciones, x_offset, y_offset)

    def obtener_nodo_en_posicion(self, arbol_avl, x, y):
        """
        Obtiene el nodo que está en la posición especificada.

        Args:
            arbol_avl: Árbol donde buscar
            x, y (int): Coordenadas a verificar

        Returns:
            Optional: Nodo en esa posición o None
        """
        if arbol_avl.raiz is None:
            return None
        
        posiciones = self.calcular_posiciones_nodos(arbol_avl)
        
        # Buscar el nodo más cercano al punto
        for nodo, (nodo_x, nodo_y) in posiciones.items():
            distancia = ((x - nodo_x) ** 2 + (y - nodo_y) ** 2) ** 0.5
            if distancia <= self.radio_nodo:
                return nodo
        
        return None

    def iniciar_animacion_recorrido(self, recorrido):
        """
        Inicia la animación de un recorrido del árbol.

        Args:
            recorrido (List): Lista de obstáculos en orden de recorrido
        """
        print(f"Iniciando animación con {len(recorrido)} obstáculos")
        self.recorrido_actual = recorrido
        self.paso_recorrido_actual = 0
        self.animando_recorrido = True

    def iniciar_recorrido_anchura(self, arbol_avl):
        """
        Inicia la animación de un recorrido en anchura (BFS).
        
        Args:
            arbol_avl: Árbol AVL a recorrer
        """
        recorrido = arbol_avl.recorrido_en_anchura()
        print(f"Iniciando recorrido en anchura con {len(recorrido)} nodos")
        self.iniciar_animacion_recorrido(recorrido)
        
    def iniciar_recorrido_profundidad(self, arbol_avl):
        """
        Inicia la animación de un recorrido en profundidad (DFS).
        
        Args:
            arbol_avl: Árbol AVL a recorrer
        """
        recorrido = arbol_avl.recorrido_en_profundidad()
        print(f"Iniciando recorrido en profundidad con {len(recorrido)} nodos")
        self.iniciar_animacion_recorrido(recorrido)

    def actualizar_animacion_recorrido(self):
        """
        Actualiza el estado de la animación del recorrido.

        Returns:
            bool: True si la animación continúa, False si terminó
        """
        if not self.animando_recorrido or not self.recorrido_actual:
            return False
            
        # Actualizar el paso actual
        self.paso_recorrido_actual += 1
        
        # Verificar si la animación ha terminado
        if self.paso_recorrido_actual >= len(self.recorrido_actual):
            self.animando_recorrido = False
            return False
            
        return True

    def dibujar_informacion_nodo(self, screen, nodo, x, y):
        """
        Dibuja información adicional sobre un nodo (altura, balance).

        Args:
            screen: Superficie donde dibujar
            nodo: Nodo con la información
            x, y (int): Posición donde dibujar la información
        """
        pass

    def dibujar_leyenda(self, screen, x, y):
        """
        Dibuja una leyenda explicando los colores y símbolos.

        Args:
            screen: Superficie donde dibujar
            x, y (int): Posición de la leyenda
        """
        pass

    def establecer_nodo_seleccionado(self, nodo):
        """
        Establece qué nodo está seleccionado.

        Args:
            nodo: Nodo a seleccionar (None para deseleccionar)
        """
        self.nodo_seleccionado = nodo

    def limpiar_seleccion(self):
        """
        Limpia la selección actual.
        """
        self.nodo_seleccionado = None
        self.recorrido_actual = []
        self.animando_recorrido = False

    def obtener_dimensiones_arbol(self, arbol_avl):
        """
        Calcula las dimensiones necesarias para dibujar el árbol.

        Args:
            arbol_avl: Árbol a analizar

        Returns:
            Tuple[int, int]: Ancho y alto necesarios
        """
        pass
