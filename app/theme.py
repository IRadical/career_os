import customtkinter as ctk

APP_THEME = {
    "bg_primary": "#0b1118",
    "bg_secondary": "#121a24",
    "bg_tertiary": "#182230",
    "bg_card": "#1d2938",
    "accent_cyan": "#35d6c9",
    "accent_cyan_hover": "#2ab8ac",
    "accent_copper": "#8b5e3c",
    "accent_copper_hover": "#734b2f",
    "text_primary": "#f3f4f6",
    "text_secondary": "#9aa4b2",
    "text_muted": "#6b7280",
    "border": "#273447",
    "danger": "#d97757",
    "success": "#4ade80",
}

def setup_theme() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")