import tkinter as tk
from tkinter import messagebox
from main import save_mensaje, get_mensajes, update_mensaje, delete_mensaje  # Importamos las funciones

class MessageManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Mensajes")
        self.geometry("400x400")

        # Entradas de texto
        tk.Label(self, text="ID (para actualizar/eliminar):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)

        tk.Label(self, text="ID Remitente:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_remitente = tk.Entry(self)
        self.entry_remitente.grid(row=1, column=1)

        tk.Label(self, text="ID Destinatario:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_destinatario = tk.Entry(self)
        self.entry_destinatario.grid(row=2, column=1)

        tk.Label(self, text="Contenido:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_contenido = tk.Entry(self)
        self.entry_contenido.grid(row=3, column=1)

        # Botones
        tk.Button(self, text="Enviar Mensaje", command=self.create_message).grid(row=4, column=0, pady=10)
        tk.Button(self, text="Actualizar Mensaje", command=self.update_message).grid(row=4, column=1, pady=10)
        tk.Button(self, text="Eliminar Mensaje", command=self.delete_message).grid(row=5, column=0, pady=10)
        tk.Button(self, text="Ver Mensajes", command=self.view_messages).grid(row=5, column=1, pady=10)

    def create_message(self):
        """Crear un nuevo mensaje"""
        remitente = self.entry_remitente.get()
        destinatario = self.entry_destinatario.get()
        contenido = self.entry_contenido.get()

        if not remitente or not destinatario or not contenido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            
            save_mensaje(int(remitente), int(destinatario), contenido)
            messagebox.showinfo("Éxito", "Mensaje enviado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar mensaje: {e}")

    def update_message(self):
        """Actualizar un mensaje existente"""
        mensaje_id = self.entry_id.get()
        remitente = self.entry_remitente.get()
        destinatario = self.entry_destinatario.get()
        contenido = self.entry_contenido.get()

        if not mensaje_id or not remitente or not destinatario or not contenido:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
          
            update_mensaje(int(mensaje_id), int(remitente), int(destinatario), contenido)
            messagebox.showinfo("Éxito", "Mensaje actualizado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar mensaje: {e}")

    def delete_message(self):
        """Eliminar un mensaje"""
        mensaje_id = self.entry_id.get()

        if not mensaje_id:
            messagebox.showerror("Error", "ID del mensaje es obligatorio para eliminar.")
            return

        try:
            
            delete_mensaje(int(mensaje_id))
            messagebox.showinfo("Éxito", "Mensaje eliminado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar mensaje: {e}")

    def view_messages(self):
        """Ver todos los mensajes"""
        try:
           
            mensajes = get_mensajes()
            mensajes_str = "\n".join([
                f"ID: {m.id_mensaje} | Remitente: {m.id_remitente} | Destinatario: {m.id_destinatario} | Contenido: {m.contenido}"
                for m in mensajes
            ])
            messagebox.showinfo("Mensajes", mensajes_str)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener mensajes: {e}")

    def clear_fields(self):
        """Limpia todos los campos de entrada"""
        self.entry_id.delete(0, tk.END)
        self.entry_remitente.delete(0, tk.END)
        self.entry_destinatario.delete(0, tk.END)
        self.entry_contenido.delete(0, tk.END)
