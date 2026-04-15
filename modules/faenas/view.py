import customtkinter as ctk

from app.theme import APP_THEME
from core.services.faena_service import FaenaService
from core.services.roadmap_service import RoadmapService


class FaenasView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        self.title_entry = None
        self.category_entry = None
        self.hours_entry = None
        self.week_entry = None
        self.list_frame = None

        self._build()

    def _build(self) -> None:
        title = ctk.CTkLabel(
            self,
            text="Faenas Diarias",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.pack(anchor="w", padx=28, pady=(24, 6))

        subtitle = ctk.CTkLabel(
            self,
            text="Trabajo diario del Jinete",
            text_color=APP_THEME["accent_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        subtitle.pack(anchor="w", padx=28, pady=(0, 14))

        form = ctk.CTkFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        form.pack(fill="x", padx=24, pady=(0, 14))

        self._add_form_label(form, "Título")
        self.title_entry = ctk.CTkEntry(form, height=40, corner_radius=12)
        self.title_entry.pack(fill="x", padx=18, pady=(0, 10))

        self._add_form_label(form, "Categoría")
        self.category_entry = ctk.CTkEntry(form, height=40, corner_radius=12)
        self.category_entry.pack(fill="x", padx=18, pady=(0, 10))
        self.category_entry.insert(0, "Career OS")

        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(0, 10))

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self._add_form_label(left, "Horas")
        self.hours_entry = ctk.CTkEntry(left, height=40, corner_radius=12)
        self.hours_entry.pack(fill="x")
        self.hours_entry.insert(0, "1")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self._add_form_label(right, "Semana")
        self.week_entry = ctk.CTkEntry(right, height=40, corner_radius=12)
        self.week_entry.pack(fill="x")
        current_week = RoadmapService.get_current_week()["week_number"]
        self.week_entry.insert(0, str(current_week))

        save_button = ctk.CTkButton(
            form,
            text="Agregar faena",
            fg_color=APP_THEME["accent_cyan"],
            hover_color=APP_THEME["accent_cyan_hover"],
            text_color="#081018",
            height=44,
            corner_radius=12,
            command=self._create_faena,
        )
        save_button.pack(fill="x", padx=18, pady=(4, 18))

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=APP_THEME["bg_secondary"],
            corner_radius=18,
            border_width=1,
            border_color=APP_THEME["border"],
        )
        self.list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self._render_faenas()

    def _add_form_label(self, master, text: str) -> None:
        label = ctk.CTkLabel(
            master,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        label.pack(anchor="w", padx=18, pady=(14, 6))

    def _render_faenas(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()

        faenas = FaenaService.get_today_faenas()

        if not faenas:
            ctk.CTkLabel(
                self.list_frame,
                text="No hay faenas para hoy.",
                text_color=APP_THEME["text_muted"],
            ).pack(anchor="w", padx=16, pady=16)
            return

        for faena in faenas:
            card = ctk.CTkFrame(
                self.list_frame,
                fg_color=APP_THEME["bg_card"],
                corner_radius=14,
                border_width=1,
                border_color=APP_THEME["border"],
            )
            card.pack(fill="x", padx=10, pady=8)

            title = ctk.CTkLabel(
                card,
                text=faena["title"],
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=APP_THEME["text_primary"],
            )
            title.pack(anchor="w", padx=16, pady=(14, 4))

            meta = ctk.CTkLabel(
                card,
                text=f"{faena['category']} | {faena['hours']}h | Semana {faena['week_number']}",
                text_color=APP_THEME["text_secondary"],
            )
            meta.pack(anchor="w", padx=16, pady=(0, 10))

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(0, 14))

            status_text = "Marcar incompleta" if faena["completed"] else "Marcar completa"
            status_color = APP_THEME["success"] if not faena["completed"] else APP_THEME["bg_tertiary"]
            status_text_color = "#081018" if not faena["completed"] else APP_THEME["text_primary"]

            toggle_button = ctk.CTkButton(
                row,
                text=status_text,
                fg_color=status_color,
                hover_color=APP_THEME["accent_copper_hover"],
                text_color=status_text_color,
                height=38,
                corner_radius=10,
                command=lambda faena_id=faena["id"]: self._toggle_faena(faena_id),
            )
            toggle_button.pack(side="left", padx=(0, 8))

            delete_button = ctk.CTkButton(
                row,
                text="Eliminar",
                fg_color=APP_THEME["danger"],
                hover_color=APP_THEME["accent_copper_hover"],
                text_color=APP_THEME["text_primary"],
                height=38,
                corner_radius=10,
                command=lambda faena_id=faena["id"]: self._delete_faena(faena_id),
            )
            delete_button.pack(side="left")

    def _create_faena(self) -> None:
        title = self.title_entry.get().strip()
        category = self.category_entry.get().strip() or "General"

        if not title:
            return

        try:
            hours = int(self.hours_entry.get().strip())
        except ValueError:
            hours = 1

        try:
            week_number = int(self.week_entry.get().strip())
        except ValueError:
            week_number = 1

        FaenaService.create_faena(
            title=title,
            category=category,
            hours=hours,
            week_number=week_number,
        )

        self.title_entry.delete(0, "end")
        self.hours_entry.delete(0, "end")
        self.hours_entry.insert(0, "1")

        self._render_faenas()

    def _toggle_faena(self, faena_id: int) -> None:
        FaenaService.toggle_completed(faena_id)
        self._render_faenas()

    def _delete_faena(self, faena_id: int) -> None:
        FaenaService.delete_faena(faena_id)
        self._render_faenas()