import tkinter as tk
from tkinter import messagebox, ttk
from main import save_perfil, update_perfil, delete_perfil, get_perfiles
from Entities.usuario import Usuario
from Entities.preferencias import Preferencias
from Entities.perfil import Perfil
from persistence.db import SessionLocal

class ProfileManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Perfiles")
        self.geometry("900x400")

        # Frame contenedor para Treeview y scrollbars
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("id", "nombre", "genero", "descripcion", "hijos", "usuario", "preferencia"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())

        # Establecer ancho para cada columna
        column_widths = {
            "id": 50,
            "nombre": 100,
            "genero": 70,
            "descripcion": 200,
            "hijos": 60,
            "usuario": 120,
            "preferencia": 100
        }
        for col in self.tree["columns"]:
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center")

        # Scrollbars
        scrollbar_y = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = tk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Posicionar con grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Expansión automática
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        # Configurar el tamaño mínimo de la ventana

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Perfil", command=self.open_add_window).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Perfil", command=self.open_edit_window).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Perfil", command=self.delete_selected_profile).grid(row=0, column=2, padx=5)

        self.load_profiles()

    def load_profiles(self):
        """Carga los perfiles desde la base de datos en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        perfiles = get_perfiles()
        db = SessionLocal()
        usuarios = {u.id_usuario: u.nombre_usuario for u in db.query(Usuario).all()}
        preferencias = {p.id_preferencia: p.descripcion for p in db.query(Preferencias).all()}
        db.close()

        self.perfil_id_map = {}  # Inicializa aquí correctamente

        for p in perfiles:
            self.tree.insert("", tk.END, values=(
                p.id_perfil,
                p.nombre,
                p.genero,
                p.descripcion,
                p.hijos,
                usuarios.get(p.id_usuario, f"Usuario {p.id_usuario}"),
                preferencias.get(p.id_preferencia, f"Preferencia {p.id_preferencia}")
            ))

            # Guarda los IDs correctos para cada perfil
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
        """Formulario para agregar o editar perfiles"""
        form = tk.Toplevel(self)
        form.title(f"{mode} Perfil")
        form.geometry("400x400")

        db = SessionLocal()
        usuarios = db.query(Usuario).all()
        preferencias = db.query(Preferencias).all()
        db.close()

        # Crear campos
        labels = ["Nombre", "Género", "Descripción", "Hijos", "Usuario", "Preferencia"]
        self.entries = {}

        for i, label in enumerate(labels[:4]):  # Solo los primeros 4 son Entry
            tk.Label(form, text=label + ":").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, pady=5)
            self.entries[label.lower()] = entry

        # ComboBox para Usuario
        tk.Label(form, text="Usuario:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        cb_usuario = ttk.Combobox(form, state="readonly")
        cb_usuario['values'] = [f"{u.id_usuario} - {u.nombre_usuario}" for u in usuarios]
        cb_usuario.grid(row=4, column=1, pady=5)

        # ComboBox para Preferencia
        tk.Label(form, text="Preferencia:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        cb_preferencia = ttk.Combobox(form, state="readonly")
        cb_preferencia['values'] = [f"{p.id_preferencia} - {p.descripcion}" for p in preferencias]
        cb_preferencia.grid(row=5, column=1, pady=5)

        # Cargar datos si es edición
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


        # Función para guardar
        def submit():
            try:
                nombre = self.entries["nombre"].get()
                genero = self.entries["género"].get()
                descripcion = self.entries["descripción"].get()
                hijos = self.entries["hijos"].get()
                id_usuario = int(cb_usuario.get().split(" - ")[0])
                id_preferencia = int(cb_preferencia.get().split(" - ")[0])

                if not all([nombre, genero, descripcion, hijos]):
                    raise ValueError("Todos los campos deben estar llenos.")

                db = SessionLocal()
                existing = db.query(Perfil).filter_by(id_usuario=id_usuario).first()
                db.close()

                if mode == "Agregar":
                    if existing:
                        messagebox.showerror("Error", "Este usuario ya tiene un perfil asignado.")
                        return
                    save_perfil(nombre, genero, descripcion, hijos, id_usuario, id_preferencia)
                    messagebox.showinfo("Éxito", "Perfil creado.")
                else:
                    # Validar que no se asigne un usuario que ya tiene otro perfil
                    if existing and existing.id_perfil != id_perfil:
                        messagebox.showerror("Error", "Este usuario ya tiene un perfil asignado.")
                        return
                    update_perfil(id_perfil, nombre, genero, descripcion, hijos, id_usuario, id_preferencia)
                    messagebox.showinfo("Éxito", "Perfil actualizado.")

                form.destroy()
                self.load_profiles()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Botones
        tk.Button(form, text="Guardar", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(form, text="Cancelar", command=form.destroy).grid(row=7, column=0, columnspan=2, pady=5)


    def save_profile(self, mode):
        try:
            perfil_data = {
                key: self.entries[key].get() for key in self.entries               
            }

            # Validación mínima
            if not perfil_data["nombre"] or not perfil_data["genero"] or not perfil_data["descripcion"] or not perfil_data["hijos"]:
                messagebox.showerror("Error", "Los campos Nombre, Género, Descripción y Hijos son obligatorios.")
                return

            if mode == "Agregar":
                save_perfil(
                    nombre=perfil_data["nombre"],
                    genero=perfil_data["genero"],
                    descripcion=perfil_data["descripcion"],
                    hijos=int(perfil_data["hijos"]),
                    id_usuario=int(perfil_data["id usuario"]) if perfil_data["id usuario"] else None,
                    id_preferencia=int(perfil_data["id preferencia"]) if perfil_data["id preferencia"] else None
                )
                messagebox.showinfo("Éxito", "Perfil creado correctamente.")
            else:
                update_perfil(
                    id_perfil=int(perfil_data["id"]),
                    nombre=perfil_data["nombre"],
                    genero=perfil_data["genero"],
                    descripcion=perfil_data["descripcion"],
                    hijos=int(perfil_data["hijos"]),
                    id_usuario=int(perfil_data["id usuario"]) if perfil_data["id usuario"] else None,
                    id_preferencia=int(perfil_data["id preferencia"]) if perfil_data["id preferencia"] else None                   
                )
                messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")

            self.load_profiles()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

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