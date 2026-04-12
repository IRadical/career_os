import customtkinter as ctk
from app.theme import APP_THEME

class XcomBridgeView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=APP_THEME["bg_primary"], corner_radius=0)

        label = ctk.CTkLabel(
            self,
            text="XCOM AI Tactical Bridge",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=APP_THEME["text_primary"],
        )
        label.pack(anchor="w", padx=28, pady=(24, 12))

        desc = ctk.CTkLabel(
            self,
            text="Seguimiento del motor de IA tactica.",
            text_color=APP_THEME["text_secondary"],
        )
        desc.pack(anchor="w", padx=28)