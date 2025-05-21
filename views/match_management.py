import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Scrollbar
from tkinter.ttk import Combobox
from main import save_match, get_matchs, update_match, delete_match, get_profiles

class MatchManagement(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Matchs")
        self.geometry("600x450")
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

        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#461220",
                        foreground="white",
                        fieldbackground="#461220",
                        rowheight=25,
                        font=("Arial", 14, "bold"))
        style.configure("Treeview.Heading",
                        background=color_base,
                        foreground="white",
                        font=("Arial", 16, "bold"))

        self.tree = Treeview(table_frame, columns=("ID Match", "Perfil 1", "Perfil 2"), show="headings")

        self.tree.heading("ID Match", text="ID Match")
        self.tree.heading("Perfil 1", text="Nombre Perfil 1")
        self.tree.heading("Perfil 2", text="Nombre Perfil 2")

        self.tree.column("ID Match", width=100, anchor="center", stretch=False)
        self.tree.column("Perfil 1", width=200, anchor="center", stretch=False)
        self.tree.column("Perfil 2", width=200, anchor="center", stretch=False)

        self.tree.grid(row=0, column=0, sticky="ns")  

        y_scroll = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Botones
        ctk.CTkButton(self, text="Agregar Match", command=self.open_add_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Actualizar Match", command=self.open_update_window, **opciones_boton).pack(pady=5)
        ctk.CTkButton(self, text="Eliminar Match", command=self.delete_selected_match, **opciones_boton).pack(pady=5)

        self.load_matchs()

    def load_matchs(self):
        self.tree.delete(*self.tree.get_children())
        for match in get_matchs():
            self.tree.insert("", "end", values=(match.id_match, match.perfil1.nombre, match.perfil2.nombre))

    def open_add_window(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Agregar Match")
        add_window.geometry("300x200")

        perfiles = get_profiles()
        nombres_perfiles = [perfil.nombre for perfil in perfiles]

        ctk.CTkLabel(add_window, text="Perfil 1:").pack(pady=5)
        perfil1_combobox = Combobox(add_window, values=nombres_perfiles)
        perfil1_combobox.pack()

        ctk.CTkLabel(add_window, text="Perfil 2:").pack(pady=5)
        perfil2_combobox = Combobox(add_window, values=nombres_perfiles)
        perfil2_combobox.pack()

        ctk.CTkButton(add_window, text="Guardar",
                      command=lambda: self.create_match(perfil1_combobox.get(), perfil2_combobox.get(), perfiles),
                      **{"fg_color": "#0f5132", "hover_color": "#198754", "text_color": "white"}).pack(pady=10)

    def create_match(self, perfil1_nombre, perfil2_nombre, perfiles):
        if not perfil1_nombre or not perfil2_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        perfil1_id = next((p.id_perfil for p in perfiles if p.nombre == perfil1_nombre), None)
        perfil2_id = next((p.id_perfil for p in perfiles if p.nombre == perfil2_nombre), None)

        if not perfil1_id or not perfil2_id:
            messagebox.showerror("Error", "Error al obtener IDs de perfiles.")
            return

        try:
            save_match(perfil1_id, perfil2_id)
            messagebox.showinfo("Éxito", "Match creado correctamente.")
            self.load_matchs()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear match: {e}")

    def open_update_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un match para actualizar.")
            return

        match_data = self.tree.item(selected[0], "values")
        match_id, perfil1_nombre, perfil2_nombre = match_data

        update_window = ctk.CTkToplevel(self)
        update_window.title("Actualizar Match")
        update_window.geometry("300x200")

        perfiles = get_profiles()
        nombres_perfiles = [perfil.nombre for perfil in perfiles]

        ctk.CTkLabel(update_window, text="Perfil 1:").pack(pady=5)
        perfil1_combobox = Combobox(update_window, values=nombres_perfiles)
        perfil1_combobox.set(perfil1_nombre)
        perfil1_combobox.pack()

        ctk.CTkLabel(update_window, text="Perfil 2:").pack(pady=5)
        perfil2_combobox = Combobox(update_window, values=nombres_perfiles)
        perfil2_combobox.set(perfil2_nombre)
        perfil2_combobox.pack()

        ctk.CTkButton(update_window, text="Guardar Cambios",
                      command=lambda: self.update_match(match_id, perfil1_combobox.get(), perfil2_combobox.get(), perfiles),
                      **{"fg_color": "#0f5132", "hover_color": "#198754", "text_color": "white"}).pack(pady=10)

    def update_match(self, match_id, perfil1_nombre, perfil2_nombre, perfiles):
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
            self.load_matchs()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar match: {e}")

    def delete_selected_match(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un match para eliminar.")
            return

        match_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que quieres eliminar este match?")
        if confirm:
            try:
                delete_match(match_id)
                self.load_matchs()
                messagebox.showinfo("Éxito", "Match eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar match: {e}")
