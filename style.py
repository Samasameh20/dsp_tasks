"""CSS-inspired palette and ttk styling for Tkinter."""
COLORS = {
    "BG": "#F4F7FB", "CARD": "#FFFFFF", "SIDEBAR": "#172033",
    "SIDEBAR_ACTIVE": "#293750", "TEXT": "#172033", "MUTED": "#718096",
    "ACCENT": "#4F7DF3", "BORDER": "#E2E8F0", "SUCCESS": "#16876D",
}
def configure_styles(root):
    from tkinter import ttk
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Modern.TEntry", padding=(10, 9),
        fieldbackground=COLORS["CARD"], foreground=COLORS["TEXT"],
        bordercolor=COLORS["BORDER"], lightcolor=COLORS["BORDER"],
        darkcolor=COLORS["BORDER"])
    style.map("Modern.TEntry", bordercolor=[("focus", COLORS["ACCENT"])],
        lightcolor=[("focus", COLORS["ACCENT"])], darkcolor=[("focus", COLORS["ACCENT"])])
    style.configure("Modern.TCombobox", padding=(8, 7),
        fieldbackground=COLORS["CARD"], background=COLORS["CARD"],
        foreground=COLORS["TEXT"], arrowcolor=COLORS["MUTED"])
    style.map("Modern.TCombobox", fieldbackground=[("readonly", COLORS["CARD"])])
