SERPAPI_KEY = ""
OPENWEATHER_KEY = ""

import streamlit as st
import pandas as pd
import requests
import sqlite3

# Database setup
conn = sqlite3.connect("plans.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT,
    plan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Helper: Web search for places
# Helper: Web search for actual restaurants
def search_places(query, city):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": f"{query} in {city}",
        "api_key": SERPAPI_KEY,
        "tbm": "lcl"  # Local results (restaurants, shops)
    }

    res = requests.get(url, params=params).json()

    results = []
    # 'local_results' usually contains actual business names
    for r in res.get("local_results", []):
        title = r.get("title")
        if title:
            results.append(title)

    # fallback to organic_results if no local_results
    if not results:
        for r in res.get("organic_results", []):
            if isinstance(r, dict):
                title = r.get("title")
                if title:
                    results.append(title)

    return results[:5]  # return top 5





# Helper: Get current weather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    res = requests.get(url).json()
    if res.get("main"):
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        return f"{temp}°C, {desc}"
    return "Weather info not available"

# Generate dynamic plan
def generate_plan(goal):
    goal_lower = goal.lower()
    days = 1  # default
    if "2-day" in goal_lower:
        days = 2
    elif "3-day" in goal_lower:
        days = 3

    city = goal.split("in")[-1].strip()
    
    plan_text = ""
    breakfast_places = search_places("vegetarian breakfast", city)
    lunch_places = search_places("vegetarian lunch", city)
    dinner_places = search_places("vegetarian dinner", city)

    for day in range(1, days + 1):
        plan_text += f"Day {day}\n"
        plan_text += f"- Breakfast: {breakfast_places[day-1] if len(breakfast_places) >= day else breakfast_places[0]}\n"
        plan_text += f"- Lunch: {lunch_places[day-1] if len(lunch_places) >= day else lunch_places[0]}\n"
        plan_text += f"- Dinner: {dinner_places[day-1] if len(dinner_places) >= day else dinner_places[0]}\n\n"

    # Append weather only for Day 1 (optional)
    plan_text += f"Weather forecast: {get_weather(city)}"

    return plan_text


# Streamlit UI
st.title("AI Agent Task Planner")
goal = st.text_input("Enter your goal:")

if st.button("Generate Plan"):
    if goal:
        plan = generate_plan(goal)
        st.subheader("Generated Plan:")
        st.text(plan)
        # Save plan
        c.execute("INSERT INTO plans (goal, plan) VALUES (?,?)", (goal, plan))
        conn.commit()
        st.success("Plan saved successfully!")

# Show previous plans
st.subheader("Previous Plans")
df = pd.read_sql_query("SELECT goal, plan, created_at FROM plans ORDER BY created_at DESC", conn)
for idx, row in df.iterrows():
    st.markdown(f"**Goal:** {row['goal']}")
    st.text(row['plan'])
    st.caption(f"Created at: {row['created_at']}")
    st.markdown("---")

