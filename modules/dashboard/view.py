import customtkinter as ctk

from app.theme import APP_THEME
from core.services.roadmap_service import RoadmapService


class DashboardView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.metrics = RoadmapService.get_progress_metrics()
        self.current_week = RoadmapService.get_current_week()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.grid(row=0, column=0, padx=28, pady=(24, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Centro de mando del Jinete",
            text_color=APP_THEME["accent_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        subtitle.grid(row=1, column=0, padx=28, pady=(0, 12), sticky="w")

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=2, column=0, padx=24, pady=(0, 12), sticky="nsew")
        top.grid_columnconfigure((0, 1), weight=1)

        rodeo_card = self._build_gran_rodeo_card(top)
        rodeo_card.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        stats_card = self._build_stats_card(top)
        stats_card.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=3, column=0, padx=24, pady=(0, 24), sticky="nsew")
        bottom.grid_columnconfigure((0, 1), weight=1)
        bottom.grid_rowconfigure((0, 1), weight=1)

        cards = [
            ("Faenas de hoy", "2 horas mínimas de faena técnica", APP_THEME["success"]),
            ("Semana actual", f"Semana {self.current_week['week_number']}", APP_THEME["accent_cyan"]),
            ("Objetivo actual", self.current_week["title"], APP_THEME["accent_copper"]),
            ("Bloque actual", self.current_week["block"], APP_THEME["text_secondary"]),
        ]

        for i, (title_text, body_text, accent) in enumerate(cards):
            row = i // 2
            col = i % 2
            card = self._build_small_card(bottom, title_text, body_text, accent)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _build_gran_rodeo_card(self, master) -> ctk.CTkFrame:
        completion_ratio = self.metrics["completion_ratio"]

        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        title = ctk.CTkLabel(
            card,
            text="Gran Rodeo",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=20, pady=(20, 6))

        desc = ctk.CTkLabel(
            card,
            text="Progreso del plan anual",
            text_color=APP_THEME["text_secondary"],
        )
        desc.pack(anchor="w", padx=20, pady=(0, 16))

        percent = ctk.CTkLabel(
            card,
            text=f"{int(completion_ratio * 100)}%",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=APP_THEME["accent_cyan"],
        )
        percent.pack(anchor="w", padx=20, pady=(0, 6))

        progress = ctk.CTkProgressBar(
            card,
            progress_color=APP_THEME["accent_cyan"],
            fg_color=APP_THEME["bg_tertiary"],
            height=18,
            corner_radius=10,
        )
        progress.pack(fill="x", padx=20, pady=(0, 16))
        progress.set(completion_ratio)

        footer = ctk.CTkLabel(
            card,
            text=f"{self.metrics['completed_weeks']} de {self.metrics['total_weeks']} semanas completadas",
            text_color=APP_THEME["text_muted"],
        )
        footer.pack(anchor="w", padx=20, pady=(0, 20))

        return card

    def _build_stats_card(self, master) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        title = ctk.CTkLabel(
            card,
            text="Estado del Jinete",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        rows = [
            ("Ruta", "Python Automation / Backend"),
            ("Semana viva", str(self.current_week["week_number"])),
            ("Horas semana", f"{self.current_week['actual_hours']} / {self.current_week['planned_hours']}"),
            ("En progreso", str(self.metrics["in_progress_weeks"])),
        ]

        for left, right in rows:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            left_label = ctk.CTkLabel(
                row,
                text=left,
                width=130,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=APP_THEME["text_primary"],
            )
            left_label.pack(side="left")

            right_label = ctk.CTkLabel(
                row,
                text=right,
                anchor="w",
                text_color=APP_THEME["text_secondary"],
            )
            right_label.pack(side="left")

        return card

    def _build_small_card(
        self,
        master,
        title_text: str,
        body_text: str,
        accent: str,
    ) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        badge = ctk.CTkFrame(
            card,
            width=46,
            height=10,
            corner_radius=999,
            fg_color=accent,
        )
        badge.pack(anchor="w", padx=18, pady=(16, 10))

        title = ctk.CTkLabel(
            card,
            text=title_text,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=18, pady=(0, 6))

        body = ctk.CTkLabel(
            card,
            text=body_text,
            text_color=APP_THEME["text_secondary"],
            wraplength=360,
            justify="left",
        )
        body.pack(anchor="w", padx=18, pady=(0, 18))

        return card