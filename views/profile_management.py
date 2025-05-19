import tkinter as tk
from tkinter import messagebox
from main import save_perfil, update_perfil, delete_perfil, get_perfiles

class ProfileManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Perfiles")
        self.geometry("400x500")

        # Entradas
        tk.Label(self, text="ID (para actualizar/eliminar):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)

        tk.Label(self, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=1, column=1)

        tk.Label(self, text="Género:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_genero = tk.Entry(self)
        self.entry_genero.grid(row=2, column=1)

        tk.Label(self, text="Descripción:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_descripcion = tk.Entry(self)
        self.entry_descripcion.grid(row=3, column=1)

        tk.Label(self, text="Hijos:").grid(row=4, column=0, padx=10, pady=5)
        self.entry_hijos = tk.Entry(self)
        self.entry_hijos.grid(row=4, column=1)

        tk.Label(self, text="ID Usuario:").grid(row=5, column=0, padx=10, pady=5)
        self.entry_id_usuario = tk.Entry(self)
        self.entry_id_usuario.grid(row=5, column=1)

        tk.Label(self, text="ID Preferencia:").grid(row=6, column=0, padx=10, pady=5)
        self.entry_id_preferencia = tk.Entry(self)
        self.entry_id_preferencia.grid(row=6, column=1)

        # Botones
        tk.Button(self, text="Crear Perfil", command=self.create_perfil).grid(row=7, column=0, pady=10)
        tk.Button(self, text="Actualizar Perfil", command=self.update_perfil).grid(row=7, column=1, pady=10)
        tk.Button(self, text="Eliminar Perfil", command=self.delete_perfil).grid(row=8, column=0, pady=10)
        tk.Button(self, text="Ver Perfiles", command=self.view_perfiles).grid(row=8, column=1, pady=10)

    def create_perfil(self):
        nombre = self.entry_nombre.get()
        genero = self.entry_genero.get()
        descripcion = self.entry_descripcion.get()
        hijos = self.entry_hijos.get()
        id_usuario = self.entry_id_usuario.get()
        id_preferencia = self.entry_id_preferencia.get()

        # Validación de campos obligatorios
        if not nombre or not genero or not descripcion or not hijos:
            messagebox.showerror("Error", "Los campos Nombre, Género, Descripción y Hijos son obligatorios.")
            return

        try:
            save_perfil(
                nombre=nombre,
                genero=genero,
                descripcion=descripcion,
                hijos=int(hijos),
                id_usuario=int(id_usuario) if id_usuario else None,
                id_preferencia=int(id_preferencia) if id_preferencia else None
            )
            messagebox.showinfo("Éxito", "Perfil creado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear perfil: {e}")

    def update_perfil(self):
        perfil_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        genero = self.entry_genero.get()
        descripcion = self.entry_descripcion.get()
        hijos = self.entry_hijos.get()
        id_preferencia = self.entry_id_preferencia.get()

        if not perfil_id:
            messagebox.showerror("Error", "ID del perfil es obligatorio para actualizar.")
            return

        if not nombre or not genero or not descripcion or not hijos:
            messagebox.showerror("Error", "Todos los campos excepto ID Usuario son obligatorios para actualizar.")
            return

        try:
            update_perfil(
                id_perfil=int(perfil_id),
                nombre=nombre,
                genero=genero,
                descripcion=descripcion,
                hijos=int(hijos),
                id_preferencia=int(id_preferencia) if id_preferencia else None
            )
            messagebox.showinfo("Éxito", "Perfil actualizado.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar perfil: {e}")

    def delete_perfil(self):
        perfil_id = self.entry_id.get()

        if not perfil_id:
            messagebox.showerror("Error", "ID del perfil es obligatorio para eliminar.")
            return

        try:
            delete_perfil(int(perfil_id))
            messagebox.showinfo("Éxito", "Perfil eliminado.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar perfil: {e}")

    def view_perfiles(self):
        try:
            perfiles = get_perfiles()
            if perfiles:
                perfiles_str = "\n".join([
                    f"ID: {p.id_perfil} | Nombre: {p.nombre} | Género: {p.genero} | Usuario: {p.id_usuario} | Preferencia: {p.id_preferencia}"
                    for p in perfiles
                ])
            else:
                perfiles_str = "No hay perfiles registrados."

            messagebox.showinfo("Perfiles", perfiles_str)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener perfiles: {e}")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_hijos.delete(0, tk.END)
        self.entry_id_usuario.delete(0, tk.END)
        self.entry_id_preferencia.delete(0, tk.END)

