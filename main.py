from Entities.usuario import Usuario
from persistence.db import SessionLocal
session = SessionLocal()


#Funciones de Usuario
def get_usuario():
    usuarios = session.query(Usuario).all()

    for u in usuarios:
        print(f"Nombre: {u.nombre_usuario}")

def save_usuario(nombre_usuario, correo, contraseña):
    u = Usuario(nombre_usuario=nombre_usuario, correo=correo, contraseña=contraseña)
    session.add(u)
    session.commit()
    print(f"Se agregó el registro {u.nombre_usuario}")

def update_usuario(id_usuario, nombre_usuario, correo, contraseña):
    usuario = session.query(Usuario).get(id_usuario)
    if usuario:
        usuario.nombre_usuario = nombre_usuario
        usuario.correo = correo
        usuario.contraseña = contraseña
        session.commit()
        print(f"Registro {id_usuario} actualizado")
    else:
        print("Registro no encontrado")

def delete(id_usuario):
    usuario = session.query(Usuario).get(id_usuario)
    if usuario:
        session.delete(usuario)
        session.commit()
        print(f"Registro {id_usuario} eliminado")
    else:
        print("Registro no encontrado")        

get_usuario()