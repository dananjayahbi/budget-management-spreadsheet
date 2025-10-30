"""
Settings Tab - Application settings and configuration
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class SettingsTab:
    """Settings and configuration tab"""
    
    def __init__(self, parent, config_manager, db_manager, colors):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.colors = colors
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=colors['bg'])
        
        # Build UI
        self._build_ui()
        
    def _build_ui(self):
        """Build settings UI"""
        # Create scrollable canvas
        canvas = tk.Canvas(self.frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        
        content_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
            
        content_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Mouse wheel scrolling - Fixed
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)
                
        bind_mousewheel(content_frame)
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Add padding
        padding = tk.Frame(content_frame, bg=self.colors['bg'], height=20)
        padding.pack(fill="x")
        
        # Budget settings
        self._create_budget_settings(content_frame)
        
        # Data management
        self._create_data_management(content_frame)
        
        # About section
        self._create_about_section(content_frame)
        
    def _create_budget_settings(self, parent):
        """Create budget configuration section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="x", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="💰 Budget Settings",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Settings card
        card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        card.pack(fill="x")
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Monthly budget
        budget_frame = tk.Frame(card, bg=self.colors['card'])
        budget_frame.pack(fill="x", padx=30, pady=20)
        
        budget_label = tk.Label(budget_frame,
                               text="Monthly Budget Limit ($):",
                               bg=self.colors['card'],
                               fg=self.colors['dark'],
                               font=('Segoe UI', 11),
                               anchor='w')
        budget_label.pack(fill="x", pady=(0, 10))
        
        budget_input_frame = tk.Frame(budget_frame, bg=self.colors['card'])
        budget_input_frame.pack(fill="x")
        
        current_budget = self.config_manager.get_monthly_budget()
        self.budget_var = tk.StringVar(value=str(current_budget))
        
        budget_entry = tk.Entry(budget_input_frame,
                               textvariable=self.budget_var,
                               font=('Segoe UI', 12),
                               relief="solid",
                               borderwidth=1,
                               width=20)
        budget_entry.pack(side="left", ipady=8)
        
        save_budget_btn = tk.Button(budget_input_frame,
                                    text="💾 Save",
                                    bg=self.colors['success'],
                                    fg=self.colors['white'],
                                    font=('Segoe UI', 10, 'bold'),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self._save_budget,
                                    padx=20,
                                    pady=8)
        save_budget_btn.pack(side="left", padx=(10, 0))
        
        # Budget alert
        alert_frame = tk.Frame(card, bg=self.colors['card'])
        alert_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.alert_var = tk.BooleanVar(value=self.config_manager.get_budget_alert())
        
        alert_check = tk.Checkbutton(alert_frame,
                                    text="Alert me when I exceed my budget",
                                    variable=self.alert_var,
                                    bg=self.colors['card'],
                                    fg=self.colors['dark'],
                                    font=('Segoe UI', 10),
                                    selectcolor=self.colors['card'],
                                    command=self._save_alert_setting)
        alert_check.pack(anchor='w')
        
    def _create_data_management(self, parent):
        """Create data management section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="x", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="💾 Data Management",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Data card
        card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        card.pack(fill="x")
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        data_frame = tk.Frame(card, bg=self.colors['card'])
        data_frame.pack(fill="x", padx=30, pady=20)
        
        # Export data
        export_label = tk.Label(data_frame,
                               text="Export your data to Excel:",
                               bg=self.colors['card'],
                               fg=self.colors['dark'],
                               font=('Segoe UI', 11),
                               anchor='w')
        export_label.pack(fill="x", pady=(0, 10))
        
        export_btn = tk.Button(data_frame,
                              text="📤 Export to Excel",
                              bg=self.colors['success'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 10, 'bold'),
                              relief="flat",
                              cursor="hand2",
                              command=self._export_data,
                              padx=20,
                              pady=10)
        export_btn.pack(anchor='w', pady=(0, 20))
        
        # Import data
        import_label = tk.Label(data_frame,
                               text="Import data from Excel:",
                               bg=self.colors['card'],
                               fg=self.colors['dark'],
                               font=('Segoe UI', 11),
                               anchor='w')
        import_label.pack(fill="x", pady=(0, 10))
        
        import_btn = tk.Button(data_frame,
                              text="📥 Import from Excel",
                              bg=self.colors['secondary'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 10, 'bold'),
                              relief="flat",
                              cursor="hand2",
                              command=self._import_data,
                              padx=20,
                              pady=10)
        import_btn.pack(anchor='w', pady=(0, 20))
        
        # Data location
        location_label = tk.Label(data_frame,
                                 text="Data Location:",
                                 bg=self.colors['card'],
                                 fg=self.colors['dark'],
                                 font=('Segoe UI', 11),
                                 anchor='w')
        location_label.pack(fill="x", pady=(0, 10))
        
        data_path = self.db_manager.get_data_path()
        path_label = tk.Label(data_frame,
                             text=data_path,
                             bg=self.colors['card'],
                             fg=self.colors['secondary'],
                             font=('Segoe UI', 9),
                             anchor='w',
                             cursor="hand2")
        path_label.pack(fill="x")
        path_label.bind("<Button-1>", lambda e: self._open_data_folder())
        
        open_folder_btn = tk.Button(data_frame,
                                    text="📁 Open Data Folder",
                                    bg=self.colors['warning'],
                                    fg=self.colors['white'],
                                    font=('Segoe UI', 10, 'bold'),
                                    relief="flat",
                                    cursor="hand2",
                                    command=self._open_data_folder,
                                    padx=20,
                                    pady=10)
        open_folder_btn.pack(anchor='w', pady=(10, 0))
        
    def _create_about_section(self, parent):
        """Create about section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="x", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="ℹ️ About",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # About card
        card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        card.pack(fill="x")
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        about_frame = tk.Frame(card, bg=self.colors['card'])
        about_frame.pack(fill="x", padx=30, pady=30)
        
        # App info
        app_name = tk.Label(about_frame,
                           text="Budget Manager Pro",
                           bg=self.colors['card'],
                           fg=self.colors['primary'],
                           font=('Segoe UI', 16, 'bold'))
        app_name.pack(pady=(0, 5))
        
        version = tk.Label(about_frame,
                          text="Version 1.0.0",
                          bg=self.colors['card'],
                          fg=self.colors['dark'],
                          font=('Segoe UI', 10))
        version.pack(pady=(0, 15))
        
        description = tk.Label(about_frame,
                              text="A modern, feature-rich budget management application\nto track expenses and manage your finances efficiently.",
                              bg=self.colors['card'],
                              fg=self.colors['dark'],
                              font=('Segoe UI', 10),
                              justify='center')
        description.pack(pady=(0, 20))
        
        # Credits
        credits = tk.Label(about_frame,
                          text="Built with Python & Tkinter",
                          bg=self.colors['card'],
                          fg=self.colors['dark'],
                          font=('Segoe UI', 9, 'italic'))
        credits.pack()
        
    def _save_budget(self):
        """Save budget setting"""
        try:
            budget = float(self.budget_var.get())
            if budget < 0:
                messagebox.showwarning("Invalid Budget", "Budget cannot be negative")
                return
            
            self.config_manager.set_monthly_budget(budget)
            messagebox.showinfo("Success", "Budget saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            
    def _save_alert_setting(self):
        """Save alert setting"""
        self.config_manager.set_budget_alert(self.alert_var.get())
            
    def _export_data(self):
        """Export data to Excel"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Export Data"
        )
        
        if filename:
            try:
                self.db_manager.export_to_excel(filename)
                messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data:\n{str(e)}")
                
    def _import_data(self):
        """Import data from Excel"""
        filename = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
            title="Import Data"
        )
        
        if filename:
            if messagebox.askyesno("Confirm Import", 
                                  "This will add data from the file. Continue?"):
                try:
                    self.db_manager.import_from_excel(filename)
                    messagebox.showinfo("Success", "Data imported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to import data:\n{str(e)}")
                    
    def _open_data_folder(self):
        """Open data folder in file explorer"""
        data_path = self.db_manager.get_data_path()
        data_dir = os.path.dirname(data_path)
        
        try:
            os.startfile(data_dir)
        except:
            messagebox.showinfo("Data Folder", data_dir)
