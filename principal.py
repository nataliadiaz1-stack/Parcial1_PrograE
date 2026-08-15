import sqlite3
conexion = sqlite3.connect("alumnos.db")
cursor = conexion.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                    carnet TEXT PRIMARY KEY UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    correo TEXT NOT NULL,
                    carrera TEXT NOT NULL,
                    curso TEXT NOT NULL,
                    horario INTEGER NOT NULL
                )''')
conexion.commit()

while True:
    try:
        print("1-Ingresar como profesor \n2-Ingresar como alumno \n3-Salir")

        menu = int(input("Seleccione el indice de la opcion que desea realizar: "))
        match menu:
            case 1:
                
                print("Ingresando como profesor... \n---------------------------------------------------------------------")
                contra = input("Ingrese la contraseña: ")
                if contra == "Catolica10":
                    print("Contraseña correcta. Accediendo al sistema... \n==================================================== \nBienvenido ingeniero Erazo! \n====================================================")

                    while True:               
                    
                            print("1-Registrar alumno \n2-Reporte de alumnos \n3-Reporte de curso \n4-Buscar alumno \n5-Administrar curso \n6-Eliminar alumno \n7-Regresar al menu principal")
                            opcion = input("--------------------------------------------------------------------- \nSeleccione una opcion: ")
            
                            match opcion:
                                case "1":
                                    nombre = input("Ingrese el nombre del alumno: ").title()
                                    while not nombre.replace(" ","").isalpha():
                                        print("Por favor, ingrese un nombre valido (solo letras)")
                                        nombre = input("Ingrese el nombre del alumno: ").title()

                                    edad = int(input("Ingrese la edad del alumno: "))
                                    carnet = input("Ingrese el carnet del alumno: ").upper()
                                    correo = input("Ingrese el correo del alumno: ")

                                    carrera = input("Ingrese la carrera del alumno: ").title()
                                    while not carrera.replace(" ","").isalpha():
                                        print("Por favor, ingrese una carrera valida (solo letras)")
                                        carrera = input("Ingrese la carrera del alumno: ").title()

                                    curso = input("Ingrese el curso del alumno: ").title()
                                    horario = int(input("Ingrese el horario del alumno: "))
                                    
                                    try:
                                        cursor.execute("INSERT INTO alumnos (carnet, nombre, edad, correo, carrera, curso, horario) VALUES (?, ?, ?, ?, ?, ?, ?)", (carnet, nombre, edad, correo, carrera, curso, horario))
                                        conexion.commit()
                                        print(f"Alumno {nombre} registrado exitosamente!")
                                    except sqlite3.IntegrityError:
                                        print(f"Error: El carnet {carnet} ya está registrado. Por favor, ingrese un carnet único.")

                                case "2":
                                    print("Mostrando reporte de alumnos...")
                                case "3":
                                    print("Mostrando reporte de curso...")

                                case "4":                            
                                    carnet_buscar = input("Ingrese el carnet del alumno a buscar: ").upper()
                                    cursor.execute("SELECT * FROM alumnos WHERE carnet = ?", (carnet_buscar,))
                                    if alumno := cursor.fetchone():
                                        print(f"Alumno con carnet {carnet_buscar} encontrado. \nNombre: {alumno[1]} \nEdad: {alumno[2]} \nCorreo: {alumno[3]} \nCarrera: {alumno[4]} \nCurso: {alumno[5]} \nHorario: {alumno[6]}")
                                    else:
                                        print(f"Alumno con carnet {carnet_buscar} no encontrado.")

                                case "5":
                                    print("Administrar curso... \n---------------------------------------------------------------------")
                                    nuevo_curso = input("Ingrese el nombre del curso: ")
                                    while not nuevo_curso.isalnum():
                                        print("Error: El curso no debe tener caracteres especiales, solo numeros y letras.")
                                        nuevo_curso = input("Ingrese el nombre del curso: ")

                                    while True:
                                        try:
                                            total_clases = int(input("Defina la cantidad total de clases programadas: "))
                                            if total_clases > 0:
                                                break
                                            print("Error: Debe ingresar un numero mayor a 0.")
                                        except ValueError:
                                            print("Error: Solo se permiten numeros enteros.")

                                    cancelar = input("Desea cancelar una clase hoy? (S/N): ").strip().upper()
                                    if cancelar == "S":
                                        total_clases -= 1
                                        print(f"Clase cancelada. El total de clases ahora es: {total_clases}")
                                        print("Aprobando asistencia automaticamente a todos los alumnos por la clase cancelada...")

                                    cursor.execute("UPDATE alumnos SET curso = ?", (nuevo_curso,))
                                    conexion.commit()
                                    print(f"Curso '{nuevo_curso}' administrado y actualizado exitosamente!")

                                case "6":
                                    carnet_eliminar = input("Ingrese el carnet del alumno a eliminar: ").upper()
                                    cursor.execute("SELECT * FROM alumnos WHERE carnet = ?", (carnet_eliminar,))
                                    if alumno := cursor.fetchone():
                                        confirmacion = input(f"Esta seguro de que desea eliminar al alumno {alumno[1]} con carnet {carnet_eliminar}? (S/N): ").strip().upper()
                                        if confirmacion == "S":
                                            cursor.execute("DELETE FROM alumnos WHERE carnet = ?", (carnet_eliminar,))
                                            conexion.commit()
                                            print(f"Alumno con carnet {carnet_eliminar} eliminado exitosamente.")
                                        else:
                                            print("Eliminación cancelada.")
                                    else:
                                        print(f"Alumno con carnet {carnet_eliminar} no encontrado.")

                                case "7":
                                    print("Regresando al menu principal... \n====================================================")
                                    break
                                case _:
                                    print("Opcion no valida. Por favor, seleccione un indice valido.")                        
                else:
                    print("Contraseña incorrecta. Intente nuevamente.")                                            

            case 2:
                print("Ingresando como alumno...")
            case 3:
                print("Saliendo...")
                conexion.close()
                break
            case _:
                print("Opcion no valida. Por favor, seleccione un indice valido.")
    except ValueError:
        print("Error: Por favor, ingrese un numero valido.")