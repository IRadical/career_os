import customtkinter as ctk
from app.theme import APP_THEME

class RoadmapView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Mapa de Ruta",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.grid(row=0, column=0, padx=28, pady=(24, 12), sticky="w")

        grid_wrap = ctk.CTkFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        grid_wrap.grid(row=1, column=0, padx=24, pady=24, sticky="nsew")

        for col in range(4):
            grid_wrap.grid_columnconfigure(col, weight=1)
        
        for row in range(13):
            grid_wrap.grid_rowconfigure(row, weight=1)

        for i in range(52):
            row - i // 4
            col = i % 4

            week_card = ctk.CTkFrame(
                grid_wrap,
                fg_color=APP_THEME["bg_tertiary"],
                corner_radius=14,
                border_width=1,
                border_color=APP_THEME["border"],
            )
            week_card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")

            week_label = ctk.CTkLabel(
                week_card,
                text=f"Semana {i+1}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=APP_THEME["text_primary"],
            )
            week_label.pack(anchor="w", padx=14, pady=(12,4))

            status_label = ctk.CTkLabel(
                week_card,
                text="Pendiente",
                text_color=APP_THEME["accent_cyan"],
            )
            status_label.pack(anchor="w", padx=14, pady=(0,12))
