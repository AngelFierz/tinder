import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from views.user_management import UserManagement 
from views.profile_management import ProfileManagement
from views.message_management import MessageManagement
from views.match_management import MatchManagement

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal - Tinder App")
        self.geometry("400x300")
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.original_image = Image.open("image/corazones.png")

        self.fondo_img = None
        self.fondo_label = ctk.CTkLabel(self, text="")
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        boton_y = 0.35
        espaciado = 0.08
        ancho = 200

        color_base = "#880d1e"
        color_hover = "#dd2d4a"

        opciones_boton = {
            "width": ancho,
            "fg_color": color_base,
            "hover_color": color_hover,
            "border_width": 0,
            "corner_radius": 3,
            "border_color": color_base,
            "text_color": "white",
            "font": ("Arial", 12, "bold"),
        }

        ctk.CTkButton(self, text="Gestión de Usuarios", command=self.open_user_management, **opciones_boton)\
            .place(relx=0.5, rely=boton_y, anchor="center")
        ctk.CTkButton(self, text="Gestión de Perfiles", command=self.open_profile_management, **opciones_boton)\
            .place(relx=0.5, rely=boton_y + espaciado, anchor="center")
        ctk.CTkButton(self, text="Gestión de Mensajes", command=self.open_message_management, **opciones_boton)\
            .place(relx=0.5, rely=boton_y + 2 * espaciado, anchor="center")
        ctk.CTkButton(self, text="Gestión de Matchs", command=self.open_match_management, **opciones_boton)\
            .place(relx=0.5, rely=boton_y + 3 * espaciado, anchor="center")
        ctk.CTkButton(self, text="Salir", command=self.destroy, **opciones_boton)\
            .place(relx=0.5, rely=boton_y + 4 * espaciado, anchor="center")


       

        self.windows = {}

        # redibujar la imagen al redimensionar
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        resized = self.original_image.resize((width, height), Image.LANCZOS)
        self.fondo_img = ImageTk.PhotoImage(resized)
        self.fondo_label.configure(image=self.fondo_img)

    def open_user_management(self):
        self.open_window("user_management", UserManagement)

    def open_profile_management(self):
        self.open_window("profile_management", ProfileManagement)

    def open_message_management(self):
        self.open_window("message_management", MessageManagement)

    def open_match_management(self):
        self.open_window("match_management", MatchManagement)

    def open_window(self, window_key, window_class):
        if window_key in self.windows:
            self.windows[window_key].focus()
        else:
            new_window = window_class(self)
            new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(window_key))
            self.windows[window_key] = new_window

    def close_window(self, window_key):
        if window_key in self.windows:
            self.windows[window_key].destroy()
            del self.windows[window_key]

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
