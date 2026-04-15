import customtkinter as ctk

from app.theme import APP_THEME, setup_theme
from modules.dashboard.view import DashboardView
from modules.jinete.view import JineteView
from modules.roadmap.view import RoadmapView
from modules.telemetry.view import TelemetryView
from modules.sandwichan.view import SandwichanView
from modules.xcom_bridge.view import XcomBridgeView
from modules.faenas.view import FaenasView


class CareerOSApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        setup_theme()

        self.title("Career OS")
        self.geometry("1440x920")
        self.minsize(1180, 760)
        self.configure(fg_color=APP_THEME["bg_primary"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=270,
            corner_radius=0,
            fg_color=APP_THEME["bg_secondary"],
            border_width=1,
            border_color=APP_THEME["border"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=APP_THEME["bg_primary"],
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.active_view = None
        self.nav_buttons = {}

        self._build_sidebar()
        self.show_view("dashboard")

    def _build_sidebar(self) -> None:
        title = ctk.CTkLabel(
            self.sidebar,
            text="Career OS",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        title.grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Modern Western Command",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=APP_THEME["accent_cyan"],
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 22), sticky="w")

        nav_items = [
            ("dashboard", "Dashboard"),
            ("roadmap", "Mapa de Ruta"),
            ("telemetry", "Dinamo 400 SS"),
            ("sandwichan", "Sandwichan"),
            ("xcom", "XCOM Bridge"),
            ("jinete", "Jinete"),
            ("faenas", "Faenas"),
        ]

        for index, (key, label) in enumerate(nav_items, start=2):
            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=46,
                corner_radius=14,
                fg_color=APP_THEME["bg_tertiary"],
                hover_color=APP_THEME["accent_copper_hover"],
                text_color=APP_THEME["text_primary"],
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda route=key: self.show_view(route),
            )
            button.grid(row=index, column=0, padx=18, pady=8, sticky="ew")
            self.nav_buttons[key] = button

        footer = ctk.CTkLabel(
            self.sidebar,
            text="El Jinete programa su salida.",
            text_color=APP_THEME["text_muted"],
        )
        footer.grid(row=9, column=0, padx=20, pady=(8, 20), sticky="sw")

    def _clear_content(self) -> None:
        if self.active_view is not None:
            self.active_view.destroy()
            self.active_view = None

    def show_view(self, route: str) -> None:
        self._clear_content()

        views = {
            "dashboard": DashboardView,
            "roadmap": RoadmapView,
            "telemetry": TelemetryView,
            "sandwichan": SandwichanView,
            "xcom": XcomBridgeView,
            "jinete": JineteView,
            "faenas": FaenasView,
        }

        view_class = views.get(route, DashboardView)
        self.active_view = view_class(self.content)
        self.active_view.grid(row=0, column=0, sticky="nsew")

        self._update_nav_state(route)

    def _update_nav_state(self, active_route: str) -> None:
        for key, button in self.nav_buttons.items():
            if key == active_route:
                button.configure(
                    fg_color=APP_THEME["accent_cyan"],
                    hover_color=APP_THEME["accent_cyan_hover"],
                    text_color="#081018",
                )
            else:
                button.configure(
                    fg_color=APP_THEME["bg_tertiary"],
                    hover_color=APP_THEME["accent_copper_hover"],
                    text_color=APP_THEME["text_primary"],
                )


if __name__ == "__main__":
    app = CareerOSApp()
    app.mainloop()