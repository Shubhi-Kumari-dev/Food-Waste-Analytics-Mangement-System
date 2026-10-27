# 🍲 Food Waste Analytics and Management System
### Data Analytics and Visualization (DAV) Laboratory Project
**Academic Level:** Third-Year B.Tech Computer Science / Data Science / IT  
**Platform:** Local Windows Environment (PowerShell)  
**Core Framework:** Python & Streamlit  

---

## 👥 Project Team & Contributors

| Member Name | Role & Core Responsibilities | GitHub Profile |
| :--- | :--- | :--- |
| **Shubhi Kumari** | Full-Stack Streamlit Dashboard, Executive Hub, UI Theming & PPT Documentation | [@Shubhi-Kumari-dev](https://github.com/Shubhi-Kumari-dev) |
| **[Friend / Teammate Name]** | ETL Pipeline, Database Architecture, Time Series Forecasting & Testing | [@FriendGitHubUsername](https://github.com/) |

---

## 1. Project Overview & Aim

Food waste in institutional facilities such as hostels, college canteens, restaurants, and catering events represents a significant economic loss and environmental burden. The **Food Waste Analytics and Management System** is an interactive, data-driven web dashboard developed to:
- Monitor and quantify preparation, serving, and waste volumes across food categories and campus locations.
- Systematically clean and validate operational food waste datasets.
- Extract, load, and query data using relational database technologies (**SQLite** & **SQLAlchemy**).
- Identify distribution patterns, outliers, and correlations using statistical visualizations (**Matplotlib**, **Seaborn**, **Plotly**).
- Examine temporal trends, compute moving averages, perform seasonal decomposition, and forecast future waste using time series models (**Statsmodels ARIMA**).
- Deliver automated, empirical recommendations to reduce avoidable food waste.

---

## 2. Practical-to-Feature Mapping

This project consolidates all required Data Analytics & Visualization lab practicals into one unified, production-ready system:

| Lab Practical / Syllabus Topic | Implemented Module in Project | Key Functions & Techniques |
| :--- | :--- | :--- |
| **Practical 5: Data Extraction & Loading (Databases)** | `utils/database.py` & Module 6 | SQLite auto-creation via SQLAlchemy engine, `DataFrame.to_sql()`, append vs replace, SQL query console |
| **Lab 7: Temporal Trends & Variable Correlations** | `utils/visualizations.py` & Module 2 | Temporal line charts, multi-variable scatter plots with OLS regression trendline, Seaborn correlation heatmap |
| **Lab 8: Distribution & Categorical Charts** | `utils/visualizations.py` & Module 3 | Histograms with adjustable bins, Box-and-whisker plots with outlier points, Bar charts, Pie & Donut charts |
| **Time Series Analysis Practical** | `utils/time_series.py` & Module 4 | Daily/weekly resampling, Moving averages, Exponential Smoothing ($\alpha$), Seasonal Decomposition (Trend, Seasonal, Residual), ARIMA forecasting |
| **Machine Learning / Predictive Modeling** | `utils/recommendations.py` & Module 5 | Scikit-learn Simple Linear Regression ($R^2$, slope, RMSE), statistical anomaly spike detection ($+2\sigma$) |
| **Automated Backend ETL & Data Cleaning** | `utils/data_processing.py` & Module 7 | Automatic backend pipeline: schema validation, missing value imputation (median/mode), duplicate removal, non-negative assertions |
| **Excel Practical & Tool Comparison** | Module 8 | Importing into Excel, building PivotTables, PivotCharts, comparing Python vs. Excel |

---

## 3. Technology Stack

- **Programming Language:** Python 3.10+ (tested on Python 3.13)
- **Web Interface:** Streamlit (clean, reactive multi-page dashboard)
- **Data Manipulation:** Pandas, NumPy
- **Relational Database:** SQLite (built-in serverless database) & SQLAlchemy ORM
- **Interactive Visualizations:** Plotly Express & Plotly Graph Objects
- **Statistical Visualizations:** Matplotlib & Seaborn
- **Time Series & Econometrics:** Statsmodels (ARIMA, Exponential Smoothing, Seasonal Decompose)
- **Spreadsheet Processing:** OpenPyXL (Excel `.xlsx` read/write)
- **Predictive Analytics:** Scikit-learn (Linear Regression)

---

## 4. Project Folder Structure

```text
c:\Users\SHUBHI\DAV\
│
├── app.py                          # Main Streamlit web application & UI navigation
├── requirements.txt                # Complete list of Python package dependencies
├── README.md                       # Comprehensive project documentation & viva guide
├── .gitignore                      # Excludes venv, pycache, and sqlite database files
│
├── data/
│   ├── food_waste_sample.csv       # 420-record realistic sample dataset
│   └── generate_sample_data.py     # Script to generate reproducible sample data
│
├── database/
│   ├── .gitkeep                    # Keeps directory tracked in version control
│   └── food_waste.db               # SQLite database file (auto-generated at runtime)
│
└── utils/
    ├── __init__.py                 # Python package initializer
    ├── data_processing.py          # Data ingestion, cleaning, validation, and KPI metrics
    ├── database.py                 # SQLite database operations via SQLAlchemy
    ├── visualizations.py           # Reusable plotting routines for Lab 7 and Lab 8
    ├── time_series.py              # Time series smoothing, decomposition, and ARIMA
    └── recommendations.py          # Scikit-learn regression and waste reduction insights
```

---

## 5. Dataset Schema & Business Rules

The sample dataset contains **420 realistic observations** across 140 operational days:

| Column Name | Data Type | Description | Internal Consistency Constraints |
| :--- | :--- | :--- | :--- |
| `Date` | Datetime (`YYYY-MM-DD`) | Date of observation | Valid chronological calendar dates |
| `Food_Category` | String | Type of food item | Rice, Vegetables, Bread, Dairy, Fruits, Meat, Other |
| `Location` | String | Dining facility | Hostel, Canteen, Restaurant, Catering |
| `Meal_Type` | String | Service period | Breakfast, Lunch, Dinner |
| `Food_Prepared_Kg` | Float | Quantity prepared in kitchen | $\ge 0$ kg |
| `Food_Served_Kg` | Float | Quantity taken by diners | $\ge 0$ kg, $\le \text{Food\_Prepared\_Kg}$ |
| `Food_Wasted_Kg` | Float | Quantity discarded (leftover + plate) | $\ge 0$ kg, $\le \text{Food\_Served\_Kg}$ |
| `Waste_Cause` | String | Primary root cause for waste | Plate Waste, Over-preparation, Spoilage, Kitchen Trimmings, Expired Ingredients, Poor Storage |

> **Primary Formula:**  
> $$\text{Food Waste Percentage (\%)} = \left(\frac{\sum \text{Food\_Wasted\_Kg}}{\sum \text{Food\_Prepared\_Kg}}\right) \times 100$$  
> *(Protected against zero-division in `calculate_kpis` and individual record vectors).*

---

## 6. Installation & Execution Guide (Windows PowerShell)

Follow these exact steps in **Windows PowerShell**:

### Step 1: Open Terminal in the Project Directory
```powershell
cd c:\Users\SHUBHI\DAV
```

### Step 2: (Optional but Recommended) Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell shows an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```powershell
streamlit run app.py
```
Streamlit will automatically open your default browser at:  
👉 **`http://localhost:8501`**

---

## 7. Database Architecture & Practical 5 Guide

The project uses **SQLAlchemy** to interface seamlessly between Pandas and **SQLite**:

### 1. Connection Engine
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///database/food_waste.db", echo=False)
```

### 2. Loading Pandas DataFrames into Database (`to_sql`)
```python
df.to_sql(
    name='food_waste_records',
    con=engine,
    if_exists='append',   # or 'replace' to drop and recreate table
    index=False
)
```

### 3. Key SQL Queries for Viva Demonstration
1. **Total Waste by Food Category:**
   ```sql
   SELECT Food_Category, 
          SUM(Food_Wasted_Kg) AS Total_Waste_Kg, 
          ROUND(AVG(Food_Wasted_Kg), 2) AS Avg_Waste_Kg 
   FROM food_waste_records 
   GROUP BY Food_Category 
   ORDER BY Total_Waste_Kg DESC;
   ```

2. **Facility Waste Efficiency Ratio:**
   ```sql
   SELECT Location, 
          SUM(Food_Prepared_Kg) AS Total_Prepared, 
          SUM(Food_Wasted_Kg) AS Total_Wasted, 
          ROUND((SUM(Food_Wasted_Kg) * 100.0 / SUM(Food_Prepared_Kg)), 2) AS Waste_Pct 
   FROM food_waste_records 
   GROUP BY Location 
   ORDER BY Waste_Pct DESC;
   ```

3. **Production Connection Strings (PostgreSQL / MySQL):**
   - **PostgreSQL:** `postgresql+psycopg2://user:password@localhost:5432/dbname`
   - **MySQL:** `mysql+pymysql://user:password@localhost:3306/dbname`
   - *Security Rule:* Never hardcode credentials in code. Use `os.getenv("DATABASE_URL")` with `.env` files.

---

## 8. Analytical & Statistical Concepts Explained

### A. Moving Average
Smooths high-frequency noise and day-to-day spikes:
$$MA_t = \frac{1}{k} \sum_{i=0}^{k-1} Y_{t-i}$$
where $k$ is the sliding window size (e.g., 7 days).

### B. Simple Exponential Smoothing
Assigns exponentially declining weights to older data points:
$$S_t = \alpha Y_t + (1 - \alpha) S_{t-1}$$
The smoothing parameter $\alpha \in (0, 1)$ governs responsiveness to recent fluctuations.

### C. Classical Time Series Decomposition
Separates the time series into three interpretable elements:
$$Y_t = \text{Trend}_t + \text{Seasonal}_t + \text{Residual}_t$$
- **Trend:** Long-term direction (upward/downward).
- **Seasonal:** Repeating cyclical fluctuations at fixed intervals (e.g., weekly meal cycles).
- **Residual:** Unpredictable random operational noise.

### D. ARIMA Forecasting
An AutoRegressive Integrated Moving Average model denoted as $\text{ARIMA}(p, d, q)$:
- $p$: Number of autoregressive lag terms.
- $d$: Degree of differencing required to attain stationarity.
- $q$: Number of moving average error terms.

### E. Scikit-Learn Linear Regression
Fits an ordinary least squares model:
$$\text{Food\_Wasted\_Kg} = \beta_1 \times \text{Food\_Prepared\_Kg} + \beta_0$$
The $R^2$ score measures the proportion of variance in food waste directly explained by preparation quantity.

---

## 9. Microsoft Excel Practical Workflow

To verify Python analytics against Microsoft Excel:
1. Open Excel and navigate to **Data** $\to$ **Get Data** $\to$ **From Text/CSV**.
2. Select `data/food_waste_sample.csv`. Verify preview and click **Load**.
3. Select any cell, press `Ctrl + A`, and click **Insert** $\to$ **PivotTable**.
4. Configure PivotTable:
   - **Rows:** `Food_Category`
   - **Values:** `Sum of Food_Prepared_Kg`, `Sum of Food_Wasted_Kg`
5. Click **PivotTable Analyze** $\to$ **Fields, Items, & Sets** $\to$ **Calculated Field**:
   - Formula: `='Food_Wasted_Kg' / 'Food_Prepared_Kg' * 100`
6. Insert a **Clustered Column PivotChart** and **Donut Chart** to present categorical waste proportions.

---

## 10. Frequently Asked Viva Questions & Answers

**Q1: Why did you choose Streamlit over web frameworks like Django or Flask?**  
*Answer:* Streamlit is specifically designed for rapid data science and analytics development. It natively binds to Pandas DataFrames and interactive Plotly charts without requiring custom frontend HTML/JavaScript or REST API routing boilerplate.

**Q2: What is the purpose of differencing ($d$) in an ARIMA model?**  
*Answer:* ARIMA requires the underlying time series to be stationary (constant mean and variance over time). Differencing ($Y'_t = Y_t - Y_{t-1}$) removes trends and non-stationarity.

**Q3: How does your system handle missing values during data cleaning?**  
*Answer:* In `utils/data_processing.py`, users can select either row deletion or statistical imputation (filling missing numeric values with the column median to avoid outlier skewing, and categorical values with the mode).

**Q4: How does a Box-and-Whisker plot identify outliers?**  
*Answer:* It calculates the Interquartile Range ($IQR = Q3 - Q1$). Data points falling below $Q1 - 1.5 \times IQR$ or above $Q3 + 1.5 \times IQR$ are plotted as isolated outlier dots.

**Q5: What is the difference between correlation and regression?**  
*Answer:* Correlation ($r$) measures the strength and direction of linear association between two variables (dimensionless between -1 and +1). Regression models the mathematical equation ($\hat{y} = \beta_1 x + \beta_0$) predicting a dependent outcome variable from an independent predictor.

---

## 11. Customization & Modification Guide

To customize this project for your specific college submission:
- **Change Categories or Locations:** Edit `data/generate_sample_data.py` and run `python data/generate_sample_data.py`.
- **Add New Visualizations:** Add custom functions to `utils/visualizations.py` and call them in `app.py`.
- **Change Database Schema:** Update table definitions in `utils/database.py`.
- **Modify Styling/Themes:** Update the CSS block at the top of `app.py`.

---

## 12. Conclusion & Operational Impact

The system demonstrates how data preprocessing, relational databases, statistical visualization, and econometric time series forecasting combine to solve real-world sustainability challenges. It provides cafeteria administrators and hostel wardens with actionable metrics to minimize surplus preparation, adjust portion sizing, and curtail avoidable food waste.
