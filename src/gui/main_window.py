"""
Main Window GUI
Modern, minimalistic interface with tabbed navigation
"""
import tkinter as tk
from tkinter import ttk
from gui.dashboard import DashboardTab
from gui.expenses import ExpensesTab
from gui.analytics import AnalyticsTab
from gui.settings import SettingsTab

class MainWindow:
    """Main application window with tabbed interface"""
    
    def __init__(self, root, config_manager, db_manager):
        self.root = root
        self.config_manager = config_manager
        self.db_manager = db_manager
        
        # Configure modern theme
        self._setup_theme()
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg="#f0f0f0")
        self.main_container.pack(fill="both", expand=True)
        
        # Create notebook (tabbed interface)
        self._create_notebook()
        
        # Create status bar
        self._create_status_bar()
        
    def _setup_theme(self):
        """Configure modern theme colors and styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Enhanced color palette
        self.colors = {
            'primary': '#1a2332',
            'primary_light': '#2C3E50',
            'secondary': '#3498DB',
            'secondary_dark': '#2980B9',
            'success': '#27AE60',
            'success_dark': '#229954',
            'danger': '#E74C3C',
            'danger_dark': '#C0392B',
            'warning': '#F39C12',
            'warning_dark': '#E67E22',
            'light': '#ECF0F1',
            'dark': '#34495E',
            'white': '#FFFFFF',
            'bg': '#F5F6FA',
            'card': '#FFFFFF',
            'card_hover': '#F8F9FA',
            'border': '#E1E8ED',
            'text_primary': '#2C3E50',
            'text_secondary': '#7F8C8D',
            'shadow': '#00000015'
        }
        
        # Configure notebook style with enhanced visuals
        style.configure('TNotebook', 
                       background=self.colors['bg'], 
                       borderwidth=0,
                       padding=0)
        style.configure('TNotebook.Tab', 
                       background=self.colors['card'],
                       foreground=self.colors['text_secondary'],
                       padding=[24, 12],
                       font=('Segoe UI', 10),
                       borderwidth=0)
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['white'])],
                 foreground=[('selected', self.colors['primary'])],
                 font=[('selected', ('Segoe UI', 10, 'bold'))],
                 padding=[('selected', [24, 14])])
        
        # Enhanced button styles with hover effects
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Primary.TButton',
                 background=[('active', self.colors['secondary_dark'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Success.TButton',
                 background=[('active', self.colors['success_dark'])])
        
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Danger.TButton',
                 background=[('active', self.colors['danger_dark'])])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Warning.TButton',
                 background=[('active', self.colors['warning_dark'])])
        
    def _create_notebook(self):
        """Create tabbed interface"""
        notebook_frame = tk.Frame(self.main_container, bg=self.colors['bg'])
        notebook_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.dashboard_tab = DashboardTab(self.notebook, self.config_manager, self.db_manager, self.colors, self.notebook)
        self.analytics_tab = AnalyticsTab(self.notebook, self.config_manager, self.db_manager, self.colors)
        self.expenses_tab = ExpensesTab(self.notebook, self.config_manager, self.db_manager, self.colors, self.dashboard_tab, self.analytics_tab)
        self.settings_tab = SettingsTab(self.notebook, self.config_manager, self.db_manager, self.colors)
        
        # Add tabs to notebook
        self.notebook.add(self.dashboard_tab.frame, text="📊 Dashboard")
        self.notebook.add(self.expenses_tab.frame, text="💳 Expenses")
        self.notebook.add(self.analytics_tab.frame, text="📈 Analytics")
        self.notebook.add(self.settings_tab.frame, text="⚙️ Settings")
        
    def _create_status_bar(self):
        """Create enhanced status bar at bottom"""
        status_bar = tk.Frame(self.main_container, bg=self.colors['primary'], height=28)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)
        
        # Status text
        self.status_label = tk.Label(status_bar,
                                     text="● Ready",
                                     bg=self.colors['primary'],
                                     fg=self.colors['light'],
                                     font=('Segoe UI', 9),
                                     anchor='w')
        self.status_label.pack(side="left", padx=25)
        
        # Separator
        separator = tk.Label(status_bar,
                            text="|",
                            bg=self.colors['primary'],
                            fg=self.colors.get('text_secondary', '#7F8C8D'),
                            font=('Segoe UI', 9))
        separator.pack(side="right", padx=10)
        
        # Version info with icon
        version_label = tk.Label(status_bar,
                                text="v1.0.0",
                                bg=self.colors['primary'],
                                fg=self.colors['light'],
                                font=('Segoe UI', 9),
                                anchor='e')
        version_label.pack(side="right", padx=10)
        
        # Data location indicator
        data_indicator = tk.Label(status_bar,
                                 text="💾",
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'],
                                 font=('Segoe UI', 9))
        data_indicator.pack(side="right", padx=(10, 5))
