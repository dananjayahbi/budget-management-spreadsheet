"""
Configuration Manager
Manages application settings and preferences
"""
import json
import os

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        self.config_file = os.path.join(self.config_dir, 'settings.json')
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from file"""
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Default configuration
        default_config = {
            'monthly_budget': 0,
            'budget_alert': True,
            'categories': [
                'Food',
                'Transport',
                'Entertainment',
                'Shopping',
                'Bills',
                'Healthcare',
                'Education',
                'Salary',
                'Other'
            ],
            'currency': 'USD',
            'currency_symbol': '$',
            'date_format': '%Y-%m-%d',
            'theme': 'light'
        }
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return default_config
        
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get_monthly_budget(self):
        """Get monthly budget limit"""
        return self.config.get('monthly_budget', 0)
        
    def set_monthly_budget(self, budget):
        """Set monthly budget limit"""
        self.config['monthly_budget'] = budget
        self._save_config()
        
    def get_budget_alert(self):
        """Get budget alert setting"""
        return self.config.get('budget_alert', True)
        
    def set_budget_alert(self, enabled):
        """Set budget alert setting"""
        self.config['budget_alert'] = enabled
        self._save_config()
        
    def get_categories(self):
        """Get expense categories"""
        return self.config.get('categories', [])
        
    def add_category(self, category):
        """Add a new category"""
        categories = self.config.get('categories', [])
        if category not in categories:
            categories.append(category)
            self.config['categories'] = categories
            self._save_config()
            return True
        return False
        
    def remove_category(self, category):
        """Remove a category"""
        categories = self.config.get('categories', [])
        if category in categories:
            categories.remove(category)
            self.config['categories'] = categories
            self._save_config()
            return True
        return False
        
    def get_currency_symbol(self):
        """Get currency symbol"""
        return self.config.get('currency_symbol', '$')
        
    def get_date_format(self):
        """Get date format"""
        return self.config.get('date_format', '%Y-%m-%d')
