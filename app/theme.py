import customtkinter as ctk

APP_THEME = {
    "bg_primary": "#0f1720",
    "bg_secondary": "#161f2b",
    "bg_tertiary": "#1c2735",
    "accent_cyan": "#32d4c8",
    "accent_copper": "#9a6b3f",
    "text_primary": "#f3f4f6",
    "text_secondary": "#9ca3af",
    "border": "#243244",
}

def setup_theme() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")