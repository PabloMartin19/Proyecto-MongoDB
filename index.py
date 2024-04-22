import pymongo

# Conexión a la base de datos
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Proyecto-MongoDB"]
collection = db["libros"]

def insertar_libro():
    print("\nINSERTAR LIBRO")
    author = input("Autor: ")
    country = input("País: ")
    language = input("Idioma: ")
    pages = int(input("Páginas: "))
    title = input("Título: ")
    year = int(input("Año: "))
    genres = input("Géneros (separados por comas): ").split(", ")
    
    libro = {
        "author": author,
        "country": country,
        "language": language,
        "pages": pages,
        "title": title,
        "year": year,
        "genres": genres
    }
    
    collection.insert_one(libro)
    print("Libro insertado correctamente.")

def eliminar_libro():
    print("\nELIMINAR LIBRO")
    print("Opciones de eliminación:")
    print("1. Eliminar un libro por título")
    print("2. Eliminar libros por año")
    print("3. Eliminar libros por país")
    print("4. Eliminar libros por idioma")
    print("5. Cancelar")

    opcion = input("Seleccione una opción de eliminación: ")

    if opcion == "1":
        titulo = input("Introduce el título del libro que deseas eliminar: ")
        result = collection.delete_one({"title": titulo})
        if result.deleted_count > 0:
            print("Libro eliminado correctamente.")
        else:
            print("El libro no se encontró.")
    elif opcion == "2":
        year = int(input("Introduce el año de los libros que deseas eliminar: "))
        result = collection.delete_many({"year": year})
        if result.deleted_count > 0:
            print(f"Se eliminaron {result.deleted_count} libros del año {year}.")
        else:
            print("No se encontraron libros del año especificado.")
    elif opcion == "3":
        pais = input("Introduce el país de los libros que deseas eliminar: ")
        result = collection.delete_many({"country": pais})
        if result.deleted_count > 0:
            print(f"Se eliminaron {result.deleted_count} libros del país {pais}.")
        else:
            print("No se encontraron libros del país especificado.")
    elif opcion == "4":
        idioma = input("Introduce el idioma de los libros que deseas eliminar: ")
        result = collection.delete_many({"language": idioma})
        if result.deleted_count > 0:
            print(f"Se eliminaron {result.deleted_count} libros en el idioma {idioma}.")
        else:
            print("No se encontraron libros en el idioma especificado.")
    elif opcion == "5":
        print("Operación de eliminación cancelada.")
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

def modificar_libro():
    print("\nMODIFICAR LIBRO")
    title = input("Introduce el título del libro que deseas modificar: ")
    nuevo_title = input("Nuevo título (dejar en blanco si no se desea modificar): ")
    nuevo_author = input("Nuevo autor (dejar en blanco si no se desea modificar): ")
    nuevo_country = input("Nuevo país (dejar en blanco si no se desea modificar): ")
    nuevo_language = input("Nuevo idioma (dejar en blanco si no se desea modificar): ")
    nuevo_pages = input("Nuevas páginas (dejar en blanco si no se desea modificar): ")
    nuevo_year = input("Nuevo año (dejar en blanco si no se desea modificar): ")
    nuevo_genres = input("Nuevos géneros (separados por comas, dejar en blanco si no se desea modificar): ").split(", ")

    update_fields = {}
    if nuevo_title:
        update_fields["title"] = nuevo_title
    if nuevo_author:
        update_fields["author"] = nuevo_author
    if nuevo_country:
        update_fields["country"] = nuevo_country
    if nuevo_language:
        update_fields["language"] = nuevo_language
    if nuevo_pages:
        update_fields["pages"] = int(nuevo_pages)
    if nuevo_year:
        update_fields["year"] = int(nuevo_year)
    if nuevo_genres:
        update_fields["genres"] = nuevo_genres

    if update_fields:
        collection.update_one({"title": title}, {"$set": update_fields})
        print("Libro modificado correctamente.")
    else:
        print("No se realizaron modificaciones.")

def consultar_libro():
    print("\nCONSULTAR LIBRO")
    print("Opciones de consulta:")
    print("1. Consulta de datos simples")
    print("2. Consulta con arrays")
    print("3. Consulta con documentos embebidos")
    print("4. Consulta de agrupación")
    print("5. Cancelar")

    opcion = input("Seleccione una opción de consulta: ")

    if opcion == "1":
        print("\nCONSULTA DE DATOS SIMPLES")
        titulo = input("Introduce el título del libro que deseas consultar: ")
        libro = collection.find_one({"title": titulo})
        if libro:
            print("Información del libro:")
            print("Título:", libro["title"])
            print("Autor:", libro["author"])
            print("País:", libro["country"])
            print("Idioma:", libro["language"])
            print("Páginas:", libro["pages"])
            print("Año:", libro["year"])
            print("Géneros:", ", ".join(libro["genres"]))
        else:
            print("El libro no se encontró.")
    elif opcion == "2":
        print("\nCONSULTA CON ARRAYS")
        idioma = input("Introduce el idioma para la consulta de libros: ")
        libros = collection.find({"language": idioma})
        print(f"Libros en {idioma}:")
        for libro in libros:
            print(libro["title"])
    elif opcion == "3":
        print("\nCONSULTA CON DOCUMENTOS EMBEBIDOS")
        autor = input("Introduce el autor para la consulta de libros: ")
        libros = collection.find({"author": autor})
        print(f"Libros de {autor}:")
        for libro in libros:
            print(libro["title"])
    elif opcion == "4":
        print("\nCONSULTA DE AGRUPACIÓN")
        country_group = collection.aggregate([
            {"$group": {"_id": "$country", "count": {"$sum": 1}}}
        ])
        print("Número de libros por país:")
        for item in country_group:
            print(f"{item['_id']}: {item['count']} libros")
    elif opcion == "5":
        print("Operación de consulta cancelada.")
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")



def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Insertar libro")
        print("2. Eliminar libro")
        print("3. Modificar libro")
        print("4. Consultar libro")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            insertar_libro()
        elif opcion == "2":
            eliminar_libro()
        elif opcion == "3":
            modificar_libro()
        elif opcion == "4":
            consultar_libro()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    menu()
