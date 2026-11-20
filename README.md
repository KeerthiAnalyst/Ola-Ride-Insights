# 🚗 Ola Ride Insights | Ride-Sharing & Mobility Analytics

An end-to-end data analytics project focused on analyzing Ola ride-booking data to uncover insights into ride performance, revenue, customer behavior, vehicle usage, and cancellations.

## 📌 Project Overview

This project analyzes Ola ride-booking data for July 2024 using Python, SQL, Power BI, and Streamlit.

The objective is to understand booking trends, identify cancellation patterns, evaluate vehicle performance, and generate actionable business insights to support better operational decisions.

## 🎯 Business Objectives

- Analyze overall ride-booking performance.
- Identify popular vehicle types and ride trends.
- Evaluate revenue and payment-method performance.
- Investigate customer and driver cancellation patterns.
- Understand customer and driver ratings.
- Identify opportunities to improve ride operations and customer experience.

## 🛠️ Tools & Technologies

- **Python:** Data cleaning and exploratory data analysis
- **Pandas & NumPy:** Data manipulation
- **SQL Server:** Business analysis and SQL queries
- **Power BI:** Interactive dashboards and visualizations
- **Streamlit:** Interactive analytics application
- **Plotly:** Interactive charts

## 📂 Project Structure

```text
Ola-Ride-Insights/
│
├── app.py
├── requirements.txt
├── OLA_Cleaned_Data.csv
├── OLA_Ride_Insights.ipynb
├── OLA_RIDES_PROJECT.sql
└── README.md
```

## 📊 Dataset Overview

- Total bookings: 103,024
- Analysis period: July 2024
- Total columns: 20
- Data includes booking status, vehicle type, locations, ride distance, booking value, payment method, cancellation details, and ratings.

## 🔍 Key Analysis Areas

1. **Overall Analysis:** Booking trends, success rate, and ride performance.
2. **Vehicle Analysis:** Vehicle-wise booking and distance performance.
3. **Revenue Analysis:** Revenue trends and payment-method analysis.
4. **Cancellation Analysis:** Customer and driver cancellation patterns.
5. **Ratings Analysis:** Customer and driver rating performance.
6. **SQL Insights:** Business-focused queries using SQL Server.

## 📈 Key Findings

- Total bookings: 103,024.
- Successful bookings: 63,967.
- Success rate: 62.1%.
- Driver cancellations: 18,434.
- Customer cancellations: 10,499.
- Driver not found: 10,124.
- Successful ride value: ₹35,080,467.
- Average customer rating: 4.00.
- Average ride distance: 14.19 km.

## 🚀 Streamlit Application

The project includes an interactive Streamlit application with:

- Date and vehicle-type filters.
- Booking performance KPIs.
- Ride and vehicle analysis.
- Revenue analysis.
- Cancellation analysis.
- Ratings analysis.
- SQL insights.

### Run Locally

Clone the repository:

```bash
git clone https://github.com/KeerthiAnalyst/Ola-Ride-Insights.git
```

Navigate to the project folder:

```bash
cd Ola-Ride-Insights
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## 💡 Business Impact

The analysis helps identify booking performance trends, understand cancellation drivers, evaluate vehicle utilization, and explore opportunities to improve operational efficiency and customer satisfaction.

## 👩‍💻 Author

**Keerthi Senthil**

GitHub: [KeerthiAnalyst](https://github.com/KeerthiAnalyst)

---

*This project was completed as an end-to-end data analytics capstone project.*
