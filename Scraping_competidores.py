import requests
from bs4 import BeautifulSoup
from colorama import Fore
import openpyxl
import json

def cargar_competidores_desde_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"{Fore.RED}Error al cargar competidores desde el archivo JSON: {e}")
        return {}

def buscar_productos_competencia(url_dict, string_competencia):
    print('--- Búsqueda en Competidores ---')
    try:
        results = []
        for competidor, url in url_dict.items():
            print(f"{Fore.YELLOW}Buscando en {competidor}...")
            search_url = f"{url}?q={string_competencia}"
            response = requests.get(search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('div', class_='andes-card')
                error_message = soup.find('div', class_='andes-message__text andes-message__text--accent')
                if error_message:
                    print(f"{Fore.RED}No se encontraron resultados en {competidor} para '{string_competencia}'")
                    continue  # Saltar a la siguiente iteración si no se encontraron productos
                if not items:
                    print(f"{Fore.RED}No se encontraron resultados en {competidor} para '{string_competencia}'")
                    continue  # Saltar a la siguiente iteración si no se encontraron productos
                for item in items:
                    title = item.find('h2', class_='ui-search-item__title').text
                    price = item.find('span', class_='andes-money-amount__fraction').text
                    discount = item.find('span', class_='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript').text
                    link = item.find('a', class_='ui-search-item__group__element')['href']
                    results.append({'Competidor': competidor.upper(), 'Articulo': title, 'Precio': price, 'Rebajado': discount, 'Link': link})
                    # Mostrar datos en la consola con colores
                    print(f"{Fore.GREEN}Competidor: {competidor.upper()}")
                    print(f"{Fore.YELLOW}Artículo: {title}")
                    print(f"{Fore.CYAN}Precio: {price}")
                    print(f"{Fore.BLUE}Rebajado: {discount}")
                    print(f"{Fore.MAGENTA}Enlace: {link}")
                    print("-" * 30)  # Separador entre productos
            else:
                print(f"{Fore.RED}Error al acceder a {competidor}: {response.status_code}")
        return results
    except Exception as e:
        print(f"{Fore.RED}Error en la búsqueda de competidores: {e}")
        return []

def exportar_a_excel(resultados, filename, url_dict):
    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Resultados'

        # Escribir los encabezados
        sheet.append(['Competidor', 'Articulo', 'Precio', 'Rebajado', 'Link'])

        # Crear un diccionario para almacenar los productos por competidor
        productos_por_competidor = {}

        # Escribir los datos en el diccionario por competidor
        for resultado in resultados:
            competidor = resultado['Competidor']
            articulo = resultado['Articulo']
            precio = resultado['Precio']
            rebajado = resultado['Rebajado']
            link = resultado['Link']

            if competidor not in productos_por_competidor:
                productos_por_competidor[competidor] = []

            productos_por_competidor[competidor].append([articulo, precio, rebajado, link])

        # Escribir los datos en la hoja de Excel
        for competidor, productos in productos_por_competidor.items():
            for producto in productos:
                sheet.append([competidor] + producto)

        # Agregar líneas para los competidores que no tienen el producto
        for competidor in url_dict.keys():
            if competidor not in productos_por_competidor:
                sheet.append([f"{competidor} no tiene el producto", "", "", "", ""])

        # Guardar el libro de Excel
        workbook.save(filename)
        print(f"{Fore.RESET}\nLos resultados se han guardado en '{filename}'.")
    except Exception as e:
        print(f"{Fore.RED}Error al exportar a Excel: {e}")

if __name__ == "__main__":
    url_dict = cargar_competidores_desde_json('diccionario_enlaces.json')

    if not url_dict:
        print("No se pudo cargar la información de los competidores.")
    else:
        string_competencia = input("Ingrese el término que desea buscar en los competidores: ")

        resultados_competencia = buscar_productos_competencia(url_dict, string_competencia)

        if resultados_competencia:
            print("\nResultados obtenidos:")
            for resultado in resultados_competencia:
                print(resultado)

            nombre_archivo = input("\nIngrese el nombre para el archivo Excel de resultados: ")
            exportar_a_excel(resultados_competencia, f'{nombre_archivo}.xlsx', url_dict)
        else:
            print("No se encontraron resultados.")