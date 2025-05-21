import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Scrollbar
from persistence.db import SessionLocal
from Entities.usuario import Usuario
from main import save_usuario, get_usuario, delete_usuario, update_usuario

class UserManagement(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("600x400")
        self.configure(fg_color="#1a1a1a")

        color_base = "#880d1e"
        color_hover = "#dd2d4a"

        opciones_boton = {
            "fg_color": color_base,
            "hover_color": color_hover,
            "corner_radius": 3,
            "text_color": "white",
            "font": ("Arial", 12, "bold"),
            "width": 160
        }

        # Tabla
        style = Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#461220",
                        foreground="white",
                        fieldbackground="#461220",
                        rowheight=25,
                        font=("Arial", 13, "bold"))
        style.configure("Treeview.Heading",
                        background=color_base,
                        foreground="white",
                        font=("Arial", 14, "bold"))

        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = Treeview(table_frame, columns=("id", "nombre", "correo"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("correo", text="Correo")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=150)
        self.tree.column("correo", width=250)
        self.tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Botones
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Agregar", command=self.open_add_window, **opciones_boton).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Editar", command=self.open_edit_window, **opciones_boton).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.delete_user, **opciones_boton).grid(row=0, column=2, padx=10)

        self.load_users()

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        try:
            for u in get_usuario():
                self.tree.insert("", "end", values=(u.id_usuario, u.nombre_usuario, u.correo))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener usuarios: {e}")

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Selecciona un usuario para eliminar.")

        user_id = int(self.tree.item(selected[0], "values")[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario {user_id}?"):
            try:
                delete_usuario(user_id)
                self.load_users()
                messagebox.showinfo("Éxito", "Usuario eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def open_add_window(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Usuario")
        ventana.geometry("300x250")
        ventana.configure(fg_color="#2b2b2b")

        ctk.CTkLabel(ventana, text="Nombre:", text_color="white").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.pack()

        ctk.CTkLabel(ventana, text="Correo:", text_color="white").pack(pady=5)
        entry_correo = ctk.CTkEntry(ventana)
        entry_correo.pack()

        ctk.CTkLabel(ventana, text="Contraseña:", text_color="white").pack(pady=5)
        entry_contrasena = ctk.CTkEntry(ventana, show="*")
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

        ctk.CTkButton(ventana, text="Guardar", command=guardar,
                      fg_color="#0f5132", hover_color="#198754", text_color="white").pack(pady=10)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Selecciona un usuario para editar.")

        values = self.tree.item(selected[0], "values")
        user_id, nombre_actual, correo_actual = values

        ventana = ctk.CTkToplevel(self)
        ventana.title("Editar Usuario")
        ventana.geometry("300x260")
        ventana.configure(fg_color="#2b2b2b")

        ctk.CTkLabel(ventana, text=f"ID: {user_id}", text_color="white").pack(pady=5)

        ctk.CTkLabel(ventana, text="Nombre:", text_color="white").pack(pady=5)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        ctk.CTkLabel(ventana, text="Correo:", text_color="white").pack(pady=5)
        entry_correo = ctk.CTkEntry(ventana)
        entry_correo.insert(0, correo_actual)
        entry_correo.pack()

        ctk.CTkLabel(ventana, text="Contraseña:", text_color="white").pack(pady=5)
        entry_contrasena = ctk.CTkEntry(ventana, show="*")
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

        ctk.CTkButton(ventana, text="Guardar Cambios", command=actualizar,
                      fg_color="#0d3b66", hover_color="#1e6091", text_color="white").pack(pady=10)
