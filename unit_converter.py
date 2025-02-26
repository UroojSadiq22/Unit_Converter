import streamlit as st
from pint import UnitRegistry
import datetime
import pandas as pd
import random
import time

# ✅ Move set_page_config to the top (Must be the first command)
st.set_page_config(page_title="AI-Powered Instant Unit Converter", page_icon="🔄", layout="centered")

# Initialize unit registry
ureg = UnitRegistry()

def convert_units(value, from_unit, to_unit):
    try:
        result = (value * ureg(from_unit)).to(to_unit)
        return result.magnitude, result.units
    except Exception as e:
        return None, str(e)

def log_conversion(value, from_unit, to_unit, result):
    with open("conversion_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {value} {from_unit} -> {result} {to_unit}\n")

def load_conversion_history():
    try:
        with open("conversion_log.txt", "r") as log_file:
            lines = log_file.readlines()
        history_data = [line.strip().split(" - ") for line in lines]
        return pd.DataFrame(history_data, columns=["Timestamp", "Conversion"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Timestamp", "Conversion"])

def ai_suggestions():
    insights = [
        "Did you know? The metric system is used by 95% of the world!",
        "Fun Fact: A mile was originally defined as 1,000 Roman paces.",
        "Energy Tip: 1 kilowatt-hour can power a TV for about 10 hours!",
        "Speed Trivia: The fastest recorded human speed is 44.72 km/h!",
        "Temperature Insight: The coldest recorded temperature on Earth is -128.6°F (-89.2°C) in Antarctica!"
    ]
    return random.choice(insights)

# ✅ Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .main {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #ff6600;
            text-align: center;
        }
        p {
            text-align: center;
        }
        .stButton>button {
            background-color: #ff6600;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 18px;
        }
        .stButton>button:hover {
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Streamlit UI
st.title("🚀 AI-Powered Instant Unit Converter – Quick & Accurate!")
st.markdown("Convert units instantly and discover fun facts! 🔄")

category = st.selectbox("📏 Category", ["Length", "Weight", "Temperature", "Speed", "Area", "Data Transfer Rate", "Digital Storage", "Energy", "Frequency", "Fuel Economy", "Plane Angle", "Pressure", "Time", "Volume"])
unit_options = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot"],
    "Area": ["square meter", "square kilometer", "square mile", "square foot", "square inch"],
    "Data Transfer Rate": ["bit/second", "kilobit/second", "megabit/second", "gigabit/second", "terabit/second"],
    "Digital Storage": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
    "Energy": ["joule", "kilojoule", "calorie", "kilocalorie", "watt hour"],
    "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
    "Fuel Economy": ["kilometer/liter", "mile/gallon"],
    "Plane Angle": ["degree", "radian"],
    "Pressure": ["pascal", "bar", "psi"],
    "Time": ["second", "minute", "hour", "day", "week", "month", "year"],
    "Volume": ["liter", "milliliter", "cubic meter", "cubic inch", "gallon"]
}

value = st.number_input("🔢 Enter Value", min_value=0.0, format="%.4f")
col1, col2 = st.columns(2)

with col1:
    from_unit = st.selectbox("📍 From Unit", unit_options[category])

with col2:
    to_unit = st.selectbox("🎯 To Unit", unit_options[category])


if st.button("🔄 Convert Now", use_container_width=True):
    
    if category == "Temperature":
        conversions = {
            ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("celsius", "kelvin"): lambda x: x + 273.15,
            ("kelvin", "celsius"): lambda x: x - 273.15,
            ("fahrenheit", "kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
            ("kelvin", "fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32
        }
        result = conversions.get((from_unit, to_unit), lambda x: x)(value)
    else:
        result, unit = convert_units(value, from_unit, to_unit)
        
    with st.spinner("Converting... Please wait! ⏳"): 
      time.sleep(2.5)  # Simulate processing delay
  
    if result is not None:
        formatted_result = f"{result:.8f}".rstrip("0").rstrip(".")
        st.success(f"🎉 Converted Value: {formatted_result} {to_unit}")
        log_conversion(value, from_unit, to_unit, result)
        st.info(f"💡 AI Insight: {ai_suggestions()} ")
    else:
        st.error("❌ Invalid Conversion!")

if st.sidebar.button("📜 Conversion History", use_container_width=True):
    history_df = load_conversion_history()
    if not history_df.empty:
        with st.expander("🔍 View Conversion History"):
            st.dataframe(history_df, height=300)
            st.download_button("📥 Download History", history_df.to_csv(index=False), "conversion_history.csv")
    else:
        st.sidebar.error("⚠️ No history found!")

if st.sidebar.button("🗑️ Clear History", use_container_width=True):
    open("conversion_log.txt", "w").close()
    st.sidebar.success("✅ History cleared!")

st.markdown("---")
st.markdown("Created with ❤️ by Urooj Sadiq - [Connect on LinkedIn](https://www.linkedin.com/in/urooj-sadiq-a91031212/)")
