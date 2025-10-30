"""
Dashboard Tab - Overview of finances
"""
import tkinter as tk
from tkinter import ttk
import datetime

class DashboardTab:
    """Dashboard showing financial overview"""
    
    def __init__(self, parent, config_manager, db_manager, colors, notebook=None):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.colors = colors
        self.notebook = notebook  # Store notebook reference for tab switching
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=colors['bg'])
        
        # Create scrollable canvas
        self._create_scrollable_content()
        
    def _create_scrollable_content(self):
        """Create scrollable content area"""
        # Create canvas and scrollbar
        canvas = tk.Canvas(self.frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        
        self.content_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Update scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update window width to match canvas
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
            
        self.content_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Mouse wheel scrolling - Fixed to work properly
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        # Bind mousewheel to canvas and all children
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)
                
        bind_mousewheel(self.content_frame)
        canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Build dashboard content
        self._build_dashboard()
        
    def _build_dashboard(self):
        """Build dashboard content"""
        # Add padding
        padding_frame = tk.Frame(self.content_frame, bg=self.colors['bg'], height=20)
        padding_frame.pack(fill="x")
        
        # Summary cards
        self._create_summary_cards()
        
        # Recent transactions
        self._create_recent_transactions()
        
        # Quick actions
        self._create_quick_actions()
        
    def _create_summary_cards(self):
        """Create summary cards showing key metrics"""
        cards_container = tk.Frame(self.content_frame, bg=self.colors['bg'])
        cards_container.pack(fill="x", padx=30, pady=10)
        
        # Get current month data
        current_month_expenses = self.db_manager.get_current_month_total()
        current_month_income = self.db_manager.get_current_month_income()
        balance = current_month_income - current_month_expenses
        budget = self.config_manager.get_monthly_budget()
        budget_remaining = budget - current_month_expenses if budget > 0 else 0
        
        # Card 1: Monthly Expenses
        self._create_card(cards_container, 
                         "Total Expenses",
                         f"${current_month_expenses:,.2f}",
                         self.colors['danger'],
                         0, 0)
        
        # Card 2: Monthly Income
        self._create_card(cards_container,
                         "Total Income",
                         f"${current_month_income:,.2f}",
                         self.colors['success'],
                         0, 1)
        
        # Card 3: Balance
        balance_color = self.colors['success'] if balance >= 0 else self.colors['danger']
        self._create_card(cards_container,
                         "Balance",
                         f"${balance:,.2f}",
                         balance_color,
                         1, 0)
        
        # Card 4: Budget Remaining
        self._create_card(cards_container,
                         "Budget Remaining",
                         f"${budget_remaining:,.2f}" if budget > 0 else "No Budget Set",
                         self.colors['warning'],
                         1, 1)
        
    def _create_card(self, parent, title, value, color, row, col):
        """Create a summary card with enhanced modern styling"""
        # Outer frame for shadow effect
        shadow_frame = tk.Frame(parent, bg="#e0e0e0", relief="flat")
        shadow_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Inner card with gradient-like effect
        card = tk.Frame(shadow_frame, bg=self.colors['card'], relief="flat")
        card.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Add colorful left border accent
        accent_color = color
        accent_bar = tk.Frame(card, bg=accent_color, width=5)
        accent_bar.place(x=0, y=0, relheight=1)
        
        # Icon/Visual indicator - larger and more prominent
        icon_map = {
            'Total Expenses': ('💸', self.colors['danger']),
            'Total Income': ('💰', self.colors['success']),
            'Balance': ('📊', self.colors['secondary']),
            'Budget Remaining': ('🎯', self.colors['warning'])
        }
        icon, icon_bg = icon_map.get(title, ('📌', color))
        
        # Icon circle background
        icon_container = tk.Frame(card, bg=icon_bg, width=60, height=60)
        icon_container.place(x=20, y=15)
        icon_container.pack_propagate(False)
        
        icon_label = tk.Label(icon_container,
                             text=icon,
                             bg=icon_bg,
                             font=('Segoe UI', 26))
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title - positioned to the right of icon
        title_label = tk.Label(card,
                              text=title,
                              bg=self.colors['card'],
                              fg=self.colors.get('text_secondary', '#7F8C8D'),
                              font=('Segoe UI', 10, 'normal'))
        title_label.place(x=95, y=20)
        
        # Value with enhanced typography - larger and bold
        value_label = tk.Label(card,
                              text=value,
                              bg=self.colors['card'],
                              fg=color,
                              font=('Segoe UI', 22, 'bold'),
                              wraplength=350)
        value_label.place(x=95, y=45)
        
        # Set minimum size - optimized for wider screen
        shadow_frame.configure(width=380, height=110)
        shadow_frame.grid_propagate(False)
        
        # Enhanced hover effect with smooth transition feel
        def on_enter(e):
            card.configure(bg='#FAFBFC')
            title_label.configure(bg='#FAFBFC')
            value_label.configure(bg='#FAFBFC')
            shadow_frame.configure(bg="#d0d0d0")
            
        def on_leave(e):
            card.configure(bg=self.colors['card'])
            title_label.configure(bg=self.colors['card'])
            value_label.configure(bg=self.colors['card'])
            shadow_frame.configure(bg="#e0e0e0")
            
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        title_label.bind('<Enter>', on_enter)
        title_label.bind('<Leave>', on_leave)
        value_label.bind('<Enter>', on_enter)
        value_label.bind('<Leave>', on_leave)
        
    def _create_recent_transactions(self):
        """Show recent transactions with enhanced styling"""
        section_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        section_frame.pack(fill="both", padx=30, pady=20)
        
        # Section title with better styling
        title_frame = tk.Frame(section_frame, bg=self.colors['bg'])
        title_frame.pack(fill="x", pady=(0, 15))
        
        title = tk.Label(title_frame,
                        text="📋 Recent Transactions",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(side="left")
        
        # View all link
        view_all = tk.Label(title_frame,
                           text="View All →",
                           bg=self.colors['bg'],
                           fg=self.colors['secondary'],
                           font=('Segoe UI', 10, 'bold'),
                           cursor="hand2")
        view_all.pack(side="right")
        
        # Transactions container (card) with shadow
        shadow_frame = tk.Frame(section_frame, bg="#d0d0d0", relief="flat")
        shadow_frame.pack(fill="both", expand=True)
        
        transactions_card = tk.Frame(shadow_frame, bg=self.colors['card'], relief="flat")
        transactions_card.place(x=0, y=0, relwidth=1, relheight=1)
        transactions_card.configure(highlightbackground=self.colors.get('border', '#e0e0e0'), 
                                   highlightthickness=1)
        
        # Get recent transactions
        recent = self.db_manager.get_recent_transactions(5)
        
        if recent:
            for i, transaction in enumerate(recent):
                self._create_transaction_row(transactions_card, transaction, i)
        else:
            # No transactions yet - improved empty state
            empty_frame = tk.Frame(transactions_card, bg=self.colors['card'])
            empty_frame.pack(expand=True, fill="both", pady=50)
            
            empty_icon = tk.Label(empty_frame,
                                 text="📝",
                                 bg=self.colors['card'],
                                 font=('Segoe UI', 48))
            empty_icon.pack(pady=(0, 15))
            
            no_data = tk.Label(empty_frame,
                              text="No transactions yet",
                              bg=self.colors['card'],
                              fg=self.colors['primary'],
                              font=('Segoe UI', 13, 'bold'))
            no_data.pack(pady=(0, 5))
            
            sub_text = tk.Label(empty_frame,
                               text="Start adding expenses to track your spending!",
                               bg=self.colors['card'],
                               fg=self.colors.get('text_secondary', self.colors['dark']),
                               font=('Segoe UI', 10))
            sub_text.pack()
            
    def _create_transaction_row(self, parent, transaction, index):
        """Create a transaction row with hover effects"""
        row = tk.Frame(parent, bg=self.colors['card'], cursor="hand2")
        row.pack(fill="x", padx=20, pady=8)
        
        # Add separator line except for first item
        if index > 0:
            separator = tk.Frame(parent, bg=self.colors.get('border', '#E1E8ED'), height=1)
            separator.pack(fill="x", padx=20, pady=0)
            separator.pack_forget()  # Pack before the row
            separator.pack(fill="x", padx=20, pady=0, before=row)
        
        # Icon/Category indicator with background
        icon_bg = tk.Frame(row, bg=self.colors.get('light', '#ECF0F1'), 
                          width=45, height=45)
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)
        
        # Use transaction type icon
        type_icon = '💸' if transaction['type'] == 'expense' else '💰'
        
        category_label = tk.Label(icon_bg,
                                 text=type_icon,
                                 bg=self.colors.get('light', '#ECF0F1'),
                                 fg=self.colors['secondary'],
                                 font=('Segoe UI', 18))
        category_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Transaction info
        info_frame = tk.Frame(row, bg=self.colors['card'])
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Description with better typography
        desc_label = tk.Label(info_frame,
                             text=transaction['description'],
                             bg=self.colors['card'],
                             fg=self.colors.get('text_primary', self.colors['dark']),
                             font=('Segoe UI', 11, 'bold'),
                             anchor='w')
        desc_label.pack(fill="x")
        
        # Date only (removed category)
        detail_text = f"{transaction['date']}"
        detail_label = tk.Label(info_frame,
                               text=detail_text,
                               bg=self.colors['card'],
                               fg=self.colors.get('text_secondary', '#7f8c8d'),
                               font=('Segoe UI', 9),
                               anchor='w')
        detail_label.pack(fill="x")
        
        # Amount with enhanced styling
        amount_color = self.colors['danger'] if transaction['type'] == 'expense' else self.colors['success']
        amount_prefix = "-" if transaction['type'] == 'expense' else "+"
        
        amount_frame = tk.Frame(row, bg=self.colors['card'])
        amount_frame.pack(side="right", padx=10)
        
        amount_label = tk.Label(amount_frame,
                               text=f"{amount_prefix}${transaction['amount']:,.2f}",
                               bg=self.colors['card'],
                               fg=amount_color,
                               font=('Segoe UI', 13, 'bold'))
        amount_label.pack()
        
        # Hover effect for entire row
        def on_enter(e):
            row.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            info_frame.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            desc_label.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            detail_label.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            amount_frame.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            amount_label.configure(bg=self.colors.get('card_hover', '#f8f9fa'))
            
        def on_leave(e):
            row.configure(bg=self.colors['card'])
            info_frame.configure(bg=self.colors['card'])
            desc_label.configure(bg=self.colors['card'])
            detail_label.configure(bg=self.colors['card'])
            amount_frame.configure(bg=self.colors['card'])
            amount_label.configure(bg=self.colors['card'])
            
        # Bind hover to all elements
        for widget in [row, info_frame, desc_label, detail_label, amount_frame, amount_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
    def _get_category_icon(self, category):
        """Get emoji icon for category"""
        icons = {
            'Food': '🍔',
            'Transport': '🚗',
            'Entertainment': '🎬',
            'Shopping': '🛍️',
            'Bills': '📄',
            'Healthcare': '⚕️',
            'Education': '📚',
            'Salary': '💼',
            'Other': '📌'
        }
        return icons.get(category, '📌')
        
    def _create_quick_actions(self):
        """Create quick action buttons with enhanced styling"""
        section_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        section_frame.pack(fill="x", padx=30, pady=20)
        
        # Section title
        title = tk.Label(section_frame,
                        text="⚡ Quick Actions",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 15))
        
        # Buttons container
        buttons_frame = tk.Frame(section_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill="x")
        
        # Enhanced button style
        def create_action_button(parent, text, icon, bg_color, hover_color, command):
            btn = tk.Button(parent,
                           text=f"{icon} {text}",
                           bg=bg_color,
                           fg=self.colors['white'],
                           font=('Segoe UI', 11, 'bold'),
                           relief="flat",
                           cursor="hand2",
                           command=command,
                           padx=25,
                           pady=15,
                           borderwidth=0,
                           activebackground=hover_color,
                           activeforeground=self.colors['white'])
            
            # Hover effects
            def on_enter(e):
                btn['background'] = hover_color
                
            def on_leave(e):
                btn['background'] = bg_color
                
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            
            return btn
        
        # Quick add expense button
        add_btn = create_action_button(
            buttons_frame,
            "Add Expense",
            "➕",
            self.colors['secondary'],
            self.colors.get('secondary_dark', '#2980B9'),
            self._quick_add_expense
        )
        add_btn.pack(side="left", padx=(0, 12))
        
        # View reports button
        report_btn = create_action_button(
            buttons_frame,
            "View Reports",
            "📊",
            self.colors['success'],
            self.colors.get('success_dark', '#229954'),
            self._view_reports
        )
        report_btn.pack(side="left", padx=(0, 12))
        
        # Add income button
        income_btn = create_action_button(
            buttons_frame,
            "Add Income",
            "💵",
            self.colors['warning'],
            self.colors.get('warning_dark', '#E67E22'),
            self._quick_add_income
        )
        income_btn.pack(side="left")
        
    def _quick_add_expense(self):
        """Quick add expense from dashboard"""
        # Switch to expenses tab (tab index 1)
        if self.notebook:
            self.notebook.select(1)
        
    def _quick_add_income(self):
        """Quick add income from dashboard"""
        # Switch to expenses tab (tab index 1)
        if self.notebook:
            self.notebook.select(1)
        
    def _view_reports(self):
        """View reports"""
        # Switch to analytics tab (tab index 2)
        if self.notebook:
            self.notebook.select(2)
    
    def refresh_data(self):
        """Refresh dashboard data after adding new transactions"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Rebuild UI
        self._build_dashboard()
