"""
Database Manager
Manages data storage using Excel spreadsheets
"""
import os
import pandas as pd
from datetime import datetime
import uuid

class DatabaseManager:
    """Manages data persistence using Excel files"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.transactions_file = os.path.join(self.data_dir, 'transactions.xlsx')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize transactions file if it doesn't exist
        self._initialize_database()
        
    def _initialize_database(self):
        """Initialize database file if it doesn't exist"""
        if not os.path.exists(self.transactions_file):
            # Create empty DataFrame with schema
            df = pd.DataFrame(columns=[
                'id',
                'date',
                'description',
                'category',
                'amount',
                'type',
                'notes',
                'created_at'
            ])
            df.to_excel(self.transactions_file, index=False, engine='openpyxl')
            
    def _load_transactions(self):
        """Load transactions from Excel file"""
        try:
            df = pd.read_excel(self.transactions_file, engine='openpyxl')
            return df
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return pd.DataFrame(columns=[
                'id', 'date', 'description', 'category', 
                'amount', 'type', 'notes', 'created_at'
            ])
            
    def _save_transactions(self, df):
        """Save transactions to Excel file"""
        try:
            df.to_excel(self.transactions_file, index=False, engine='openpyxl')
        except Exception as e:
            print(f"Error saving transactions: {e}")
            raise
            
    def add_transaction(self, date, description, category, amount, 
                       transaction_type='expense', notes=''):
        """Add a new transaction"""
        df = self._load_transactions()
        
        # Create new transaction
        new_transaction = {
            'id': str(uuid.uuid4()),
            'date': date,
            'description': description,
            'category': category,
            'amount': float(amount),
            'type': transaction_type,
            'notes': notes,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Append to DataFrame using pd.concat
        new_df = pd.DataFrame([new_transaction])
        df = pd.concat([df, new_df], ignore_index=True)
        
        # Save
        self._save_transactions(df)
        return new_transaction['id']
        
    def get_all_transactions(self):
        """Get all transactions"""
        df = self._load_transactions()
        
        if df.empty:
            return []
        
        # Sort by date descending
        df = df.sort_values('date', ascending=False)
        
        # Convert to list of dictionaries
        transactions = df.to_dict('records')
        return transactions
        
    def get_recent_transactions(self, limit=10):
        """Get recent transactions"""
        df = self._load_transactions()
        
        if df.empty:
            return []
        
        # Sort by date descending and limit
        df = df.sort_values('date', ascending=False).head(limit)
        
        return df.to_dict('records')
        
    def delete_transaction(self, transaction_id):
        """Delete a transaction"""
        df = self._load_transactions()
        
        # Remove transaction
        df = df[df['id'] != transaction_id]
        
        # Save
        self._save_transactions(df)
        
    def get_current_month_total(self):
        """Get total expenses for current month"""
        df = self._load_transactions()
        
        if df.empty:
            return 0.0
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filter current month expenses
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        month_df = df[(df['date'].dt.month == current_month) & 
                     (df['date'].dt.year == current_year) &
                     (df['type'] == 'expense')]
        
        if month_df.empty:
            return 0.0
        
        return float(month_df['amount'].sum())
        
    def get_current_month_income(self):
        """Get total income for current month"""
        df = self._load_transactions()
        
        if df.empty:
            return 0.0
        
        df['date'] = pd.to_datetime(df['date'])
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        month_df = df[(df['date'].dt.month == current_month) & 
                     (df['date'].dt.year == current_year) &
                     (df['type'] == 'income')]
        
        if month_df.empty:
            return 0.0
        
        return float(month_df['amount'].sum())
        
    def get_month_total(self, year, month):
        """Get total expenses for a specific month"""
        df = self._load_transactions()
        
        if df.empty:
            return 0.0
        
        df['date'] = pd.to_datetime(df['date'])
        
        month_df = df[(df['date'].dt.month == month) & 
                     (df['date'].dt.year == year) &
                     (df['type'] == 'expense')]
        
        if month_df.empty:
            return 0.0
        
        return float(month_df['amount'].sum())
        
    def get_filtered_transactions(self, period):
        """Get transactions filtered by period"""
        df = self._load_transactions()
        
        if df.empty:
            return []
        
        df['date'] = pd.to_datetime(df['date'])
        today = datetime.now()
        
        if period == "This Week":
            start_date = today - pd.Timedelta(days=7)
        elif period == "This Month":
            start_date = today.replace(day=1)
        elif period == "Last Month":
            last_month = today.replace(day=1) - pd.Timedelta(days=1)
            start_date = last_month.replace(day=1)
            end_date = today.replace(day=1) - pd.Timedelta(days=1)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            return df.to_dict('records')
        elif period == "Last 3 Months":
            start_date = today - pd.Timedelta(days=90)
        elif period == "This Year":
            start_date = today.replace(month=1, day=1)
        elif period == "All Time":
            return df.to_dict('records')
        else:
            start_date = today.replace(day=1)
        
        df = df[df['date'] >= start_date]
        return df.to_dict('records')
        
    def export_to_excel(self, filename):
        """Export data to Excel file"""
        df = self._load_transactions()
        df.to_excel(filename, index=False, engine='openpyxl')
        
    def import_from_excel(self, filename):
        """Import data from Excel file"""
        try:
            import_df = pd.read_excel(filename, engine='openpyxl')
            
            # Validate columns
            required_columns = ['date', 'description', 'category', 'amount', 'type']
            if not all(col in import_df.columns for col in required_columns):
                raise ValueError("Invalid file format. Missing required columns.")
            
            # Load existing transactions
            existing_df = self._load_transactions()
            
            # Add IDs and timestamps to imported data
            for idx in import_df.index:
                if 'id' not in import_df.columns or pd.isna(import_df.at[idx, 'id']):
                    import_df.at[idx, 'id'] = str(uuid.uuid4())
                if 'created_at' not in import_df.columns or pd.isna(import_df.at[idx, 'created_at']):
                    import_df.at[idx, 'created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if 'notes' not in import_df.columns:
                    import_df.at[idx, 'notes'] = ''
            
            # Combine and save
            combined_df = pd.concat([existing_df, import_df], ignore_index=True)
            self._save_transactions(combined_df)
            
        except Exception as e:
            print(f"Error importing data: {e}")
            raise
            
    def get_data_path(self):
        """Get the path to the data file"""
        return self.transactions_file
