Alumnos = []

while True:
    try:
        print("1-Ingresar como profesor \n2-Ingresar como alumno \n3-Salir")

        menu = int(input("Seleccione el indice de la opcion que desea realizar: "))
        match menu:
            case 1:
                
                print("Ingresando como profesor... \n---------------------------------------------------------------------")

                while True:                  
                
                    contra = input("Ingrese la contraseña: ")
                    if contra == "Catolica10":
                        print("Contraseña correcta. Accediendo al sistema... \n==================================================== \nBienvenido ingeniero Erazo! \n====================================================")
                        print("1-Registrar alumno \n2-Reporte de alumnos \n3-Reporte de curso \n4-Buscar alumno \n5-Administrar curso \n6-Eliminar alumno \n7-Regresar al menu principal")
                        opcion = input("--------------------------------------------------------------------- \nSeleccione una opcion: ")
        
                        match opcion:
                            case "1":
                                nombre = input("Ingrese el nombre del alumno: ").title().isalpha()
                                while not nombre:
                                    print("Por favor, ingrese un nombre valido (solo letras)")
                                    nombre = input("Ingrese el nombre del alumno: ").title().isalpha()
                                edad = int(input("Ingrese la edad del alumno: "))
                                carnet = input("Ingrese el carnet del alumno: ").upper()
                                correo = input("Ingrese el correo del alumno: ")
                                carrera = input("Ingrese la carrera del alumno: ").title().isalpha()
                                while not carrera:
                                    print("Por favor, ingrese una carrera valida (solo letras)")
                                    carrera = input("Ingrese la carrera del alumno: ").title().isalpha()
                                curso = input("Ingrese el curso del alumno: ").title()
                                horario = int(input("Ingrese el horario del alumno: "))
                                Alumnos.append({
                                    "nombre": nombre,
                                    "edad": edad,
                                    "carnet": carnet,
                                    "correo": correo,
                                    "carrera": carrera,
                                    "curso": curso,
                                    "horario": horario
                                })
                                print(f"Alumno {nombre} registrado exitosamente!")

                            case "2":
                                print("Mostrando reporte de alumnos...")
                            case "3":
                                print("Mostrando reporte de curso...")

                            case "4":                            
                                carnet_buscar = input("Ingrese el carnet del alumno a buscar: ").upper()
                                if carnet_buscar in Alumnos:
                                    print(f"Alumno con carnet {carnet_buscar} encontrado.")
                                else:
                                    print(f"Alumno con carnet {carnet_buscar} no encontrado.")

                            case "5":
                                print("Administrar curso...")
                            case "6":
                                print("Eliminando alumno...")
                            case "7":
                                print("Regresando al menu principal... \n====================================================")
                                break
                            case _:
                                print("Opcion no valida. Por favor, seleccione un indice valido.")                        
                    else:
                        print("Contraseña incorrecta. Intente nuevamente.")
                        continue

            case 2:
                print("Ingresando como alumno...")
            case 3:
                print("Saliendo...")
                break
            case _:
                print("Opcion no valida. Por favor, seleccione un indice valido.")
    except ValueError:
        print("Error: Por favor, ingrese un numero valido.")