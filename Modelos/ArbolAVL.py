from Modelos.Nodo import Nodo
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    #################################### Inserción #################################################
    def insertar(self, valor):
        self.raiz = self.insertar_recursivo(self.raiz, valor)

    def insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.valor:
            nodo.izquierda = self.insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self.insertar_recursivo(nodo.derecha, valor)
        else:
            # Valor ya existe en el árbol, podemos manejarlo como quieras
            return nodo

        # Actualizar la altura del nodo actual
        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

        # Obtener el factor de balance del nodo
        balance = self.factor_balance(nodo)

        # Caso 1: rotación simple a la derecha
        if balance > 1 and valor < nodo.izquierda.valor:
            return self.rotacion_derecha(nodo)

        # Caso 2: rotación simple a la izquierda
        if balance < -1 and valor > nodo.derecha.valor:
            return self.rotacion_izquierda(nodo)

        # Caso 3: rotación doble a la derecha
        if balance > 1 and valor > nodo.izquierda.valor:
            nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        # Caso 4: rotación doble a la izquierda
        if balance < -1 and valor < nodo.derecha.valor:
            nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self.altura(z.izquierda), self.altura(z.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self.altura(z.izquierda), self.altura(z.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    #################################### Búsqueda #################################################
    def buscar(self, valor):
        return self.buscar_recursivo(self.raiz, valor)

    def buscar_recursivo(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo is not None
        if valor < nodo.valor:
            return self.buscar_recursivo(nodo.izquierda, valor)
        else:
            return self.buscar_recursivo(nodo.derecha, valor)

    #################################### Recorridos #################################################
    def preorden(self):
        return self._preorden_recursivo(self.raiz)

    def _preorden_recursivo(self, nodo):
        if nodo is not None:
            print(nodo.valor, end=" ")
            self._preorden_recursivo(nodo.izquierda)
            self._preorden_recursivo(nodo.derecha)

    def inorden(self):
        return self._inorden_recursivo(self.raiz)

    def _inorden_recursivo(self, nodo):
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierda)
            print(nodo.valor, end=" ")
            self._inorden_recursivo(nodo.derecha)

    def postorden(self):
        return self._postorden_recursivo(self.raiz)

    def _postorden_recursivo(self, nodo):
        if nodo is not None:
            self._postorden_recursivo(nodo.izquierda)
            self._postorden_recursivo(nodo.derecha)
            print(nodo.valor, end=" ")

    #################### Eliminación ##################################
    def eliminar(self, valor):
        self.raiz = self.eliminar_recursivo(self.raiz, valor)

    def eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self.eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self.eliminar_recursivo(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                temp = nodo.derecha
                nodo = None
                return temp
            elif nodo.derecha is None:
                temp = nodo.izquierda
                nodo = None
                return temp

            temp = self.obtener_sucesor(nodo.derecha)
            nodo.valor = temp.valor
            nodo.derecha = self.eliminar_recursivo(nodo.derecha, temp.valor)

        if nodo is None:
            return nodo

        nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))
        balance = self.factor_balance(nodo)

        if balance > 1 and self.factor_balance(nodo.izquierda) >= 0:
            return self.rotacion_derecha(nodo)

        if balance < -1 and self.factor_balance(nodo.derecha) <= 0:
            return self.rotacion_izquierda(nodo)

        if balance > 1 and self.factor_balance(nodo.izquierda) < 0:
            nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
            return self.rotacion_derecha(nodo)

        if balance < -1 and self.factor_balance(nodo.derecha) > 0:
            nodo.derecha = self.rotacion_derecha(nodo.derecha)
            return self.rotacion_izquierda(nodo)

        return nodo

    def obtener_sucesor(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    ############### Imprimir ######################
    def dibujar_arbol(self, nodo, x, y, espaciado, ax):
        if nodo is None:
            return

        radio = 0.2  # Tamaño del círculo

        if nodo.izquierda:
            ax.plot([x, x - espaciado], [y, y - 1], '-k')
            self.dibujar_arbol(nodo.izquierda, x - espaciado, y - 1, espaciado / 2, ax)
        if nodo.derecha:
            ax.plot([x, x + espaciado], [y, y - 1], '-k')
            self.dibujar_arbol(nodo.derecha, x + espaciado, y - 1, espaciado / 2, ax)

        nodo_circle = Circle((x, y), radius=radio, fill=True, color='lightblue',
                             zorder=2)  # Usamos zorder para asegurar que los círculos estén sobre las líneas
        ax.add_patch(nodo_circle)
        ax.text(x, y, str(nodo.valor), ha='center', va='center', color='black')

    def dibujar(self):
        fig, ax = plt.subplots()
        self.dibujar_arbol(self.raiz, 0, 0, 4, ax)  # Modificar el último parámetro para ajustar el espaciado horizontal
        ax.set_aspect('equal')
        ax.axis('off')
        figManager = plt.get_current_fig_manager()
        figManager.window.state('zoomed')
        plt.show()