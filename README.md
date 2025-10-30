# Budget Manager Pro 💰

A modern, feature-rich budget management application built with Python and Tkinter. Track your expenses, manage your finances, and gain insights into your spending habits with an intuitive, beautiful interface powered by **Machine Learning**.

## Features ✨

### Core Features
- **📊 Dashboard**: Get an overview of your finances with summary cards and recent transactions
- **💳 Expense Tracking**: Easily add and manage daily expenses and income with date filters
- **📈 Analytics**: Visualize your spending patterns with charts and statistics
- **⚙️ Settings**: Customize your budget limits and manage your data

### 🤖 NEW: Machine Learning Features
- **Financial Survival Prediction**: ML-powered analysis to predict if you'll finish the month with a positive balance
- **Confidence Scoring**: Get reliability scores (0-100%) for predictions based on data availability
- **Trend Analysis**: Compare current spending patterns vs previous months
- **Smart Projections**: Daily average calculations to project month-end balance
- **Visual Charts**: Interactive matplotlib charts showing 6-month expense/income trends

### Additional Features
- **💾 Data Management**: 
  - Multiple spreadsheet support (Excel files)
  - Import/Export functionality
  - Automatic data persistence
- **🎨 Modern UI**: 
  - Clean, minimalistic, and user-friendly interface
  - Color-coded transactions (green for income, red for expenses)
  - Enhanced dashboard with accent bars and hover effects
  - Optimized for 1080p displays (1200x900 window, maximized on startup)
- **📅 Date Filters**: Filter transactions by Today, Yesterday, Current Month, or Custom Range
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

The requirements include:
- `pandas` - Data handling
- `openpyxl` - Excel file support
- `numpy` - Numerical operations
- `tkcalendar` - Date picker widgets
- `pillow` - Image handling
- **`matplotlib`** - Data visualization charts (NEW)
- **`scikit-learn`** - Machine learning algorithms (NEW)

3. Run the application:
```bash
python src/app.py
```

## 🤖 Machine Learning Features

### Financial Prediction
The app uses ML algorithms to analyze your spending patterns and predict:
- Whether you can survive the current month financially
- Your projected month-end balance
- Daily spending averages
- Trend comparisons with previous months

**See [ML_FEATURES.md](ML_FEATURES.md) for detailed documentation.**

### How It Works
1. Analyzes current and previous month transactions
2. Calculates daily expense and income averages
3. Projects remaining month spending based on patterns
4. Generates confidence scores based on data availability
5. Provides color-coded predictions (green = positive, red = warning)

### Visual Analytics
- **6-month trend charts** showing expense vs income
- Interactive matplotlib visualizations
- Color-coded for easy understanding
- Professional chart styling with legends and labels

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
├── src/
│   ├── app.py             # Main application class
│   └── gui/               # GUI components
│       ├── main_window.py # Main window
│       ├── dashboard.py   # Dashboard tab with enhanced cards
│       ├── expenses.py    # Expenses tab with date filters
│       ├── analytics.py   # Analytics tab with ML predictions
│       └── settings.py    # Settings tab
├── utils/
│   ├── config_manager.py     # Configuration management
│   ├── database_manager.py   # Database operations
│   └── predictor.py          # ML prediction engine (NEW)
├── data/                  # Data storage (Excel files)
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── ML_FEATURES.md        # ML features documentation (NEW)
```

## Usage Guide

### Adding Expenses

1. Navigate to the **Expenses** tab
2. Select transaction type (Expense/Income)
3. Enter the amount and description
4. Select the date using the date picker
5. Add optional notes
6. Click **Save**
7. Transaction will appear color-coded in the table (green for income, red for expense)

### Using Date Filters

In the **Expenses** tab, you can filter transactions by:
- **Today**: Shows only today's transactions
- **Yesterday**: Shows yesterday's transactions
- **Current Month**: Shows all transactions from the current month (default)
- **Custom Range**: Select specific start and end dates

### Setting Budget

1. Go to **Settings** tab
2. Enter your monthly budget limit
3. Enable budget alerts if desired
4. Click **Save**

### Viewing ML Predictions

1. Go to **Analytics** tab
2. View the **Financial Prediction** section at the top
3. Check your survival prediction (green = good, red = warning)
4. Review confidence score and projected balance
5. Analyze the **6-month trend chart** below
6. Read spending insights for tips

### Understanding Predictions

- **Green Card**: You're projected to finish the month with positive balance
- **Red Card**: Warning - you may finish with negative balance
- **Confidence Score**: Higher % = more reliable prediction
  - 100% = 15+ days of data
  - Lower % = fewer days of data
- **Projected Balance**: Your estimated balance at month-end

### Viewing Analytics

1. Go to **Analytics** tab
2. Review the **ML-powered financial prediction** at the top
3. View the **6-month trend chart** with expense/income lines
4. Check **summary statistics** cards
5. Review **spending overview** bars
6. Read **monthly trends** for the last 6 months
7. Get personalized **spending insights**
8. Select different time periods to analyze
9. Click **Refresh** to update all data

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
| id | String (UUID) | Unique transaction ID |
| date | Date | Transaction date |
| description | String | Transaction description |
| amount | Float | Transaction amount |
| type | String | 'expense' or 'income' |
| notes | String | Additional notes |
| created_at | DateTime | Creation timestamp |

## Screenshots

### Dashboard
- Enhanced card design with colored accent bars
- Color-coded transaction types
- Quick action buttons
- Real-time balance updates

### Analytics with ML Predictions
- Financial survival prediction with confidence scores
- 6-month trend visualization
- Projected month-end balance
- Trend comparisons

### Expenses Page
- Clean, minimalistic form design
- Date filters (Today, Yesterday, Current Month, Custom Range)
- Color-coded transaction table
- Easy delete and refresh functionality

## Technical Details

### Window Specifications
- **Resolution**: 1200x900 pixels
- **Display**: Optimized for 1080p (1920x1080) displays
- **Startup**: Maximized window on launch
- **Design**: Modern, minimalistic with card-based layout

### Color Scheme
- **Success/Income**: Green (#27AE60)
- **Danger/Expense**: Red (#E74C3C)
- **Primary**: Dark (#2C3E50)
- **Secondary**: Blue (#3498DB)
- **Warning**: Orange (#F39C12)

### ML Algorithm Details
- Daily average expense/income calculation
- Linear projection based on current trends
- Confidence scoring based on data availability
- Month-to-month trend comparison
- See [ML_FEATURES.md](ML_FEATURES.md) for technical details

## Troubleshooting

### ML Predictions Not Showing
- Ensure you have transactions in the current month
- At least 1 day of data is required for predictions
- More days = higher confidence scores

### Charts Not Displaying
- Verify matplotlib is installed: `pip install matplotlib>=3.8.0`
- Check that you have transaction history for visualization
- Restart the application if needed

### Application Not Maximizing
- Works on Windows with `root.state('zoomed')`
- For other OS, window will open at 1200x900

---

Made with ❤️ using Python, Tkinter, and Machine Learning