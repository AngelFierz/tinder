import tkinter as tk
from tkinter import messagebox
from main import save_match, get_matchs, update_match, delete_match  # Importamos las funciones

class MatchManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Matchs")
        self.geometry("400x400")

        # Entradas de texto
        tk.Label(self, text="ID (para actualizar/eliminar):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_id = tk.Entry(self)
        self.entry_id.grid(row=0, column=1)

        tk.Label(self, text="ID Perfil 1:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_perfil1 = tk.Entry(self)
        self.entry_perfil1.grid(row=1, column=1)

        tk.Label(self, text="ID Perfil 2:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_perfil2 = tk.Entry(self)
        self.entry_perfil2.grid(row=2, column=1)

        # Botones
        tk.Button(self, text="Crear Match", command=self.create_match).grid(row=3, column=0, pady=10)
        tk.Button(self, text="Actualizar Match", command=self.update_match).grid(row=3, column=1, pady=10)
        tk.Button(self, text="Eliminar Match", command=self.delete_match).grid(row=4, column=0, pady=10)
        tk.Button(self, text="Ver Matchs", command=self.view_matchs).grid(row=4, column=1, pady=10)

    def create_match(self):
        """Crear un nuevo match"""
        perfil1 = self.entry_perfil1.get()
        perfil2 = self.entry_perfil2.get()

        if not perfil1 or not perfil2:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            
            save_match(int(perfil1), int(perfil2))
            messagebox.showinfo("Éxito", "Match creado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear match: {e}")

    def update_match(self):
        """Actualizar un match existente"""
        match_id = self.entry_id.get()
        perfil1 = self.entry_perfil1.get()
        perfil2 = self.entry_perfil2.get()

        if not match_id or not perfil1 or not perfil2:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            
            update_match(int(match_id), int(perfil1), int(perfil2))
            messagebox.showinfo("Éxito", "Match actualizado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar match: {e}")

    def delete_match(self):
        """Eliminar un match"""
        match_id = self.entry_id.get()

        if not match_id:
            messagebox.showerror("Error", "ID del match es obligatorio para eliminar.")
            return

        try:
           
            delete_match(int(match_id))
            messagebox.showinfo("Éxito", "Match eliminado correctamente.")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar match: {e}")

    def view_matchs(self):
        """Ver todos los matchs"""
        try:
            
            matchs = get_matchs()
            matchs_str = "\n".join([
                f"ID: {m.id_match} | Perfil 1: {m.id_perfil1} | Perfil 2: {m.id_perfil2}"
                for m in matchs
            ])
            messagebox.showinfo("Matchs", matchs_str)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener matchs: {e}")

    def clear_fields(self):
        """Limpia todos los campos de entrada"""
        self.entry_id.delete(0, tk.END)
        self.entry_perfil1.delete(0, tk.END)
        self.entry_perfil2.delete(0, tk.END)
