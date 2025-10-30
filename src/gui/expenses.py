"""
Expenses Tab - Add and manage expenses
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

class ExpensesTab:
    """Expenses management tab"""
    
    def __init__(self, parent, config_manager, db_manager, colors, dashboard_tab=None, analytics_tab=None):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.colors = colors
        self.dashboard_tab = dashboard_tab
        self.analytics_tab = analytics_tab
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=colors['bg'])
        
        # Build UI
        self._build_ui()
        
    def _build_ui(self):
        """Build expenses tab UI"""
        # Create two-column layout
        left_panel = tk.Frame(self.frame, bg=self.colors['bg'])
        left_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        right_panel = tk.Frame(self.frame, bg=self.colors['bg'])
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Left panel: Add Expense Form
        self._create_expense_form(left_panel)
        
        # Right panel: Expense List
        self._create_expense_list(right_panel)
        
    def _create_expense_form(self, parent):
        """Create expense entry form with minimalistic design"""
        # Form container with minimal styling
        form_card = tk.Frame(parent, bg=self.colors['bg'])
        form_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Simple title
        title = tk.Label(form_card,
                        text="Add Transaction",
                        bg=self.colors['bg'],
                        fg=self.colors['dark'],
                        font=('Segoe UI', 13, 'bold'))
        title.pack(pady=(0, 15), anchor='w')
        
        # Form fields frame with minimal padding
        fields_frame = tk.Frame(form_card, bg=self.colors['bg'])
        fields_frame.pack(fill="both", expand=True)
        
        # Transaction Type - Inline compact style
        type_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        type_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(type_frame,
                text="Type:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9),
                width=12,
                anchor='w').pack(side="left")
        
        self.type_var = tk.StringVar(value="expense")
        type_inner = tk.Frame(type_frame, bg=self.colors['bg'])
        type_inner.pack(side="left", fill="x", expand=True)
        
        expense_radio = tk.Radiobutton(type_inner,
                                      text="Expense",
                                      variable=self.type_var,
                                      value="expense",
                                      bg=self.colors['bg'],
                                      fg=self.colors['dark'],
                                      font=('Segoe UI', 9),
                                      selectcolor=self.colors['bg'])
        expense_radio.pack(side="left", padx=(0, 15))
        
        income_radio = tk.Radiobutton(type_inner,
                                     text="Income",
                                     variable=self.type_var,
                                     value="income",
                                     bg=self.colors['bg'],
                                     fg=self.colors['dark'],
                                     font=('Segoe UI', 9),
                                     selectcolor=self.colors['bg'])
        income_radio.pack(side="left")
        
        # Amount - Compact inline
        amount_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        amount_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(amount_frame,
                text="Amount ($):",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9),
                width=12,
                anchor='w').pack(side="left")
        
        self.amount_entry = tk.Entry(amount_frame,
                                     font=('Segoe UI', 10),
                                     relief="solid",
                                     borderwidth=1,
                                     bg='white')
        self.amount_entry.pack(side="left", fill="x", expand=True, ipady=6)
        
        # Description - Compact inline
        desc_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        desc_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(desc_frame,
                text="Description:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9),
                width=12,
                anchor='w').pack(side="left")
        
        self.desc_entry = tk.Entry(desc_frame,
                                   font=('Segoe UI', 10),
                                   relief="solid",
                                   borderwidth=1,
                                   bg='white')
        self.desc_entry.pack(side="left", fill="x", expand=True, ipady=6)
        
        # Date - Compact inline
        date_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        date_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(date_frame,
                text="Date:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9),
                width=12,
                anchor='w').pack(side="left")
        
        try:
            self.date_entry = DateEntry(date_frame,
                                       width=18,
                                       background=self.colors['secondary'],
                                       foreground='white',
                                       borderwidth=1,
                                       font=('Segoe UI', 9),
                                       date_pattern='yyyy-mm-dd')
            self.date_entry.pack(side="left", ipady=6)
        except:
            # Fallback if tkcalendar not available
            self.date_entry = tk.Entry(date_frame,
                                      font=('Segoe UI', 10),
                                      relief="solid",
                                      borderwidth=1,
                                      bg='white',
                                      width=20)
            self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
            self.date_entry.pack(side="left", ipady=6)
        
        # Notes - Compact
        notes_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        notes_frame.pack(fill="x", pady=(0, 12))
        
        tk.Label(notes_frame,
                text="Notes:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9),
                width=12,
                anchor='nw').pack(side="left")
        
        self.notes_text = tk.Text(notes_frame,
                                 font=('Segoe UI', 9),
                                 relief="solid",
                                 borderwidth=1,
                                 bg='white',
                                 height=2)
        self.notes_text.pack(side="left", fill="both", expand=True)
        
        # Buttons - Minimal spacing
        buttons_frame = tk.Frame(fields_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill="x", pady=(15, 0))
        
        save_btn = tk.Button(buttons_frame,
                            text="Save",
                            bg=self.colors['success'],
                            fg=self.colors['white'],
                            font=('Segoe UI', 9, 'bold'),
                            relief="flat",
                            cursor="hand2",
                            command=self._save_expense,
                            padx=20,
                            pady=6)
        save_btn.pack(side="left", padx=(0, 8))
        
        clear_btn = tk.Button(buttons_frame,
                             text="Clear",
                             bg=self.colors['light'],
                             fg=self.colors['dark'],
                             font=('Segoe UI', 9),
                             relief="flat",
                             cursor="hand2",
                             command=self._clear_form,
                             padx=20,
                             pady=6)
        clear_btn.pack(side="left")
        
    def _create_expense_list(self, parent):
        """Create expense list view with minimalistic design"""
        # List container with minimal styling
        list_card = tk.Frame(parent, bg=self.colors['bg'])
        list_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Simple title
        title = tk.Label(list_card,
                        text="Recent Transactions",
                        bg=self.colors['bg'],
                        fg=self.colors['dark'],
                        font=('Segoe UI', 13, 'bold'))
        title.pack(pady=(0, 10), anchor='w')
        
        # Date filter buttons frame
        date_filter_frame = tk.Frame(list_card, bg=self.colors['bg'])
        date_filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(date_filter_frame,
                text="Date Filter:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9, 'bold')).pack(side="left", padx=(0, 10))
        
        self.date_filter_var = tk.StringVar(value="current_month")
        
        # Today button
        today_btn = tk.Radiobutton(date_filter_frame,
                                   text="Today",
                                   variable=self.date_filter_var,
                                   value="today",
                                   bg=self.colors['bg'],
                                   fg=self.colors['dark'],
                                   font=('Segoe UI', 9),
                                   selectcolor=self.colors['bg'],
                                   command=self._apply_date_filter)
        today_btn.pack(side="left", padx=(0, 10))
        
        # Yesterday button
        yesterday_btn = tk.Radiobutton(date_filter_frame,
                                       text="Yesterday",
                                       variable=self.date_filter_var,
                                       value="yesterday",
                                       bg=self.colors['bg'],
                                       fg=self.colors['dark'],
                                       font=('Segoe UI', 9),
                                       selectcolor=self.colors['bg'],
                                       command=self._apply_date_filter)
        yesterday_btn.pack(side="left", padx=(0, 10))
        
        # Current Month button
        month_btn = tk.Radiobutton(date_filter_frame,
                                   text="Current Month",
                                   variable=self.date_filter_var,
                                   value="current_month",
                                   bg=self.colors['bg'],
                                   fg=self.colors['dark'],
                                   font=('Segoe UI', 9),
                                   selectcolor=self.colors['bg'],
                                   command=self._apply_date_filter)
        month_btn.pack(side="left", padx=(0, 10))
        
        # Custom range button
        custom_btn = tk.Radiobutton(date_filter_frame,
                                    text="Custom Range",
                                    variable=self.date_filter_var,
                                    value="custom",
                                    bg=self.colors['bg'],
                                    fg=self.colors['dark'],
                                    font=('Segoe UI', 9),
                                    selectcolor=self.colors['bg'],
                                    command=self._show_date_range_dialog)
        custom_btn.pack(side="left")
        
        # Search/Filter frame - Compact
        filter_frame = tk.Frame(list_card, bg=self.colors['bg'])
        filter_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(filter_frame,
                text="Search:",
                bg=self.colors['bg'],
                fg=self.colors['dark'],
                font=('Segoe UI', 9)).pack(side="left", padx=(0, 8))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._filter_expenses)
        search_entry = tk.Entry(filter_frame,
                               textvariable=self.search_var,
                               font=('Segoe UI', 9),
                               relief="solid",
                               borderwidth=1,
                               bg='white')
        search_entry.pack(side="left", fill="x", expand=True, ipady=4)
        
        # Treeview for expenses
        tree_frame = tk.Frame(list_card, bg=self.colors['bg'])
        tree_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview - removed Category column
        columns = ('Date', 'Description', 'Amount', 'Type')
        self.expense_tree = ttk.Treeview(tree_frame,
                                        columns=columns,
                                        show='headings',
                                        yscrollcommand=scrollbar.set,
                                        height=15)
        
        scrollbar.config(command=self.expense_tree.yview)
        
        # Configure columns
        self.expense_tree.heading('Date', text='Date')
        self.expense_tree.heading('Description', text='Description')
        self.expense_tree.heading('Amount', text='Amount')
        self.expense_tree.heading('Type', text='Type')
        
        self.expense_tree.column('Date', width=120)
        self.expense_tree.column('Description', width=250)
        self.expense_tree.column('Amount', width=120)
        self.expense_tree.column('Type', width=100)
        
        # Configure tags for color-coding transaction types
        self.expense_tree.tag_configure('income', foreground=self.colors['success'])
        self.expense_tree.tag_configure('expense', foreground=self.colors['danger'])
        
        self.expense_tree.pack(fill="both", expand=True)
        
        # Buttons for expense management - with 10px top margin
        action_frame = tk.Frame(list_card, bg=self.colors['bg'])
        action_frame.pack(fill="x", pady=(10, 0))
        
        delete_btn = tk.Button(action_frame,
                              text="🗑️ Delete Selected",
                              bg=self.colors['danger'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 9, 'bold'),
                              relief="flat",
                              cursor="hand2",
                              command=self._delete_expense,
                              padx=15,
                              pady=6)
        delete_btn.pack(side="left", padx=(0, 8))
        
        refresh_btn = tk.Button(action_frame,
                               text="🔄 Refresh",
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               font=('Segoe UI', 9, 'bold'),
                               relief="flat",
                               cursor="hand2",
                               command=self._load_expenses,
                               padx=15,
                               pady=6)
        refresh_btn.pack(side="left")
        
        # Load expenses
        self._load_expenses()
        
    def _save_expense(self):
        """Save expense to database"""
        try:
            # Validate inputs
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get().strip()
            transaction_type = self.type_var.get()
            notes = self.notes_text.get("1.0", "end-1c").strip()
            
            # Get date
            try:
                if hasattr(self.date_entry, 'get_date'):
                    date = self.date_entry.get_date().strftime('%Y-%m-%d')
                else:
                    date = self.date_entry.get()
            except:
                date = datetime.now().strftime('%Y-%m-%d')
            
            # Description is now optional - only amount and date are required
            if amount <= 0:
                messagebox.showwarning("Validation Error", "Amount must be greater than 0")
                return
            
            # Save to database - no category
            self.db_manager.add_transaction(
                date=date,
                description=description if description else "No description",
                category='General',  # Default category
                amount=amount,
                transaction_type=transaction_type,
                notes=notes
            )
            
            messagebox.showinfo("Success", "Transaction saved successfully!")
            self._clear_form()
            self._load_expenses()
            
            # Refresh other tabs
            if self.dashboard_tab:
                self.dashboard_tab.refresh_data()
            if self.analytics_tab:
                self.analytics_tab._refresh_analytics()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")
            
    def _clear_form(self):
        """Clear form fields"""
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)
        if hasattr(self.date_entry, 'set_date'):
            self.date_entry.set_date(datetime.now())
        else:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.type_var.set("expense")
        
    def _load_expenses(self):
        """Load expenses into treeview with current date filter"""
        self._apply_date_filter()
            
    def _filter_expenses(self, *args):
        """Filter expenses based on search and current date filter"""
        self._apply_date_filter()
                
    def _delete_expense(self):
        """Delete selected expense"""
        selected = self.expense_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an expense to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            for item in selected:
                # The iid is the transaction ID
                transaction_id = item
                self.db_manager.delete_transaction(transaction_id)
            
            self._load_expenses()
            
            # Refresh other tabs
            if self.dashboard_tab:
                self.dashboard_tab.refresh_data()
            if self.analytics_tab:
                self.analytics_tab._refresh_analytics()
            messagebox.showinfo("Success", "Transaction deleted successfully!")
    
    def _apply_date_filter(self):
        """Apply the selected date filter"""
        filter_type = self.date_filter_var.get()
        from datetime import datetime, timedelta
        
        # Get current date
        today = datetime.now().date()
        
        # Determine date range based on filter
        if filter_type == "today":
            start_date = today
            end_date = today
        elif filter_type == "yesterday":
            start_date = today - timedelta(days=1)
            end_date = today - timedelta(days=1)
        elif filter_type == "current_month":
            # Get first and last day of current month
            start_date = today.replace(day=1)
            # Get last day of month
            if today.month == 12:
                end_date = today.replace(day=31)
            else:
                next_month = today.replace(month=today.month + 1, day=1)
                end_date = next_month - timedelta(days=1)
        else:
            return  # Custom range handled separately
        
        self._load_filtered_expenses(start_date, end_date)
    
    def _show_date_range_dialog(self):
        """Show dialog for custom date range selection"""
        from tkinter import Toplevel
        from datetime import datetime
        
        dialog = Toplevel(self.frame)
        dialog.title("Select Date Range")
        dialog.geometry("350x200")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f'350x200+{x}+{y}')
        
        # From date
        tk.Label(dialog, text="From Date:", font=('Segoe UI', 10)).pack(pady=(20, 5))
        try:
            from_date = DateEntry(dialog, width=20, font=('Segoe UI', 10), date_pattern='yyyy-mm-dd')
            from_date.pack(pady=5)
        except:
            from_date = tk.Entry(dialog, font=('Segoe UI', 10))
            from_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
            from_date.pack(pady=5)
        
        # To date
        tk.Label(dialog, text="To Date:", font=('Segoe UI', 10)).pack(pady=(10, 5))
        try:
            to_date = DateEntry(dialog, width=20, font=('Segoe UI', 10), date_pattern='yyyy-mm-dd')
            to_date.pack(pady=5)
        except:
            to_date = tk.Entry(dialog, font=('Segoe UI', 10))
            to_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
            to_date.pack(pady=5)
        
        def apply_range():
            try:
                if hasattr(from_date, 'get_date'):
                    start = from_date.get_date()
                    end = to_date.get_date()
                else:
                    start = datetime.strptime(from_date.get(), '%Y-%m-%d').date()
                    end = datetime.strptime(to_date.get(), '%Y-%m-%d').date()
                
                self._load_filtered_expenses(start, end)
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid date format: {str(e)}")
        
        tk.Button(dialog, text="Apply", bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10, 'bold'), relief="flat", command=apply_range,
                 padx=20, pady=8).pack(pady=15)
    
    def _load_filtered_expenses(self, start_date, end_date):
        """Load expenses filtered by date range"""
        from datetime import datetime
        
        # Clear existing items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Load from database
        expenses = self.db_manager.get_all_transactions()
        
        # Apply search filter if any
        search_term = self.search_var.get().lower()
        
        for expense in expenses:
            # Parse expense date
            try:
                expense_date = datetime.strptime(expense['date'], '%Y-%m-%d').date()
            except:
                continue
            
            # Check if within date range
            if start_date <= expense_date <= end_date:
                # Check search filter
                if search_term and search_term not in expense['description'].lower():
                    continue
                
                trans_type = expense['type']
                self.expense_tree.insert('', 'end',
                                       iid=expense['id'],
                                       values=(
                                           expense['date'],
                                           expense['description'],
                                           f"${expense['amount']:.2f}",
                                           trans_type.capitalize()
                                       ),
                                       tags=(trans_type,))
