from tkinter.font import Font
from pathlib import Path
import pyglet
from customtkinter import CTkFont

def font_path_with_size(family:str, size: str):
        current_dir = Path(__file__).parent
        project_root = current_dir.parents[1]
        return project_root / f"assets/fonts/{family}/{family}-{size}.ttf"

class Poppins:
    @staticmethod
    def regular():
        pyglet.font.add_file(str(font_path_with_size("Poppins", "Regular")))
        regular = CTkFont(family="Poppins")
        # regular.configure(file=str(font_path_with_size("Poppins", "Regular")))
        return regular