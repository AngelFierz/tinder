import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview, Combobox
from main import save_match, get_matchs, update_match, delete_match, get_profiles  # Función para obtener perfiles de gente cool

class MatchManagement(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Matchs")
        self.geometry("500x400")

        # Crear la tabla con nombres
        self.tree = Treeview(self, columns=("ID Match", "Perfil 1", "Perfil 2"), show="headings")
        self.tree.heading("ID Match", text="ID Match")
        self.tree.heading("Perfil 1", text="Nombre Perfil 1")
        self.tree.heading("Perfil 2", text="Nombre Perfil 2")

        # Ajustar ancho de columnas
        self.tree.column("ID Match", width=100)
        self.tree.column("Perfil 1", width=150)
        self.tree.column("Perfil 2", width=150)

        self.tree.pack(pady=10)

        # Cargar datos al iniciar
        self.load_matchs()

        # Botones
        tk.Button(self, text="Agregar Match", command=self.open_add_window).pack(pady=5)
        tk.Button(self, text="Actualizar Match", command=self.open_update_window).pack(pady=5)
        tk.Button(self, text="Eliminar Match", command=self.delete_selected_match).pack(pady=5)

    def load_matchs(self):
        """Carga los datos de la base de datos y muestra los nombres de los perfiles"""
        self.tree.delete(*self.tree.get_children())  # Limpiar tabla antes de cargar nuevos datos
        for match in get_matchs():
            self.tree.insert("", "end", values=(match.id_match, match.perfil1.nombre, match.perfil2.nombre))

    def open_add_window(self):
        """Abre una ventana para agregar un nuevo match con Combobox mostrando nombres"""
        add_window = tk.Toplevel(self)
        add_window.title("Agregar Match")

        # Obtener lista de perfiles desde la base de datos
        perfiles = get_profiles()
        nombres_perfiles = [perfil.nombre for perfil in perfiles]

        tk.Label(add_window, text="Perfil 1:").pack()
        perfil1_combobox = Combobox(add_window, values=nombres_perfiles)
        perfil1_combobox.pack()
        
        tk.Label(add_window, text="Perfil 2:").pack()
        perfil2_combobox = Combobox(add_window, values=nombres_perfiles)
        perfil2_combobox.pack()

        tk.Button(add_window, text="Guardar", command=lambda: self.create_match(perfil1_combobox.get(), perfil2_combobox.get(), perfiles)).pack()

    def create_match(self, perfil1_nombre, perfil2_nombre, perfiles):
        """Guardar match con IDs basados en nombres seleccionados"""
        if not perfil1_nombre or not perfil2_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Buscar los IDs de los nombres seleccionados
        perfil1_id = next((p.id_perfil for p in perfiles if p.nombre == perfil1_nombre), None)
        perfil2_id = next((p.id_perfil for p in perfiles if p.nombre == perfil2_nombre), None)

        if not perfil1_id or not perfil2_id:
            messagebox.showerror("Error", "Error al obtener IDs de perfiles.")
            return

        try:
            save_match(perfil1_id, perfil2_id)
            messagebox.showinfo("Éxito", "Match creado correctamente.")
            self.load_matchs()  # Recargar datos en la tabla
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear match: {e}")

    def open_update_window(self):
        """Abre una ventana para actualizar el match seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un match para actualizar.")
            return

        match_data = self.tree.item(selected[0], "values")
        match_id, perfil1_nombre, perfil2_nombre = match_data

        update_window = tk.Toplevel(self)
        update_window.title("Actualizar Match")

        # Obtener lista de perfiles desde la base de datos
        perfiles = get_profiles()
        nombres_perfiles = [perfil.nombre for perfil in perfiles]

        tk.Label(update_window, text="Perfil 1:").pack()
        perfil1_combobox = Combobox(update_window, values=nombres_perfiles)
        perfil1_combobox.set(perfil1_nombre)  # Prellenar datos
        perfil1_combobox.pack()
        
        tk.Label(update_window, text="Perfil 2:").pack()
        perfil2_combobox = Combobox(update_window, values=nombres_perfiles)
        perfil2_combobox.set(perfil2_nombre)  # Prellenar datos
        perfil2_combobox.pack()

        tk.Button(update_window, text="Guardar Cambios", command=lambda: self.update_match(match_id, perfil1_combobox.get(), perfil2_combobox.get(), perfiles)).pack()

    def update_match(self, match_id, perfil1_nombre, perfil2_nombre, perfiles):
        """Actualizar match con nombres seleccionados en `Combobox`"""
        if not perfil1_nombre or not perfil2_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        perfil1_id = next((p.id_perfil for p in perfiles if p.nombre == perfil1_nombre), None)
        perfil2_id = next((p.id_perfil for p in perfiles if p.nombre == perfil2_nombre), None)

        if not perfil1_id or not perfil2_id:
            messagebox.showerror("Error", "Error al obtener IDs de perfiles.")
            return

        try:
            update_match(match_id, perfil1_id, perfil2_id)
            messagebox.showinfo("Éxito", "Match actualizado correctamente.")
            self.load_matchs()  # Recargar datos en la tabla
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar match: {e}")

    def delete_selected_match(self):
        """Eliminar un match seleccionado en la tabla"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un match para eliminar.")
            return

        match_id = self.tree.item(selected[0], "values")[0]

        try:
            delete_match(int(match_id))
            messagebox.showinfo("Éxito", "Match eliminado correctamente.")
            self.tree.delete(selected[0])  # Eliminar la fila en la tabla
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar match: {e}")
