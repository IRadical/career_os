import customtkinter as ctk
from app.theme import APP_THEME

class DashboardView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self) -> None:
        header = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"]
        )
        header.grid(row=0, column=0, padx=28, pady=(24, 10), sticky="w")

        body = ctk.CTkFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"]
        )
        body.grid(row=1, column=0, padx=24, pady=24, sticky="nsew")
        body.grid_columnconfigure((0,1), weight=1)
        body.grid_rowconfigure((0,1), weight=1)

        cards = [
            ("Progeso anual", "Ruta principal: Python Automation / Backend Enginner"),
            ("Faenas de hoy", "2 horas minimas de faena tecnica"),
            ("Gran Rodeo", "Meta mayor del año en progreso"),
            ("Estado de proyectos", "Telemetry / XCOM / Career OS"),
        ]

        for i, (title, subtitle) in enumerate(cards):
            row = i // 2
            col = i % 2

            card = ctk.CTkFrame(
                body,
                fg_color=APP_THEME["bg_tertiary"],
                corner_radius=16,
                border_width=1,
                border_color=APP_THEME["border"]
            )
            card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")

            label = ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=APP_THEME["text_primary"],   
            )
            label.pack(anchor="w", padx=18, pady=(18,8))

            text = ctk.CTkLabel(
                card,
                text=subtitle,
                text_color=APP_THEME["text_secondary"],
                wraplength =380,
                justify="left",
            )
            text.pack(anchor="w", padx=18, pady=(0,18))

