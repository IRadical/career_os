import customtkinter as ctk

class CareerOSApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Career OS")
        self.geometry("1400x900")
        self.minsize(1100, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(7, weight=1)

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self._build_sidebar()
        self._build_dashboard()

    def _build_sidebar(self) -> None:
        title = ctk.CTkLabel(
            self.sidebar,
            text="Career OS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")

        subtitule = ctk.CTkLabel(
            self.sidebar,
            text="Vaquero Moderno",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitule.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        buttons = [
            "Dashboard",
            "Mapa de Ruta",
            "Dinamo 400 SS",
            "Sandwichan",
            "XCOM Bridge",
            "Jinete",
        ]

        for index, name in enumerate(buttons, start=2):
            button = ctk.CTkButton(
                self.sidebar,
                text=name,
                height=42,
                corner_radius=12,
            )
            button.grid(row=index, column=0, padx=18, pady=8, sticky="ew")
        
    def _build_dashboard(self) -> None:
        header = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        header.grid(row=0, column=0, padx=28, pady=(24, 10), sticky="w")

        body = ctk.CTkFrame(self.content, corner_radius=18)
        body.grid(row=1, column=0, padx=24, pady=24, sticky="nsew")
        body.grid_columnconfigure((0,1), weight=1)
        body.grid_rowconfigure((0,1), weight=1)

        cards= [
            "Progreso anual",
            "faenas de hoy",
            "Gran Rodeo",
            "Estado de proyectos"
        ]

        for i, title in enumerate(cards):
            row = i // 2
            col = i % 2
            card = ctk.CTkFrame(body, corner_radius=16)
            card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")

            label = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
            )
            label.pack(anchor="w", padx=18, pady=(18,8))

            text = ctk.CTkLabel(
                card,
                text="Placeholder inicial",
                text_color="gray70",
            )
            text.pack(anchor="w", padx=18, pady=(0, 18))

if __name__ == "__main__":
    app = CareerOSApp()
    app.mainloop()
