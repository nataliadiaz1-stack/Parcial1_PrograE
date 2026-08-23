import os
import time
import cv2
import json
import sqlite3
import face_recognition
import getpass

conexion = sqlite3.connect("alumnos.db")
cursor = conexion.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                    carnet TEXT PRIMARY KEY UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    correo TEXT NOT NULL,
                    asignatura TEXT NOT NULL,                    
                    horario INTEGER NOT NULL,                    
                    asistencia INTEGER NOT NULL,
                    curso TEXT NOT NULL DEFAULT 'General',
                    firma TEXT
                )''')
conexion.commit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(1)

def guardar_rostro_directo(carnet_alumno, frame_bgr):
    try:
        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_frame)

        if len(encodings) > 0:
            firma_vector = encodings[0].tolist()
            firma_texto = json.dumps(firma_vector)

            cursor.execute(
                "UPDATE alumnos SET firma = ? WHERE carnet = ?", (firma_texto, carnet_alumno)
            )
            conexion.commit()
            print(f"\n¡ÉXITO! Rostro del alumno ({carnet_alumno}) procesado y guardado en la base de datos.")
            input("\nPresione ENTER para continuar...")
        else:
            print("\nADVERTENCIA: No se detectó ningún rostro. Asegúrese de tener buena iluminación e intente de nuevo.")
            input("\nPresione ENTER para continuar...")
    except Exception as e:
        print(f"\nError al guardar el rostro: {e}")
        input("\nPresione ENTER para continuar...")

def tomar_asistencia_por_rostro():
    cursor.execute("SELECT carnet, nombre, firma FROM alumnos WHERE firma IS NOT NULL AND firma != ''")
    registros = cursor.fetchall()

    if not registros:
        print("\nNo hay alumnos con firma facial registrada en el sistema.")
        input("\nPresione ENTER para continuar...")
        return

    rostros_conocidos = []
    carnets_conocidos = []
    nombres_conocidos = []

    for carnet, nombre, firma_texto in registros:
        try:
            vector_rostro = json.loads(firma_texto)
            rostros_conocidos.append(vector_rostro)
            carnets_conocidos.append(carnet)
            nombres_conocidos.append(nombre)
        except Exception:
            continue

    cap = cv2.VideoCapture(0)
    print("Iniciando cámara... Colóquese frente al lente y presione 'ESPACIO' para verificar su identidad.")

    frame_capturado = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            break

        cv2.imshow("Verificacion de Asistencia - Presione ESPACIO", frame)

        if cv2.waitKey(1) & 0xFF == ord(' '):
            frame_capturado = frame
            break

    cap.release()
    cv2.destroyAllWindows()

    if frame_capturado is not None:
        try:
            rgb_frame = cv2.cvtColor(frame_capturado, cv2.COLOR_BGR2RGB)
            encodings_captura = face_recognition.face_encodings(rgb_frame)

            if len(encodings_captura) > 0:
                encoding_desconocido = encodings_captura[0]
                coincidencias = face_recognition.compare_faces(rostros_conocidos, encoding_desconocido, tolerance=0.5)

                if True in coincidencias:
                    indice_coincidencia = coincidencias.index(True)
                    carnet_detectado = carnets_conocidos[indice_coincidencia]
                    nombre_detectado = nombres_conocidos[indice_coincidencia]

                    print(f"\n¡Bienvenido {nombre_detectado} ({carnet_detectado})!")
                    print("Asistencia registrada exitosamente en el sistema.")

                    cursor.execute("UPDATE alumnos SET asistencia = asistencia + 1 WHERE carnet = ?", (carnet_detectado,))
                    conexion.commit()
                else:
                    print("\nRostro no reconocido. No se encontró coincidencia en la base de datos.")
            else:
                print("\nNo se detectó ningún rostro en la imagen capturada.")

        except Exception as e:
            print(f"Error durante el proceso de verificación: {e}")
            
    input("\nPresione ENTER para continuar...")

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
    lista = ["Programacion Estructurada", "Matematica IV", "Diseno de Bases de Datos", "Sistemas Operativos y Redes"]
    print("Asignaturas disponibles: \n1- Programacion Estructurada \n2- Matematica IV \n3- Diseno de Bases de Datos \n4- Sistemas Operativos y Redes")
    while True:
        try:
            asignatura = int(input("Seleccione el indice de la asignatura que desea: "))
            if 1 <= asignatura <= 4:
                return lista[asignatura - 1]
            else:
                print("Error: Por favor, ingrese un numero entre 1 y 4.")
        except ValueError:
            print("Error: Por favor, ingrese un indice valido.")

def registrar_alumno():
    nombre = input("Ingrese el nombre completo del alumno: ").title()
    while not nombre.replace(" ","").isalpha():
        print("Por favor, ingrese un nombre valido (solo letras)")
        nombre = input("Ingrese el nombre completo del alumno: ").title()
    while True:
        try:
            edad = int(input("Ingrese la edad: "))
            if edad < 16 or edad > 80:
                print("Por favor, ingrese una edad valida (entre 16 y 80)")
                edad = int(input("Ingrese la edad: "))
            else:
                break
        except ValueError:
            print("Error: Por favor, ingrese una edad valida.")
    carnet = input("Ingrese el carnet: ").upper()
    correo = input("Ingrese el correo: ")
    asignatura = asignaturas()
    horario = horarios()
    curso = input("Ingrese la seccion o grupo de la asignatura: ").title()

    try:
        cursor.execute("INSERT INTO alumnos (carnet, nombre, edad, correo, asignatura, horario, curso) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (carnet, nombre, edad, correo, asignatura, horario, curso,))
        conexion.commit()
        print(f"Alumno {nombre} registrado exitosamente!")

        tomar_foto = input("¿Desea tomar la foto del rostro ahora con la cámara? (S/N): ").strip().upper()
        if tomar_foto == "S":
            cap = cv2.VideoCapture(0)
            print("Presione la tecla 'ESPACIO' para tomar la foto...")
            frame_capturado = None
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Registro Facial - Presione ESPACIO", frame)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    frame_capturado = frame
                    break
            
            cap.release()
            cv2.destroyAllWindows()

            if frame_capturado is not None:
                guardar_rostro_directo(carnet, frame_capturado)

    except sqlite3.IntegrityError:
        print(f"Error: El carnet {carnet} ya está registrado.")

def mostrar_alumnos():
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()

    if alumnos:
        for alumno in alumnos:
            print(f"\nCarnet: {alumno[0]}")
            print(f"Nombre: {alumno[1]}")
            print(f"Edad: {alumno[2]}")
            print(f"Correo: {alumno[3]}")
            print(f"Asignatura: {alumno[4]}")
            print(f"Horario: {alumno[5]}")
            print(f"Asistencia: {alumno[6]}%")
    else:
        print("No hay alumnos registrados.")   

def reporte_curso():
    cursor.execute("SELECT DISTINCT curso FROM alumnos")
    cursos = cursor.fetchall()

    if cursos:
        for curso in cursos:
            nombre_curso = curso[0]

            print(f"Asignatura: {nombre_curso}")

            cursor.execute("SELECT * FROM alumnos WHERE curso = ?", (nombre_curso,))
            alumnos_curso = cursor.fetchall()

            aprobados = 0
            reprobados = 0
            suma_asistencia = 0

            cantidad = len(alumnos_curso)
            promedio_asistencia = suma_asistencia / cantidad

            print(f"\nTotal de alumnos: {cantidad}")
            print(f"Alumnos aprobados: {aprobados}")
            print(f"Alumnos reprobados: {reprobados}")
            print(f"Promedio de asistencia: {promedio_asistencia:.2f}%")
    else:
        print("No hay cursos registrados.")     

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
        clear_screen()
        match menu:
            case 1:
                print("Ingresando como profesor... \n---------------------------------------------------------------------")
                contra = getpass.getpass("Ingrese la contraseña: ")
                if contra == "Catolica10":
                    print("Contraseña correcta. Accediendo al sistema... \n==================================================== \nBienvenido ingeniero Erazo! \n====================================================")
                    clear_screen()

                    while True:               
                        print("1-Registrar alumno \n2-Reporte de alumnos \n3-Reporte de curso \n4-Buscar alumno \n5-Administrar curso \n6-Eliminar alumno \n7-Regresar al menu principal")
                        opcion = input("--------------------------------------------------------------------- \nSeleccione una opcion: ")
            
                        match opcion:
                            case "1":
                                registrar_alumno()
                                clear_screen()
                            case "2":
                                mostrar_alumnos()
                                input("\nPresione ENTER para regresar...")
                                clear_screen()
                            case "3":
                                reporte_curso()
                                input("\nPresione ENTER para regresar...")
                                clear_screen()
                            case "4":                            
                                carnet_buscar = input("Ingrese el carnet del alumno a buscar: ").upper()
                                if alumno := buscar_alumno(carnet_buscar):
                                    print(f"Alumno con carnet {carnet_buscar} encontrado. \nCarnet: {alumno[0]} \nNombre: {alumno[1]} \nEdad: {alumno[2]} \nCorreo: {alumno[3]} \nAsignatura: {alumno[4]} \nHorario: {alumno[5]} \nAsistencia: {alumno[6]}%")
                                else:
                                    print(f"Alumno con carnet {carnet_buscar} no encontrado.")
                                input("\nPresione ENTER para regresar...")
                                clear_screen()

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
                                input("\nPresione ENTER para regresar...")
                                clear_screen()

                            case "6":
                                carnet_eliminar = input("Ingrese el carnet del alumno a eliminar: ").upper()
                                cursor.execute("SELECT * FROM alumnos WHERE carnet = ?", (carnet_eliminar,))
                                if alumno := cursor.fetchone():
                                    confirmacion = input(f"Esta seguro de que desea eliminar al alumno {alumno[1]} con carnet {carnet_eliminar}? (S/N): ").strip().upper()
                                    if confirmacion == "S":
                                        eliminar_alumno(carnet_eliminar)
                                        print(f"Alumno con carnet {carnet_eliminar} eliminado exitosamente.")
                                    else:
                                        print("Eliminación cancelada.")
                                else:
                                    print(f"Alumno con carnet {carnet_eliminar} no encontrado.")
                                input("\nPresione ENTER para regresar...")
                                clear_screen()

                            case "7":
                                print("Regresando al menu principal... \n====================================================")
                                clear_screen()
                                break
                            case _:
                                print("Opcion no valida. Por favor, seleccione un indice valido.")                        
                else:
                    print("Contraseña incorrecta. Intente nuevamente.")                                            

            case 2:
                print("Ingresando como alumno...")
                tomar_asistencia_por_rostro()
                clear_screen()
            case 3:
                print("Saliendo...")
                conexion.close()
                break
            case _:
                print("Opcion no valida. Por favor, seleccione un indice valido.")
    except ValueError:
        print("Error: Por favor, ingrese un numero valido.")