import tkinter as tk
from tkinter import Canvas

from database_manager import MoodboardDB
from moodboard import MoodboardApp

class InitialLoadScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Moodboard Welcome")
        self.root.geometry("850x400")

        # # Initialize database
        self.db = MoodboardDB()
        self.current_project_id = None

    def create_selection_boxes(self):
        """
        Create the initial selection options on start screen
        """
        # Create selection boxes for project creation and loading
        canvas = Canvas(self.root, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_text(400, 75, text="Welcome to Moodboard", font=("Arial", 20, "bold"))

        # Project creation box
        canvas.create_rectangle(100, 100, 400, 250, fill="beige", outline="black", tags="create")
        canvas.create_text(250, 175, text="Create New Project", font=("Arial", 16), tags="create")

        # Project loading box
        canvas.create_rectangle(450, 100, 750, 250, fill="grey", outline="black", tags="load")
        canvas.create_text(600, 175, text="Load Existing Project", font=("Arial", 16), tags="load")

        # Bind click events
        canvas.tag_bind("create", "<Button-1>", self.on_create_click)
        canvas.tag_bind("load", "<Button-1>", self.on_load_click)

    def on_create_click(self, event):
        return

    def on_load_click(self, event):
        # Destroy the initial screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Now create the moodboard app in the cleared window
        MoodboardApp(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = InitialLoadScreen(root)
    app.create_selection_boxes()
    root.mainloop()