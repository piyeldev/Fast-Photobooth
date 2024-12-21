import customtkinter as ctk
from views.main_view import MainView

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Fast Photo")
    root.geometry("1024x600")


    main_view = MainView(root)
    root.protocol("WM_DELETE_WINDOW", main_view.on_closing)
    root.mainloop()