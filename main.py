# main.py - Menú principal del sistema de señas unificado

import os
import sys

MENU = """
==============================
 LENGUA DE SEÑAS UNIFICADA
==============================
1. Capturar nueva clase (letra, número o frase)
2. Entrenar modelo LSTM
3. Ejecutar predicción en tiempo real
4. Salir
"""

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(MENU)
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == '1':
            import capturar_secuencias
            capturar_secuencias.main()
        elif opcion == '2':
            import entrenar_modelo
            entrenar_modelo.main()
        elif opcion == '3':
            import predecir_secuencias
            predecir_secuencias.main()
        elif opcion == '4':
            print("\n👋 Saliendo del sistema.")
            sys.exit(0)
        else:
            print("\n❌ Opción inválida. Intente de nuevo.")

        input("\nPresione ENTER para continuar...")

if __name__ == '__main__':
    main()