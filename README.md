🎓 Engineering College Information Scraper is a Python 🐍 GUI app that collects data on Indian engineering colleges. 🔍 Search by state, branch & type, 🌐 scrape websites automatically, and 📊 export structured results to Excel. 🖥️ Built with Tkinter, Selenium & Pandas. ⚠️ For educational use only.
Here is your complete **README.md** file content 👇 (You can copy and paste this directly into `README.md`)

---

```markdown
# 🎓 Engineering College Information Scraper

A Python-based GUI desktop application that scrapes and organizes information about Indian engineering colleges and universities, with Excel export functionality.

---

## 🚀 Overview

The **Engineering College Information Scraper** is designed to automate the collection of structured academic data. Users can search for engineering colleges based on state, branch, and college type, and export the results into a formatted Excel file.

This project is ideal for students, researchers, and analysts who need organized college data without manual searching.

---

## ✨ Features

- 🔍 Smart Search (State, Branch, College Type)
- 🌐 Automated Web Scraping
- 📊 Excel Export with formatted sheets
- 🖥️ User-Friendly GUI (Tkinter)
- 📝 Logging system for tracking progress and errors
- ⚙️ Modular and scalable project structure

---

## 📌 Data Extracted

The application attempts to extract:

- College Name  
- University Affiliation  
- College Type (Government / Private / Autonomous)  
- Location / Address  
- Email Address  
- Contact Numbers  
- HOD Contact Information  
- Administration Contact Information  
- Engineering Branches Offered  
- Official Website URL  

---

## 🛠️ Tech Stack

- Python 3.8+
- BeautifulSoup4
- Requests
- Selenium
- Pandas
- OpenPyXL
- lxml
- WebDriver Manager
- Tkinter

---

## 📂 Project Structure

```

collegescraper/
│
├── main.py
├── requirements.txt
├── config/
├── gui/
├── scraper/
├── data/
├── utils/
├── logs/
└── output/

```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```

git clone [https://github.com/anandthosar03-hub/EnggCollegeDataScraper.git](https://github.com/anandthosar03-hub/EnggCollegeDataScraper.git)
cd EnggCollegeDataScraper

```

### 2️⃣ Create Virtual Environment (Recommended)

```

python -m venv .venv
.venv\Scripts\activate   # Windows

```

### 3️⃣ Install Dependencies

```

pip install -r requirements.txt

```

---

## ▶️ Usage

Run the application:

```

python main.py

```

### Steps:
1. Select State
2. Select Engineering Branch
3. Select College Type
4. Set Maximum Results
5. Click **Start Search**
6. Click **Export to Excel**

The Excel file will be saved in the `output/` directory.

---

## ⚠️ Important Notes

- This project is for **educational and research purposes only**.
- Web scraping may be subject to website terms of service.
- Data accuracy depends on website availability and structure.
- Manual verification is recommended for official use.

---

## 🐞 Troubleshooting

**No results found**
- Check internet connection
- Try broader search filters

**Application crashes**
- Check logs inside the `logs/` folder
- Ensure dependencies are installed properly

**Excel export fails**
- Ensure file is not already open
- Check write permissions

---

## 📁 Logs & Output
- mkdir output
- run ./main.py
- Logs → `logs/`
- Excel Files → `output/`




