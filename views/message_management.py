import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Scrollbar, Combobox
from main import save_mensaje, get_mensajes, update_mensaje, delete_mensaje
from Entities.perfil import Perfil
from persistence.db import SessionLocal

class MessageManagement(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Mensajes")
        self.geometry("800x500")
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

        # Frame tabla
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

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
                        font=("Arial", 15, "bold"))

        self.tree = Treeview(table_frame, columns=("id", "remitente", "destinatario", "contenido"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("remitente", text="Remitente")
        self.tree.heading("destinatario", text="Destinatario")
        self.tree.heading("contenido", text="Contenido")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("remitente", width=150, anchor="center")
        self.tree.column("destinatario", width=150, anchor="center")
        self.tree.column("contenido", width=350, anchor="w")

        self.tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Botones
        ctk.CTkButton(self, text="Agregar Mensaje", command=self.open_add_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Editar Mensaje", command=self.open_edit_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Eliminar Mensaje", command=self.delete_selected_message, **opciones_boton).pack(pady=5)

        self.load_messages()

    def load_messages(self):
        self.tree.delete(*self.tree.get_children())

        db = SessionLocal()
        perfiles = {p.id_perfil: p.nombre for p in db.query(Perfil).all()}
        mensajes = get_mensajes()
        db.close()

        for m in mensajes:
            nombre_rem = perfiles.get(m.id_remitente, f"ID {m.id_remitente}")
            nombre_dest = perfiles.get(m.id_destinatario, f"ID {m.id_destinatario}")
            self.tree.insert("", "end", values=(m.id_mensaje, nombre_rem, nombre_dest, m.contenido))

    def open_add_window(self):
        self._open_message_form("Agregar")

    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un mensaje para editar.")
            return

        values = self.tree.item(selected[0])["values"]
        self._open_message_form("Editar", values)

    def _open_message_form(self, mode, values=None):
        form = ctk.CTkToplevel(self)
        form.title(f"{mode} Mensaje")
        form.geometry("350x300")
        form.configure(fg_color="#2b2b2b")

        db = SessionLocal()
        perfiles = db.query(Perfil).all()
        db.close()

        nombres_perfiles = [f"{p.id_perfil} - {p.nombre}" for p in perfiles]

        ctk.CTkLabel(form, text="Remitente:", text_color="white").pack(pady=5)
        cb_rem = Combobox(form, values=nombres_perfiles, state="readonly")
        cb_rem.pack()

        ctk.CTkLabel(form, text="Destinatario:", text_color="white").pack(pady=5)
        cb_dest = Combobox(form, values=nombres_perfiles, state="readonly")
        cb_dest.pack()

        ctk.CTkLabel(form, text="Contenido:", text_color="white").pack(pady=5)
        contenido_entry = ctk.CTkEntry(form)
        contenido_entry.pack(pady=5)

        if mode == "Editar" and values:
            mensaje_id, remitente, destinatario, contenido = values
            contenido_entry.insert(0, contenido)
            for p in perfiles:
                if p.nombre == remitente:
                    cb_rem.set(f"{p.id_perfil} - {p.nombre}")
                if p.nombre == destinatario:
                    cb_dest.set(f"{p.id_perfil} - {p.nombre}")

        def submit():
            try:
                id_rem = int(cb_rem.get().split(" - ")[0])
                id_dest = int(cb_dest.get().split(" - ")[0])
                contenido = contenido_entry.get()

                if not contenido:
                    raise ValueError("Contenido vacío.")

                if mode == "Agregar":
                    save_mensaje(id_rem, id_dest, contenido)
                    messagebox.showinfo("Éxito", "Mensaje creado.")
                else:
                    update_mensaje(mensaje_id, id_rem, id_dest, contenido)
                    messagebox.showinfo("Éxito", "Mensaje actualizado.")

                form.destroy()
                self.load_messages()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(form, text="Guardar", command=submit,
                      fg_color="#0f5132", hover_color="#198754", text_color="white").pack(pady=10)

    def delete_selected_message(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un mensaje para eliminar.")
            return

        mensaje_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que quieres eliminar este mensaje?")
        if confirm:
            try:
                delete_mensaje(mensaje_id)
                messagebox.showinfo("Éxito", "Mensaje eliminado.")
                self.load_messages()
            except Exception as e:
                messagebox.showerror("Error", str(e))
