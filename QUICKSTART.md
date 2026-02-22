# Quick Start Guide

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd c:\Users\ASUS\OneDrive\Desktop\collegescraper
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install beautifulsoup4 requests openpyxl pandas lxml
   ```

## Running the Application

```bash
python main.py
```

## How to Use

1. **Select State**: Choose an Indian state from the dropdown
2. **Select Branch**: Choose an engineering branch (or "All Branches")
3. **Select Type**: Government, Private, or All Types
4. **Set Max Results**: Number of colleges to search (5-50)
5. **Click "Start Search"**: Wait for scraping to complete
6. **Click "Export to Excel"**: Save results to Excel file

## Example Search

- **State**: Karnataka
- **Branch**: Computer Science Engineering
- **Type**: Government
- **Max Results**: 20

This will search for up to 20 government engineering colleges in Karnataka offering Computer Science Engineering.

## Output

The Excel file will contain:
- **Summary Sheet**: Search parameters and statistics
- **Colleges Sheet**: Detailed information for each college found

### Data Columns
- College Name
- University
- Type (Government/Private)
- Location
- Branches Offered
- Email
- HOD Contact
- Admin Contact
- Other Contacts
- Website

## Tips

- Start with smaller "Max Results" (10-15) for faster searches
- "All Branches" will search for all engineering colleges regardless of specialization
- Check the `logs/` folder if you encounter any errors
- Results are saved in the `output/` folder by default

## Troubleshooting

**No results found?**
- Try a different state or branch
- Increase "Max Results"
- Check your internet connection

**Application won't start?**
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip list`
- Check logs in `logs/` folder

**Export fails?**
- Ensure you have write permissions
- Close any open Excel files with the same name
- Choose a different save location

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Internet**: Required for web scraping
