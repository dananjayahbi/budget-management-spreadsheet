"""
Main Application Class
Manages the tkinter application lifecycle
"""
import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindow
from utils.config_manager import ConfigManager
from utils.database_manager import DatabaseManager
import os

class BudgetApp:
    """Main application controller"""
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title("Budget Manager Pro")
        
        # Set window size optimized for 1920x1080 display
        self.root.geometry("1200x900")
        self.root.minsize(1000, 700)
        
        # Maximize window on startup (Windows)
        self.root.state('zoomed')
        
        # Initialize managers
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        
        # Create main window
        self.main_window = MainWindow(self.root, self.config_manager, self.db_manager)
        
        # Set up close protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Budget Manager?"):
            self.root.destroy()
            
    def run(self):
        """Run the application"""
        self.root.mainloop()
