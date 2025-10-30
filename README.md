# Budget Manager Pro 💰

A modern, feature-rich budget management application built with Python and Tkinter. Track your expenses, manage your finances, and gain insights into your spending habits with an intuitive and beautiful interface.

## Features ✨

- **📊 Dashboard**: Get an overview of your finances with summary cards and recent transactions
- **💳 Expense Tracking**: Easily add and manage daily expenses and income
- **📈 Analytics**: Visualize your spending patterns with charts and statistics
- **⚙️ Settings**: Customize categories, set budget limits, and manage your data
- **💾 Data Management**: 
  - Multiple spreadsheet support (Excel files)
  - Import/Export functionality
  - Automatic data persistence
- **🎨 Modern UI**: Clean, minimalistic, and user-friendly interface
- **🔔 Budget Alerts**: Get notified when you exceed your budget

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/budget-management-spreadsheet.git
cd budget-management-spreadsheet
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Building Executable with PyInstaller

To create a standalone executable:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed --name "BudgetManagerPro" main.py
```

3. Find your executable in the `dist` folder

## Project Structure

```
budget-management-spreadsheet/
├── main.py                 # Application entry point
├── src/
│   ├── app.py             # Main application class
│   └── gui/               # GUI components
│       ├── main_window.py # Main window
│       ├── dashboard.py   # Dashboard tab
│       ├── expenses.py    # Expenses tab
│       ├── analytics.py   # Analytics tab
│       └── settings.py    # Settings tab
├── utils/
│   ├── config_manager.py  # Configuration management
│   └── database_manager.py # Database operations
├── assets/                # Images and icons
├── data/                  # Data storage (Excel files)
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage Guide

### Adding Expenses

1. Navigate to the **Expenses** tab
2. Select transaction type (Expense/Income)
3. Enter the amount, description, and category
4. Select the date
5. Add optional notes
6. Click **Save**

### Setting Budget

1. Go to **Settings** tab
2. Enter your monthly budget limit
3. Enable budget alerts if desired
4. Click **Save**

### Managing Categories

1. Navigate to **Settings** tab
2. Scroll to the Categories section
3. Use **Add Category** to create new categories
4. Select and use **Remove Selected** to delete categories

### Viewing Analytics

1. Go to **Analytics** tab
2. Select the time period you want to analyze
3. View spending by category, monthly trends, and insights
4. Click **Refresh** to update the data

### Importing/Exporting Data

**Export:**
1. Go to **Settings** → Data Management
2. Click **Export to Excel**
3. Choose save location

**Import:**
1. Go to **Settings** → Data Management
2. Click **Import from Excel**
3. Select the file to import

## Data Format

The application uses Excel (.xlsx) files to store data. The transaction file has the following structure:

| Column | Type | Description |
|--------|------|-------------|
| id | String | Unique transaction ID |
| date | Date | Transaction date |
| description | String | Transaction description |
| category | String | Category name |
| amount | Float | Transaction amount |
| type | String | 'expense' or 'income' |
| notes | String | Additional notes |
| created_at | DateTime | Creation timestamp |

---

Made with ❤️ using Python