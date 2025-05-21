import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Combobox
from main import save_perfil, update_perfil, delete_perfil, get_perfiles
from Entities.usuario import Usuario
from Entities.preferencias import Preferencias
from Entities.perfil import Perfil
from persistence.db import SessionLocal


class ProfileManagement(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Perfiles")
        self.geometry("950x500")
        self.configure(fg_color="#1a1a1a")

        color_base = "#880d1e"
        color_hover = "#dd2d4a"

        opciones_boton = {
            "fg_color": color_base,
            "hover_color": color_hover,
            "corner_radius": 3,
            "text_color": "white",
            "font": ("Arial", 12, "bold"),
            "width": 180
        }

        # Frame de tabla
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#461220",
                        foreground="white",
                        fieldbackground="#461220",
                        rowheight=25,
                        font=("Arial", 12, "bold"))
        style.configure("Treeview.Heading",
                        background=color_base,
                        foreground="white",
                        font=("Arial", 14, "bold"))

        columns = ("id", "nombre", "genero", "descripcion", "hijos", "usuario", "preferencia")
        self.tree = Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        column_widths = {
            "id": 50,
            "nombre": 100,
            "genero": 80,
            "descripcion": 220,
            "hijos": 60,
            "usuario": 140,
            "preferencia": 140
        }

        for col in columns:
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ctk.CTkScrollbar(table_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Botones
        ctk.CTkButton(self, text="Agregar Perfil", command=self.open_add_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Editar Perfil", command=self.open_edit_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Eliminar Perfil", command=self.delete_selected_profile, **opciones_boton).pack(pady=5)

        self.load_profiles()

    def load_profiles(self):
        self.tree.delete(*self.tree.get_children())
        perfiles = get_perfiles()
        db = SessionLocal()
        usuarios = {u.id_usuario: u.nombre_usuario for u in db.query(Usuario).all()}
        preferencias = {p.id_preferencia: p.descripcion for p in db.query(Preferencias).all()}
        db.close()

        self.perfil_id_map = {}

        for p in perfiles:
            self.tree.insert("", "end", values=(
                p.id_perfil,
                p.nombre,
                p.genero,
                p.descripcion,
                p.hijos,
                usuarios.get(p.id_usuario, f"Usuario {p.id_usuario}"),
                preferencias.get(p.id_preferencia, f"Preferencia {p.id_preferencia}")
            ))
            self.perfil_id_map[p.id_perfil] = {
                "id_usuario": p.id_usuario,
                "id_preferencia": p.id_preferencia
            }

    def open_add_window(self):
        self.open_form_window("Agregar")

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un perfil para editar.")
            return

        values = self.tree.item(selected[0])["values"]
        id_perfil = values[0]

        ids_reales = self.perfil_id_map.get(id_perfil, {})
        id_usuario = ids_reales.get("id_usuario")
        id_preferencia = ids_reales.get("id_preferencia")

        self.open_form_window("Editar", values, id_usuario, id_preferencia)

    def open_form_window(self, mode, values=None, id_usuario=None, id_preferencia=None):
        form = ctk.CTkToplevel(self)
        form.title(f"{mode} Perfil")
        form.geometry("400x420")
        form.configure(fg_color="#1a1a1a")

        db = SessionLocal()
        usuarios = db.query(Usuario).all()
        preferencias = db.query(Preferencias).all()
        db.close()

        labels = ["Nombre", "Género", "Descripción", "Hijos"]
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(form, text=label + ":", text_color="white").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(form, width=200)
            entry.grid(row=i, column=1, pady=5)
            self.entries[label.lower()] = entry

        ctk.CTkLabel(form, text="Usuario:", text_color="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        cb_usuario = Combobox(form, values=[f"{u.id_usuario} - {u.nombre_usuario}" for u in usuarios], state="readonly")
        cb_usuario.grid(row=4, column=1, pady=5)

        ctk.CTkLabel(form, text="Preferencia:", text_color="white").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        cb_preferencia = Combobox(form, values=[f"{p.id_preferencia} - {p.descripcion}" for p in preferencias], state="readonly")
        cb_preferencia.grid(row=5, column=1, pady=5)

        if mode == "Editar" and values:
            id_perfil, nombre, genero, descripcion, hijos, _, _ = values
            self.entries["nombre"].insert(0, nombre)
            self.entries["género"].insert(0, genero)
            self.entries["descripción"].insert(0, descripcion)
            self.entries["hijos"].insert(0, hijos)

            if id_usuario is not None:
                for u in usuarios:
                    if u.id_usuario == id_usuario:
                        cb_usuario.set(f"{u.id_usuario} - {u.nombre_usuario}")
                        break
            if id_preferencia is not None:
                for p in preferencias:
                    if p.id_preferencia == id_preferencia:
                        cb_preferencia.set(f"{p.id_preferencia} - {p.descripcion}")
                        break

        def submit():
            try:
                nombre = self.entries["nombre"].get()
                genero = self.entries["género"].get()
                descripcion = self.entries["descripción"].get()
                hijos = self.entries["hijos"].get()
                id_usuario_val = int(cb_usuario.get().split(" - ")[0])
                id_preferencia_val = int(cb_preferencia.get().split(" - ")[0])

                if not all([nombre, genero, descripcion, hijos]):
                    raise ValueError("Todos los campos son obligatorios.")

                db = SessionLocal()
                existing = db.query(Perfil).filter_by(id_usuario=id_usuario_val).first()
                db.close()

                if mode == "Agregar":
                    if existing:
                        messagebox.showerror("Error", "Este usuario ya tiene un perfil asignado.")
                        return
                    save_perfil(nombre, genero, descripcion, hijos, id_usuario_val, id_preferencia_val)
                    messagebox.showinfo("Éxito", "Perfil creado.")
                else:
                    if existing and existing.id_perfil != id_perfil:
                        messagebox.showerror("Error", "Este usuario ya tiene un perfil asignado.")
                        return
                    update_perfil(id_perfil, nombre, genero, descripcion, hijos, id_usuario_val, id_preferencia_val)
                    messagebox.showinfo("Éxito", "Perfil actualizado.")

                form.destroy()
                self.load_profiles()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form, text="Guardar", command=submit,
                      fg_color="#0f5132", hover_color="#198754", text_color="white").grid(row=6, column=0, columnspan=2, pady=10)
        ctk.CTkButton(form, text="Cancelar", command=form.destroy,
                      fg_color=color_base, hover_color=color_hover, text_color="white").grid(row=7, column=0, columnspan=2, pady=5)

    def delete_selected_profile(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un perfil para eliminar.")
            return

        perfil_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este perfil?"):
            try:
                delete_perfil(int(perfil_id))
                self.load_profiles()
                messagebox.showinfo("Éxito", "Perfil eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el perfil: {e}")
