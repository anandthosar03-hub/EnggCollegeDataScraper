# Engineering College Information Scraper

A GUI-based desktop application to scrape information about Indian engineering colleges and universities, with Excel export functionality.

## Features

- 🔍 **Smart Search**: Search for engineering colleges by state, branch, and type (Government/Private)
- 🌐 **Web Scraping**: Automatically extracts college information from websites
- 📊 **Excel Export**: Export results to formatted Excel spreadsheets
- 🎯 **Data Extraction**: Extracts college name, email, location, branches, contact numbers, HOD contacts, admin contacts
- 🖥️ **User-Friendly GUI**: Easy-to-use graphical interface built with Tkinter
- 📝 **Logging**: Comprehensive logging for debugging and tracking

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**

2. **Install required dependencies**:
   ```bash
   cd collegescraper
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Using the application**:
   - Select a **State** from the dropdown
   - Select an **Engineering Branch** (or "All Branches")
   - Select **College Type** (Government/Private/All Types)
   - Set **Max Results** (number of colleges to search for)
   - Click **"Start Search"** to begin scraping
   - Wait for the search to complete
   - Click **"Export to Excel"** to save the results

3. **Output**:
   - Excel file will be saved to your chosen location
   - Contains college information in a formatted spreadsheet
   - Includes a summary sheet with search parameters

## Data Extracted

The application attempts to extract the following information for each college:

- College Name
- University Affiliation
- College Type (Government/Private/Autonomous)
- Location/Address
- Email Address
- Contact Numbers
- HOD Contact Information
- Administration Contact Information
- Engineering Branches Offered
- Website URL

## Project Structure

```
collegescraper/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── states.py          # Indian states and branches configuration
├── gui/
│   └── main_window.py     # GUI interface
├── scraper/
│   ├── google_search.py   # Google/DuckDuckGo search functionality
│   ├── college_scraper.py # College website scraper
│   └── data_extractor.py  # Data extraction utilities
├── data/
│   ├── college_data.py    # Data models
│   └── excel_exporter.py  # Excel export functionality
├── utils/
│   └── logger.py          # Logging configuration
├── logs/                  # Application logs (created automatically)
└── output/                # Excel output files (created automatically)
```

## Important Notes

### Web Scraping Considerations

- **Legal**: Web scraping may be subject to website terms of service. Use responsibly.
- **Rate Limiting**: The application includes delays between requests to avoid overwhelming servers
- **Accuracy**: Data accuracy depends on website structure and availability
- **Blocking**: Some websites may block automated scraping attempts

### Data Accuracy

- Not all colleges may have complete information available online
- Information may become outdated
- Manual verification of critical data is recommended

## Troubleshooting

### No results found
- Try different search parameters
- Check your internet connection
- Some states/branches may have limited online presence

### Application crashes
- Check the log files in the `logs/` directory
- Ensure all dependencies are installed correctly
- Try reducing the "Max Results" value

### Export fails
- Ensure you have write permissions to the output directory
- Check that the Excel file is not already open

## Logs

Application logs are stored in the `logs/` directory with timestamps. Check these files for detailed information about scraping progress and any errors.

## Dependencies

- **beautifulsoup4**: HTML parsing and web scraping
- **requests**: HTTP requests
- **selenium**: Browser automation (for dynamic content)
- **openpyxl**: Excel file creation
- **pandas**: Data manipulation
- **webdriver-manager**: Automatic WebDriver management
- **lxml**: XML/HTML parser

## Future Enhancements

- Add support for more data fields
- Implement caching to avoid re-scraping
- Add database storage option
- Support for other educational institutions
- API integration for more reliable data

## License

This project is for educational purposes. Please respect website terms of service and use responsibly.

## Support

For issues or questions, check the log files in the `logs/` directory for detailed error information.
