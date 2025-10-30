"""
Financial Predictor - ML-based expense/income prediction
"""
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression


class FinancialPredictor:
    """Predicts financial outcomes based on historical data"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def predict_month_survival(self):
        """
        Predict if user can survive the current month based on patterns
        Returns dict with prediction, confidence, and details
        """
        # Get data for current and previous months
        current_month_data = self._get_month_data(0)
        previous_month_data = self._get_month_data(1)
        
        if not current_month_data['transactions']:
            return {
                'can_survive': None,
                'confidence': 0,
                'message': 'Not enough data to make prediction',
                'details': {}
            }
        
        # Calculate patterns
        current_income = current_month_data['total_income']
        current_expenses = current_month_data['total_expenses']
        current_balance = current_income - current_expenses
        
        # Get daily averages
        days_passed = current_month_data['days_passed']
        if days_passed == 0:
            days_passed = 1
        
        daily_expense_avg = current_expenses / days_passed
        daily_income_avg = current_income / days_passed
        
        # Project for rest of month
        days_remaining = current_month_data['days_in_month'] - days_passed
        projected_expenses = current_expenses + (daily_expense_avg * days_remaining)
        projected_income = current_income + (daily_income_avg * days_remaining)
        projected_balance = projected_income - projected_expenses
        
        # Determine survival
        can_survive = projected_balance >= 0
        
        # Calculate confidence based on data quality
        confidence = min(100, (days_passed / 7) * 100)  # More days = more confidence
        
        # Add previous month comparison if available
        trend_message = ""
        if previous_month_data['transactions']:
            prev_balance = previous_month_data['total_income'] - previous_month_data['total_expenses']
            if current_balance > prev_balance:
                trend_message = "Your financial situation is improving compared to last month."
            elif current_balance < prev_balance:
                trend_message = "Your expenses have increased compared to last month."
            else:
                trend_message = "Your financial pattern is stable."
        
        # Generate message
        if can_survive:
            message = f"✅ Prediction: You can survive this month with an estimated balance of ${projected_balance:.2f}"
        else:
            message = f"⚠️ Warning: You may face a deficit of ${abs(projected_balance):.2f} by month end"
        
        return {
            'can_survive': can_survive,
            'confidence': round(confidence, 1),
            'message': message,
            'trend': trend_message,
            'details': {
                'current_balance': current_balance,
                'projected_balance': projected_balance,
                'daily_expense_avg': daily_expense_avg,
                'daily_income_avg': daily_income_avg,
                'days_passed': days_passed,
                'days_remaining': days_remaining,
                'projected_total_expenses': projected_expenses,
                'projected_total_income': projected_income
            }
        }
    
    def get_spending_trend(self, months=3):
        """
        Get spending trend for the past N months
        Returns list of (month_name, total_expenses, total_income) tuples
        """
        trend_data = []
        
        for i in range(months):
            month_data = self._get_month_data(i)
            if month_data['transactions']:
                trend_data.append({
                    'month': month_data['month_name'],
                    'expenses': month_data['total_expenses'],
                    'income': month_data['total_income'],
                    'balance': month_data['total_income'] - month_data['total_expenses']
                })
        
        return list(reversed(trend_data))  # Oldest first
    
    def _get_month_data(self, months_ago=0):
        """
        Get aggregated data for a specific month
        months_ago: 0 = current month, 1 = last month, etc.
        """
        # Calculate target month
        today = datetime.now()
        target_date = today - timedelta(days=30 * months_ago)
        target_month = target_date.month
        target_year = target_date.year
        
        # Get days in month
        if target_month == 12:
            next_month = datetime(target_year + 1, 1, 1)
        else:
            next_month = datetime(target_year, target_month + 1, 1)
        days_in_month = (next_month - datetime(target_year, target_month, 1)).days
        
        # Calculate days passed in month
        if months_ago == 0:
            days_passed = today.day
        else:
            days_passed = days_in_month
        
        # Get all transactions
        all_transactions = self.db_manager.get_all_transactions()
        
        # Filter for target month
        month_transactions = []
        total_income = 0
        total_expenses = 0
        
        for trans in all_transactions:
            try:
                trans_date = datetime.strptime(trans['date'], '%Y-%m-%d')
                if trans_date.month == target_month and trans_date.year == target_year:
                    month_transactions.append(trans)
                    if trans['type'] == 'income':
                        total_income += trans['amount']
                    else:
                        total_expenses += trans['amount']
            except:
                continue
        
        return {
            'month_name': target_date.strftime('%B %Y'),
            'transactions': month_transactions,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'days_in_month': days_in_month,
            'days_passed': days_passed
        }
