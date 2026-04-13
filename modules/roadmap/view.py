import customtkinter as ctk

from app.theme import APP_THEME
from core.services.roadmap_service import RoadmapService


class RoadmapView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.weeks = RoadmapService.get_all_weeks()

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
        title.grid(row=0, column=0, padx=28, pady=(24, 8), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Plan anual de 52 semanas",
            text_color=APP_THEME["accent_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        subtitle.grid(row=0, column=0, padx=28, pady=(58, 0), sticky="w")

        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        scroll.grid(row=1, column=0, padx=24, pady=24, sticky="nsew")

        for col in range(4):
            scroll.grid_columnconfigure(col, weight=1)

        for i, week in enumerate(self.weeks):
            row = i // 4
            col = i % 4

            week_card = self._build_week_card(scroll, week)
            week_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _build_week_card(self, master, week: dict) -> ctk.CTkFrame:
        status = week["status"]
        status_text, status_color = self._get_status_style(status)

        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_card"],
            corner_radius=14,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        week_label = ctk.CTkLabel(
            card,
            text=f"Semana {week['week_number']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        week_label.pack(anchor="w", padx=14, pady=(12, 4))

        title_label = ctk.CTkLabel(
            card,
            text=week["title"],
            text_color=APP_THEME["text_secondary"],
            wraplength=250,
            justify="left",
        )
        title_label.pack(anchor="w", padx=14, pady=(0, 8))

        status_badge = ctk.CTkLabel(
            card,
            text=status_text,
            fg_color=status_color,
            corner_radius=999,
            text_color="#081018" if status != "pending" else APP_THEME["text_primary"],
            padx=10,
            pady=4,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        status_badge.pack(anchor="w", padx=14, pady=(0, 8))

        hours_label = ctk.CTkLabel(
            card,
            text=f"Horas: {week['actual_hours']} / {week['planned_hours']}",
            text_color=APP_THEME["text_muted"],
        )
        hours_label.pack(anchor="w", padx=14, pady=(0, 12))

        return card

    def _get_status_style(self, status: str) -> tuple[str, str]:
        if status == "completed":
            return "Completada", APP_THEME["success"]
        if status == "in_progress":
            return "En progreso", APP_THEME["accent_cyan"]
        return "Pendiente", APP_THEME["bg_tertiary"]