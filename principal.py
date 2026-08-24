import os
import time
import re
import cv2
import json
import sqlite3
import face_recognition
import getpass
import subprocess

conexion = sqlite3.connect("alumnos.db")
cursor = conexion.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                    carnet TEXT PRIMARY KEY UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    correo TEXT NOT NULL,
                    asistencia INTEGER NOT NULL DEFAULT 0,
                    firma TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS matriculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    carnet_alumno TEXT NOT NULL,
                    asignatura TEXT NOT NULL,
                    horario_id INTEGER NOT NULL,
                    seccion TEXT NOT NULL,
                    FOREIGN KEY (carnet_alumno) REFERENCES alumnos (carnet) ON DELETE CASCADE
                )''')
conexion.commit()

DICCIONARIO_HORARIOS = {
    1: "6:45 am a 8:25 am",
    2: "8:30 am a 10:10 am",
    3: "10:15 am a 11:45 am",
    4: "11:50 am a 1:00 pm",
    5: "1:00 pm a 2:30 pm",
    6: "2:30 pm a 4:00 pm",
    7: "4:00 pm a 5:30 pm",
    8: "5:30 pm a 7:00 pm"
}

def clear_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    time.sleep(0.5)

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def abrir_camara():
    # Intenta con DirectShow para evitar congelamientos en Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    return cap

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
            print(f"\n¡ÉXITO! Rostro del alumno ({carnet_alumno}) procesado y guardado.")
        else:
            print("\nADVERTENCIA: No se detectó ningún rostro. Asegúrese de tener buena iluminación.")
    except Exception as e:
        print(f"\nError al guardar el rostro: {e}")
    input("\nPresione ENTER para continuar...")

def tomar_asistencia_por_rostro():
    cursor.execute("SELECT carnet, nombre, firma FROM alumnos WHERE firma IS NOT NULL AND firma != ''")
    registros = cursor.fetchall()

    if not registros:
        print("\nNo hay alumnos con firma facial registrada.")
        input("\nPresione ENTER para continuar...")
        return

    rostros_conocidos, carnets_conocidos, nombres_conocidos = [], [], []

    for carnet, nombre, firma_texto in registros:
        try:
            vector_rostro = json.loads(firma_texto)
            rostros_conocidos.append(vector_rostro)
            carnets_conocidos.append(carnet)
            nombres_conocidos.append(nombre)
        except Exception:
            continue

    cap = abrir_camara()
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        input("\nPresione ENTER para continuar...")
        return

    print("Iniciando cámara... Colóquese frente al lente y presione 'ESPACIO' para verificar asistencia.")

    frame_capturado = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer datos de la cámara.")
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
                    indice = coincidencias.index(True)
                    carnet_detectado = carnets_conocidos[indice]
                    nombre_detectado = nombres_conocidos[indice]

                    print(f"\n¡Bienvenido {nombre_detectado} ({carnet_detectado})!")
                    print("Asistencia registrada exitosamente.")

                    cursor.execute("UPDATE alumnos SET asistencia = asistencia + 1 WHERE carnet = ?", (carnet_detectado,))
                    conexion.commit()
                else:
                    print("\nRostro no reconocido en el sistema.")
            else:
                print("\nNo se detectó ningún rostro en la imagen.")
        except Exception as e:
            print(f"Error durante el proceso: {e}")

    input("\nPresione ENTER para continuar...")

def seleccionar_horario():
    print("\nHorarios disponibles:")
    for key, val in DICCIONARIO_HORARIOS.items():
        print(f"{key}- {val}")
    while True:
        try:
            horario = int(input("Seleccione el índice del horario: "))
            if 1 <= horario <= 8:
                return horario
            print("Error: Ingrese un número entre 1 y 8.")
        except ValueError:
            print("Error: Ingrese un índice válido.")

def seleccionar_asignatura():
    lista = ["Programación Estructurada", "Matemática IV", "Diseño de Bases de Datos", "Sistemas Operativos y Redes"]
    print("\nAsignaturas disponibles:")
    for idx, mat in enumerate(lista, 1):
        print(f"{idx}- {mat}")
    while True:
        try:
            asig = int(input("Seleccione el índice de la asignatura: "))
            if 1 <= asig <= len(lista):
                return lista[asig - 1]
            print(f"Error: Ingrese un número entre 1 y {len(lista)}.")
        except ValueError:
            print("Error: Ingrese un índice válido.")

def registrar_alumno():
    nombre = input("Ingrese el nombre completo del alumno: ")[:40].title()
    while not nombre.replace(" ", "").isalpha():
        print("Por favor, ingrese un nombre válido (solo letras).")
        nombre = input("Ingrese el nombre completo del alumno: ")[:40].title()

    while True:
        try:
            edad = int(input("Ingrese la edad (16-80): "))
            if 16 <= edad <= 80:
                break
            print("Ingrese una edad válida (entre 16 y 80).")
        except ValueError:
            print("Error: Ingrese un número válido.")

    carnet = input("Ingrese el carnet: ").upper()
    
    correo = input("Ingrese el correo: ")
    while not validar_correo(correo):
        print("Correo no válido. Ejemplo de requerimiento: correo@catolica.edu.sv")
        correo = input("Ingrese el correo: ")

    try:
        cursor.execute(
            "INSERT INTO alumnos (carnet, nombre, edad, correo, asistencia) VALUES (?, ?, ?, ?, 0)",
            (carnet, nombre, edad, correo)
        )
        conexion.commit()

        while True:
            asig = seleccionar_asignatura()
            horario_id = seleccionar_horario()
            seccion = input("Ingrese la sección/grupo de la materia: ").title()

            cursor.execute(
                "INSERT INTO matriculas (carnet_alumno, asignatura, horario_id, seccion) VALUES (?, ?, ?, ?)",
                (carnet, asig, horario_id, seccion)
            )
            conexion.commit()
            print(f"-> Materia '{asig}' vinculada en horario ({DICCIONARIO_HORARIOS[horario_id]}).")

            otra = input("¿Desea inscribir otra materia a este alumno? (S/N): ").strip().upper()
            if otra != 'S':
                break

        print(f"\nAlumno {nombre} registrado exitosamente!")

        tomar_foto = input("¿Desea tomar la foto del rostro ahora? (S/N): ").strip().upper()
        if tomar_foto == "S":
            cap = abrir_camara()
            if cap.isOpened():
                print("Presione 'ESPACIO' para tomar la foto...")
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
            else:
                print("No se pudo abrir la cámara.")

    except sqlite3.IntegrityError:
        print(f"Error: El carnet {carnet} ya está registrado.")
        input("\nPresione ENTER para continuar...")

def mostrar_alumnos():
    cursor.execute("SELECT carnet, nombre, edad, correo, asistencia FROM alumnos")
    alumnos = cursor.fetchall()

    if alumnos:
        for al in alumnos:
            print(f"\nCarnet: {al[0]}")
            print(f"Nombre: {al[1]} | Edad: {al[2]}")
            print(f"Correo: {al[3]}")
            print(f"Asistencias registradas: {al[4]}")
            
            cursor.execute("SELECT asignatura, horario_id, seccion FROM matriculas WHERE carnet_alumno = ?", (al[0],))
            mats = cursor.fetchall()
            print("Materias inscritas:")
            for m in mats:
                print(f"  - {m[0]} | Sección: {m[2]} | Horario: {DICCIONARIO_HORARIOS.get(m[1], 'N/A')}")
            print("-" * 50)
    else:
        print("No hay alumnos registrados.")

def reporte_curso():
    cursor.execute("SELECT DISTINCT asignatura FROM matriculas")
    cursos = cursor.fetchall()

    if cursos:
        for c in cursos:
            nombre_asig = c[0]
            cursor.execute("SELECT COUNT(DISTINCT carnet_alumno) FROM matriculas WHERE asignatura = ?", (nombre_asig,))
            total = cursor.fetchone()[0]
            print(f"\nAsignatura: {nombre_asig} | Alumnos inscritos: {total}")
    else:
        print("No hay materias inscritas en el sistema.")

def buscar_alumno(carnet):
    cursor.execute("SELECT carnet, nombre, edad, correo, asistencia FROM alumnos WHERE carnet = ?", (carnet,))
    return cursor.fetchone()

def eliminar_alumno(carnet):
    cursor.execute("DELETE FROM alumnos WHERE carnet = ?", (carnet,))
    conexion.commit()

while True:
    try:
        print("\n=== Bienvenido al Sistema de Control Escolar ===")
        print("1- Ingresar como profesor")
        print("2- Ingresar como alumno (Marcar Asistencia)")
        print("3- Salir")

        menu = int(input("Seleccione una opción: "))
        clear_screen()

        if menu == 1:
            autenticado = False
            while True:
                contra = getpass.getpass("Ingrese su contraseña Ingeniero Erazo :D (o '0' para cancelar): ")
                if contra == "Catolica10":
                    autenticado = True
                    break
                elif contra == "0":
                    break
                else:
                    print("Contraseña incorrecta. Intente de nuevo.\n")

            if autenticado:
                clear_screen()
                while True:
                    print("\n--- MENÚ PROFESOR ---")
                    print("1- Registrar alumno")
                    print("2- Reporte de alumnos")
                    print("3- Reporte de cursos")
                    print("4- Buscar alumno")
                    print("5- Administrar curso")
                    print("6- Eliminar alumno")
                    print("7- Regresar al menú principal")
                    
                    opcion = input("Seleccione una opción: ")

                    if opcion == "1":
                        registrar_alumno()
                        clear_screen()
                    elif opcion == "2":
                        mostrar_alumnos()
                        input("\nPresione ENTER para regresar...")
                        clear_screen()
                    elif opcion == "3":
                        reporte_curso()
                        input("\nPresione ENTER para regresar...")
                        clear_screen()
                    elif opcion == "4":
                        carnet_b = input("Ingrese el carnet a buscar: ").upper()
                        al = buscar_alumno(carnet_b)
                        if al:
                            print(f"\nCarnet: {al[0]}\nNombre: {al[1]}\nEdad: {al[2]}\nCorreo: {al[3]}\nAsistencias: {al[4]}")
                            cursor.execute("SELECT asignatura, horario_id, seccion FROM matriculas WHERE carnet_alumno = ?", (al[0],))
                            mats = cursor.fetchall()
                            print("Materias:")
                            for m in mats:
                                print(f"  - {m[0]} ({m[2]}) en horario {DICCIONARIO_HORARIOS.get(m[1])}")
                        else:
                            print("Alumno no encontrado.")
                        input("\nPresione ENTER para regresar...")
                        clear_screen()
                    elif opcion == "5":
                        print("--- Administrar Curso ---")
                        nuevo_curso = input("Ingrese el nombre de la asignatura a modificar/crear: ")
                        cancelar = input("¿Desea justificar asistencia general para una clase? (S/N): ").strip().upper()
                        if cancelar == "S":
                            cursor.execute("UPDATE alumnos SET asistencia = asistencia + 1")
                            conexion.commit()
                            print("Asistencia incrementada a todos los alumnos.")
                        input("\nPresione ENTER para regresar...")
                        clear_screen()
                    elif opcion == "6":
                        carnet_e = input("Ingrese el carnet del alumno a eliminar: ").upper()
                        al = buscar_alumno(carnet_e)
                        if al:
                            conf = input(f"¿Eliminar a {al[1]} ({carnet_e})? (S/N): ").strip().upper()
                            if conf == "S":
                                eliminar_alumno(carnet_e)
                                print("Alumno eliminado correctamente.")
                        else:
                            print("Alumno no encontrado.")
                        input("\nPresione ENTER para regresar...")
                        clear_screen()
                    elif opcion == "7":
                        clear_screen()
                        break
                    else:
                        print("Opción no válida.")

        elif menu == 2:
            print("Ingresando como alumno...")
            tomar_asistencia_por_rostro()
            clear_screen()
        elif menu == 3:
            print("Saliendo...")
            conexion.close()
            break
        else:
            print("Opción no válida.")
    except ValueError:
        print("Error: Por favor, ingrese un número válido.")