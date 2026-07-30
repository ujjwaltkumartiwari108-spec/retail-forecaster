import streamlit as st
import pandas as pd
import pickle
import datetime
import base64
import random

# 1. Premium Page Configuration
st.set_page_config(page_title="AI Retail Forecaster", page_icon="🛒", layout="wide")

# 2. Background Image Function
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            html, body, [class*="css"], span, label, p, h3 {{
                color: #ffffff !important;
            }}
            [data-testid="stAppViewBlockContainer"] {{
                background-color: rgba(0, 0, 0, 0.5) !important;
                padding: 2.5rem;
                border-radius: 15px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
                margin-top: 2rem;
            }}
            [data-testid="stSidebar"] {{
                background-color: rgba(0, 0, 0, 0.85) !important;
            }}
            [data-testid="stMetricValue"] {{
                color: #00d2ff !important;
                font-weight: bold;
            }}
            .stButton>button {{
                background-color: #2e66ff !important;
                color: white !important;
                border-radius: 8px;
                height: 3em;
                width: 100%;
                font-weight: bold;
                border: none;
            }}
            .stButton>button:hover {{
                background-color: #1a4fcf !important;
            }}
            /* Tab text colour fix */
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
                color: #ffffff !important;
                font-weight: bold;
                font-size: 16px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        pass

# Function Call
add_bg_from_local('background.png')

# 3. Sidebar Panel
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081840.png", width=120) 
    st.title("⚙️ Settings Panel")
    st.markdown("---")
    
    st.write("### Control Panel")
    selected_date = st.date_input("🗓️ Select Forecast Date", datetime.date.today())
    predict_btn = st.button("Predict Full Dashboard 🚀")
    
    st.markdown("---")
    st.write("**Babu Banarasi Das University**")
    st.write("B.Tech CSE Minor Project")
    st.write("Developed by: **Ujjwal**")

# 4. Main Dashboard Area - STRICT BLACK TITLE
st.markdown("""
    <div style="color: black !important; font-size: 42px; font-weight: 800; margin-bottom: 10px;">
        🛒 AI Retail Demand Forecasting
    </div>
    <div style="color: black !important; font-weight: 600; font-size: 18px;">
        Welcome to the next-generation inventory intelligence dashboard.
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# Load Model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        return pickle.load(file)

try:
    model = load_model()
except FileNotFoundError:
    st.error("Error: 'model.pkl' file not found.")
    st.stop()

# 5. Full Dashboard Logic
if predict_btn:
    year, month, day, day_of_week = selected_date.year, selected_date.month, selected_date.day, selected_date.weekday()
    input_features = pd.DataFrame([[year, month, day, day_of_week]], columns=['Year', 'Month', 'Day', 'DayOfWeek'])
    
    # AI Prediction (Total Sales)
    prediction = model.predict(input_features)[0]
    
    # Simulated Calculations based on Predicted Sales
    avg_ticket_size = random.uniform(35.0, 50.0)
    expected_footfall = int(prediction / avg_ticket_size)
    
    # Peak hour logic based on Day of the week (Weekends vs Weekdays)
    if day_of_week >= 5: # Saturday/Sunday
        peak_hour = "06:00 PM - 08:00 PM"
        rating = round(random.uniform(4.0, 4.4), 1) # Rush implies slightly lower rating
    else:
        peak_hour = "01:00 PM - 03:00 PM"
        rating = round(random.uniform(4.5, 4.9), 1)
        
    # Categories percentage split
    electronics_sales = prediction * 0.40
    groceries_sales = prediction * 0.35
    clothing_sales = prediction * 0.25
    
    # UI TABS SETUP
    tab1, tab2, tab3 = st.tabs(["💰 Total Sales Trend", "👥 Footfall & Categories", "⭐ Store Operations"])
    
    # --- TAB 1: Main Sales ---
    with tab1:
        st.write("### Financial Forecast")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="🎯 Predicted Revenue", value=f"${prediction:,.2f}", delta="AI Generated")
        col2.metric(label="📅 Target Date", value=selected_date.strftime("%b %d, %Y"))
        col3.metric(label="🤖 ML Engine", value="Active", delta="Random Forest")
        
        st.markdown("---")
        st.write("#### 📈 Upcoming 7-Day Trend")
        future_dates = [selected_date + datetime.timedelta(days=i) for i in range(7)]
        future_features = pd.DataFrame([[d.year, d.month, d.day, d.weekday()] for d in future_dates], columns=['Year', 'Month', 'Day', 'DayOfWeek'])
        future_predictions = model.predict(future_features)
        
        chart_data = pd.DataFrame({'Date': future_dates, 'Sales ($)': future_predictions}).set_index('Date')
        st.area_chart(chart_data)

    # --- TAB 2: Footfall & Categories ---
    with tab2:
        st.write("### Traffic & Category Demand")
        c1, c2 = st.columns(2)
        c1.metric(label="🚶‍♂️ Estimated Customer Footfall", value=f"{expected_footfall} People", delta="High Traffic" if expected_footfall > 300 else "Normal Traffic")
        c2.metric(label="🛒 Avg. Cart Value", value=f"${avg_ticket_size:.2f}")
        
        st.markdown("---")
        st.write("#### 📦 Predicted Category Split")
        st.progress(40, text=f"💻 Electronics & Gadgets (${electronics_sales:,.0f})")
        st.progress(35, text=f"🍞 Groceries & Essentials (${groceries_sales:,.0f})")
        st.progress(25, text=f"👕 Clothing & Apparel (${clothing_sales:,.0f})")
        
    # --- TAB 3: Operations ---
    with tab3:
        st.write("### Store Management & Feedback")
        o1, o2 = st.columns(2)
        o1.metric(label="⏰ Predicted Peak Hour", value=peak_hour, delta="Max Staff Needed", delta_color="inverse")
        o2.metric(label="⭐ Expected Customer Rating", value=f"{rating} / 5.0")
        
        st.info("💡 Tip for Manager: Schedule maximum billing counter staff during the predicted Peak Hour to maintain the customer rating.")
    
    st.balloons()
else:
    st.info("👈 Please select a date from the sidebar and click **'Predict Full Dashboard'** to generate the AI forecast.")