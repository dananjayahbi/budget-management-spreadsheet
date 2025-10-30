"""
Analytics Tab - Charts and reports
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar

class AnalyticsTab:
    """Analytics and reporting tab"""
    
    def __init__(self, parent, config_manager, db_manager, colors):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.colors = colors
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=colors['bg'])
        
        # Build UI
        self._build_ui()
        
    def _build_ui(self):
        """Build analytics UI"""
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
        
        # Period selector
        self._create_period_selector(content_frame)
        
        # Statistics summary
        self._create_statistics_summary(content_frame)
        
        # Category breakdown
        self._create_category_breakdown(content_frame)
        
        # Monthly trends
        self._create_monthly_trends(content_frame)
        
        # Spending insights
        self._create_spending_insights(content_frame)
        
    def _create_period_selector(self, parent):
        """Create period selection controls"""
        selector_frame = tk.Frame(parent, bg=self.colors['bg'])
        selector_frame.pack(fill="x", padx=30, pady=10)
        
        label = tk.Label(selector_frame,
                        text="Analysis Period:",
                        bg=self.colors['bg'],
                        fg=self.colors['dark'],
                        font=('Segoe UI', 11, 'bold'))
        label.pack(side="left", padx=(0, 15))
        
        self.period_var = tk.StringVar(value="This Month")
        periods = ["This Week", "This Month", "Last Month", "Last 3 Months", "This Year", "All Time"]
        
        period_combo = ttk.Combobox(selector_frame,
                                   textvariable=self.period_var,
                                   values=periods,
                                   font=('Segoe UI', 10),
                                   state='readonly',
                                   width=20)
        period_combo.pack(side="left")
        period_combo.bind('<<ComboboxSelected>>', lambda e: self._refresh_analytics())
        
        refresh_btn = tk.Button(selector_frame,
                               text="🔄 Refresh",
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               font=('Segoe UI', 10, 'bold'),
                               relief="flat",
                               cursor="hand2",
                               command=self._refresh_analytics,
                               padx=15,
                               pady=5)
        refresh_btn.pack(side="left", padx=(15, 0))
        
    def _create_statistics_summary(self, parent):
        """Create statistics summary cards"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="x", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="Summary Statistics",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Stats container
        stats_container = tk.Frame(section_frame, bg=self.colors['bg'])
        stats_container.pack(fill="x")
        
        # Get statistics
        stats = self._get_statistics()
        
        # Create stat cards
        self._create_stat_card(stats_container, "Total Transactions", 
                              str(stats['total_transactions']), "📊", 0)
        self._create_stat_card(stats_container, "Average Expense", 
                              f"${stats['avg_expense']:.2f}", "💵", 1)
        self._create_stat_card(stats_container, "Highest Expense", 
                              f"${stats['highest_expense']:.2f}", "📈", 2)
        self._create_stat_card(stats_container, "Total Income", 
                              f"${self.db_manager.get_current_month_income():.2f}", "💵", 3)
        
    def _create_stat_card(self, parent, title, value, icon, index):
        """Create a small stat card"""
        card = tk.Frame(parent, bg=self.colors['card'], relief="flat")
        card.grid(row=0, column=index, padx=8, pady=10, sticky="nsew")
        card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        parent.grid_columnconfigure(index, weight=1)
        
        # Icon
        icon_label = tk.Label(card,
                             text=icon,
                             bg=self.colors['card'],
                             font=('Segoe UI', 20))
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = tk.Label(card,
                              text=value,
                              bg=self.colors['card'],
                              fg=self.colors['primary'],
                              font=('Segoe UI', 16, 'bold'),
                              wraplength=280)
        value_label.pack(pady=5)
        
        # Title
        title_label = tk.Label(card,
                              text=title,
                              bg=self.colors['card'],
                              fg=self.colors['dark'],
                              font=('Segoe UI', 9),
                              wraplength=280)
        title_label.pack(pady=(5, 15))
        
        card.configure(height=150)
        card.pack_propagate(False)
        
    def _create_category_breakdown(self, parent):
        """Create spending overview chart"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="both", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="Spending Overview",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Chart container
        chart_card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        chart_card.pack(fill="both", expand=True)
        chart_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Show simple statistics instead of category breakdown
        transactions = self.db_manager.get_filtered_transactions(self.period_var.get())
        expenses = [t for t in transactions if t['type'] == 'expense']
        income = [t for t in transactions if t['type'] == 'income']
        
        if expenses or income:
            stats_frame = tk.Frame(chart_card, bg=self.colors['card'])
            stats_frame.pack(fill="both", expand=True, padx=40, pady=30)
            
            # Total Expenses
            if expenses:
                exp_total = sum(e['amount'] for e in expenses)
                self._create_stat_row(stats_frame, "Total Expenses", f"${exp_total:,.2f}", 
                                     self.colors['danger'], exp_total, exp_total if exp_total > 0 else 1)
            
            # Total Income
            if income:
                inc_total = sum(i['amount'] for i in income)
                max_val = max(inc_total, sum(e['amount'] for e in expenses) if expenses else 0)
                self._create_stat_row(stats_frame, "Total Income", f"${inc_total:,.2f}", 
                                     self.colors['success'], inc_total, max_val if max_val > 0 else 1)
        else:
            no_data = tk.Label(chart_card,
                              text="No data available for the selected period",
                              bg=self.colors['card'],
                              fg=self.colors['dark'],
                              font=('Segoe UI', 11),
                              pady=40)
            no_data.pack()
    
    def _create_stat_row(self, parent, label, value, color, amount, max_amount):
        """Create a statistics row with bar"""
        row_frame = tk.Frame(parent, bg=self.colors['card'])
        row_frame.pack(fill="x", pady=12)
        
        # Label
        label_widget = tk.Label(row_frame,
                               text=label,
                               bg=self.colors['card'],
                               fg=self.colors['dark'],
                               font=('Segoe UI', 11),
                               width=18,
                               anchor='w')
        label_widget.pack(side="left", padx=(0, 15))
        
        # Bar background
        bar_bg = tk.Frame(row_frame, bg=self.colors['light'], height=30)
        bar_bg.pack(side="left", fill="x", expand=True)
        
        # Filled bar
        if max_amount > 0:
            percentage = (amount / max_amount) * 100
        else:
            percentage = 0
            
        bar_fill = tk.Frame(bar_bg, bg=color, height=30)
        bar_fill.place(x=0, y=0, relwidth=percentage/100, relheight=1)
        
        # Value label
        value_widget = tk.Label(row_frame,
                               text=value,
                               bg=self.colors['card'],
                               fg=color,
                               font=('Segoe UI', 11, 'bold'),
                               width=15,
                               anchor='e')
        value_widget.pack(side="right", padx=(15, 0))
        
    def _create_monthly_trends(self, parent):
        """Create monthly trends section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="both", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="Monthly Trends (Last 6 Months)",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Trends container
        trends_card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        trends_card.pack(fill="both", expand=True)
        trends_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Get monthly data
        monthly_data = self._get_monthly_trends()
        
        if monthly_data:
            # Create simple line chart representation
            chart_frame = tk.Frame(trends_card, bg=self.colors['card'])
            chart_frame.pack(fill="both", expand=True, padx=30, pady=20)
            
            max_value = max(monthly_data.values()) if monthly_data else 0
            
            for month, amount in monthly_data.items():
                self._create_trend_bar(chart_frame, month, amount, max_value)
        else:
            no_data = tk.Label(trends_card,
                              text="No trend data available",
                              bg=self.colors['card'],
                              fg=self.colors['dark'],
                              font=('Segoe UI', 11),
                              pady=40)
            no_data.pack()
            
    def _create_trend_bar(self, parent, month, amount, max_value):
        """Create a trend bar for monthly data"""
        bar_container = tk.Frame(parent, bg=self.colors['card'])
        bar_container.pack(side="left", fill="both", expand=True, padx=5)
        
        # Calculate height percentage
        if max_value > 0:
            height_pct = (amount / max_value) * 100
        else:
            height_pct = 0
            
        # Bar (inverted - grows from bottom)
        bar_frame = tk.Frame(bar_container, bg=self.colors['card'], height=200)
        bar_frame.pack(fill="x")
        bar_frame.pack_propagate(False)
        
        # Spacer (creates bottom-up effect)
        spacer_height = int(200 * (1 - height_pct / 100))
        if spacer_height > 0:
            spacer = tk.Frame(bar_frame, bg=self.colors['card'], height=spacer_height)
            spacer.pack(side="top", fill="x")
        
        # Actual bar
        bar = tk.Frame(bar_frame, bg=self.colors['secondary'])
        bar.pack(side="top", fill="both", expand=True)
        
        # Amount on top
        amount_label = tk.Label(bar_container,
                               text=f"${amount:,.0f}",
                               bg=self.colors['card'],
                               fg=self.colors['dark'],
                               font=('Segoe UI', 9, 'bold'))
        amount_label.pack(pady=5)
        
        # Month label
        month_label = tk.Label(bar_container,
                              text=month,
                              bg=self.colors['card'],
                              fg=self.colors['dark'],
                              font=('Segoe UI', 9))
        month_label.pack()
        
    def _create_spending_insights(self, parent):
        """Create spending insights section"""
        section_frame = tk.Frame(parent, bg=self.colors['bg'])
        section_frame.pack(fill="both", padx=30, pady=20)
        
        title = tk.Label(section_frame,
                        text="💡 Spending Insights",
                        bg=self.colors['bg'],
                        fg=self.colors['primary'],
                        font=('Segoe UI', 14, 'bold'),
                        anchor='w')
        title.pack(fill="x", pady=(0, 10))
        
        # Insights container
        insights_card = tk.Frame(section_frame, bg=self.colors['card'], relief="flat")
        insights_card.pack(fill="both", expand=True)
        insights_card.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Get insights
        insights = self._generate_insights()
        
        for i, insight in enumerate(insights):
            insight_frame = tk.Frame(insights_card, bg=self.colors['card'])
            insight_frame.pack(fill="x", padx=30, pady=12)
            
            # Bullet point
            bullet = tk.Label(insight_frame,
                            text="•",
                            bg=self.colors['card'],
                            fg=self.colors['secondary'],
                            font=('Segoe UI', 16, 'bold'))
            bullet.pack(side="left", padx=(0, 10))
            
            # Insight text
            text = tk.Label(insight_frame,
                          text=insight,
                          bg=self.colors['card'],
                          fg=self.colors['dark'],
                          font=('Segoe UI', 10),
                          wraplength=550,
                          justify='left',
                          anchor='w')
            text.pack(side="left", fill="x", expand=True)
            
    def _get_statistics(self):
        """Get statistical data"""
        transactions = self.db_manager.get_filtered_transactions(self.period_var.get())
        expenses = [t for t in transactions if t['type'] == 'expense']
        
        if not expenses:
            return {
                'total_transactions': 0,
                'avg_expense': 0,
                'highest_expense': 0,
                'top_category': 'N/A'
            }
        
        amounts = [e['amount'] for e in expenses]
        
        return {
            'total_transactions': len(expenses),
            'avg_expense': sum(amounts) / len(amounts),
            'highest_expense': max(amounts),
            'top_category': 'General'  # Since we removed categories
        }
        
    def _get_monthly_trends(self):
        """Get last 6 months trends"""
        trends = {}
        today = datetime.now()
        
        for i in range(6):
            month_date = today - timedelta(days=30 * i)
            month_name = month_date.strftime('%b')
            
            # Get transactions for this month
            month_total = self.db_manager.get_month_total(
                month_date.year, 
                month_date.month
            )
            trends[month_name] = month_total
            
        # Reverse to show oldest first
        return dict(reversed(list(trends.items())))
        
    def _generate_insights(self):
        """Generate spending insights"""
        insights = []
        
        stats = self._get_statistics()
        
        if stats['total_transactions'] > 0:
            insights.append(f"You've made {stats['total_transactions']} transactions in this period.")
            insights.append(f"Your average expense is ${stats['avg_expense']:.2f}.")
            insights.append(f"Your highest single expense was ${stats['highest_expense']:.2f}.")
                
            budget = self.config_manager.get_monthly_budget()
            if budget > 0:
                current_spending = self.db_manager.get_current_month_total()
                if current_spending > budget:
                    insights.append(f"⚠️ You've exceeded your monthly budget by ${current_spending - budget:.2f}!")
                else:
                    insights.append(f"✅ You're within budget! ${budget - current_spending:.2f} remaining.")
        else:
            insights.append("No transaction data available for the selected period.")
            insights.append("Start tracking your expenses to get personalized insights!")
            
        return insights
        
    def _refresh_analytics(self):
        """Refresh all analytics data"""
        # Rebuild the entire UI
        for widget in self.frame.winfo_children():
            widget.destroy()
        self._build_ui()
