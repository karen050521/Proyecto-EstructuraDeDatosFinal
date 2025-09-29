"""
Nodo para el árbol AVL que almacena obstáculos por coordenadas.
Responsabilidad: Representar un nodo individual del árbol con balanceamiento automático.
"""

from typing import Optional
from .obstaculo import Obstaculo


class NodoAVL:
    """
    Nodo individual del árbol AVL que contiene un obstáculo.
    Mantiene referencias a hijos, altura y factor de balance.
    """

    def __init__(self, obstaculo: Obstaculo) -> None:
        """
        Inicializa un nodo AVL con un obstáculo.

        Args:
            obstaculo (Obstaculo): Obstáculo a almacenar en este nodo
        """
        self.obstaculo: Obstaculo = obstaculo
        self.izquierdo: Optional["NodoAVL"] = None
        self.derecho: Optional["NodoAVL"] = None
        self.altura: int = 1

    def obtener_factor_balance(self) -> int:
        """
        Calcula el factor de balance del nodo.

        Returns:
            int: Diferencia entre altura del subárbol izquierdo y derecho
        """
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        return altura_izq - altura_der

    def actualizar_altura(self) -> None:
        """
        Actualiza la altura del nodo basándose en las alturas de sus hijos.
        """
        altura_izq = self.izquierdo.altura if self.izquierdo else 0
        altura_der = self.derecho.altura if self.derecho else 0
        self.altura = 1 + max(altura_izq, altura_der)

    def es_mayor_que(self, otro_obstaculo: Obstaculo) -> bool:
        """
        Compara este nodo con otro obstáculo según las reglas de ordenamiento.
        Primero por coordenada X, luego por Y en caso de empate.

        Args:
            otro_obstaculo (Obstaculo): Obstáculo a comparar

        Returns:
            bool: True si este nodo debe ir a la derecha del otro
        """
        if self.obstaculo.x > otro_obstaculo.x:
            return True
        elif self.obstaculo.x == otro_obstaculo.x:
            return self.obstaculo.y > otro_obstaculo.y
        return False

    def es_igual_a(self, otro_obstaculo: Obstaculo) -> bool:
        """
        Verifica si este nodo contiene el mismo obstáculo (mismas coordenadas).

        Args:
            otro_obstaculo (Obstaculo): Obstáculo a comparar

        Returns:
            bool: True si tienen las mismas coordenadas
        """
        return (
            self.obstaculo.x == otro_obstaculo.x
            and self.obstaculo.y == otro_obstaculo.y
        )

    def __str__(self) -> str:
        """
        Representación en string del nodo para debugging.

        Returns:
            str: Información del obstáculo contenido
        """
        return f"NodoAVL({self.obstaculo}, altura: {self.altura}, balance: {self.obtener_factor_balance()})"
