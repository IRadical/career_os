import customtkinter as ctk

from app.theme import APP_THEME
from core.services.faena_service import FaenaService
from core.services.roadmap_service import RoadmapService


class DashboardView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.metrics = RoadmapService.get_progress_metrics()
        self.current_week = RoadmapService.get_current_week()
        self.faena_metrics = FaenaService.get_today_metrics()
        self.today_faenas = FaenaService.get_today_faenas()

        self.grid_columnconfigure(0, weight=1)

        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=28, pady=(24, 6))

        subtitle = ctk.CTkLabel(
            self,
            text="Centro de mando del Jinete",
            text_color=APP_THEME["accent_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        subtitle.pack(anchor="w", padx=28, pady=(0, 14))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(0, 12))
        top.grid_columnconfigure((0, 1), weight=1)

        self._build_gran_rodeo_card(top).grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self._build_today_card(top).grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        middle = ctk.CTkFrame(self, fg_color="transparent")
        middle.pack(fill="x", padx=24, pady=(0, 12))
        middle.grid_columnconfigure((0, 1), weight=1)

        self._build_current_week_card(middle).grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self._build_week_notes_card(middle).grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        bottom = ctk.CTkFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        bottom.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        header = ctk.CTkLabel(
            bottom,
            text="Faenas de hoy",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        header.pack(anchor="w", padx=20, pady=(18, 10))

        if self.today_faenas:
            for faena in self.today_faenas:
                row = ctk.CTkFrame(bottom, fg_color=APP_THEME["bg_card"], corner_radius=12)
                row.pack(fill="x", padx=18, pady=6)

                status = "✔" if faena["completed"] else "•"
                text = f"{status} {faena['title']}  |  {faena['category']}  |  {faena['hours']}h"
                label = ctk.CTkLabel(
                    row,
                    text=text,
                    text_color=APP_THEME["text_secondary"],
                )
                label.pack(anchor="w", padx=14, pady=12)
        else:
            empty = ctk.CTkLabel(
                bottom,
                text="No hay faenas registradas para hoy.",
                text_color=APP_THEME["text_muted"],
            )
            empty.pack(anchor="w", padx=20, pady=(0, 18))

    def _build_gran_rodeo_card(self, master) -> ctk.CTkFrame:
        completion_ratio = self.metrics["completion_ratio"]

        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        ctk.CTkLabel(
            card,
            text="Gran Rodeo",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        ).pack(anchor="w", padx=20, pady=(20, 6))

        ctk.CTkLabel(
            card,
            text="Progreso del plan anual",
            text_color=APP_THEME["text_secondary"],
        ).pack(anchor="w", padx=20, pady=(0, 16))

        ctk.CTkLabel(
            card,
            text=f"{int(completion_ratio * 100)}%",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=APP_THEME["accent_cyan"],
        ).pack(anchor="w", padx=20, pady=(0, 6))

        progress = ctk.CTkProgressBar(
            card,
            progress_color=APP_THEME["accent_cyan"],
            fg_color=APP_THEME["bg_tertiary"],
            height=18,
            corner_radius=10,
        )
        progress.pack(fill="x", padx=20, pady=(0, 16))
        progress.set(completion_ratio)

        ctk.CTkLabel(
            card,
            text=f"{self.metrics['completed_weeks']} de {self.metrics['total_weeks']} semanas completadas",
            text_color=APP_THEME["text_muted"],
        ).pack(anchor="w", padx=20, pady=(0, 20))

        return card

    def _build_today_card(self, master) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        ctk.CTkLabel(
            card,
            text="Faena diaria",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        ).pack(anchor="w", padx=20, pady=(20, 6))

        rows = [
            ("Total", str(self.faena_metrics["total"])),
            ("Completadas", str(self.faena_metrics["completed"])),
            ("Horas hoy", str(self.faena_metrics["total_hours"])),
            ("Horas hechas", str(self.faena_metrics["completed_hours"])),
        ]

        for left, right in rows:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row,
                text=left,
                width=130,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=APP_THEME["text_primary"],
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=right,
                text_color=APP_THEME["text_secondary"],
            ).pack(side="left")

        return card

    def _build_current_week_card(self, master) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        ctk.CTkLabel(
            card,
            text=f"Semana {self.current_week['week_number']}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        ).pack(anchor="w", padx=20, pady=(20, 8))

        lines = [
            ("Bloque", self.current_week["block"]),
            ("Título", self.current_week["title"]),
            ("Horas", f"{self.current_week['actual_hours']} / {self.current_week['planned_hours']}"),
        ]

        for left, right in lines:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row,
                text=left,
                width=80,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=APP_THEME["text_primary"],
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=right,
                text_color=APP_THEME["text_secondary"],
                wraplength=260,
                justify="left",
            ).pack(side="left")

        return card

    def _build_week_notes_card(self, master) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=20,
            border_width=1,
            border_color=APP_THEME["border"],
        )

        ctk.CTkLabel(
            card,
            text="Notas de la semana viva",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=APP_THEME["text_primary"],
        ).pack(anchor="w", padx=20, pady=(20, 8))

        notes = self.current_week.get("notes", "").strip() or "Sin notas registradas todavía."

        ctk.CTkLabel(
            card,
            text=notes,
            text_color=APP_THEME["text_secondary"],
            wraplength=320,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 20))

        return card