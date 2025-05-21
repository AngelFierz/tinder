import tkinter as tk
from tkinter import messagebox, ttk
from main import save_mensaje, get_mensajes, update_mensaje, delete_mensaje
from Entities.perfil import Perfil
from persistence.db import SessionLocal

class MessageManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Mensajes")
        self.geometry("700x400")

        # Tabla de mensajes
        self.tree = ttk.Treeview(self, columns=("id", "remitente", "destinatario", "contenido"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("remitente", text="Remitente")
        self.tree.heading("destinatario", text="Destinatario")
        self.tree.heading("contenido", text="Contenido")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Mensaje", command=self.open_add_window).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Mensaje", command=self.open_edit_window).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar Mensaje", command=self.delete_selected_message).grid(row=0, column=2, padx=5)

        self.load_messages()

    def load_messages(self):
        """Carga todos los mensajes en la tabla"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        mensajes = get_mensajes()
        db = SessionLocal()
        perfiles = {p.id_perfil: p.nombre for p in db.query(Perfil).all()}

        for m in mensajes:
            nombre_rem = perfiles.get(m.id_remitente, f"ID {m.id_remitente}")
            nombre_dest = perfiles.get(m.id_destinatario, f"ID {m.id_destinatario}")
            self.tree.insert("", tk.END, values=(m.id_mensaje, nombre_rem, nombre_dest, m.contenido))

        db.close()

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
        """Formulario para agregar o editar mensajes"""
        form = tk.Toplevel(self)
        form.title(f"{mode} Mensaje")
        form.geometry("300x250")

        db = SessionLocal()
        perfiles = db.query(Perfil).all()
        db.close()

        tk.Label(form, text="Remitente:").pack(pady=5)
        cb_rem = ttk.Combobox(form, state="readonly")
        cb_rem['values'] = [f"{p.id_perfil} - {p.nombre}" for p in perfiles]
        cb_rem.pack()

        tk.Label(form, text="Destinatario:").pack(pady=5)
        cb_dest = ttk.Combobox(form, state="readonly")
        cb_dest['values'] = [f"{p.id_perfil} - {p.nombre}" for p in perfiles]
        cb_dest.pack()

        tk.Label(form, text="Contenido:").pack(pady=5)
        contenido_entry = tk.Entry(form)
        contenido_entry.pack(pady=5)

        if mode == "Editar" and values:
            mensaje_id, remitente, destinatario, contenido = values
            contenido_entry.insert(0, contenido)

            # Selección automática de remitente y destinatario
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

        tk.Button(form, text="Guardar", command=submit).pack(pady=10)

    def delete_selected_message(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un mensaje para eliminar.")
            return

        mensaje_id = self.tree.item(selected[0])["values"][0]
        try:
            delete_mensaje(mensaje_id)
            messagebox.showinfo("Éxito", "Mensaje eliminado.")
            self.load_messages()
        except Exception as e:
            messagebox.showerror("Error", str(e))

