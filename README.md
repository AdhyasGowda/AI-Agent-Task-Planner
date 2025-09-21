# AI-Agent-Task-Planner
This project implements an AI agent that generates structured, day-by-day plans from natural language goals.
It integrates:
-Web search (SerpAPI) for dynamic context like restaurants.
-Weather API (OpenWeather) for contextual information.
-SQLite database for storing past plans.
-Streamlit web interface for user input and plan display.

## Simple Diagram:
User Input (Goal)
        ↓
  LLM Planner Logic
        ↓
   Web Search API
        ↓
   Weather API
        ↓
Generate Day-by-Day Plan
        ↓
 Save to SQLite DB
        ↓
Display in Streamlit

## Setup / Run Instructions:
1. Clone the repo:
  git clone https://github.com/AdhyasGowda/AI-Agent-Task-Planner.git
  cd AI-Agent-Task-Planner

2. Install dependencies:
   pip install -r requirements.txt

3. Add API keys:
   SERPAPI_KEY = "your_serpapi_key_here"
   OPENWEATHER_KEY = "your_openweather_key_here"

4. Run Streamlit app:
   streamlit run ai_agent_planner.py

## Example Goals & Generated Plans:
Goal 1: “Plan a 2-day vegetarian food tour in Hyderabad”
Generated Plan:
Day 1
- Breakfast: Taaza Kitchen
- Lunch: Ishtaa - Vegetarian Cuisine | Basheerbagh
- Dinner: Parampara - Flavours Of India
Weather forecast: 31.23°C, scattered clouds

Day 2
- Breakfast: Chutneys
- Lunch: Sarvi Restaurant
- Dinner: Paradise (Veg Menu)

## AI Assistance Disclosure:
-Used AI (ChatGPT/GPT-4) for:
-Generating structured day-by-day plan logic.
-Writing Streamlit interface skeleton.

## link
https://drive.google.com/file/d/1Vg5a-Y3Lqwli68jay7xaP0HTlfDc-G9P/view?usp=sharing
