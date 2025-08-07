# ⚽ Football Agent Influence Dashboard

An interactive dashboard project that scrapes and analyzes English Premier League transfer data to visualize football agent influence — built entirely using Python.

![Dashboard Screenshot](## 📊 Dashboard Preview

![Dashboard Screenshot](dashboard.png.jpg)
) <!-- Add your screenshot image here -->

---

## 🔍 Key Features

- ✅ Real-time scraping of Premier League transfer data from [Transfermarkt](https://www.transfermarkt.com).
- ✅ Automated data cleaning and storage in a local SQLite database.
- ✅ Scraping of individual player pages to extract **agent information**.
- ✅ Interactive dashboard with:
  - 📊 **Top 10 Agents by Total Deal Value** bar chart
  - 🌐 **Player-Club-Agent Transfer Network** visualization
  - 💰 Metric Cards: Total Spending, Income, etc.
  - 🔎 Searchable, sortable **transfer data table**

---

## 🛠️ Tech Stack

| Layer            | Technologies                      |
|------------------|-----------------------------------|
| Language         | Python                            |
| Scraping         | `requests`, `BeautifulSoup`       |
| Data Processing  | `pandas`                          |
| Database         | `SQLite`                          |
| Dashboard (UI)   | `Dash`, `Plotly`, `dash-bootstrap-components` |

---

## 🚀 Run It Locally

### 1. Clone the Repo

```bash
git clone https://github.com/Pradeep0410-03/Football-Agent-Dashboard.git
cd Football-Agent-Dashboard
