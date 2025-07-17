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
# Ensure these keys match the 'short' team names in your data (e.g., 'MI', 'CSK').
team_colors = {
    'MI': '#004B8D',  # Mumbai Indians (Dark Blue)
    'CSK': '#FCCA03', # Chennai Super Kings (Yellow)
    'RCB': '#652528', # Royal Challengers Bangalore (Red/Black)
    'KKR': '#30135B', # Kolkata Knight Riders (Purple)
    'SRH': '#FF8220', # Sunrisers Hyderabad (Orange)
    'DC': '#00008B',  # Delhi Capitals (Dark Blue)
    'KXIP': '#BB172B',# Kings XI Punjab (Red)
    'PBKS': '#BB172B',# Punjab Kings (Red) - assuming same color after name change
    'RR': '#2D4B7D',  # Rajasthan Royals (Royal Blue)
    'GT': '#1C294F',  # Gujarat Titans (Navy Blue)
    'LSG': '#046A38', # Lucknow Super Giants (Green)
    'DEC': '#4C287F', # Deccan Chargers (Purple) - old team
    'PW': '#543F57',  # Pune Warriors (Greyish Purple) - old team
    'RPS': '#C71F42', # Rising Pune Supergiant(s) (Red) - old team
    'KTK': '#DA552F', # Kochi Tuskers Kerala (Orange) - old team
    # Add more teams as necessary to match your dataset
}
default_team_color = '#F0F2F6' # A neutral, light grey for teams not in the map

# Helper function for coloring dataframe cells based on team
def highlight_team_background(val):
    """
    Applies background color to a single cell value based on team name.
    """
    if pd.isna(val): # Handle NaN values which might appear if player not found in a match
        return ''
    color = team_colors.get(val, default_team_color)
    # Adjust text color for readability against light backgrounds (like yellow or very light grey)
    text_color = 'white' if color not in ["#FCCA03", "#F0F2F6"] else "black"
    return f'background-color: {color}; color: {text_color};'



# team_map = {'Mumbai Indians': 'MI', 'Chennai Super Kings': 'CSK', ...} # Define your actual team map here if it's not already


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
# Apply team mapping to relevant columns for consistent short names in df_delivery
df_delivery['batting_team_short'] = df_delivery['batting_team'].apply(lambda x: team_map.get(x, x))
df_delivery['bowling_team_short'] = df_delivery['bowling_team'].apply(lambda x: team_map.get(x, x))
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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🏡 Dashboard Overview",
    "📈 Match Trends & Insights",
    "🏆 Team Season Performance",
    "🏏 Batting Giants",
    "💥 Bowling Maestros",
    "🏅 Individual Player Stats",
    "⚔️ Player Matchups",
    "🆚 Player vs Player Analysis"
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

with tab6: # Individual Player Stats
    st.header("🌟 Individual Player Statistics")
    st.write("Dive deep into the performance of your favorite players and analyze their core strengths!")

    # Combine all unique batters, bowlers, non-strikers, and fielders for the player selection dropdown
    # Ensure to drop NaNs from each series before concatenating and sorting
    all_players = sorted(pd.concat([
        df_delivery_filtered['batter'].dropna(),
        df_delivery_filtered['bowler'].dropna(),
        df_delivery_filtered['non_striker'].dropna(),
        df_delivery_filtered['fielder'].dropna()
    ]).unique())

    # Set a default player if available, otherwise pick the first one
    default_player_index = 0
    if 'V Kohli' in all_players:
        default_player_index = all_players.index('V Kohli')
    elif all_players:
        default_player_index = 0
    else:
        default_player_index = None # No players available

    selected_player = st.selectbox("Select a Player", all_players, index=default_player_index)

    if selected_player:
        st.subheader(f"Detailed Stats for {selected_player}")

        # Batting Stats
        player_batting_df = df_delivery_filtered[df_delivery_filtered['batter'] == selected_player]
        if not player_batting_df.empty:
            total_runs = player_batting_df['batsman_runs'].sum()
            
            # Filter out wide and no-ball deliveries for balls faced using 'extras_type'
            legitimate_balls_faced = player_batting_df[
                ~player_batting_df['extras_type'].isin(['wides', 'noballs'])
            ]
            balls_faced = legitimate_balls_faced.shape[0]

            strike_rate = (total_runs / balls_faced * 100) if balls_faced > 0 else 0
            
            highest_score = player_batting_df.groupby('match_id')['batsman_runs'].sum().max()
            if pd.isna(highest_score): # Handle case where highest_score might be NaN if no runs
                highest_score = 0
            
            fours = player_batting_df[player_batting_df['batsman_runs'] == 4].shape[0]
            sixes = player_batting_df[player_batting_df['batsman_runs'] == 6].shape[0]
            
            # Calculate 1s, 2s, and 3s
            ones = player_batting_df[player_batting_df['batsman_runs'] == 1].shape[0]
            twos = player_batting_df[player_batting_df['batsman_runs'] == 2].shape[0]
            threes = player_batting_df[player_batting_df['batsman_runs'] == 3].shape[0]

            dismissals_df = df_delivery_filtered[df_delivery_filtered['player_dismissed'] == selected_player]
            dismissals = dismissals_df.shape[0]
            
            innings_batted = player_batting_df['match_id'].nunique() # Number of unique matches batted in
            
            # Average calculation: total runs / number of dismissals (if dismissed)
            average = (total_runs / dismissals) if dismissals > 0 else (total_runs if innings_batted > 0 else 0) 

            st.markdown("#### Batting Overview")
            col1, col2, col3, col4, col5 = st.columns(5) # Standard metrics row
            col1.metric("Total Runs", total_runs)
            col2.metric("Balls Faced", balls_faced)
            col3.metric("Strike Rate", f"{strike_rate:.2f}")
            col4.metric("Highest Score", highest_score)
            col5.metric("Innings Batted", innings_batted) 
            
            col_b1, col_b2, col_b3, col_b4, col_b5, col_b6, col_b7 = st.columns(7) 
            col_b1.metric("Fours", fours)
            col_b2.metric("Sixes", sixes)
            col_b3.metric("Ones", ones) 
            col_b4.metric("Twos", twos) 
            col_b5.metric("Threes", threes) 
            col_b6.metric("Average", f"{average:.2f}")
            col_b7.metric("Total Dismissals", dismissals)

            st.markdown("---")
            st.markdown("#### Batting Milestones & Efficiency")

            # Half-Centuries, Centuries, Thirties
            player_runs_per_match_batting = player_batting_df.groupby(['match_id', 'inning'])['batsman_runs'].sum().reset_index()
            fifties = (player_runs_per_match_batting['batsman_runs'] >= 50).sum()
            centuries = (player_runs_per_match_batting['batsman_runs'] >= 100).sum()
            thirties = ((player_runs_per_match_batting['batsman_runs'] >= 30) & (player_runs_per_match_batting['batsman_runs'] < 50)).sum()
            
            col_bm1, col_bm2, col_bm3 = st.columns(3)
            col_bm1.metric("Half-Centuries (50s)", fifties)
            col_bm2.metric("Centuries (100s)", centuries)
            col_bm3.metric("Thirties (30-49)", thirties)

            # Boundary Runs & Percentage
            boundary_runs = (fours * 4) + (sixes * 6)
            boundary_percentage = (boundary_runs / total_runs * 100) if total_runs > 0 else 0
            
            # Runs from 1s, 2s, 3s
            runs_from_singles_doubles_triples = (ones * 1) + (twos * 2) + (threes * 3)

            col_br1, col_br2, col_br3 = st.columns(3)
            col_br1.metric("Boundary Runs", boundary_runs)
            col_br2.metric("Boundary % (of Runs)", f"{boundary_percentage:.2f}%")
            col_br3.metric("Runs from 1s, 2s, 3s", runs_from_singles_doubles_triples)

            # Dot Ball Percentage (Batting)
            dot_balls_faced = legitimate_balls_faced[legitimate_balls_faced['batsman_runs'] == 0].shape[0]
            dot_ball_percentage_batting = (dot_balls_faced / balls_faced * 100) if balls_faced > 0 else 0

            # Duck Outs (Revised Logic)
            # Find all innings where the player batted
            player_innings_runs = player_batting_df.groupby(['match_id', 'inning'])['batsman_runs'].sum().reset_index()
            
            # Find all innings where the player was dismissed
            player_dismissed_innings = df_delivery_filtered[
                (df_delivery_filtered['player_dismissed'] == selected_player)
            ][['match_id', 'inning']].drop_duplicates()

            # Merge to find innings where player batted and was dismissed
            dismissed_innings_with_runs = pd.merge(
                player_dismissed_innings,
                player_innings_runs,
                on=['match_id', 'inning'],
                how='inner'
            )
            
            # Count ducks: dismissed for 0 runs in that innings
            duck_outs = dismissed_innings_with_runs[dismissed_innings_with_runs['batsman_runs'] == 0].shape[0]


            col_bd1, col_bd2 = st.columns(2)
            col_bd1.metric("Dot Ball % (faced)", f"{dot_ball_percentage_batting:.2f}%")
            col_bd2.metric("Duck Outs", duck_outs)

            # Batting Dismissal Breakdown
            st.markdown("---")
            st.markdown("#### Batting Dismissal Breakdown")
            if not dismissals_df.empty:
                batsman_dismissal_kind_counts = dismissals_df['dismissal_kind'].value_counts().reset_index()
                batsman_dismissal_kind_counts.columns = ['Dismissal Type', 'Count']
                st.dataframe(batsman_dismissal_kind_counts, use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player} has not been dismissed in the selected season(s).")

        else:
            st.info(f"{selected_player} has no batting records in the selected season(s).")

        # Bowling Stats
        st.markdown("---")
        st.markdown("#### Bowling Overview")
        player_bowling_df = df_delivery_filtered[df_delivery_filtered['bowler'] == selected_player]
        if not player_bowling_df.empty:
            wickets_taken_by_bowler = df_delivery_filtered[
                (df_delivery_filtered['bowler'] == selected_player) &
                (df_delivery_filtered['is_wicket'] == 1) &
                (~df_delivery_filtered['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field']))
            ].shape[0]
            
            runs_conceded = player_bowling_df['total_runs'].sum()
            
            # Filter out wide and no-ball deliveries for legitimate balls bowled
            legitimate_deliveries_bowled = player_bowling_df[
                ~player_bowling_df['extras_type'].isin(['wides', 'noballs'])
            ]
            balls_bowled = legitimate_deliveries_bowled.shape[0]
            
            economy = (runs_conceded / (balls_bowled / 6)) if balls_bowled > 0 else 0 
            
            no_of_innings_bowled = player_bowling_df['match_id'].nunique() 

            # First row of bowling metrics
            col_bowl1, col_bowl2, col_bowl3, col_bowl4, col_bowl5 = st.columns(5)
            col_bowl1.metric("Total Wickets", wickets_taken_by_bowler)
            col_bowl2.metric("Runs Conceded", runs_conceded)
            col_bowl3.metric("Economy", f"{economy:.2f}")
            col_bowl4.metric("Innings Bowled", no_of_innings_bowled)
            col_bowl5.metric("Balls Bowled", balls_bowled) 
            
            st.markdown("#### Bowling Efficiency & Milestones")

            # Bowling Average and Strike Rate
            # Handle division by zero for wickets taken
            bowling_average = (runs_conceded / wickets_taken_by_bowler) if wickets_taken_by_bowler > 0 else (runs_conceded if balls_bowled > 0 else 0)
            bowling_strike_rate = (balls_bowled / wickets_taken_by_bowler) if wickets_taken_by_bowler > 0 else (balls_bowled if balls_bowled > 0 else 0)

            col_be1, col_be2 = st.columns(2)
            col_be1.metric("Bowling Average", f"{bowling_average:.2f}")
            col_be2.metric("Bowling Strike Rate", f"{bowling_strike_rate:.2f}")

            # Dot Ball Percentage (Bowling)
            dot_balls_bowled_count = legitimate_deliveries_bowled[
                legitimate_deliveries_bowled['batsman_runs'] == 0
            ].shape[0]
            dot_ball_percentage_bowling = (dot_balls_bowled_count / balls_bowled * 100) if balls_bowled > 0 else 0

            # Extras Conceded (only wides and no-balls for bowler attribution)
            extras_conceded_bowler = player_bowling_df[
                player_bowling_df['extras_type'].isin(['wides', 'noballs'])
            ]['total_runs'].sum()

            # Boundaries Conceded (Fours & Sixes off bowler's bowling)
            fours_conceded = player_bowling_df[player_bowling_df['batsman_runs'] == 4].shape[0]
            sixes_conceded = player_bowling_df[player_bowling_df['batsman_runs'] == 6].shape[0]
            boundaries_conceded_bowler = (fours_conceded * 4) + (sixes_conceded * 6)

            col_be3, col_be4, col_be5 = st.columns(3)
            col_be3.metric("Dot Ball % (bowled)", f"{dot_ball_percentage_bowling:.2f}%")
            col_be4.metric("Extras Conceded", extras_conceded_bowler)
            col_be5.metric("Boundaries Conceded", boundaries_conceded_bowler)

            # 4-Wicket and 5-Wicket Hauls, BBI
            bowler_wickets_per_match = df_delivery_filtered[
                (df_delivery_filtered['is_wicket'] == 1) &
                (~df_delivery_filtered['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field']))
            ].groupby(['match_id', 'bowler'])['is_wicket'].sum().reset_index()
            
            player_wickets_per_match_df = bowler_wickets_per_match[bowler_wickets_per_match['bowler'] == selected_player]
            four_wicket_hauls = (player_wickets_per_match_df['is_wicket'] >= 4).sum()
            five_wicket_hauls = (player_wickets_per_match_df['is_wicket'] >= 5).sum()
            
            BBI = "N/A"
            if not player_wickets_per_match_df.empty:
                player_runs_conceded_per_match = player_bowling_df.groupby('match_id')['total_runs'].sum().reset_index()
                
                bowler_match_stats = pd.merge(
                    player_wickets_per_match_df,
                    player_runs_conceded_per_match,
                    on='match_id',
                    how='inner'
                )
                
                if not bowler_match_stats.empty:
                    bowler_match_stats_sorted = bowler_match_stats.sort_values(
                        by=['is_wicket', 'total_runs'],
                        ascending=[False, True]
                    )
                    best_bowling_figures_row = bowler_match_stats_sorted.iloc[0]
                    BBI = f"{int(best_bowling_figures_row['is_wicket'])}/{int(best_bowling_figures_row['total_runs'])}"
            
            col_bh1, col_bh2, col_bh3 = st.columns(3)
            col_bh1.metric("4-Wicket Hauls", four_wicket_hauls)
            col_bh2.metric("5-Wicket Hauls", five_wicket_hauls)
            col_bh3.metric("Best Bowling Figures (BBI)", BBI)

            # Existing Wicket Breakdown
            st.markdown("#### Wicket Breakdown (Bowler's Credit)")
            bowling_dismissals_df = df_delivery_filtered[
                (df_delivery_filtered['bowler'] == selected_player) &
                (df_delivery_filtered['is_wicket'] == 1) &
                (~df_delivery_filtered['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field'])) 
            ]

            lbws = bowling_dismissals_df[bowling_dismissals_df['dismissal_kind'] == 'lbw'].shape[0]
            bowled_wickets = bowling_dismissals_df[bowling_dismissals_df['dismissal_kind'] == 'bowled'].shape[0]
            caught_outs = bowling_dismissals_df[bowling_dismissals_df['dismissal_kind'] == 'caught'].shape[0]
            
            col_d1, col_d2, col_d3 = st.columns(3) 
            col_d1.metric("LBWs", lbws)
            col_d2.metric("Bowled", bowled_wickets)
            col_d3.metric("Caught Out", caught_outs)

        else:
            st.info(f"{selected_player} has no bowling records in the selected season(s).")


        # --- GENERAL / OVERALL STATS ---
        st.markdown("---")
        st.markdown("#### Overall Achievements & Fielding")

        # Player of the Match Awards
        player_of_match_awards = df_filtered[df_filtered['player_of_match'] == selected_player].shape[0]
        
        # Matches Played (as batter, bowler, non-striker, or fielder)
        matches_played = df_delivery_filtered[
            (df_delivery_filtered['batter'] == selected_player) |
            (df_delivery_filtered['bowler'] == selected_player) |
            (df_delivery_filtered['non_striker'] == selected_player) | 
            (df_delivery_filtered['fielder'] == selected_player)
        ]['match_id'].nunique()

        # Matches Won (Revised Logic - compatible with older Pandas)
        matches_won = 0
        if matches_played > 0 and not df_filtered.empty:
        # Get all deliveries where the player was involved
        player_deliveries_for_team = df_delivery_filtered[
            (df_delivery_filtered['batter'] == selected_player) |
            (df_delivery_filtered['bowler'] == selected_player) |
            (df_delivery_filtered['non_striker'] == selected_player) |
            (df_delivery_filtered['fielder'] == selected_player)
        ].copy()

        # For each match, find the team the player was on.
        # Use .agg() to get a list of unique teams and then take the first non-null one.
        player_teams_in_matches_raw = player_deliveries_for_team.groupby('match_id').agg(
            batting_team_in_match=('batting_team_short', lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan),
            bowling_team_in_match=('bowling_team_short', lambda x: x.dropna().iloc[0] if not x.dropna().empty else np.nan)
        ).reset_index()

        # Consolidate player's team for each match
        player_teams_in_matches_raw['player_team_in_match'] = player_teams_in_matches_raw.apply(
            lambda row: row['batting_team_in_match'] if pd.notna(row['batting_team_in_match']) else row['bowling_team_in_match'],
            axis=1
        )
                
        # Select only the necessary columns for merging and drop NaNs
        player_teams_in_matches = player_teams_in_matches_raw[['match_id', 'player_team_in_match']].dropna(subset=['player_team_in_match'])

        # Filter out any NaN teams if a player was involved in a match but their team couldn't be determined
        player_teams_in_matches = player_teams_in_matches.dropna(subset=['player_team_in_match'])

        if not player_teams_in_matches.empty:
            # Merge with the filtered matches DataFrame to get the winner of each match
            merged_matches_winners = pd.merge(
                player_teams_in_matches,
                df_filtered[['id', 'winner_short']],
                left_on='match_id',
                right_on='id',
                how='inner'
            )

            # Count matches where the player's team won
            matches_won = merged_matches_winners[
                merged_matches_winners['player_team_in_match'] == merged_matches_winners['winner_short']
            ].shape[0]
            # Most Run Outs (Effected)
            most_run_outs_effected = df_delivery_filtered[
                (df_delivery_filtered['dismissal_kind'] == 'run out') &
                (df_delivery_filtered['fielder'] == selected_player)
            ].shape[0]

            # Most Catches
            most_catches = df_delivery_filtered[
                (df_delivery_filtered['dismissal_kind'] == 'caught') &
                (df_delivery_filtered['fielder'] == selected_player)
            ].shape[0]

            col_g1, col_g2, col_g3 = st.columns(3)
            col_g1.metric("Player of the Match Awards", player_of_match_awards)
            col_g2.metric("Matches Played", matches_played)
            col_g3.metric("Matches Won", matches_won)

            col_g4, col_g5 = st.columns(2)
            col_g4.metric("Run Outs (as Fielder)", most_run_outs_effected)
            col_g5.metric("Catches (as Fielder)", most_catches)
        
with tab7: # NEW TAB: Player Matchups (for Dismissals/Wickets and Runs/SR)
    st.header("⚔️ Player Matchups: Head-to-Head Analysis")
    st.write("Uncover fascinating one-on-one battles! See how your selected player performs against specific opponents, both as a batsman and a bowler.")

    # Combine all unique batters and bowlers for the player selection dropdown
    all_players_matchup = sorted(pd.concat([df_delivery_filtered['batter'], df_delivery_filtered['bowler']]).unique())
    selected_player_matchup = st.selectbox("Select a Player for Matchup Analysis", all_players_matchup, 
                                            index=all_players_matchup.index('V Kohli') if 'V Kohli' in all_players_matchup else (0 if all_players_matchup else None),
                                            key="matchup_player_select") # Added a unique key

    if selected_player_matchup:
        # Define player-specific dataframes for this tab
        player_batting_matchup_df = df_delivery_filtered[df_delivery_filtered['batter'] == selected_player_matchup]
        player_bowling_matchup_df = df_delivery_filtered[df_delivery_filtered['bowler'] == selected_player_matchup]

        # Filter out wide and no-ball deliveries for legitimate balls faced/bowled
        legitimate_balls_faced_matchup = player_batting_matchup_df[
            ~player_batting_matchup_df['extras_type'].isin(['wides', 'noballs'])
        ]
        legitimate_wickets_df_matchup = df_delivery_filtered[
            (df_delivery_filtered['bowler'] == selected_player_matchup) &
            (df_delivery_filtered['is_wicket'] == 1) &
            (~df_delivery_filtered['dismissal_kind'].isin(['run out', 'retired hurt', 'obstructing the field']))
        ]

        # --- As a Batsman: Runs & Strike Rate Against Opponents ---
        if not player_batting_matchup_df.empty:
            st.markdown("#### As a Batsman: Runs & Strike Rate Against Opponents") 
            # Most Runs Against Bowler
            runs_vs_bowler = player_batting_matchup_df.groupby('bowler')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
            st.write(f"Most Runs Scored by {selected_player_matchup} Against Bowlers:")
            st.dataframe(runs_vs_bowler.head(5), use_container_width=True, hide_index=True) # Display top 5

            # Highest Strike Rate Against Bowler (min 10 balls faced)
            sr_vs_bowler_data = legitimate_balls_faced_matchup.groupby('bowler').agg(
                total_runs=('batsman_runs', 'sum'),
                balls_faced=('ball', 'count') 
            ).reset_index()
            
            sr_vs_bowler_data = sr_vs_bowler_data[sr_vs_bowler_data['balls_faced'] >= 10].copy() 
            sr_vs_bowler_data['strike_rate'] = (sr_vs_bowler_data['total_runs'] / sr_vs_bowler_data['balls_faced']) * 100
            sr_vs_bowler_data = sr_vs_bowler_data.sort_values(by='strike_rate', ascending=False).round(2)
            
            if not sr_vs_bowler_data.empty:
                st.write(f"Highest Strike Rate for {selected_player_matchup} Against Bowlers (min 10 balls faced):")
                st.dataframe(sr_vs_bowler_data[['bowler', 'strike_rate', 'total_runs', 'balls_faced']].head(5), use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not faced any bowler for at least 10 balls in the selected season(s) to calculate strike rate.")


            # Most Runs Against Team
            runs_vs_team = player_batting_matchup_df.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
            st.write(f"Most Runs Scored by {selected_player_matchup} Against Teams:")
            # Apply styling to the 'bowling_team' column
            styled_runs_vs_team = runs_vs_team.head(3).style.map(highlight_team_background, subset=['bowling_team'])
            st.dataframe(styled_runs_vs_team, use_container_width=True, hide_index=True) # Display top 3

            # Highest Strike Rate Against Team (min 30 balls faced)
            sr_vs_team_data = legitimate_balls_faced_matchup.groupby('bowling_team').agg(
                total_runs=('batsman_runs', 'sum'),
                balls_faced=('ball', 'count') 
            ).reset_index()

            sr_vs_team_data = sr_vs_team_data[sr_vs_team_data['balls_faced'] >= 30].copy() 
            sr_vs_team_data['strike_rate'] = (sr_vs_team_data['total_runs'] / sr_vs_team_data['balls_faced']) * 100
            sr_vs_team_data = sr_vs_team_data.sort_values(by='strike_rate', ascending=False).round(2)

            if not sr_vs_team_data.empty:
                st.write(f"Highest Strike Rate for {selected_player_matchup} Against Teams (min 30 balls faced):")
                # Apply styling to the 'bowling_team' column
                styled_sr_vs_team = sr_vs_team_data[['bowling_team', 'strike_rate', 'total_runs', 'balls_faced']].head(3).style.map(highlight_team_background, subset=['bowling_team'])
                st.dataframe(styled_sr_vs_team, use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not faced any team for at least 30 balls in the selected season(s) to calculate strike rate.")
        else:
            st.info(f"{selected_player_matchup} has no batting records to analyze against opponents in the selected season(s).")


        # --- Most Dismissals for a Batsman against a Bowler and Team ---
        if not player_batting_matchup_df.empty: # Only proceed if the player has batting records (i.e., can be dismissed)
            st.markdown("#### As a Batsman: Dismissals Analysis")
            
            # Most Dismissals Against Specific Bowlers
            dismissals_by_bowler = df_delivery_filtered[
                (df_delivery_filtered['player_dismissed'] == selected_player_matchup)
            ].groupby('bowler').size().sort_values(ascending=False).reset_index(name='Dismissals')
            
            if not dismissals_by_bowler.empty:
                st.write(f"Most Times {selected_player_matchup} Dismissed By Bowlers:")
                st.dataframe(dismissals_by_bowler.head(5), use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not been dismissed in the selected season(s).")

            # Most Dismissals Against Specific Teams
            dismissals_by_team = df_delivery_filtered[
                (df_delivery_filtered['player_dismissed'] == selected_player_matchup)
            ].groupby('bowling_team').size().sort_values(ascending=False).reset_index(name='Dismissals')

            if not dismissals_by_team.empty:
                st.write(f"Most Times {selected_player_matchup} Dismissed By Teams:")
                # Apply styling to the 'bowling_team' column
                styled_dismissals_by_team = dismissals_by_team.head(3).style.map(highlight_team_background, subset=['bowling_team'])
                st.dataframe(styled_dismissals_by_team, use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not been dismissed by any team in the selected season(s).")
        else:
            st.info(f"{selected_player_matchup} has no batting records to analyze dismissals in the selected season(s).")


        # --- Most Wickets for a Bowler against a Batsman and Team ---
        if not player_bowling_matchup_df.empty: # Only proceed if the player has bowling records
            st.markdown("#### As a Bowler: Wicket-Taking Analysis")
            
            # Most Wickets Against Specific Batsmen
            wickets_vs_batsman = legitimate_wickets_df_matchup.groupby('player_dismissed').size().sort_values(ascending=False).reset_index(name='Wickets')
            
            if not wickets_vs_batsman.empty:
                st.write(f"Most Wickets Taken by {selected_player_matchup} Against Batsmen:")
                st.dataframe(wickets_vs_batsman.head(5), use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not taken any wickets against batsmen in the selected season(s).")

            # Most Wickets Against Specific Teams
            wickets_vs_team = legitimate_wickets_df_matchup.groupby('batting_team').size().sort_values(ascending=False).reset_index(name='Wickets')

            if not wickets_vs_team.empty:
                st.write(f"Most Wickets Taken by {selected_player_matchup} Against Teams:")
                # Apply styling to the 'batting_team' column
                styled_wickets_vs_team = wickets_vs_team.head(3).style.map(highlight_team_background, subset=['batting_team'])
                st.dataframe(styled_wickets_vs_team, use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not taken any wickets against teams in the selected season(s).")
                
            # --- Most Runs Conceded by a Bowler against Specific Batsmen ---
            st.markdown("##### Most Runs Conceded Against Batsmen")
            runs_conceded_vs_batsman = player_bowling_matchup_df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
            runs_conceded_vs_batsman.columns = ['Batsman', 'Runs Conceded']

            if not runs_conceded_vs_batsman.empty:
                st.write(f"Most Runs Conceded by {selected_player_matchup} Against Batsmen:")
                st.dataframe(runs_conceded_vs_batsman.head(5), use_container_width=True, hide_index=True)
            else:
                st.info(f"{selected_player_matchup} has not bowled against any batsmen in the selected season(s) to concede runs.")

        else:
            st.info(f"{selected_player_matchup} has no bowling records to analyze wickets in the selected season(s).")

    else:
        st.warning("Please select a player to view matchup statistics.")

with tab8: # NEW TAB: Player vs Player Analysis
    st.header("🆚 Player vs. Player: Head-to-Head Duel")
    st.write("Pick two players to analyze their direct confrontations! Who dominates when these two cross paths on the field?")

    all_players_h2h = sorted(pd.concat([df_delivery_filtered['batter'], df_delivery_filtered['bowler']]).unique())

    col_h2h_1, col_h2h_2 = st.columns(2)
    with col_h2h_1:
        player1 = st.selectbox("Select Player 1:", all_players_h2h, key="player1_h2h", index=all_players_h2h.index('V Kohli') if 'V Kohli' in all_players_h2h else 0)
    with col_h2h_2:
        player2 = st.selectbox("Select Player 2:", all_players_h2h, key="player2_h2h", index=all_players_h2h.index('MS Dhoni') if 'MS Dhoni' in all_players_h2h else (1 if len(all_players_h2h) > 1 else 0))

    if player1 and player2 and player1 != player2:
        st.subheader(f"Head-to-Head: {player1} vs {player2}")

        # --- Deliveries where Player 1 is Batter and Player 2 is Bowler ---
        h2h_p1_bats_p2_bowl = df_delivery_filtered[
            (df_delivery_filtered['batter'] == player1) &
            (df_delivery_filtered['bowler'] == player2)
        ].copy() # Use .copy() to avoid SettingWithCopyWarning

        # --- Deliveries where Player 2 is Batter and Player 1 is Bowler ---
        h2h_p2_bats_p1_bowl = df_delivery_filtered[
            (df_delivery_filtered['batter'] == player2) &
            (df_delivery_filtered['bowler'] == player1)
        ].copy() # Use .copy() to avoid SettingWithCopyWarning

        # Identify common matches where they faced each other
        matches_where_faced_ids = pd.concat([h2h_p1_bats_p2_bowl['match_id'], h2h_p2_bats_p1_bowl['match_id']]).unique()
        total_matches_faced = len(matches_where_faced_ids)

        st.metric("Direct Head-to-Head Encounters (Matches Faced Each Other)", total_matches_faced)
        st.markdown("---")

        if total_matches_faced > 0:
            # --- Player 1 (Batsman) vs Player 2 (Bowler) Stats ---
            st.markdown(f"#### {player1} (Batsman) vs {player2} (Bowler)")
            if not h2h_p1_bats_p2_bowl.empty:
                p1_runs_vs_p2 = h2h_p1_bats_p2_bowl['batsman_runs'].sum()
                p1_balls_faced_vs_p2 = h2h_p1_bats_p2_bowl[~h2h_p1_bats_p2_bowl['extras_type'].isin(['wides', 'noballs'])].shape[0]
                p1_sr_vs_p2 = (p1_runs_vs_p2 / p1_balls_faced_vs_p2 * 100) if p1_balls_faced_vs_p2 > 0 else 0
                p1_dismissals_by_p2 = h2h_p1_bats_p2_bowl[h2h_p1_bats_p2_bowl['player_dismissed'] == player1].shape[0]

                col_p1_b1, col_p1_b2, col_p1_b3, col_p1_b4 = st.columns(4)
                col_p1_b1.metric("Runs Scored", p1_runs_vs_p2)
                col_p1_b2.metric("Balls Faced", p1_balls_faced_vs_p2)
                col_p1_b3.metric("Strike Rate", f"{p1_sr_vs_p2:.2f}")
                col_p1_b4.metric("Dismissals", p1_dismissals_by_p2)

                if p1_dismissals_by_p2 > 0:
                    dismissal_types_p1 = h2h_p1_bats_p2_bowl[h2h_p1_bats_p2_bowl['player_dismissed'] == player1]['dismissal_kind'].value_counts().reset_index()
                    dismissal_types_p1.columns = ['Dismissal Type', 'Count']
                    st.write("Dismissal Types:")
                    st.dataframe(dismissal_types_p1, use_container_width=True, hide_index=True)
                else:
                    st.info(f"{player1} has not been dismissed by {player2} in the selected season(s).")
            else:
                st.info(f"{player1} has not faced {player2} as a bowler in the selected season(s).")

            # --- Player 2 (Batsman) vs Player 1 (Bowler) Stats ---
            st.markdown(f"#### {player2} (Batsman) vs {player1} (Bowler)")
            if not h2h_p2_bats_p1_bowl.empty:
                p2_runs_vs_p1 = h2h_p2_bats_p1_bowl['batsman_runs'].sum()
                p2_balls_faced_vs_p1 = h2h_p2_bats_p1_bowl[~h2h_p2_bats_p1_bowl['extras_type'].isin(['wides', 'noballs'])].shape[0]
                p2_sr_vs_p1 = (p2_runs_vs_p1 / p2_balls_faced_vs_p1 * 100) if p2_balls_faced_vs_p1 > 0 else 0
                p2_dismissals_by_p1 = h2h_p2_bats_p1_bowl[h2h_p2_bats_p1_bowl['player_dismissed'] == player2].shape[0]

                col_p2_b1, col_p2_b2, col_p2_b3, col_p2_b4 = st.columns(4)
                col_p2_b1.metric("Runs Scored", p2_runs_vs_p1)
                col_p2_b2.metric("Balls Faced", p2_balls_faced_vs_p1)
                col_p2_b3.metric("Strike Rate", f"{p2_sr_vs_p1:.2f}")
                col_p2_b4.metric("Dismissals", p2_dismissals_by_p1)

                if p2_dismissals_by_p1 > 0:
                    dismissal_types_p2 = h2h_p2_bats_p1_bowl[h2h_p2_bats_p1_bowl['player_dismissed'] == player2]['dismissal_kind'].value_counts().reset_index()
                    dismissal_types_p2.columns = ['Dismissal Type', 'Count']
                    st.write("Dismissal Types:")
                    st.dataframe(dismissal_types_p2, use_container_width=True, hide_index=True)
                else:
                    st.info(f"{player2} has not been dismissed by {player1} in the selected season(s).")
            else:
                st.info(f"{player2} has not faced {player1} as a bowler in the selected season(s).")
            
            st.markdown("---")

            # --- "Who Won More" (Team Wins in H2H Matches) ---
            st.markdown("#### Head-to-Head Match Outcomes (Team Wins)")
            p1_team_wins_h2h = 0
            p2_team_wins_h2h = 0

            # Get match details for all H2H encounters
            h2h_match_details = df_filtered[df_filtered['id'].isin(matches_where_faced_ids)].copy()

            # Helper function to get a player's team in a specific match
            def get_player_team_in_match(player_name, match_id_val, df_delivery, team_map_dict):
                # Check if player was a batter in this match
                player_batting_data = df_delivery[
                    (df_delivery['match_id'] == match_id_val) & 
                    (df_delivery['batter'] == player_name)
                ]
                if not player_batting_data.empty:
                    team = player_batting_data['batting_team'].iloc[0]
                    return team_map_dict.get(team, team) # Return mapped team name or original if not found

                # Check if player was a bowler in this match
                player_bowling_data = df_delivery[
                    (df_delivery['match_id'] == match_id_val) & 
                    (df_delivery['bowler'] == player_name)
                ]
                if not player_bowling_data.empty:
                    team = player_bowling_data['bowling_team'].iloc[0]
                    return team_map_dict.get(team, team) # Return mapped team name or original if not found
                
                return None # Should ideally not happen if player participated in the H2H match


            for idx, match_row in h2h_match_details.iterrows():
                match_id = match_row['id']
                winner_short = match_row['winner_short']

                # Determine which team Player 1 was on for this match using the helper function
                player1_team_in_match = get_player_team_in_match(player1, match_id, df_delivery_filtered, team_map)
                
                # Determine which team Player 2 was on for this match using the helper function
                player2_team_in_match = get_player_team_in_match(player2, match_id, df_delivery_filtered, team_map)

                if winner_short == player1_team_in_match and player1_team_in_match is not None:
                    p1_team_wins_h2h += 1
                elif winner_short == player2_team_in_match and player2_team_in_match is not None:
                    p2_team_wins_h2h += 1

            col_win_1, col_win_2, col_win_3 = st.columns(3)
            col_win_1.metric(f"Wins for {player1}'s Team", p1_team_wins_h2h)
            col_win_2.metric(f"Wins for {player2}'s Team", p2_team_wins_h2h)
            
            if p1_team_wins_h2h > p2_team_wins_h2h:
                col_win_3.success(f"{player1}'s team has won more head-to-head matches ({p1_team_wins_h2h} - {p2_team_wins_h2h})!")
            elif p2_team_wins_h2h > p1_team_wins_h2h:
                col_win_3.success(f"{player2}'s team has won more head-to-head matches ({p2_team_wins_h2h} - {p1_team_wins_h2h})!")
            else:
                col_win_3.info("It's a draw in head-to-head matches!")

            st.markdown("---")

            # --- Chronological Match History ---
            st.markdown("#### Chronological Head-to-Head Match History")
            
            h2h_history = df_filtered[df_filtered['id'].isin(matches_where_faced_ids)][['id', 'date', 'team1_short', 'team2_short', 'winner_short']].sort_values('date').copy()
            
            # Add columns for which team each player played for in that specific match
            h2h_history['Player 1 Team'] = None
            h2h_history['Player 2 Team'] = None

            for idx, row in h2h_history.iterrows():
                match_id = row['id']
                
                # Get player1's team in this match using the helper function
                h2h_history.loc[idx, 'Player 1 Team'] = get_player_team_in_match(player1, match_id, df_delivery_filtered, team_map)
                
                # Get player2's team in this match using the helper function
                h2h_history.loc[idx, 'Player 2 Team'] = get_player_team_in_match(player2, match_id, df_delivery_filtered, team_map)

            h2h_history.rename(columns={
                'id': 'Match ID',
                'date': 'Date',
                'team1_short': 'Team 1',
                'team2_short': 'Team 2',
                'winner_short': 'Winning Team',
                'Player 1 Team': f"{player1}'s Team",  # Dynamically rename with player name
                'Player 2 Team': f"{player2}'s Team"   # Dynamically rename with player name
            }, inplace=True)

            # Apply styling to relevant team columns in the match history table
            columns_to_style = [ f"{player1}'s Team", f"{player2}'s Team", 'Winning Team']
            styled_h2h_history = h2h_history[['Date',  f"{player1}'s Team", f"{player2}'s Team", 'Winning Team']].style.map(highlight_team_background, subset=columns_to_style)
            st.dataframe(styled_h2h_history, use_container_width=True, hide_index=True)

        else:
            st.info(f"No direct head-to-head encounters found between {player1} and {player2} in the selected season(s).")
    elif player1 == player2:
        st.warning("Please select two different players for head-to-head analysis.")

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