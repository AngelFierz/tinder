import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from persistence.db import SessionLocal
from Entities.usuario import Usuario
from main import save_usuario, get_usuario, delete_usuario, update_usuario

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  

class UserManagement(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("600x400")
        
        self.color_primary = "#880d1e"
        self.color_accent = "#dd2d4a"
        self.color_bg = "#262626"
        self.configure(fg_color=self.color_bg)

        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("Custom.Treeview",
                        background=self.color_bg,
                        fieldbackground=self.color_bg,
                        foreground="white",
                        font=("Arial", 14, "bold"))
        style.configure("Custom.Treeview.Heading",
                        background=self.color_primary,
                        foreground="white",
                        font=("Arial", 16, "bold"))

        style.map("Custom.Treeview",
                  background=[("selected", self.color_accent)],
                  foreground=[("selected", "white")])

        self.tree = ttk.Treeview(
            self,
            columns=("id", "nombre", "correo"),
            show="headings",
            height=8,
            style="Custom.Treeview"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("correo", text="Correo")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=180)
        self.tree.column("correo", width=280)
        self.tree.grid(row=0, column=0, columnspan=4, padx=15, pady=(15, 0), sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=4, sticky="ns", pady=(15, 0))

        btn_agregar = ctk.CTkButton(self, text="Agregar", width=120, fg_color=self.color_primary,
                                    hover_color=self.color_accent, command=self.open_add_window)
        btn_editar = ctk.CTkButton(self, text="Editar", width=120, fg_color=self.color_primary,
                                   hover_color=self.color_accent, command=self.open_edit_window)
        btn_eliminar = ctk.CTkButton(self, text="Eliminar", width=120, fg_color=self.color_primary,
                                     hover_color=self.color_accent, command=self.delete_user)

        btn_agregar.grid(row=1, column=0, pady=20, padx=10, sticky="ew")
        btn_editar.grid(row=1, column=1, pady=20, padx=10, sticky="ew")
        btn_eliminar.grid(row=1, column=2, pady=20, padx=10, sticky="ew")

        # Ajustar expansión
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.load_users()

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            for u in get_usuario():
                self.tree.insert("", "end", values=(u.id_usuario, u.nombre_usuario, u.correo))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener usuarios: {e}")

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

    def open_add_window(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Usuario")
        ventana.geometry("350x250")
        ventana.configure(fg_color=self.color_bg)

        # Entradas con etiquetas ctk y colores aplicados
        ctk.CTkLabel(ventana, text="Nombre:", text_color="white").pack(pady=(15, 5))
        entry_nombre = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white")
        entry_nombre.pack()

        ctk.CTkLabel(ventana, text="Correo:", text_color="white").pack(pady=(15, 5))
        entry_correo = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white")
        entry_correo.pack()

        ctk.CTkLabel(ventana, text="Contraseña:", text_color="white").pack(pady=(15, 5))
        entry_contrasena = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white", show="*")
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

        ctk.CTkButton(ventana, text="Guardar", width=100, fg_color=self.color_primary,
                      hover_color=self.color_accent, command=guardar).pack(pady=20)

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showerror("Error", "Selecciona un usuario para editar.")

        values = self.tree.item(selected[0], "values")
        user_id, nombre_actual, correo_actual = values

        ventana = ctk.CTkToplevel(self)
        ventana.title("Editar Usuario")
        ventana.geometry("350x280")
        ventana.configure(fg_color=self.color_bg)

        ctk.CTkLabel(ventana, text=f"ID: {user_id}", text_color="white").pack(pady=(15, 5))

        ctk.CTkLabel(ventana, text="Nombre:", text_color="white").pack(pady=(10, 5))
        entry_nombre = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white")
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack()

        ctk.CTkLabel(ventana, text="Correo:", text_color="white").pack(pady=(10, 5))
        entry_correo = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white")
        entry_correo.insert(0, correo_actual)
        entry_correo.pack()

        ctk.CTkLabel(ventana, text="Contraseña:", text_color="white").pack(pady=(10, 5))
        entry_contrasena = ctk.CTkEntry(ventana, width=280, fg_color="#461220", text_color="white", show="*")
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

        ctk.CTkButton(ventana, text="Guardar Cambios", width=140, fg_color=self.color_primary,
                      hover_color=self.color_accent, command=actualizar).pack(pady=20)
