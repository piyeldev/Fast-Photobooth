import customtkinter as ctk
import components.fonts as CustomFonts
class MainView:
    def __init__(self, root):
        self.root = root

        self.test()

    def test(self):
        text = ctk.CTkLabel(
            self.root,
            text="poppins",
            font=CustomFonts.Poppins.regular()
        )

        text_not = ctk.CTkLabel(
            self.root,
            text="not poppins",
        )

        text.grid(row=0, column=0)
        text_not.grid(row=0, column=1)

    def on_closing(self):
        self.root.destroy()