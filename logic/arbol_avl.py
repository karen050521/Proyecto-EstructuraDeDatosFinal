"""
Implementación del árbol AVL para gestionar obstáculos de forma eficiente.
Responsabilidad: Mantener obstáculos ordenados y balanceados para consultas rápidas.
"""

from .nodo_avl import NodoAVL
from .obstaculo import Obstaculo
from typing import List, Optional


class ArbolAVL:
    """
    Árbol AVL que almacena obstáculos ordenados por coordenadas (x, y).
    Permite inserción, eliminación y búsquedas por rango eficientes.
    """

    def __init__(self) -> None:
        """Inicializa un árbol AVL vacío."""
        self.raiz: Optional[NodoAVL] = None
        self.total_obstaculos: int = 0

    def insertar(self, obstaculo: Obstaculo) -> bool:
        """
        Inserta un obstáculo en el árbol manteniendo el balance AVL.

        Args:
            obstaculo (Obstaculo): Obstáculo a insertar

        Returns:
            bool: True si se insertó correctamente, False si ya existía
        """
        if self.raiz is None:
            self.raiz = NodoAVL(obstaculo)
            self.total_obstaculos += 1
            return True

        # Verificar si ya existe
        if self._buscar_obstaculo(self.raiz, obstaculo) is not None:
            return False

        self.raiz = self._insertar_recursivo(self.raiz, obstaculo)
        self.total_obstaculos += 1
        return True

    def _insertar_recursivo(
        self, nodo: Optional[NodoAVL], obstaculo: Obstaculo
    ) -> Optional[NodoAVL]:
        """
        Función recursiva para insertar un obstáculo.

        Args:
            nodo (NodoAVL): Nodo actual
            obstaculo (Obstaculo): Obstáculo a insertar

        Returns:
            NodoAVL: Nuevo nodo raíz del subárbol
        """
        if nodo is None:
            return NodoAVL(obstaculo)

        if nodo.es_mayor_que(obstaculo):
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, obstaculo)
        else:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, obstaculo)

        # Actualizar altura y balancear
        nodo.actualizar_altura()
        return self.balancear(nodo)

    def _buscar_obstaculo(
        self, nodo: Optional[NodoAVL], obstaculo: Obstaculo
    ) -> Optional[NodoAVL]:
        """
        Busca un obstáculo específico en el árbol.

        Args:
            nodo (Optional[NodoAVL]): Nodo actual
            obstaculo (Obstaculo): Obstáculo a buscar

        Returns:
            Optional[NodoAVL]: Nodo que contiene el obstáculo, None si no existe
        """
        if nodo is None:
            return None

        if nodo.es_igual_a(obstaculo):
            return nodo
        elif nodo.es_mayor_que(obstaculo):
            return self._buscar_obstaculo(nodo.izquierdo, obstaculo)
        else:
            return self._buscar_obstaculo(nodo.derecho, obstaculo)

    def _encontrar_minimo(self, nodo: NodoAVL) -> NodoAVL:
        """
        Encuentra el nodo con el valor mínimo en un subárbol.

        Args:
            nodo (NodoAVL): Nodo raíz del subárbol

        Returns:
            NodoAVL: Nodo con el valor mínimo
        """
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def eliminar(self, obstaculo: Obstaculo) -> bool:
        """
        Elimina un obstáculo del árbol manteniendo el balance AVL.

        Args:
            obstaculo (Obstaculo): Obstáculo a eliminar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        if self.raiz is None:
            return False

        # Verificar si existe
        if self._buscar_obstaculo(self.raiz, obstaculo) is None:
            return False

        self.raiz = self._eliminar_recursivo(self.raiz, obstaculo)
        self.total_obstaculos -= 1
        return True

    def _eliminar_recursivo(
        self, nodo: Optional[NodoAVL], obstaculo: Obstaculo
    ) -> Optional[NodoAVL]:
        """
        Función recursiva para eliminar un obstáculo.

        Args:
            nodo (NodoAVL): Nodo actual
            obstaculo (Obstaculo): Obstáculo a eliminar

        Returns:
            NodoAVL: Nuevo nodo raíz del subárbol
        """
        if nodo is None:
            return None

        if nodo.es_igual_a(obstaculo):
            # Caso 1: Nodo hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: Un solo hijo
            elif nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: Dos hijos - encontrar sucesor in-order
            else:
                sucesor = self._encontrar_minimo(nodo.derecho)
                nodo.obstaculo = sucesor.obstaculo
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.obstaculo)
        elif nodo.es_mayor_que(obstaculo):
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, obstaculo)
        else:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, obstaculo)

        # Actualizar altura y balancear
        nodo.actualizar_altura()
        return self.balancear(nodo)

    def buscar_en_rango(
        self, x_min: int, x_max: int, y_min: int, y_max: int
    ) -> List[Obstaculo]:
        """
        Busca todos los obstáculos dentro del rango especificado.
        Esta es la función clave para la optimización del juego.

        Args:
            x_min (int): Límite inferior X
            x_max (int): Límite superior X
            y_min (int): Límite inferior Y
            y_max (int): Límite superior Y

        Returns:
            List[Obstaculo]: Lista de obstáculos en el rango
        """
        resultado = []
        self._buscar_rango_recursivo(self.raiz, x_min, x_max, y_min, y_max, resultado)
        return resultado

    def _buscar_rango_recursivo(
        self,
        nodo: Optional[NodoAVL],
        x_min: int,
        x_max: int,
        y_min: int,
        y_max: int,
        resultado: List[Obstaculo],
    ) -> None:
        """
        Función recursiva para búsqueda por rango.

        Args:
            nodo (NodoAVL): Nodo actual
            x_min, x_max, y_min, y_max: Límites del rango
            resultado (List[Obstaculo]): Lista donde acumular resultados
        """
        if nodo is None:
            return

        obstaculo = nodo.obstaculo

        # Verificar si el obstáculo está en el rango
        if obstaculo.esta_en_rango(x_min, x_max, y_min, y_max):
            resultado.append(obstaculo)

        # Decidir qué subárboles explorar basándose en la posición del nodo
        if (
            obstaculo.x >= x_min
        ):  # Puede haber obstáculos en el rango en el subárbol izquierdo
            self._buscar_rango_recursivo(
                nodo.izquierdo, x_min, x_max, y_min, y_max, resultado
            )

        if (
            obstaculo.x <= x_max
        ):  # Puede haber obstáculos en el rango en el subárbol derecho
            self._buscar_rango_recursivo(
                nodo.derecho, x_min, x_max, y_min, y_max, resultado
            )

    def recorrido_en_anchura(self) -> List[Obstaculo]:
        """
        Realiza un recorrido por anchura (BFS) del árbol.

        Returns:
            List[Obstaculo]: Obstáculos en orden de anchura
        """
        if self.raiz is None:
            return []

        resultado = []
        cola = [self.raiz]

        while cola:
            nodo = cola.pop(0)
            resultado.append(nodo.obstaculo)

            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.derecho:
                cola.append(nodo.derecho)

        return resultado

    def recorrido_en_profundidad(self) -> List[Obstaculo]:
        """
        Realiza un recorrido en profundidad (in-order) del árbol.

        Returns:
            List[Obstaculo]: Obstáculos en orden in-order
        """
        resultado: List[Obstaculo] = []
        self._recorrido_inorder_recursivo(self.raiz, resultado)
        return resultado

    def _recorrido_inorder_recursivo(
        self, nodo: Optional[NodoAVL], resultado: List[Obstaculo]
    ) -> None:
        """
        Función recursiva para recorrido in-order.

        Args:
            nodo (Optional[NodoAVL]): Nodo actual
            resultado (List[Obstaculo]): Lista donde acumular resultados
        """
        if nodo is not None:
            self._recorrido_inorder_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.obstaculo)
            self._recorrido_inorder_recursivo(nodo.derecho, resultado)

    def obtener_altura(self, nodo: Optional[NodoAVL]) -> int:
        """
        Obtiene la altura de un nodo (0 si es None).

        Args:
            nodo (Optional[NodoAVL]): Nodo a consultar

        Returns:
            int: Altura del nodo
        """
        return nodo.altura if nodo is not None else 0

    def rotar_derecha(self, nodo: NodoAVL) -> NodoAVL:
        """
        Realiza una rotación a la derecha para balancear el árbol.

        Args:
            nodo (NodoAVL): Nodo desbalanceado

        Returns:
            NodoAVL: Nueva raíz del subárbol rotado
        """
        hijo_izquierdo = nodo.izquierdo
        nodo.izquierdo = hijo_izquierdo.derecho
        hijo_izquierdo.derecho = nodo

        # Actualizar alturas
        nodo.actualizar_altura()
        hijo_izquierdo.actualizar_altura()

        return hijo_izquierdo

    def rotar_izquierda(self, nodo: NodoAVL) -> NodoAVL:
        """
        Realiza una rotación a la izquierda para balancear el árbol.

        Args:
            nodo (NodoAVL): Nodo desbalanceado

        Returns:
            NodoAVL: Nueva raíz del subárbol rotado
        """
        hijo_derecho = nodo.derecho
        nodo.derecho = hijo_derecho.izquierdo
        hijo_derecho.izquierdo = nodo

        # Actualizar alturas
        nodo.actualizar_altura()
        hijo_derecho.actualizar_altura()

        return hijo_derecho

    def balancear(self, nodo: NodoAVL) -> NodoAVL:
        """
        Balancea un nodo aplicando las rotaciones necesarias.

        Args:
            nodo (NodoAVL): Nodo a balancear

        Returns:
            NodoAVL: Nodo balanceado
        """
        factor_balance = nodo.obtener_factor_balance()

        # Rotación simple a la derecha
        if (
            factor_balance > 1
            and nodo.izquierdo
            and nodo.izquierdo.obtener_factor_balance() >= 0
        ):
            return self.rotar_derecha(nodo)

        # Rotación simple a la izquierda
        if (
            factor_balance < -1
            and nodo.derecho
            and nodo.derecho.obtener_factor_balance() <= 0
        ):
            return self.rotar_izquierda(nodo)

        # Rotación doble derecha-izquierda
        if (
            factor_balance > 1
            and nodo.izquierdo
            and nodo.izquierdo.obtener_factor_balance() < 0
        ):
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        # Rotación doble izquierda-derecha
        if (
            factor_balance < -1
            and nodo.derecho
            and nodo.derecho.obtener_factor_balance() > 0
        ):
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def esta_vacio(self) -> bool:
        """
        Verifica si el árbol está vacío.

        Returns:
            bool: True si no tiene nodos
        """
        return self.raiz is None

    def obtener_total_obstaculos(self) -> int:
        """
        Obtiene el número total de obstáculos en el árbol.

        Returns:
            int: Cantidad de obstáculos
        """
        return self.total_obstaculos

    def limpiar(self) -> None:
        """Elimina todos los obstáculos del árbol."""
        self.raiz = None
        self.total_obstaculos = 0
