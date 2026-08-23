import sqlite3
from unittest import case
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

def horarios():
    print("Horarios disponibles: \n1- 6:45 am a 8:25 am \n2- 8:30 am a 10:10 am \n3- 10:15 am a 11:45 am \n4- 11:50 am a 1:00 pm \n5- 1:00 pm a 2:30 pm \n6- 2:30 pm a 4:00 pm \n7- 4:00 pm a 5:30 pm \n8- 5:30 pm a 7:00 pm")
    while True:
        try:
            horario = int(input("Seleccione el indice del horario que desea: "))
            if 1 <= horario <= 8:
                return horario
            else:
                print("Error: Por favor, ingrese un numero entre 1 y 8.")
        except ValueError:
            print("Error: Por favor, ingrese un indice valido.")

def asignaturas():
    print("Asignaturas disponibles: \n1- Programacion Estructurada \n2- Matematica IV \n3- Diseno de Bases de Datos \n4- Sistemas Operativos y Redes")
    while True:
        try:
            asignatura = int(input("Seleccione el indice de la asignatura que desea: "))
            if 1 <= asignatura <= 4:
                return asignatura
            else:
                print("Error: Por favor, ingrese un numero entre 1 y 4.")
        except ValueError:
            print("Error: Por favor, ingrese un indice valido.")

def registrar_alumno():
    nombre = input("Ingrese el nombre del alumno: ").title()
    while not nombre.replace(" ","").isalpha():
        print("Por favor, ingrese un nombre valido (solo letras)")
        nombre = input("Ingrese el nombre del alumno: ").title()

    edad = int(input("Ingrese la edad del alumno: "))
    carnet = input("Ingrese el carnet del alumno: ").upper()
    correo = input("Ingrese el correo del alumno: ")
    asignatura = asignaturas()
    horario = horarios()
    asistencia = int(input("Ingrese el porcentaje de asistencia del alumno: "))

    try:
        cursor.execute("INSERT INTO alumnos (carnet, nombre, edad, correo, asignatura, horario, asistencia) VALUES (?, ?, ?, ?, ?, ?, ?)", (carnet, nombre, edad, correo, asignatura, horario, asistencia))
        conexion.commit()
        print(f"Alumno {nombre} registrado exitosamente!")
    except sqlite3.IntegrityError:
        print(f"Error: El carnet {carnet} ya está registrado. Por favor, ingrese un carnet único.")

def mostrar_alumnos():
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()

    if alumnos:
        for alumno in alumnos:
            print(f"\nCarnet: {alumno[0]}")
            print(f"Nombre: {alumno[1]}")
            print(f"Edad: {alumno[2]}")
            print(f"Correo: {alumno[3]}")
            print(f"Asignatura: {asignaturas()}")
            print(f"Horario: {horarios()}")
            print(f"Asistencia: {alumno[6]}%")
    else:
        print("No hay alumnos registrados.")        

def buscar_alumno(carnet):
    cursor.execute("SELECT * FROM alumnos WHERE carnet = ?", (carnet,))
    return cursor.fetchone()

def eliminar_alumno(carnet):
    cursor.execute("DELETE FROM alumnos WHERE carnet = ?", (carnet,))
    conexion.commit()

while True:
    try:
        print("Bienvenido al administrador para Ingenieria en Desarrollo de Software! \n1-Ingresar como profesor \n2-Ingresar como alumno \n3-Salir")

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
                                    registrar_alumno()
                                case "2":
                                    mostrar_alumnos()
                                case "3":
                                    print("Mostrando reporte de curso...")

                                    cursor.execute("SELECT DISTINCT curso FROM alumnos")
                                    cursos = cursor.fetchall()

                                    if cursos:
                                        for curso in cursos:
                                            nombre_curso = curso[0]

                                            print(f"\nCurso: {nombre_curso}")

                                            cursor.execute("SELECT * FROM alumnos WHERE curso = ?", (nombre_curso,))
                                            alumnos_curso = cursor.fetchall()

                                            aprobados = 0
                                            reprobados = 0
                                            suma_notas = 0
                                            suma_asistencia = 0

                                            for alumno in alumnos_curso:
                                                nota = alumno[5]
                                                asistencia = alumno[6]

                                                suma_notas += nota
                                                suma_asistencia += asistencia

                                                if nota >= 6 and asistencia >= 80:
                                                    state = "Aprobado"
                                                    aprobados += 1
                                                else:
                                                    state = "Reprobado"
                                                    reprobados += 1

                                                print(f"\nCarnet: {alumno[0]}")
                                                print(f"Nombre: {alumno[1]}")
                                                print(f"Asignatura: {asignaturas()}")
                                                print(f"Horario: {horarios()}")
                                                print(f"Nota: {nota}")
                                                print(f"Asistencia: {asistencia}%")
                                                print(f"Estado   : {state}")

                                            cantidad = len(alumnos_curso)
                                            promedio_nota = suma_notas / cantidad
                                            promedio_asistencia = suma_asistencia / cantidad

                                            print(f"\nTotal de alumnos: {cantidad}")
                                            print(f"Alumnos aprobados: {aprobados}")
                                            print(f"Alumnos reprobados: {reprobados}")
                                            print(f"Promedio del curso: {promedio_nota:.2f}")
                                            print(f"Promedio de asistencia: {promedio_asistencia:.2f}%")
                                    else:
                                        print("No hay cursos registrados.")

                                case "4":                            
                                    carnet_buscar = input("Ingrese el carnet del alumno a buscar: ").upper()
                                    if alumno := buscar_alumno(carnet_buscar):
                                        print(f"Alumno con carnet {carnet_buscar} encontrado. \nCarnet: {alumno[0]} \nNombre: {alumno[1]} \nCorreo: {alumno[2]} \nAsignatura: {asignaturas()} \nHorario: {horarios()} \nEdad: {alumno[5]} \nAsistencia: {alumno[6]}%")
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

                                    cursor.execute("UPDATE alumnos SET asignatura = ?", (nuevo_curso,))
                                    conexion.commit()
                                    print(f"Asignatura '{nuevo_curso}' administrada y actualizada exitosamente!")

                                case "6":
                                    carnet_eliminar = input("Ingrese el carnet del alumno a eliminar: ").upper()
                                    cursor.execute("SELECT * FROM alumnos WHERE carnet = ?", (carnet_eliminar,))
                                    if alumno := cursor.fetchone():
                                        confirmacion = input(f"Esta seguro de que desea eliminar al alumno {alumno[1]} con carnet {carnet_eliminar}? (S/N): ").strip().upper()
                                        if confirmacion == "S":
                                            eliminar_alumno(carnet_eliminar)
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