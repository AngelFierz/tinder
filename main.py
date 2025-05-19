from Entities.usuario import Usuario
from Entities.perfil import Perfil
from Entities.matchs import Matchs
from Entities.mensajes import Mensajes
from Entities.preferencias import Preferencias
from persistence.db import SessionLocal

session = SessionLocal()


# === FUNCIONES DE USUARIO ===

def get_usuario():
    try:
        usuarios = session.query(Usuario).all()
        return usuarios  # Devuelve la lista de usuarios para que la interfaz pueda usarla
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []  # Devuelve lista vacía en caso de error


def save_usuario(nombre_usuario, correo, contraseña):
    try:
        u = Usuario(nombre_usuario=nombre_usuario, correo=correo, contraseña=contraseña)
        session.add(u)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar usuario:", e)
        return False


def update_usuario(id_usuario, nombre_usuario, correo, contraseña):
    try:
        usuario = session.get(Usuario, id_usuario)
        if usuario:
            usuario.nombre_usuario = nombre_usuario
            usuario.correo = correo
            usuario.contraseña = contraseña
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al actualizar usuario:", e)
        return False


def delete_usuario(id_usuario):
    try:
        usuario = session.get(Usuario, id_usuario)
        if usuario:
            session.delete(usuario)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al eliminar usuario:", e)
        return False


# === FUNCIONES DE PERFIL ===

def get_perfiles():
    try:
        perfiles = session.query(Perfil).all()
        return perfiles  # Devuelve la lista de perfiles
    except Exception as e:
        print("Error al obtener perfiles:", e)
        return []  # Lista vacía en caso de error


def save_perfil(nombre, genero, descripcion, hijos, id_usuario, id_preferencia):
    try:
        p = Perfil(
            nombre=nombre,
            genero=genero,
            descripcion=descripcion,
            hijos=hijos,
            id_usuario=id_usuario,
            id_preferencia=id_preferencia
        )
        session.add(p)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar perfil:", e)
        return False


def update_perfil(id_perfil, nombre, genero, descripcion, hijos, id_preferencia):
    try:
        perfil = session.get(Perfil, id_perfil)
        if perfil:
            perfil.nombre = nombre
            perfil.genero = genero
            perfil.descripcion = descripcion
            perfil.hijos = hijos
            perfil.id_preferencia = id_preferencia
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al actualizar perfil:", e)
        return False


def delete_perfil(id_perfil):
    try:
        perfil = session.get(Perfil, id_perfil)
        if perfil:
            session.delete(perfil)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al eliminar perfil:", e)
        return False


# === FUNCIONES DE PREFERENCIAS ===

def get_preferencias():
    try:
        prefs = session.query(Preferencias).all()
        return prefs  # Devuelve lista de preferencias
    except Exception as e:
        print("Error al obtener preferencias:", e)
        return []


def save_preferencia(descripcion):
    try:
        p = Preferencias(descripcion=descripcion)
        session.add(p)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar preferencia:", e)
        return False


def update_preferencia(id_preferencia, descripcion):
    try:
        pref = session.get(Preferencias, id_preferencia)
        if pref:
            pref.descripcion = descripcion
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al actualizar preferencia:", e)
        return False


def delete_preferencia(id_preferencia):
    try:
        pref = session.get(Preferencias, id_preferencia)
        if pref:
            session.delete(pref)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al eliminar preferencia:", e)
        return False


# === FUNCIONES DE MATCHS ===
def get_matchs():
    try:
        matchs = session.query(Matchs).all()
        return matchs  # Devuelve la lista de matchs
    except Exception as e:
        print("Error al obtener matchs:", e)
        return []


def save_match(id_perfil1, id_perfil2):
    try:
        m = Matchs(id_perfil1=id_perfil1, id_perfil2=id_perfil2)
        session.add(m)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar match:", e)
        return False


def update_match(id_match, id_perfil1, id_perfil2):
    try:
        match = session.get(Matchs, id_match)
        if match:
            match.id_perfil1 = id_perfil1
            match.id_perfil2 = id_perfil2
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al actualizar match:", e)
        return False


def delete_match(id_match):
    try:
        match = session.get(Matchs, id_match)
        if match:
            session.delete(match)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al eliminar match:", e)
        return False


# === FUNCIONES DE MENSAJES ===
def get_mensajes():
    try:
        mensajes = session.query(Mensajes).all()
        return mensajes  # Devuelve la lista de mensajes
    except Exception as e:
        print("Error al obtener mensajes:", e)
        return []


def save_mensaje(id_remitente, id_destinatario, contenido):
    try:
        msj = Mensajes(id_remitente=id_remitente, id_destinatario=id_destinatario, contenido=contenido)
        session.add(msj)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print("Error al guardar mensaje:", e)
        return False


def update_mensaje(id_mensaje, id_remitente, id_destinatario, contenido):
    try:
        msj = session.get(Mensajes, id_mensaje)
        if msj:
            msj.id_remitente = id_remitente
            msj.id_destinatario = id_destinatario
            msj.contenido = contenido
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al actualizar mensaje:", e)
        return False


def delete_mensaje(id_mensaje):
    try:
        msj = session.get(Mensajes, id_mensaje)
        if msj:
            session.delete(msj)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        print("Error al eliminar mensaje:", e)
        return False


# === MENÚ PRINCIPAL ===

def menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Usuario")
        print("2. Perfil")
        print("3. Preferencias")
        print("4. Matchs")
        print("5. Mensajes")
        print("6. Salir")
        opcion_tabla = input("Selecciona una tabla (1-6): ")

        if opcion_tabla == "6":
            print("Saliendo del programa.")
            break

        if opcion_tabla not in ["1", "2", "3", "4", "5"]:
            print("Opción no válida.")
            continue

        print("\n--- ACCIONES DISPONIBLES ---")
        print("1. Mostrar registros")
        print("2. Agregar nuevo registro")
        print("3. Editar registro existente")
        print("4. Eliminar registro")
        print("5. Volver")

        opcion_accion = input("Selecciona una acción (1-5): ")
        if opcion_accion == "5":
            continue

        try:
            # === USUARIOS ===
            if opcion_tabla == "1":
                if opcion_accion == "1":
                    get_usuario()
                elif opcion_accion == "2":
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    contraseña = input("Contraseña: ")
                    save_usuario(nombre, correo, contraseña)
                elif opcion_accion == "3":
                    idu = int(input("ID del usuario: "))
                    nombre = input("Nuevo nombre: ")
                    correo = input("Nuevo correo: ")
                    contraseña = input("Nueva contraseña: ")
                    update_usuario(idu, nombre, correo, contraseña)
                elif opcion_accion == "4":
                    idu = int(input("ID del usuario: "))
                    delete_usuario(idu)

            # === PERFILES ===
            elif opcion_tabla == "2":
                if opcion_accion == "1":
                    get_perfiles()
                elif opcion_accion == "2":
                    nombre = input("Nombre: ")
                    genero = input("Género: ")
                    descripcion = input("Descripción: ")
                    hijos = int(input("Hijos (número): "))
                    id_usuario = int(input("ID de usuario: "))
                    id_preferencia = int(input("ID de preferencia: "))
                    save_perfil(nombre, genero, descripcion, hijos, id_usuario, id_preferencia)
                elif opcion_accion == "3":
                    idp = int(input("ID del perfil: "))
                    nombre = input("Nuevo nombre: ")
                    genero = input("Nuevo género: ")
                    descripcion = input("Nueva descripción: ")
                    hijos = int(input("Hijos (número): "))
                    id_preferencia = int(input("Nuevo ID de preferencia: "))
                    update_perfil(idp, nombre, genero, descripcion, hijos, id_preferencia)
                elif opcion_accion == "4":
                    idp = int(input("ID del perfil: "))
                    delete_perfil(idp)

            # === PREFERENCIAS ===
            elif opcion_tabla == "3":
                if opcion_accion == "1":
                    get_preferencias()
                elif opcion_accion == "2":
                    descripcion = input("Descripción: ")
                    save_preferencia(descripcion)
                elif opcion_accion == "3":
                    idpref = int(input("ID de preferencia: "))
                    descripcion = input("Nueva descripción: ")
                    update_preferencia(idpref, descripcion)
                elif opcion_accion == "4":
                    idpref = int(input("ID de preferencia: "))
                    delete_preferencia(idpref)

            # === MATCHS ===
            elif opcion_tabla == "4":
                if opcion_accion == "1":
                    get_matchs()
                elif opcion_accion == "2":
                    id1 = int(input("ID Perfil 1: "))
                    id2 = int(input("ID Perfil 2: "))
                    save_match(id1, id2)
                elif opcion_accion == "3":
                    idm = int(input("ID del match: "))
                    id1 = int(input("Nuevo ID Perfil 1: "))
                    id2 = int(input("Nuevo ID Perfil 2: "))
                    update_match(idm, id1, id2)
                elif opcion_accion == "4":
                    idm = int(input("ID del match: "))
                    delete_match(idm)

            # === MENSAJES ===
            elif opcion_tabla == "5":
                if opcion_accion == "1":
                    get_mensajes()
                elif opcion_accion == "2":
                    idr = int(input("ID Remitente: "))
                    idd = int(input("ID Destinatario: "))
                    contenido = input("Mensaje: ")
                    save_mensaje(idr, idd, contenido)
                elif opcion_accion == "3":
                    idm = int(input("ID del mensaje: "))
                    idr = int(input("Nuevo ID Remitente: "))
                    idd = int(input("Nuevo ID Destinatario: "))
                    contenido = input("Nuevo mensaje: ")
                    update_mensaje(idm, idr, idd, contenido)
                elif opcion_accion == "4":
                    idm = int(input("ID del mensaje: "))
                    delete_mensaje(idm)

        except ValueError:
            print("Por favor, ingresa un número válido para los IDs o cantidades.")
        except Exception as e:
            print("Error:", e)


# === EJECUTAR PROGRAMA ===

if __name__ == "__main__":
    menu()

