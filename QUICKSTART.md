# Quick Start Guide - Budget Manager Pro

## Installation Steps

### 1. Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data handling)
- openpyxl (Excel file support)
- tkcalendar (date picker widget)
- pillow (image handling)

### 2. Run the Application

Simply execute:

```bash
python main.py
```

## First Time Setup

When you first run the application:

1. The app will create necessary folders:
   - `data/` - stores your transaction Excel files
   - `config/` - stores application settings

2. Default categories are pre-configured:
   - Food, Transport, Entertainment, Shopping
   - Bills, Healthcare, Education, Salary, Other

3. You can customize these in Settings tab

## Quick Feature Overview

### 📊 Dashboard Tab
- View summary cards (Total Expenses, Income, Balance, Budget)
- See recent transactions
- Quick action buttons

### 💳 Expenses Tab
- **Left Panel**: Add new expenses/income
- **Right Panel**: View and manage all transactions
- Search functionality
- Delete unwanted entries

### 📈 Analytics Tab
- Summary statistics
- Spending by category (bar charts)
- Monthly trends (last 6 months)
- AI-powered spending insights

### ⚙️ Settings Tab
- Set monthly budget limit
- Enable/disable budget alerts
- Add or remove categories
- Export/Import data to Excel
- View data storage location

## Building Executable

### Method 1: Using spec file
```bash
pyinstaller BudgetManagerPro.spec
```

### Method 2: Direct command
```bash
pyinstaller --onefile --windowed --name "BudgetManagerPro" main.py
```

The executable will be in the `dist/` folder.

## Tips for Best Experience

1. **Set a budget first**: Go to Settings → Budget Settings
2. **Customize categories**: Add categories that match your lifestyle
3. **Regular updates**: Add expenses daily for accurate tracking
4. **Check analytics**: Review your spending weekly/monthly
5. **Backup data**: Export your data regularly

## Troubleshooting

**Can't import tkcalendar?**
```bash
pip install tkcalendar
```

**Excel files not opening?**
```bash
pip install openpyxl pandas
```

**Application window too small/large?**
- Window size is 720x1000px by default
- You can manually resize it

**Need to reset everything?**
- Delete the `data/` folder to clear all transactions
- Delete the `config/` folder to reset settings

## Data Backup

Your data is stored in:
- `data/transactions.xlsx` - All your transactions
- `config/settings.json` - Your preferences

**To backup**: Copy these files to a safe location

**To restore**: Replace the files with your backup

## Support

For issues or questions:
- Check the main README.md
- Review the code documentation
- Open an issue on GitHub

Happy budgeting! 💰
