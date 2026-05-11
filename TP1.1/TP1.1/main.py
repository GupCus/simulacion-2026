# Consignas del TP:
# El trabajo de investigación consiste en construir un programa en lenguaje Python 3.x que simule el funcionamiento del
# plato de una ruleta. Para esto se debe tener en cuenta los siguientes temas:
# • Generación de valores aleatorios enteros.
# • Uso de listas para el almacenamiento de datos.
# • Uso de la estructura de control FOR para iterar las listas.
# • Empleo de funciones estadísticas.
# • Gráficos de los resultados mediante el paquete Matplotlib.
# • Ingreso por consola de parámetros para la simulación (cantidad de tiradas, corridas y número elegido, ejemplo
# python programa.py -c XXX -n YYY -e ZZ).
import mesa


def main():
    print("Simulación TP 1.1")
    mesa.premiar()


# Esta es una buena práctica en Python 3 para indicar que main() solo debe ejecutarse si ejecutamos ESTE archivo directamente.
if __name__ == "__main__":
    main()