import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# Load Data
# --------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("data/cricbuzz_matches.csv")
    teams = pd.read_csv("data/teams.csv")
    series = pd.read_csv("data/series.csv")
    venues = pd.read_csv("data/venues.csv")
    return matches, teams, series, venues

matches, teams, series, venues = load_data()

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "KPIs & Metrics", "Visualizations", "User Profile"])

# --------------------------
# HOME PAGE
# --------------------------
if page == "Home":
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🏏 Cricbuzz Matches Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **Cricbuzz Cricket Dashboard**!  
    This project analyzes cricket match data, including matches, teams, venues, and series.  
    Explore insights like **Top Teams, Venues, Match Trends, and Performance Metrics**.

    **Features:**
    - 📊 KPIs & Key Metrics
    - 📈 Interactive Visualizations
    - 👤 User Profile
    """)
    st.image("https://upload.wikimedia.org/wikipedia/en/4/4e/Cricket_equipment.jpg", use_container_width=True)

# --------------------------
# KPIs & Metrics
# --------------------------
elif page == "KPIs & Metrics":
    st.markdown("<h1 style='text-align: center; color: #1E90FF;'>📊 Cricbuzz Matches - KPIs & Metrics</h1>", unsafe_allow_html=True)

    total_matches = len(matches)
    total_teams = len(teams)
    total_series = len(series)
    total_venues = len(venues)

    most_played_venue = matches['Venue'].mode()[0] if 'Venue' in matches.columns else "N/A"
    upcoming_matches = matches[matches['Match Category'].str.lower() == 'upcoming'].shape[0]
    live_matches = matches[matches['Match Category'].str.lower() == 'live'].shape[0]
    recent_matches = matches[matches['Match Category'].str.lower() == 'recent'].shape[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", total_matches)
    col2.metric("Total Teams", total_teams)
    col3.metric("Total Series", total_series)
    col4.metric("Total Venues", total_venues)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Most Played Venue", most_played_venue)
    col6.metric("Upcoming Matches", upcoming_matches)
    col7.metric("Live Matches", live_matches)
    col8.metric("Recent Matches", recent_matches)

    st.markdown("### 📋 Quick Match Stats")
    st.dataframe(matches.head(10))

# --------------------------
# VISUALIZATIONS
# --------------------------
elif page == "Visualizations":
    st.markdown("<h1 style='text-align: center; color: #32CD32;'>📈 Visualizations</h1>", unsafe_allow_html=True)

    # First select box: choose visualization
    viz_option = st.selectbox("Select Visualization", [
        "Matches by City",
        "Top 10 Teams by Matches Played",
        "Matches Over Years",
        "Top 10 Venues",
        "Top 10 Series"
    ])

    # Second select box: all options for reference (does NOT filter visualization)
    filter_options = []
    if viz_option == "Matches by City":
        filter_label = "Select City (Reference)"
        filter_options = matches['City'].dropna().unique()
    elif viz_option == "Top 10 Teams by Matches Played":
        filter_label = "Select Team (Reference)"
        filter_options = pd.concat([matches['Team 1'], matches['Team 2']]).unique()
    elif viz_option == "Matches Over Years":
        filter_label = "Select Match Category (Reference)"
        filter_options = matches['Match Category'].dropna().unique()
    elif viz_option == "Top 10 Venues":
        filter_label = "Select Venue (Reference)"
        filter_options = matches['Venue'].dropna().unique()
    elif viz_option == "Top 10 Series":
        filter_label = "Select Series (Reference)"
        filter_options = matches['Series'].dropna().unique()

    selected_filter = st.selectbox(filter_label, options=filter_options)

    # Generate button
    if st.button("Generate"):
        # Visualizations ignore slicer; show full data
        if viz_option == "Matches by City":
            city_counts = matches['City'].value_counts().reset_index()
            city_counts.columns = ['City', 'Matches']
            fig = px.bar(city_counts, x='City', y='Matches', color='Matches', color_continuous_scale='darkmint', title="Matches by City")
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
            st.plotly_chart(fig, use_container_width=True)

        elif viz_option == "Top 10 Teams by Matches Played":
            team_counts = pd.concat([matches['Team 1'], matches['Team 2']]).value_counts().reset_index()
            team_counts.columns = ['Team', 'Matches Played']
            fig = px.bar(team_counts.head(10), x='Team', y='Matches Played', color='Matches Played', color_continuous_scale='darkmint', title="Top 10 Teams by Matches Played")
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
            st.plotly_chart(fig, use_container_width=True)

        elif viz_option == "Matches Over Years":
            matches['Start Date'] = pd.to_datetime(matches['Start Date'], unit='ms', errors='coerce')
            over_years = matches.groupby(matches['Start Date'].dt.year).size().reset_index(name='Matches')
            fig = px.line(over_years, x='Start Date', y='Matches', markers=True, title="Matches Over Years")
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
            st.plotly_chart(fig, use_container_width=True)

        elif viz_option == "Top 10 Venues":
            venue_counts = matches['Venue'].value_counts().reset_index()
            venue_counts.columns = ['Venue', 'Matches']
            fig = px.pie(venue_counts.head(10), names='Venue', values='Matches', hole=0.4, title="Top 10 Venues", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
            st.plotly_chart(fig, use_container_width=True)

        elif viz_option == "Top 10 Series":
            series_counts = matches['Series'].value_counts().reset_index()
            series_counts.columns = ['Series', 'Matches']
            fig = px.pie(series_counts.head(10), names='Series', values='Matches', hole=0.4, title="Top 10 Series", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')
            st.plotly_chart(fig, use_container_width=True)

# --------------------------
# USER PROFILE
# --------------------------
elif page == "User Profile":
    st.markdown("<h1 style='text-align: center; color: #FFA500;'>👤 User Profile</h1>", unsafe_allow_html=True)
    st.markdown("""
    **Name:** Nithish Rexson  
    **Role:** Data Analyst  
    **Skills:** Python, Pandas, MySQL, Power BI, Excel  
    **Projects:**  
    - IPL Win Prediction  
    - Flight Delay Analysis  
    - Bird Species Distribution  
    - Food Waste Management System  

    **About Me:**  
    Passionate about data analytics, visualization, and building solutions that create impact.
    """)
