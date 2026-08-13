while True:
    try:
        print("1-Ingresar como profesor \n2-Ingresar como alumno \n3-Salir")

        menu = int(input("Seleccione el indice de la opcion que desea realizar: "))
        match menu:
            case 1:
                print("Ingresando como profesor...")
                while True:
                    print("1-Registrar alumno \n2-Reporte de alumnos \n3-Reporte de curso \n4-Buscar alumno \n5-Administrar curso \n6-Eliminar alumno \n7-Salir")
                    opcion = input("Seleccione una opcion: ").upper()

                    match opcion:
                        case "1":
                            print("Registrando alumno...")
                        case "2":
                            print("Mostrando reporte de alumnos...")
                        case "3":
                            print("Mostrando reporte de curso...")
                        case "4":
                            print("Buscando alumno...")
                        case "5":
                            print("Administrar curso...")
                        case "6":
                            print("Eliminando alumno...")
                        case "7":
                            print("Saliendo...")
                            break
                        case _:
                            print("Opcion no valida. Por favor, seleccione una opcion valida.")
            case 2:
                print("Ingresando como alumno...")
            case 3:
                print("Saliendo...")
                break
            case _:
                print("Opcion no valida. Por favor, seleccione una opcion valida.")
    except ValueError:
        print("Error: Por favor, ingrese un numero valido.")