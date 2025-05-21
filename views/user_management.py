import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from persistence.db import SessionLocal
from Entities.usuario import Usuario
from main import save_usuario, get_usuario, delete_usuario, update_usuario  # Importamos las funciones

class UserManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("550x380")

        # Tabla
        self.tree = ttk.Treeview(
            self,
            columns=("id", "nombre", "correo"),
            show="headings",
            height=8
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("correo", text="Correo")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=150)
        self.tree.column("correo", width=200)
        self.tree.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="nsew")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky="ns", pady=(10, 0))

        # Botones
        tk.Button(self, text="Agregar",  command=self.open_add_window, width=12).grid(row=1, column=0, pady=15)
        tk.Button(self, text="Editar",   command=self.open_edit_window, width=12).grid(row=1, column=1, pady=15)
        tk.Button(self, text="Eliminar", command=self.delete_user, width=12).grid(row=1, column=2, pady=15)

        # Ajustar expansión de filas/columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Cargar usuarios al arrancar
        self.load_users()

    # Cargar datos
    def load_users(self):
        """Vuelve a cargar la tabla completa"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            for u in get_usuario():
                self.tree.insert("", "end", values=(u.id_usuario, u.nombre_usuario, u.correo))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener usuarios: {e}")

    # Eliminar
    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Selecciona un usuario para eliminar.")

        values = self.tree.item(selected[0], "values")
        user_id = int(values[0])

        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario {user_id}?"):
            try:
                delete_usuario(user_id)
                self.load_users()
                messagebox.showinfo("Éxito", "Usuario eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    # Ventana: Agregar
    def open_add_window(self):
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Usuario")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Correo:").pack(pady=5)
        entry_correo = tk.Entry(ventana)
        entry_correo.pack()

        tk.Label(ventana, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(ventana, show="*")
        entry_contrasena.pack()

        def guardar():
            nombre = entry_nombre.get().strip()
            correo = entry_correo.get().strip()
            contrasena = entry_contrasena.get().strip()

            if not (nombre and correo and contrasena):
                return messagebox.showerror("Error", "Todos los campos son obligatorios.")

            try:
                save_usuario(nombre, correo, contrasena)
                self.load_users()
                ventana.destroy()
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear: {e}")

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    # Ventana: Editar
    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Selecciona un usuario para editar.")

        values = self.tree.item(selected[0], "values")
        user_id, nombre_actual, correo_actual = values

        ventana = tk.Toplevel(self)
        ventana.title("Editar Usuario")
        ventana.geometry("300x230")

        tk.Label(ventana, text=f"ID: {user_id}").pack(pady=5)

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        tk.Label(ventana, text="Correo:").pack(pady=5)
        entry_correo = tk.Entry(ventana)
        entry_correo.insert(0, correo_actual)
        entry_correo.pack()

        tk.Label(ventana, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(ventana, show="*")
        entry_contrasena.pack()

        def actualizar():
            nombre = entry_nombre.get().strip()
            correo = entry_correo.get().strip()
            contrasena = entry_contrasena.get().strip()

            if not (nombre and correo and contrasena):
                return messagebox.showerror("Error", "Todos los campos son obligatorios.")

            try:
                update_usuario(int(user_id), nombre, correo, contrasena)
                self.load_users()
                ventana.destroy()
                messagebox.showinfo("Éxito", "Usuario actualizado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        tk.Button(ventana, text="Guardar Cambios", command=actualizar).pack(pady=10)