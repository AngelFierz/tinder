import tkinter as tk
from tkinter import messagebox
from persistence.db import SessionLocal
from Entities.usuario import Usuario
from main import save_usuario, get_usuario, delete_usuario, update_usuario  # Importamos las funciones

class UserManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("400x300")

        # Entradas
        tk.Label(self, text="ID (para actualizar/eliminar):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)

        tk.Label(self, text="Nombre Usuario:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=1, column=1)

        tk.Label(self, text="Correo:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_correo = tk.Entry(self)
        self.entry_correo.grid(row=2, column=1)

        tk.Label(self, text="Contraseña:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_contrasena = tk.Entry(self, show="*")
        self.entry_contrasena.grid(row=3, column=1)

        # Botones
        tk.Button(self, text="Crear Usuario", command=self.create_user).grid(row=4, column=0, pady=10)
        tk.Button(self, text="Actualizar Usuario", command=self.update_user).grid(row=4, column=1, pady=10)
        tk.Button(self, text="Eliminar Usuario", command=self.delete_user).grid(row=5, column=0, pady=10)
        tk.Button(self, text="Ver Usuarios", command=self.view_users).grid(row=5, column=1, pady=10)

    def create_user(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()

        if not nombre or not correo or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            save_usuario(nombre, correo, contrasena)
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {e}")

    def update_user(self):
        user_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        contrasena = self.entry_contrasena.get()

        if not user_id or not nombre or not correo or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            
            update_usuario(int(user_id), nombre, correo, contrasena)
            messagebox.showinfo("Éxito", "Usuario actualizado.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {e}")

    def delete_user(self):
        user_id = self.entry_id.get()

        if not user_id:
            messagebox.showerror("Error", "ID requerido para eliminar.")
            return

        try:
            
            delete_usuario(int(user_id))
            messagebox.showinfo("Éxito", "Usuario eliminado.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario: {e}")

    def view_users(self):
        try:
           
            usuarios = get_usuario()
            usuarios_str = "\n".join([f"{u.id_usuario}: {u.nombre_usuario} - {u.correo}" for u in usuarios])
            messagebox.showinfo("Usuarios", usuarios_str)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")

    def clear_fields(self):
        """Limpia todos los campos de entrada"""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
