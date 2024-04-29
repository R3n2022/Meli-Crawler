from colorama import init, Fore
from DB import gestionar_diccionario, cargar_diccionario_desde_archivo
from Scraping_general import buscar_productos
from Scraping_competidores import buscar_productos_competencia, exportar_a_excel, cargar_competidores_desde_json
import pandas as pd

# Inicializar colorama
init(autoreset=True)

# Definir función para guardar resultados en un archivo Excel
def guardar_resultados_excel(resultados, nombre_archivo):
    df = pd.DataFrame(resultados)
    df.to_excel(nombre_archivo, index=False)
    print(f'Resultados guardados en "{nombre_archivo}"')

def mostrar_menu():
    print('\n--- Menú ---')
    print('A. Buscar Productos en Listado General')
    print('B. Buscar Productos en Base de Competidores')
    print('C. Modificar Base de Competidores')
    print('D. Salir')

def main():
    print('Bienvenido al Script de Búsqueda en MercadoLibre V1.0')
    nombre_archivo_links = 'diccionario_enlaces.json'
    diccionario_links = cargar_diccionario_desde_archivo(nombre_archivo_links)

    while True:
        mostrar_menu()
        opcion = input('Elige una opción: ')
        if opcion == 'A':
            string = input('¿Qué quieres buscar? ')
            try:
                resultados = buscar_productos(string)
                if resultados:
                    guardar_resultados_excel(resultados, 'resultados_general.xlsx')
                    input("Presione Enter para volver al menú.")
                else:
                    print(Fore.YELLOW + 'No se encontraron productos para la búsqueda.')
            except Exception as e:
                print(Fore.RED + f"Error al buscar productos: {e}")
        elif opcion == 'B':
            url_dict = cargar_competidores_desde_json('diccionario_enlaces.json')
            if not url_dict:
                print(Fore.RED + "No se pudo cargar la información de los competidores.")
            else:
                string_competencia = input("Ingrese el término que desea buscar en los competidores: ")
                resultados_competencia = buscar_productos_competencia(url_dict, string_competencia)
                if resultados_competencia:
                    nombre_archivo = input("\nIngrese el nombre para el archivo Excel de resultados: ")
                    exportar_a_excel(resultados_competencia, f'{nombre_archivo}.xlsx', url_dict)
                    input("Presione Enter para volver al menú.")
                else:
                    print(Fore.YELLOW + "No se encontraron resultados en los competidores.")
        elif opcion == 'C':
            gestionar_diccionario(nombre_archivo_links)
        elif opcion == 'D':
            print('¡Hasta luego!')
            break
        else:
            print('Opción inválida. Inténtalo de nuevo.')

if __name__ == '__main__':
    main()
