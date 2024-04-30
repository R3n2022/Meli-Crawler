import os
import json

def cargar_diccionario_desde_archivo(nombre_archivo):
    diccionario = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            diccionario = json.load(archivo)
    return diccionario

def guardar_diccionario_en_archivo(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(diccionario, archivo, indent=4)# Usar indent=4 para formatear el JSON con indentación

def menu_diccionario(diccionario_links, nombre_archivo):
    while True:
        print("\nMenú Listado de Competidores:")
        print("1. Agregar entrada")
        print("2. Eliminar entrada")
        print("3. Editar entrada")
        print("4. Mostrar listado de competidores")
        print("5. Guardar y volver al menu principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_entrada(diccionario_links)
        elif opcion == '2':
            eliminar_entrada(diccionario_links)
        elif opcion == '3':
            editar_entrada(diccionario_links)
        elif opcion == '4':
            mostrar_listado(diccionario_links)
        elif opcion == '5':
            guardar_diccionario_en_archivo(diccionario_links, nombre_archivo)
            print("El Listado se ha guardado. Saliendo del programa.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def agregar_entrada(diccionario_links):
    nombre = input("Ingrese el nombre: ")
    enlace = input("Ingrese el enlace correspondiente a {}: ".format(nombre))
    diccionario_links[nombre] = enlace
    input("¡{} agregado exitosamente! Presione Enter para volver al menú.".format(nombre))

def eliminar_entrada(diccionario_links):
    nombre = input("Ingrese el nombre de la entrada que desea eliminar: ")
    if nombre in diccionario_links:
        del diccionario_links[nombre]
        print("Entrada '{}' eliminada exitosamente.".format(nombre))
    else:
        print("La entrada '{}' no existe en el diccionario.".format(nombre))
    input("Presione Enter para volver al menú.")

def editar_entrada(diccionario_links):
    nombre = input("Ingrese el nombre de la entrada que desea editar: ")
    if nombre in diccionario_links:
        enlace = input("Ingrese el nuevo enlace correspondiente a '{}': ".format(nombre))
        diccionario_links[nombre] = enlace
        print("Entrada '{}' editada exitosamente.".format(nombre))
    else:
        print("La entrada '{}' no existe en el diccionario.".format(nombre))
    input("Presione Enter para volver al menú.")

def mostrar_listado(diccionario_links):
    print("Listado de enlaces:")
    for nombre, enlace in diccionario_links.items():
        print("{}: {}".format(nombre, enlace))
    input("Presione Enter para volver al menú.")

def gestionar_diccionario(nombre_archivo):
    diccionario_links = cargar_diccionario_desde_archivo(nombre_archivo)
    menu_diccionario(diccionario_links, nombre_archivo)
    guardar_diccionario_en_archivo(diccionario_links, nombre_archivo)
