import customtkinter as ctk

from app.theme import APP_THEME
from core.services.roadmap_service import RoadmapService


class RoadmapView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.weeks = RoadmapService.get_all_weeks()
        self.selected_week_number = 1

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.scroll_frame = None
        self.detail_panel = None

        self.title_entry = None
        self.goal_textbox = None
        self.planned_hours_entry = None
        self.actual_hours_entry = None
        self.notes_textbox = None

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
            text="Plan anual interactivo de 52 semanas",
            text_color=APP_THEME["accent_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        subtitle.grid(row=0, column=0, padx=28, pady=(58, 0), sticky="w")

        self._build_grid_panel()
        self._build_detail_panel()

    def _build_grid_panel(self) -> None:
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        self.scroll_frame.grid(row=1, column=0, padx=(24, 12), pady=24, sticky="nsew")

        for col in range(4):
            self.scroll_frame.grid_columnconfigure(col, weight=1)

        self._render_week_cards()

    def _build_detail_panel(self) -> None:
        self.detail_panel = ctk.CTkScrollableFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        self.detail_panel.grid(row=1, column=1, padx=(12, 24), pady=24, sticky="nsew")

        self._render_selected_week_details()

    def _render_week_cards(self) -> None:
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        self.weeks = RoadmapService.get_all_weeks()

        for i, week in enumerate(self.weeks):
            row = i // 4
            col = i % 4

            week_card = self._build_week_card(self.scroll_frame, week)
            week_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def _render_selected_week_details(self) -> None:
        for child in self.detail_panel.winfo_children():
            child.destroy()

        week = RoadmapService.get_week_by_number(self.selected_week_number)
        if week is None:
            return

        status_text, status_color = self._get_status_style(week["status"])

        title = ctk.CTkLabel(
            self.detail_panel,
            text=f"Semana {week['week_number']}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=20, pady=(20, 6))

        badge = ctk.CTkLabel(
            self.detail_panel,
            text=status_text,
            fg_color=status_color,
            corner_radius=999,
            text_color="#081018" if week["status"] != "pending" else APP_THEME["text_primary"],
            padx=10,
            pady=4,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        badge.pack(anchor="w", padx=20, pady=(0, 14))

        self._add_label("Bloque")
        block_value = ctk.CTkLabel(
            self.detail_panel,
            text=week["block"],
            text_color=APP_THEME["text_secondary"],
        )
        block_value.pack(fill="x", padx=20, pady=(0, 10))

        self._add_label("Título")
        self.title_entry = ctk.CTkEntry(
            self.detail_panel,
            height=40,
            corner_radius=12,
        )
        self.title_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.title_entry.insert(0, week["title"])

        self._add_label("Objetivo")
        self.goal_textbox = ctk.CTkTextbox(
            self.detail_panel,
            height=90,
            corner_radius=12,
        )
        self.goal_textbox.pack(fill="x", padx=20, pady=(0, 10))
        self.goal_textbox.insert("1.0", week["goal"])

        self._add_label("Horas planeadas")
        self.planned_hours_entry = ctk.CTkEntry(
            self.detail_panel,
            height=40,
            corner_radius=12,
        )
        self.planned_hours_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.planned_hours_entry.insert(0, str(week["planned_hours"]))

        self._add_label("Horas reales")
        self.actual_hours_entry = ctk.CTkEntry(
            self.detail_panel,
            height=40,
            corner_radius=12,
        )
        self.actual_hours_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.actual_hours_entry.insert(0, str(week["actual_hours"]))

        self._add_label("Notas")
        self.notes_textbox = ctk.CTkTextbox(
            self.detail_panel,
            height=120,
            corner_radius=12,
        )
        self.notes_textbox.pack(fill="x", padx=20, pady=(0, 14))
        self.notes_textbox.insert("1.0", week.get("notes", ""))

        save_button = ctk.CTkButton(
            self.detail_panel,
            text="Guardar cambios",
            fg_color=APP_THEME["accent_cyan"],
            hover_color=APP_THEME["accent_cyan_hover"],
            text_color="#081018",
            height=44,
            corner_radius=12,
            command=self._save_week_details,
        )
        save_button.pack(fill="x", padx=20, pady=(0, 16))

        divider = ctk.CTkFrame(
            self.detail_panel,
            height=1,
            fg_color=APP_THEME["border"],
        )
        divider.pack(fill="x", padx=20, pady=12)

        actions_title = ctk.CTkLabel(
            self.detail_panel,
            text="Estado",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        actions_title.pack(anchor="w", padx=20, pady=(0, 12))

        actions = [
            ("Marcar pendiente", "pending", APP_THEME["bg_tertiary"], APP_THEME["text_primary"]),
            ("Marcar en progreso", "in_progress", APP_THEME["accent_cyan"], "#081018"),
            ("Marcar completada", "completed", APP_THEME["success"], "#081018"),
        ]

        for text, status, fg_color, text_color in actions:
            button = ctk.CTkButton(
                self.detail_panel,
                text=text,
                fg_color=fg_color,
                hover_color=APP_THEME["accent_copper_hover"],
                text_color=text_color,
                height=42,
                corner_radius=12,
                command=lambda s=status: self._change_status(s),
            )
            button.pack(fill="x", padx=20, pady=6)

        divider_2 = ctk.CTkFrame(
            self.detail_panel,
            height=1,
            fg_color=APP_THEME["border"],
        )
        divider_2.pack(fill="x", padx=20, pady=18)

        reset_button = ctk.CTkButton(
            self.detail_panel,
            text="Restaurar roadmap inicial",
            fg_color=APP_THEME["danger"],
            hover_color=APP_THEME["accent_copper_hover"],
            text_color=APP_THEME["text_primary"],
            height=42,
            corner_radius=12,
            command=self._reset_roadmap,
        )
        reset_button.pack(fill="x", padx=20, pady=(0, 18))

    def _add_label(self, text: str) -> None:
        label = ctk.CTkLabel(
            self.detail_panel,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        label.pack(anchor="w", padx=20, pady=(4, 6))

    def _build_week_card(self, master, week: dict) -> ctk.CTkFrame:
        status = week["status"]
        status_text, status_color = self._get_status_style(status)

        is_selected = week["week_number"] == self.selected_week_number
        border_color = APP_THEME["accent_cyan"] if is_selected else APP_THEME["border"]
        border_width = 2 if is_selected else 1

        card = ctk.CTkFrame(
            master,
            fg_color=APP_THEME["bg_card"],
            corner_radius=14,
            border_width=border_width,
            border_color=border_color,
        )

        card.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

        week_label = ctk.CTkLabel(
            card,
            text=f"Semana {week['week_number']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        week_label.pack(anchor="w", padx=14, pady=(12, 4))
        week_label.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

        title_label = ctk.CTkLabel(
            card,
            text=week["title"],
            text_color=APP_THEME["text_secondary"],
            wraplength=250,
            justify="left",
        )
        title_label.pack(anchor="w", padx=14, pady=(0, 8))
        title_label.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

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
        status_badge.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

        hours_label = ctk.CTkLabel(
            card,
            text=f"Horas: {week['actual_hours']} / {week['planned_hours']}",
            text_color=APP_THEME["text_muted"],
        )
        hours_label.pack(anchor="w", padx=14, pady=(0, 4))
        hours_label.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

        notes_preview = (week.get("notes", "") or "").strip()
        if notes_preview:
            notes_preview = notes_preview[:60] + ("..." if len(notes_preview) > 60 else "")
            notes_label = ctk.CTkLabel(
                card,
                text=notes_preview,
                text_color=APP_THEME["accent_copper"],
                wraplength=250,
                justify="left",
            )
            notes_label.pack(anchor="w", padx=14, pady=(0, 12))
            notes_label.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))
        else:
            spacer = ctk.CTkLabel(
                card,
                text="Sin notas",
                text_color=APP_THEME["text_muted"],
            )
            spacer.pack(anchor="w", padx=14, pady=(0, 12))
            spacer.bind("<Button-1>", lambda _e, n=week["week_number"]: self._select_week(n))

        return card

    def _select_week(self, week_number: int) -> None:
        self.selected_week_number = week_number
        self._render_week_cards()
        self._render_selected_week_details()

    def _change_status(self, new_status: str) -> None:
        RoadmapService.update_week_status(self.selected_week_number, new_status)
        self.weeks = RoadmapService.get_all_weeks()
        self._render_week_cards()
        self._render_selected_week_details()

    def _save_week_details(self) -> None:
        week = RoadmapService.get_week_by_number(self.selected_week_number)
        if week is None:
            return

        title = self.title_entry.get().strip()
        goal = self.goal_textbox.get("1.0", "end").strip()
        notes = self.notes_textbox.get("1.0", "end").strip()

        try:
            planned_hours = int(self.planned_hours_entry.get().strip())
        except ValueError:
            planned_hours = week["planned_hours"]

        try:
            actual_hours = int(self.actual_hours_entry.get().strip())
        except ValueError:
            actual_hours = week["actual_hours"]

        RoadmapService.update_week_details(
            week_number=self.selected_week_number,
            title=title,
            goal=goal,
            planned_hours=planned_hours,
            actual_hours=actual_hours,
            notes=notes,
        )

        self.weeks = RoadmapService.get_all_weeks()
        self._render_week_cards()
        self._render_selected_week_details()

    def _reset_roadmap(self) -> None:
        RoadmapService.reset_to_seed()
        self.weeks = RoadmapService.get_all_weeks()
        self.selected_week_number = 1
        self._render_week_cards()
        self._render_selected_week_details()

    def _get_status_style(self, status: str) -> tuple[str, str]:
        if status == "completed":
            return "Completada", APP_THEME["success"]
        if status == "in_progress":
            return "En progreso", APP_THEME["accent_cyan"]
        return "Pendiente", APP_THEME["bg_tertiary"]