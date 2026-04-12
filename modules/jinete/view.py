import customtkinter as ctk
from app.theme import APP_THEME


class JineteView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Jinete",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=28, pady=(24, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Perfil, enfoque anual y estadísticas del vaquero.",
            text_color=APP_THEME["text_secondary"],
        )
        subtitle.pack(anchor="w", padx=28, pady=(0, 20))

        card = ctk.CTkFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        card.pack(fill="both", expand=True, padx=24, pady=24)

        sections = [
            ("Ruta principal", "Python Automation / Backend Engineer"),
            ("Enfoque", "Telemetría, observabilidad, IA aplicada"),
            ("Especialidad secundaria", "Seguridad defensiva y tooling"),
            ("Meta anual", "Cerrar 2 proyectos fuertes y reposicionarme"),
        ]

        for title_text, value_text in sections:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=22, pady=12)

            title = ctk.CTkLabel(
                row,
                text=title_text,
                width=220,
                anchor="w",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=APP_THEME["text_primary"],
            )
            title.pack(side="left")

            value = ctk.CTkLabel(
                row,
                text=value_text,
                anchor="w",
                text_color=APP_THEME["text_secondary"],
            )
            value.pack(side="left", padx=8)