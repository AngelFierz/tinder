import tkinter as tk
from tkinter import messagebox
from views.user_management import UserManagement 
from views.profile_management import ProfileManagement
from views.message_management import MessageManagement
from views.match_management import MatchManagement

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal - Tinder App")
        self.geometry("400x300")

        
        self.windows = {}

        tk.Button(self, text="Gestión de Usuarios", command=self.open_user_management).pack(pady=10)
        tk.Button(self, text="Gestión de Perfiles", command=self.open_profile_management).pack(pady=10)
        tk.Button(self, text="Gestión de Mensajes", command=self.open_message_management).pack(pady=10)
        tk.Button(self, text="Gestión de Matchs", command=self.open_match_management).pack(pady=10)
        tk.Button(self, text="Salir", command=self.destroy).pack(pady=10)

    def open_user_management(self):
        self.open_window("user_management", UserManagement)

    def open_profile_management(self):
        self.open_window("profile_management", ProfileManagement)

    def open_message_management(self):
        self.open_window("message_management", MessageManagement)

    def open_match_management(self):
        self.open_window("match_management", MatchManagement)

    def open_window(self, window_key, window_class):
        """ Evitar ventanas duplicadas """
        if window_key in self.windows:
            self.windows[window_key].focus()
        else:
            new_window = window_class(self)
            new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(window_key))
            self.windows[window_key] = new_window

    def close_window(self, window_key):
        """ Cerrar ventana y eliminar referencia """
        if window_key in self.windows:
            self.windows[window_key].destroy()
            del self.windows[window_key]

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()

