
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from database import create_database, get_buildings

# Page Configuration
st.set_page_config(
    page_title="EcoTrack | Campus Energy Monitoring",
    page_icon="⚡",
    layout="wide"
)
create_database()

# Main Heading
st.title("⚡ EcoTrack")
st.subheader("Campus Energy Monitoring Dashboard")

st.write(
    "Monitor electricity consumption, track energy usage "
    "and improve campus energy efficiency."
)

st.success("Welcome to EcoTrack!")

# Custom CSS Styling
st.markdown("""
<style>

.stApp {
    background-color: #0E1726;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #142235;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #FFFFFF;
}

p {
    color: #B8C5D6;
}

</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("⚡ EcoTrack")
st.sidebar.caption("Campus Energy Management")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Building Monitoring",
        "Live Monitoring",
        "Alerts & Notifications",
        "Energy Analytics",
        "Reports",
        "Settings"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Campus Energy Monitoring System")
st.sidebar.caption("Version 1.0")


# Dashboard Overview
if page == "Dashboard":

    st.title("Campus Energy Overview")
    st.write("Monitor overall campus electricity consumption.")

    # Fetch building data from SQLite
    building_data = get_buildings()

    total_consumption = building_data["consumption"].sum()
    total_buildings = len(building_data)
    electricity_rate = st.session_state.get("electricity_rate", 10)
    total_cost = total_consumption * electricity_rate

    active_alerts = (
        building_data["consumption"] >
        building_data["monthly_limit"]
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Energy Consumption",
            value=f"{total_consumption:,.0f} kWh"
        )

    with col2:
        st.metric(
            label="Total Buildings",
            value=total_buildings
        )

    with col3:
        st.metric(
            label="Estimated Electricity Cost",
            value=f"₹{total_cost:,.0f}"
        )

    with col4:
        st.metric(
            label="Active Alerts",
            value=int(active_alerts)
        )

    st.caption(
        "Cost is estimated at ₹10 per kWh. "
        "Alert count is based on building consumption exceeding its limit."
    )

    st.divider()

    st.subheader("Daily Energy Consumption")

    # Simulated daily energy data for demonstration
    days = list(range(1, 31))

    energy_data = pd.DataFrame({
        "Day": days,
        "Energy Consumption": np.random.randint(300, 600, 30)
    })

    fig = px.area(
        energy_data,
        x="Day",
        y="Energy Consumption",
        title="Simulated Daily Electricity Usage (kWh)",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Day of Month",
        yaxis_title="Energy (kWh)",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Building-wise Energy Consumption")

    # Prepare database data for chart
    chart_data = building_data.rename(columns={
        "building_name": "Building",
        "consumption": "Consumption"
    })

    fig2 = px.bar(
        chart_data,
        x="Building",
        y="Consumption",
        color="Consumption",
        title="Electricity Consumption by Building",
        color_continuous_scale="Greens",
        text="Consumption"
    )

    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Campus Buildings",
        yaxis_title="Energy (kWh)",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)


# Building Monitoring Page
if page == "Building Monitoring":

    st.title("🏢 Building Monitoring")
    st.write("Monitor electricity consumption across campus buildings.")

    # Fetch data from SQLite database
    building_data = get_buildings()

    # Rename database columns
    building_data = building_data.rename(columns={
        "building_name": "Building",
        "consumption": "Consumption (kWh)",
        "monthly_limit": "Monthly Limit (kWh)"
    })

    # Calculate building status
    building_data["Status"] = building_data.apply(
        lambda row: "High Usage"
        if row["Consumption (kWh)"] > row["Monthly Limit (kWh)"]
        else "Normal",
        axis=1
    )

    # Search Building
    search = st.text_input("Search Building")

    if search:
        building_data = building_data[
            building_data["Building"].str.contains(
                search, case=False, na=False
            )
        ]

    # Display Building Table
    st.dataframe(
        building_data,
        use_container_width=True,
        hide_index=True
    )

    # Building Consumption Chart
    st.subheader("Building Consumption Comparison")

    fig = px.bar(
        building_data,
        x="Building",
        y="Consumption (kWh)",
        color="Status",
        color_discrete_map={
            "Normal": "#22C55E",
            "High Usage": "#EF4444"
        },
        title="Building-wise Electricity Usage"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# Live Energy Monitoring Page
if page == "Live Monitoring":

    st.title("⚡ Live Energy Monitoring")
    st.write("Simulated smart meter readings across campus.")

    import random
    from datetime import datetime

    col1, col2, col3 = st.columns(3)

    power = random.randint(120, 250)
    voltage = random.randint(215, 240)
    current = round(power * 1000 / voltage, 2)

    with col1:
        st.metric("Current Power", f"{power} kW")

    with col2:
        st.metric("Voltage", f"{voltage} V")

    with col3:
        st.metric("Current", f"{current} A")

    st.divider()

    st.subheader("Smart Meter Status")

    meter_data = pd.DataFrame({
        "Meter ID": ["SM-001", "SM-002", "SM-003", "SM-004"],
        "Building": [
            "Academic Block",
            "Library",
            "Computer Lab",
            "Hostel A"
        ],
        "Power (kW)": [
            random.randint(40, 90),
            random.randint(20, 60),
            random.randint(30, 80),
            random.randint(25, 70)
        ],
        "Status": ["Online", "Online", "Online", "Online"]
    })

    st.dataframe(
        meter_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Last updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    if st.button("Refresh Meter Readings"):
        st.rerun()

    st.info(
        "Demo Mode: These readings are simulated. "
        "Actual smart meter integration can be added using IoT communication protocols."
    )


# Alerts and Notifications Page
if page == "Alerts & Notifications":

    st.title("🔔 Alerts & Notifications")
    st.write("Monitor buildings with excessive electricity consumption.")

    # Fetch building data from SQLite
    alert_data = get_buildings()

    # Rename database columns
    alert_data = alert_data.rename(columns={
        "building_name": "Building",
        "consumption": "Consumption (kWh)",
        "monthly_limit": "Limit (kWh)"
    })

    # Calculate excess usage
    alert_data["Excess Usage"] = (
        alert_data["Consumption (kWh)"] -
        alert_data["Limit (kWh)"]
    )

    # Determine alert level
    alert_data["Alert Level"] = alert_data.apply(
        lambda row: "Critical"
        if row["Excess Usage"] > 500
        else "Warning"
        if row["Excess Usage"] > 0
        else "Normal",
        axis=1
    )

    critical = len(
        alert_data[alert_data["Alert Level"] == "Critical"]
    )

    warning = len(
        alert_data[alert_data["Alert Level"] == "Warning"]
    )

    normal = len(
        alert_data[alert_data["Alert Level"] == "Normal"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Buildings", len(alert_data))
    col2.metric("Critical Alerts", critical)
    col3.metric("Warnings", warning)
    col4.metric("Normal Buildings", normal)

    st.divider()

    st.subheader("Energy Alert Details")

    for _, row in alert_data.iterrows():

        if row["Alert Level"] == "Critical":
            st.error(
                f"🚨 {row['Building']} - Critical: "
                f"{row['Excess Usage']} kWh above limit"
            )

        elif row["Alert Level"] == "Warning":
            st.warning(
                f"⚠️ {row['Building']} - Warning: "
                f"{row['Excess Usage']} kWh above limit"
            )

        else:
            st.success(
                f"✅ {row['Building']} - Normal consumption"
            )

    st.divider()

    st.subheader("Complete Alert Report")

    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )


# Energy Analytics Page
if page == "Energy Analytics":

    st.title("📊 Energy Analytics")
    st.write("Analyze campus electricity consumption patterns.")

    period = st.selectbox(
        "Select Analysis Period",
        ["Daily", "Weekly", "Monthly"]
    )

    # Sample trend data for demonstration
    if period == "Daily":
        labels = [f"Day {i}" for i in range(1, 8)]
        values = [420, 450, 390, 510, 480, 530, 460]

    elif period == "Weekly":
        labels = [
            "Week 1", "Week 2",
            "Week 3", "Week 4"
        ]
        values = [3200, 3500, 3100, 3800]

    else:
        labels = [
            "July", "August", "September",
            "October", "November", "December"
        ]
        values = [11000, 12500, 11800, 13200, 12450, 11900]

    analytics_data = pd.DataFrame({
        "Period": labels,
        "Consumption (kWh)": values
    })

    total = sum(values)
    average = round(total / len(values), 2)

    col1, col2 = st.columns(2)

    col1.metric("Sample Total Consumption", f"{total:,} kWh")
    col2.metric("Sample Average Consumption", f"{average:,} kWh")

    st.caption(
        "Daily, weekly and monthly trends use sample data. "
        "Historical readings are not yet connected."
    )

    st.divider()

    st.subheader(f"{period} Consumption Trend")

    fig = px.line(
        analytics_data,
        x="Period",
        y="Consumption (kWh)",
        markers=True,
        title=f"{period} Energy Consumption"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Building-wise Energy Distribution")

    # Fetch live building records from SQLite
    distribution = get_buildings()

    distribution = distribution.rename(columns={
        "building_name": "Building",
        "consumption": "Energy"
    })

    fig2 = px.pie(
        distribution,
        names="Building",
        values="Energy",
        title="Energy Consumption Distribution",
        hole=0.4
    )

    fig2.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)


# Reports Page
if page == "Reports":

    st.title("📄 Energy Reports")
    st.write("Generate and download campus electricity reports.")

    # Fetch latest building data from SQLite
    report_data = get_buildings()

    # Rename database columns
    report_data = report_data.rename(columns={
        "building_name": "Building",
        "consumption": "Consumption (kWh)",
        "monthly_limit": "Monthly Limit (kWh)"
    })

    # Calculate building status
    report_data["Status"] = report_data.apply(
        lambda row: "High Usage"
        if row["Consumption (kWh)"] > row["Monthly Limit (kWh)"]
        else "Normal",
        axis=1
    )

    total_energy = report_data["Consumption (kWh)"].sum()

    high_usage = len(
        report_data[report_data["Status"] == "High Usage"]
    )

    st.subheader("Report Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Buildings", len(report_data))
    col2.metric("Total Energy", f"{total_energy:,.0f} kWh")
    col3.metric("High Usage Buildings", high_usage)

    st.divider()

    st.subheader("Campus Energy Consumption Report")

    st.dataframe(
        report_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Download Report")

    csv = report_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Energy Report (CSV)",
        data=csv,
        file_name="EcoTrack_Energy_Report.csv",
        mime="text/csv"
    )

    st.success("Your database-based energy report is ready for download.")



# Settings Page
if page == "Settings":

    st.title("⚙️ System Settings")
    st.write("Configure campus energy monitoring preferences.")

    # Initialize default settings
    if "energy_limit" not in st.session_state:
        st.session_state.energy_limit = 2000

    if "electricity_rate" not in st.session_state:
        st.session_state.electricity_rate = 10.0

    if "email_alerts" not in st.session_state:
        st.session_state.email_alerts = True

    st.subheader("Energy Consumption Settings")

    with st.form("energy_settings"):

        energy_limit = st.number_input(
            "Maximum Energy Consumption Limit (kWh)",
            min_value=100,
            max_value=10000,
            value=int(st.session_state.energy_limit),
            step=100
        )

        electricity_rate = st.number_input(
            "Electricity Cost per Unit (₹)",
            min_value=1.0,
            max_value=100.0,
            value=float(st.session_state.electricity_rate),
            step=0.5
        )

        email_alerts = st.checkbox(
            "Enable Email Alert Preference",
            value=st.session_state.email_alerts
        )

        submit = st.form_submit_button("Save Settings")

        if submit:
            st.session_state.energy_limit = energy_limit
            st.session_state.electricity_rate = electricity_rate
            st.session_state.email_alerts = email_alerts

            st.success("Settings saved successfully!")

    st.divider()

    st.subheader("Current Configuration")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Energy Limit",
        f"{st.session_state.energy_limit} kWh"
    )

    col2.metric(
        "Electricity Rate",
        f"₹{st.session_state.electricity_rate}/unit"
    )

    col3.metric(
        "Email Alerts",
        "Enabled" if st.session_state.email_alerts else "Disabled"
    )

    st.info(
        "Settings are maintained during the current application session. "
        "Email alert preference is stored, but automatic email delivery "
        "has not been implemented."
    )



