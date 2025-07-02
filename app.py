import streamlit as st
import pandas as pd
import altair as alt

# --- Configuration and Initial Setup ---
# Set page configuration for a wider layout, a title, and a custom icon
st.set_page_config(
    page_title="IPL Data Dashboard by Eshaan - Dive into Cricket Stats!",
    layout="wide",
    initial_sidebar_state="expanded",
    # You can use a custom emoji or an image URL for the icon
    # For a cricket theme, consider 🏏 or 🏆 or the IPL logo URL
    page_icon="🏏"
)

# --- Custom CSS for Blue Theme and Enhanced Typography ---
st.markdown("""
    <style>
    /* Main background and text color */
    .stApp {
        background-color: #F0F2F6; /* Light grey/blueish background for softness */
        color: #333333; /* Darker text for readability */
    }

    /* Header & Title Styling */
    h1 {
        color: #004080; /* Darker blue for main titles */
        text-align: center;
        font-family: 'Arial Black', sans-serif; /* Stronger font */
        margin-bottom: 0.5em;
    }
    h2 {
        color: #0056b3; /* Medium blue for section headers */
        font-family: 'Arial', sans-serif;
        border-bottom: 2px solid #0056b3; /* Underline for emphasis */
        padding-bottom: 5px;
        margin-top: 1.5em;
    }
    h3, h4, h5, h6 {
        color: #0069d9; /* Lighter blue for subheaders */
        font-family: 'Arial', sans-serif;
    }

    /* Sidebar Styling */
    .st-emotion-cache-vk337y { /* Target sidebar background */
        background-color: #ADD8E6; /* Light blue */
        border-right: 1px solid #0056b3;
    }
    .st-emotion-cache-1wivf4j { /* Target sidebar header/text */
        color: #004080; /* Darker blue */
    }
    .st-emotion-cache-1jm69f1 { /* Target sidebar header */
        color: #004080;
    }


    /* Button Styling (if any were added) */
    .stButton>button {
        background-color: #007bff; /* Primary blue */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #E0F2F7; /* Very light blue */
        border-left: 5px solid #007bff; /* Blue border on left */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1); /* Subtle shadow */
    }
    [data-testid="stMetricValue"] {
        color: #004080; /* Dark blue for metric values */
        font-size: 2em; /* Larger font size */
    }
    [data-testid="stMetricLabel"] {
        color: #555555;
        font-size: 0.9em;
    }

    /* Tabs Styling */
    .stTabs [data-testid="stTab"] {
        background-color: #E0F2F7; /* Light blue tab background */
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
        color: #0056b3; /* Blue text for inactive tabs */
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background-color: #007bff; /* Primary blue for active tab */
        color: white; /* White text for active tab */
        border-bottom: 3px solid #007bff; /* Highlight active tab */
    }
    .stTabs [data-testid="stTab"]:hover {
        background-color: #B3E0FF; /* Lighter blue on hover */
    }

    /* Dataframes Styling */
    .st-emotion-cache-jpifc2 { /* Target dataframe cells */
        font-size: 0.9em;
    }

    /* Info/Warning/Error boxes */
    .stAlert {
        border-left: 5px solid;
        border-radius: 5px;
        padding: 10px;
    }
    .stAlert > div > span { /* Target the text inside alerts */
        color: #333333 !important; /* Ensure good contrast */
    }
    </style>
""", unsafe_allow_html=True)


# Team mapping - keep as is
team_map = {
    'Royal Challengers Bangalore': "RCB",
    'Kings XI Punjab': "PBKS",
    'Delhi Daredevils': "DD",
    'Mumbai Indians': "MI",
    'Kolkata Knight Riders': "KKR",
    'Rajasthan Royals': "RR",
    'Deccan Chargers': "SRH", # Note: Deccan Chargers were replaced by SRH. Mapping them to SRH.
    'Chennai Super Kings': "CSK",
    'Kochi Tuskers Kerala': "KTK",
    'Pune Warriors': "PW",
    'Sunrisers Hyderabad': "SRH",
    'Gujarat Lions': "GT", # Note: Gujarat Lions was a team, GT is Gujarat Titans
    'Rising Pune Supergiants': "PW", # Used a distinct code for RPS
    'Rising Pune Supergiant': "PW", # Used a distinct code for RPS
    'Delhi Capitals': "DD", # Used a distinct code for DC
    'Punjab Kings': "PBKS", # Mapping to PBKS
    'Lucknow Super Giants': "LSG",
    'Gujarat Titans': "GT",
    'Royal Challengers Bengaluru': "RCB" # New name for RCB
}


# --- Header Section ---
col1, col2 = st.columns([0.1, 0.9])
with col1:
    # Using a general IPL logo for the header
    st.image("./images/teams/IPLlogo.jpg", width=100) # Ensure you have 'IPLlogo.jpg' in your images/teams folder

with col2:
    st.title("The Ultimate IPL Data Hub!")
    st.markdown("##### Delve into the captivating world of Indian Premier League statistics, powered by Eshaan's Streamlit app.")

st.markdown("---") # Visual separator

# --- Data Loading ---
@st.cache_data # Cache data loading for performance
def load_data(matches_path, deliveries_path):
    try:
        df = pd.read_csv(matches_path)
        df_delivery = pd.read_csv(deliveries_path)
        # Convert date column to datetime objects for potential future use
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df, df_delivery
    except FileNotFoundError:
        st.error("🚨 **Data Files Missing!** Please ensure 'matches.csv' and 'deliveries.csv' are in the correct directory.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ **Data Loading Error:** An unexpected issue occurred while loading data: {e}")
        st.stop()

df, df_delivery = load_data('./matches.csv', './deliveries.csv')

# --- Data Preprocessing (Apply mappings consistently) ---
# Apply team mapping to relevant columns for consistent short names
df['team1_short'] = df['team1'].apply(lambda x: team_map.get(x, x))
df['team2_short'] = df['team2'].apply(lambda x: team_map.get(x, x))
df['winner_short'] = df['winner'].apply(lambda x: team_map.get(x, x))
df['toss_winner_short'] = df['toss_winner'].apply(lambda x: team_map.get(x, x))

# Ensure 'yr' column is created before it's used
df['yr'] = df.date.dt.year.astype(str) # Extract year from datetime object

# --- Sidebar Enhancements ---
with st.sidebar:
    st.header("Explore the IPL Universe! 🌟")
    st.markdown("---") # Separator for sidebar sections

    st.subheader("Teams at a Glance")
    st.write("Click on a team logo to dive into their journey!")

    unique_teams_short = sorted(df['team1_short'].unique().tolist()) # Use the mapped names
    
    # Create columns for the team logos in the sidebar for a cleaner grid
    cols_per_row = 3
    num_rows = (len(unique_teams_short) + cols_per_row - 1) // cols_per_row
    
    for i in range(num_rows):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i * cols_per_row + j
            if idx < len(unique_teams_short):
                team_short = unique_teams_short[idx]
                with cols[j]:
                    try:
                        # Make logo clickable (simple navigation for now, can expand later)
                        if st.image(f"./images/teams/{team_short}.png", width=50, caption=team_short):
                            # This part requires more advanced logic if you want to navigate
                            # to a dedicated team page. For now, it's just a visual cue.
                            pass
                    except FileNotFoundError:
                        st.write(f"Logo for {team_short} not found. 😔")

    st.markdown("---")
    st.subheader("Filter Your View")
    selected_season = st.slider(
        "Select Season Year:",
        min_value=int(df['yr'].min()),
        max_value=int(df['yr'].max()),
        value=(int(df['yr'].min()), int(df['yr'].max()))
    )
    # Filter dataframes based on selected season
    df_filtered = df[(df['yr'].astype(int) >= selected_season[0]) & (df['yr'].astype(int) <= selected_season[1])]
    df_delivery_filtered = df_delivery[df_delivery['match_id'].isin(df_filtered['id'])]


# --- Main Content Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏡 Dashboard Overview",
    "📈 Match Trends & Insights",
    "🏆 Team Season Performance",
    "🌟 Batting Giants",
    "💥 Bowling Maestros"
])

with tab1: # Dashboard Overview
    st.header("📊 IPL At A Glance: Key Statistics Across Seasons")
    st.markdown("Explore the heart of IPL with these overarching numbers!")

    total_matches = df_filtered.shape[0]
    total_seasons = df_filtered['yr'].nunique()
    unique_venues = df_filtered['venue'].nunique()
    total_runs_scored = df_delivery_filtered['total_runs'].sum() # Sum of all runs from deliveries
    total_wickets_taken = df_delivery_filtered[df_delivery_filtered['is_wicket'] == 1].shape[0]

    col_metric1, col_metric2, col_metric3, col_metric4, col_metric5 = st.columns(5) # More columns for more metrics
    with col_metric1:
        st.metric("Matches Analyzed", total_matches, help="Total number of matches in the selected seasons.")
    with col_metric2:
        st.metric("Seasons Covered", total_seasons, help="Number of IPL seasons in the selected range.")
    with col_metric3:
        st.metric("Iconic Venues", unique_venues, help="Total unique stadiums where matches were played.")
    with col_metric4:
        st.metric("Total Runs Scored", f"{total_runs_scored:,}", help="Aggregate runs scored by all teams across all matches.") # Format with comma
    with col_metric5:
        st.metric("Total Wickets Fallen", f"{total_wickets_taken:,}", help="Total wickets fallen including run-outs etc.") # Format with comma


    st.markdown("---")
    st.subheader("Fun Facts & Highlights")
    st.info("💡 **Did you know?** The IPL is renowned for its thrilling finishes and record-breaking performances!")
    st.write(f"The earliest match in this dataset was played on **{df_filtered['date'].min().strftime('%B %d, %Y')}** and the latest on **{df_filtered['date'].max().strftime('%B %d, %Y')}**.")
    st.write(f"A whopping **{total_runs_scored:,} runs** have been scored and **{total_wickets_taken:,} wickets** have fallen across the IPL journey in your selected seasons!")


with tab2: # Match Trends & Insights (Pivot Table)
    st.header("📊 Uncover Match Trends with Pivot Tables")
    st.write("Select different criteria to analyze how match outcomes vary across seasons, venues, and team performances. Perfect for identifying patterns!")

    col_pivot = st.multiselect(
        "Select Column(s) for Pivot Table (e.g., 'winner_short', 'toss_winner_short'):",
        [c for c in df.columns if c not in ['id', 'date', 'team1', 'team2', 'winner', 'toss_winner']], # Exclude raw names
        default=['winner_short']
    )
    row_pivot = st.multiselect(
        "Select Row(s) for Pivot Table (e.g., 'yr', 'venue'):",
        [c for c in df.columns if c not in ['id', 'date', 'team1', 'team2', 'winner', 'toss_winner']],
        default=['yr']
    )

    if not col_pivot or not row_pivot:
        st.warning("⚠️ **Heads Up!** Please select at least one column and one row for the pivot table to generate insights.")
    else:
        try:
            df_piv1 = df_filtered.pivot_table( # Use filtered DataFrame
                index=row_pivot,
                columns=col_pivot,
                aggfunc='count',
                values='id'
            ).fillna(0)
            st.dataframe(df_piv1, use_container_width=True)
            st.markdown(f"*(Counts represent the number of matches for the selected criteria in the selected seasons)*")
        except KeyError as e:
            st.error(f"❌ **Data Error:** Column '{e}' not found in the dataset. Please verify column names.")
        except Exception as e:
            st.error(f"🔥 **An Error Occurred!** Unable to create pivot table. Details: {e}")

with tab3: # Team Season Performance (Altair Chart)
    st.header("📈 Team Triumphs Through the Seasons")
    st.write("Witness the journey of your favorite IPL teams. See their performance trajectory, match wins, and dominance over the years!")

    df_chart = df_filtered.groupby(['yr', 'winner_short']).size().reset_index(name='matches_won')

    # Define a color scheme for teams (you can expand this with more specific team colors if desired)
    # Using a categorical scheme from Altair
    # You could also map specific team short names to hex codes for brand colors
    # color_scale = alt.Scale(domain=unique_teams_short, range=['#004080', '#FFD700', '#FF4500', '#8A2BE2', '#008080', ...])

    chart1 = alt.Chart(df_chart).mark_circle(opacity=0.8, stroke='black', strokeWidth=1).encode( # Added stroke for better visibility
        x=alt.X('winner_short', title='Winning Team', axis=alt.Axis(labels=False)), # Remove labels if too crowded
        y=alt.Y('yr', title='Season', type='ordinal'),
        size=alt.Size('matches_won', title='Matches Won', scale=alt.Scale(rangeMin=100, rangeMax=1000)),
        color=alt.Color('winner_short', title='Team',
                         legend=alt.Legend(title="Team Acronyms")), # Add legend title
        tooltip=[
            alt.Tooltip('yr', title='Season'),
            alt.Tooltip('winner_short', title='Team'),
            alt.Tooltip('matches_won', title='Matches Won')
        ]
    ).properties(
        title='Matches Won by Team per Season'
    ).interactive()

    st.altair_chart(chart1, use_container_width=True)
    st.info("💡 **Tip:** Each circle represents a team's wins in a given season. Larger circles mean more wins!")
    st.markdown("---")
    st.subheader("Legend: Team Acronyms")
    # Display the full team names corresponding to the short forms for clarity
    team_full_names = {v: k for k, v in team_map.items() if v in unique_teams_short}
    team_legend_cols = st.columns(3)
    col_idx = 0
    for short_name in sorted(team_full_names.keys()):
        with team_legend_cols[col_idx % 3]:
            st.markdown(f"**{short_name}**: {team_full_names[short_name]}")
        col_idx += 1


with tab4: # Top Run Scorers
    st.header("🏏 IPL's Batting Maestros: Top Run Scorers")
    st.write("Witness the legends who have dominated the IPL with their willow. These batsmen have consistently piled up runs, etching their names in history!")

    # Ensure to use the filtered delivery data
    top_run_scorers = df_delivery_filtered.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
    top_run_scorers.columns = ['Batter', 'Runs']
    
    st.dataframe(top_run_scorers, use_container_width=True, hide_index=True) # Hide default index for cleaner look

    chart_runs = alt.Chart(top_run_scorers).mark_bar(color='#007bff').encode( # Blue bars
        x=alt.X('Runs', title='Total Runs Scored', axis=alt.Axis(format=',.0f')), # Format runs
        y=alt.Y('Batter', sort='-x', title='Batter'),
        tooltip=['Batter', alt.Tooltip('Runs', format=',.0f')] # Format tooltip runs
    ).properties(
        title='Top 10 IPL Run Scorers'
    ).interactive()
    st.altair_chart(chart_runs, use_container_width=True)

    st.success("🎉 These batters are truly the run-scoring giants of the IPL!")


with tab5: # Top Wicket Takers
    st.header("🔥 IPL's Bowling Dynamos: Top Wicket Takers")
    st.write("Salute the bowlers who have bamboozled batsmen and changed the course of matches with their wicket-taking prowess. Their spells have been legendary!")

    # Ensure to use the filtered delivery data
    wickets_df = df_delivery_filtered[df_delivery_filtered['is_wicket'] == 1]
    wickets_df = wickets_df[~wickets_df['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field'])]
    
    top_wicket_takers = wickets_df.groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(10).reset_index()
    top_wicket_takers.columns = ['Bowler', 'Wickets']
    
    st.dataframe(top_wicket_takers, use_container_width=True, hide_index=True) # Hide default index

    chart_wickets = alt.Chart(top_wicket_takers).mark_bar(color='#FFA500').encode( # Orange for wickets (contrasting with blue)
        x=alt.X('Wickets', title='Total Wickets Taken', axis=alt.Axis(format=',.0f')), # Format wickets
        y=alt.Y('Bowler', sort='-x', title='Bowler'),
        tooltip=['Bowler', alt.Tooltip('Wickets', format=',.0f')] # Format tooltip wickets
    ).properties(
        title='Top 10 IPL Wicket Takers'
    ).interactive()
    st.altair_chart(chart_wickets, use_container_width=True)

    st.success("🎯 These bowlers have consistently delivered crucial breakthroughs!")

    # --- Footer Section ---
st.markdown("""
    <div class="footer" style="
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #D0D0F6; /* Match main background */
        color: #333333; /* Match main text color */
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
        font-weight: bold;
    ">
        Developed with 💙 by <a href="https://github.com/Eshaan-14" target="_blank">Eshaan-14</a> | 
        Repository: <a href="https://github.com/Eshaan-14/iplt20-stats" target="_blank">iplt20-stats</a> | 
        Contact: <a href="mailto:eshaanmane954386@gmail.com">eshaanmane954386@gmail.com</a>
    </div>
""", unsafe_allow_html=True)