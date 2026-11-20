
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Ola Ride Insights",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

BG = "#101B18"
SIDEBAR = "#0B1713"
CARD = "#1D2C25"
LIME = "#B8F36B"
GREEN = "#438C68"
TEAL = "#35C6B0"
WHITE = "#F4F7F2"
MUTED = "#A6B5AC"
ORANGE = "#D99B54"
RED = "#C66B6B"

st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
    color: {WHITE};
}}
[data-testid="stSidebar"] {{
    background-color: {SIDEBAR};
}}
[data-testid="stSidebar"] * {{
    color: {WHITE};
}}
h1, h2, h3, h4 {{
    color: {WHITE} !important;
}}
p, label {{
    color: {MUTED};
}}
[data-testid="stMetric"] {{
    background-color: {CARD};
    border: 1px solid #34483D;
    padding: 16px;
    border-radius: 12px;
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}
[data-testid="stMetricValue"] {{
    color: {LIME} !important;
}}
.section-title {{
    color: {LIME};
    font-size: 22px;
    font-weight: 700;
    margin: 18px 0 12px 0;
}}
.main-title {{
    font-size: 34px;
    font-weight: 800;
    color: {WHITE};
}}
.subtitle {{
    color: {LIME};
    font-size: 14px;
    margin-bottom: 24px;
}}
div.stButton > button {{
    background-color: {GREEN};
    color: white;
    border-radius: 8px;
    border: none;
}}
div.stButton > button:hover {{
    background-color: {LIME};
    color: {BG};
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 2. LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = Path(__file__).parent / "OLA_Cleaned_Data.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            "Place OLA_Cleaned_Data.csv in the same folder as app.py."
        )

    data = pd.read_csv(file_path, low_memory=False)

    required = [
        "Date", "Time", "Booking_ID", "Booking_Status",
        "Customer_ID", "Vehicle_Type", "Pickup_Location",
        "Drop_Location", "V_TAT", "C_TAT",
        "Canceled_Rides_by_Customer",
        "Canceled_Rides_by_Driver",
        "Incomplete_Rides", "Incomplete_Rides_Reason",
        "Booking_Value", "Payment_Method", "Ride_Distance",
        "Driver_Ratings", "Customer_Rating", "Vehicle Images"
    ]

    missing = [col for col in required if col not in data.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Clean text columns
    for col in data.select_dtypes(include="object").columns:
        data[col] = data[col].map(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Date
    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    # Numeric fields
    numeric_cols = [
        "Booking_Value",
        "Ride_Distance",
        "Driver_Ratings",
        "Customer_Rating"
    ]

    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Standardize booking status text
    data["Booking_Status"] = (
        data["Booking_Status"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

def money(value):
    return f"₹{value:,.0f}"


def heading(title):
    st.markdown(
        f"<div class='section-title'>{title}</div>",
        unsafe_allow_html=True
    )


def successful_rows(data):
    return data[
        data["Booking_Status"].str.lower() == "success"
    ]


def driver_cancelled_rows(data):
    return data[
        data["Booking_Status"].str.lower() == "canceled by driver"
    ]


def customer_cancelled_rows(data):
    return data[
        data["Booking_Status"].str.lower() == "canceled by customer"
    ]


def incomplete_rows(data):
    return data[
        data["Incomplete_Rides"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
    ]


def valid_reason_counts(series, name="Reason"):
    values = series.dropna().astype(str).str.strip()
    values = values[values != ""]

    result = values.value_counts().reset_index()
    result.columns = [name, "Count"]

    return result


def chart_style(fig, height=370):

    fig.update_layout(
        height=height,
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(
            family="Arial",
            color=WHITE,
            size=12
        ),
        title=dict(
            font=dict(color=WHITE, size=17),
            x=0.03,
            xanchor="left"
        ),
        margin=dict(l=30, r=25, t=65, b=35),
        legend=dict(
            font=dict(color=WHITE),
            title_font=dict(color=WHITE)
        ),
        xaxis=dict(
            title_font=dict(color=MUTED),
            tickfont=dict(color=WHITE),
            gridcolor="#34483D"
        ),
        yaxis=dict(
            title_font=dict(color=MUTED),
            tickfont=dict(color=WHITE),
            gridcolor="#34483D"
        )
    )

    return fig


def show_chart(fig):
    st.plotly_chart(
        chart_style(fig),
        use_container_width=True,
        config={"displayModeBar": False}
    )


# =========================================================
# 4. SIDEBAR
# =========================================================

st.sidebar.markdown(
    f"<h1 style='color:{LIME};'>OLA</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown("### MOVE BETTER. LIVE SMARTER.")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Vehicle Analysis",
        "Revenue Analysis",
        "Cancellation Analysis",
        "Ratings Analysis",
        "SQL Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("OLA RIDE INSIGHTS | DATA ANALYTICS PROJECT")


# =========================================================
# 5. GLOBAL FILTERS
# IMPORTANT: NO BOOKING STATUS OR PAYMENT FILTER
# =========================================================

st.sidebar.markdown("### FILTER DATA")

filtered = df.copy()

valid_dates = df["Date"].dropna()

if not valid_dates.empty:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range

        filtered = filtered[
            filtered["Date"].dt.date.between(start_date, end_date)
        ]


vehicle_options = sorted(
    df["Vehicle_Type"].dropna().astype(str).unique()
)

selected_vehicles = st.sidebar.multiselect(
    "Vehicle Type",
    vehicle_options,
    default=vehicle_options
)

if selected_vehicles:
    filtered = filtered[
        filtered["Vehicle_Type"].astype(str).isin(selected_vehicles)
    ]

if st.sidebar.button("Reset Filters"):
    st.rerun()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# =========================================================
# 6. COMMON KPI VALUES
# =========================================================

success_data = successful_rows(filtered)

total_bookings = len(filtered)
success_count = len(success_data)

success_rate = (
    success_count / total_bookings
    if total_bookings else 0
)

total_revenue = success_data["Booking_Value"].sum()

avg_customer_rating = filtered["Customer_Rating"].mean()
avg_distance = filtered["Ride_Distance"].mean()


# =========================================================
# 7. HEADER
# =========================================================

st.markdown(
    "<div class='main-title'>OLA RIDE INSIGHTS</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>"
    "MOVE BETTER. LIVE SMARTER. | RIDE-SHARING ANALYTICS"
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 8. KPI CARDS
# =========================================================

def show_kpis():

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Bookings", f"{total_bookings:,}")
    c2.metric("Success Rate", f"{success_rate:.1%}")
    c3.metric("Successful Ride Value", money(total_revenue))

    c4.metric(
        "Avg Customer Rating",
        f"{avg_customer_rating:.2f}"
        if pd.notna(avg_customer_rating) else "N/A"
    )

    c5.metric(
        "Avg Ride Distance",
        f"{avg_distance:.2f} km"
        if pd.notna(avg_distance) else "N/A"
    )


# =========================================================
# PAGE 1: OVERVIEW
# =========================================================

if page == "Overview":

    show_kpis()
    heading("Ride Performance Overview")

    left, right = st.columns(2)

    # Chart 1: Ride Volume Over Time
    with left:

        daily = filtered.dropna(subset=["Date"]).copy()
        daily["Ride_Date"] = daily["Date"].dt.normalize()

        daily_bookings = (
            daily.groupby("Ride_Date")["Booking_ID"]
            .count()
            .reset_index(name="Bookings")
            .sort_values("Ride_Date")
        )

        fig = px.line(
            daily_bookings,
            x="Ride_Date",
            y="Bookings",
            title="Ride Volume Over Time"
        )

        fig.update_traces(
            line=dict(color=LIME, width=3),
            mode="lines"
        )

        show_chart(fig)

    # Chart 2: Booking Status Breakdown
    with right:

        status_data = (
            filtered["Booking_Status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = ["Booking Status", "Bookings"]

        fig = px.pie(
            status_data,
            names="Booking Status",
            values="Bookings",
            hole=0.58,
            title="Booking Status Breakdown",
            color="Booking Status",
            color_discrete_map={
                "Success": LIME,
                "Canceled by Driver": ORANGE,
                "Canceled by Customer": RED,
                "Driver Not Found": TEAL
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color=CARD, width=3))
        )

        show_chart(fig)

    left, right = st.columns(2)

    # Chart 3: Top 5 Vehicle Types by Distance
    with left:

        vehicle_distance = (
            filtered.groupby("Vehicle_Type")["Ride_Distance"]
            .sum()
            .nlargest(5)
            .reset_index()
        )

        fig = px.bar(
            vehicle_distance,
            x="Ride_Distance",
            y="Vehicle_Type",
            orientation="h",
            title="Top 5 Vehicle Types by Distance",
            color="Ride_Distance",
            color_continuous_scale=[GREEN, LIME]
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending")
        )

        show_chart(fig)

    # Chart 4: Daily Ride Distance
    with right:

        daily_distance_data = filtered.dropna(subset=["Date"]).copy()
        daily_distance_data["Ride_Date"] = (
            daily_distance_data["Date"].dt.normalize()
        )

        daily_distance = (
            daily_distance_data.groupby("Ride_Date")["Ride_Distance"]
            .sum()
            .reset_index()
            .sort_values("Ride_Date")
        )

        fig = px.area(
            daily_distance,
            x="Ride_Date",
            y="Ride_Distance",
            title="Daily Ride Distance"
        )

        fig.update_traces(
            line=dict(color=TEAL, width=2),
            fillcolor="rgba(53,198,176,0.20)"
        )

        show_chart(fig)

    heading("Dataset Preview")

    st.dataframe(
        filtered.head(10),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 2: VEHICLE ANALYSIS
# =========================================================

elif page == "Vehicle Analysis":

    heading("Vehicle Performance Analysis")

    vehicle_data = (
        filtered.groupby("Vehicle_Type")
        .agg(
            Total_Bookings=("Booking_ID", "count"),
            Average_Distance=("Ride_Distance", "mean"),
            Total_Distance=("Ride_Distance", "sum"),
            Average_Customer_Rating=("Customer_Rating", "mean"),
            Average_Driver_Rating=("Driver_Ratings", "mean")
        )
        .reset_index()
    )

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            vehicle_data.sort_values(
                "Average_Distance", ascending=False
            ),
            x="Vehicle_Type",
            y="Average_Distance",
            title="Average Distance by Vehicle Type",
            color="Average_Distance",
            color_continuous_scale=[GREEN, LIME]
        )

        show_chart(fig)

    with right:

        fig = px.bar(
            vehicle_data.sort_values(
                "Total_Bookings", ascending=False
            ),
            x="Vehicle_Type",
            y="Total_Bookings",
            title="Total Bookings by Vehicle Type",
            color="Total_Bookings",
            color_continuous_scale=[GREEN, TEAL]
        )

        show_chart(fig)

    heading("Vehicle Performance Table")

    st.dataframe(
        vehicle_data.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 3: REVENUE ANALYSIS
# =========================================================

elif page == "Revenue Analysis":

    heading("Revenue Performance Analysis")

    revenue_data = successful_rows(filtered)

    total_revenue_page = revenue_data["Booking_Value"].sum()
    avg_booking_value = revenue_data["Booking_Value"].mean()

    c1, c2, c3 = st.columns(3)

    c1.metric("Successful Ride Revenue", money(total_revenue_page))
    c2.metric("Successful Bookings", f"{len(revenue_data):,}")

    c3.metric(
        "Average Booking Value",
        money(avg_booking_value)
        if pd.notna(avg_booking_value) else "₹0"
    )

    left, right = st.columns(2)

    # Revenue by Payment Method
    with left:

        payment_data = revenue_data.copy()

        payment_data["Payment_Method"] = (
            payment_data["Payment_Method"].fillna("Unknown")
        )

        payment_revenue = (
            payment_data.groupby("Payment_Method")["Booking_Value"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            payment_revenue,
            names="Payment_Method",
            values="Booking_Value",
            hole=0.55,
            title="Revenue by Payment Method",
            color_discrete_sequence=[LIME, TEAL, GREEN, ORANGE, RED]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        show_chart(fig)

    # Top 5 Customers
    with right:

        top_customers = (
            revenue_data.groupby("Customer_ID")["Booking_Value"]
            .sum()
            .nlargest(5)
            .reset_index()
        )

        fig = px.bar(
            top_customers,
            x="Booking_Value",
            y="Customer_ID",
            orientation="h",
            title="Top 5 Customers by Booking Value",
            color="Booking_Value",
            color_continuous_scale=[GREEN, LIME]
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending")
        )

        show_chart(fig)

    vehicle_revenue = (
        revenue_data.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        vehicle_revenue,
        x="Vehicle_Type",
        y="Booking_Value",
        title="Successful Ride Revenue by Vehicle",
        color="Booking_Value",
        color_continuous_scale=[GREEN, LIME]
    )

    show_chart(fig)


# =========================================================
# PAGE 4: CANCELLATION ANALYSIS
# =========================================================

elif page == "Cancellation Analysis":

    heading("Cancellation Analysis")

    # Exact status matching from your dataset
    driver_data = driver_cancelled_rows(filtered)
    customer_data = customer_cancelled_rows(filtered)
    incomplete_data = incomplete_rows(filtered)

    driver_count = len(driver_data)
    customer_count = len(customer_data)
    incomplete_count = len(incomplete_data)

    c1, c2, c3 = st.columns(3)

    c1.metric("Driver Cancellations", f"{driver_count:,}")
    c2.metric("Customer Cancellations", f"{customer_count:,}")
    c3.metric("Incomplete Rides", f"{incomplete_count:,}")

    left, right = st.columns(2)

    # Driver cancellation reasons
    with left:

        driver_reasons = valid_reason_counts(
            driver_data["Canceled_Rides_by_Driver"],
            "Driver Cancellation Reason"
        )

        fig = px.bar(
            driver_reasons,
            x="Count",
            y="Driver Cancellation Reason",
            orientation="h",
            title="Driver Cancellation Reasons",
            color="Count",
            color_continuous_scale=[GREEN, LIME]
        )

        fig.update_layout(
            yaxis=dict(categoryorder="total ascending")
        )

        show_chart(fig)

    # Customer cancellation reasons
    with right:

        customer_reasons = valid_reason_counts(
            customer_data["Canceled_Rides_by_Customer"],
            "Customer Cancellation Reason"
        )

        fig = px.pie(
            customer_reasons,
            names="Customer Cancellation Reason",
            values="Count",
            hole=0.5,
            title="Customer Cancellation Reasons",
            color_discrete_sequence=[LIME, TEAL, GREEN, ORANGE, RED]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        show_chart(fig)

    heading("Incomplete Ride Reasons")

    incomplete_reasons = valid_reason_counts(
        incomplete_data["Incomplete_Rides_Reason"],
        "Incomplete Ride Reason"
    )

    fig = px.bar(
        incomplete_reasons,
        x="Incomplete Ride Reason",
        y="Count",
        title="Incomplete Ride Reasons",
        color="Count",
        color_continuous_scale=[GREEN, TEAL]
    )

    show_chart(fig)

    # Actual counts for verification
    with st.expander("View cancellation and incomplete ride data"):

        st.write("Booking status counts")

        status_counts = (
            filtered["Booking_Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = ["Booking Status", "Count"]

        st.dataframe(
            status_counts,
            use_container_width=True,
            hide_index=True
        )

        st.write("Driver cancellation reasons")
        st.dataframe(driver_reasons, use_container_width=True, hide_index=True)

        st.write("Customer cancellation reasons")
        st.dataframe(customer_reasons, use_container_width=True, hide_index=True)

        st.write("Incomplete ride reasons")
        st.dataframe(incomplete_reasons, use_container_width=True, hide_index=True)


# =========================================================
# PAGE 5: RATINGS ANALYSIS
# =========================================================

elif page == "Ratings Analysis":

    heading("Customer & Driver Ratings")

    driver_avg = filtered["Driver_Ratings"].mean()
    customer_avg = filtered["Customer_Rating"].mean()

    c1, c2 = st.columns(2)

    c1.metric(
        "Average Driver Rating",
        f"{driver_avg:.2f}" if pd.notna(driver_avg) else "N/A"
    )

    c2.metric(
        "Average Customer Rating",
        f"{customer_avg:.2f}" if pd.notna(customer_avg) else "N/A"
    )

    left, right = st.columns(2)

    with left:

        driver_ratings = filtered.dropna(
            subset=["Driver_Ratings"]
        )

        fig = px.histogram(
            driver_ratings,
            x="Driver_Ratings",
            nbins=10,
            title="Driver Rating Distribution",
            color_discrete_sequence=[LIME]
        )

        show_chart(fig)

    with right:

        customer_ratings = filtered.dropna(
            subset=["Customer_Rating"]
        )

        fig = px.histogram(
            customer_ratings,
            x="Customer_Rating",
            nbins=10,
            title="Customer Rating Distribution",
            color_discrete_sequence=[TEAL]
        )

        show_chart(fig)

    heading("Customer vs Driver Ratings by Vehicle")

    rating_comparison = (
        filtered.groupby("Vehicle_Type")
        .agg(
            Customer_Rating=("Customer_Rating", "mean"),
            Driver_Rating=("Driver_Ratings", "mean")
        )
        .reset_index()
    )

    rating_long = rating_comparison.melt(
        id_vars="Vehicle_Type",
        value_vars=["Customer_Rating", "Driver_Rating"],
        var_name="Rating Type",
        value_name="Average Rating"
    )

    fig = px.bar(
        rating_long,
        x="Vehicle_Type",
        y="Average Rating",
        color="Rating Type",
        barmode="group",
        title="Customer vs Driver Ratings",
        color_discrete_sequence=[LIME, TEAL]
    )

    show_chart(fig)


# =========================================================
# PAGE 6: SQL INSIGHTS
# =========================================================

elif page == "SQL Insights":

    heading("SQL Business Insights")

    st.caption(
        "Ten business questions answered using the cleaned dataset."
    )

    data = filtered.copy()
    success = successful_rows(data)

    # 1. Successful bookings
    st.markdown("### 1. Successful Bookings")

    st.metric("Total Successful Bookings", f"{len(success):,}")

    # 2. Average distance by vehicle
    st.markdown("### 2. Average Ride Distance per Vehicle Type")

    q2 = (
        data.groupby("Vehicle_Type")["Ride_Distance"]
        .mean()
        .reset_index(name="Average_Ride_Distance")
        .sort_values("Average_Ride_Distance", ascending=False)
    )

    st.dataframe(q2.round(2), use_container_width=True, hide_index=True)

    # 3. Customer cancellations
    st.markdown("### 3. Customer Cancelled Rides")

    st.metric(
        "Customer Cancelled Rides",
        f"{len(customer_cancelled_rows(data)):,}"
    )

    # 4. Top 5 customers
    st.markdown("### 4. Top 5 Customers by Ride Count")

    q4 = (
        data.groupby("Customer_ID")["Booking_ID"]
        .count()
        .reset_index(name="Total_Rides")
        .nlargest(5, "Total_Rides")
    )

    st.dataframe(q4, use_container_width=True, hide_index=True)

    # 5. Driver cancellation reasons
    st.markdown("### 5. Driver Cancellation Reasons")

    q5 = valid_reason_counts(
        driver_cancelled_rows(data)["Canceled_Rides_by_Driver"],
        "Cancellation Reason"
    )

    st.dataframe(q5, use_container_width=True, hide_index=True)

    # 6. Prime Sedan ratings
    st.markdown("### 6. Maximum and Minimum Driver Ratings for Prime Sedan")

    prime_sedan = data[
        data["Vehicle_Type"].astype(str).str.strip().str.lower()
        == "prime sedan"
    ]

    prime_ratings = prime_sedan["Driver_Ratings"].dropna()

    if not prime_ratings.empty:

        c1, c2 = st.columns(2)

        c1.metric("Maximum Driver Rating", f"{prime_ratings.max():.2f}")
        c2.metric("Minimum Driver Rating", f"{prime_ratings.min():.2f}")

    else:
        st.info("No Prime Sedan rating records found.")

    # 7. UPI rides
    st.markdown("### 7. UPI Rides")

    upi_count = (
        data["Payment_Method"].fillna("").astype(str)
        .str.strip().str.lower().eq("upi").sum()
    )

    st.metric("UPI Bookings", f"{upi_count:,}")

    # 8. Average customer rating by vehicle
    st.markdown("### 8. Average Customer Rating per Vehicle Type")

    q8 = (
        data.groupby("Vehicle_Type")["Customer_Rating"]
        .mean()
        .reset_index(name="Average_Customer_Rating")
        .sort_values("Average_Customer_Rating", ascending=False)
    )

    st.dataframe(q8.round(2), use_container_width=True, hide_index=True)

    # 9. Successful booking value
    st.markdown("### 9. Total Booking Value for Successful Rides")

    st.metric(
        "Successful Booking Value",
        money(success["Booking_Value"].sum())
    )

    # 10. Incomplete rides
    st.markdown("### 10. Incomplete Rides and Reasons")

    incomplete = incomplete_rows(data)

    st.metric("Total Incomplete Rides", f"{len(incomplete):,}")

    q10 = valid_reason_counts(
        incomplete["Incomplete_Rides_Reason"],
        "Incomplete Ride Reason"
    )

    st.dataframe(q10, use_container_width=True, hide_index=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    f"""
    <p style='text-align:center;color:{MUTED};'>
    OLA RIDE INSIGHTS | DATA ANALYTICS PROJECT<br>
    MOVE BETTER. LIVE SMARTER.
    </p>
    """,
    unsafe_allow_html=True
)
