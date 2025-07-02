-----

# IPL Data Dashboard

A comprehensive and interactive Streamlit application to explore the fascinating world of Indian Premier League (IPL) cricket statistics. Dive deep into match trends, team performances, and discover the top-performing batsmen and bowlers across all seasons.

-----
## Live Demo

Available at https://iplt20-stats.streamlit.app/


## Features

  * **Dynamic Data Overview:** Get instant key metrics like total matches, seasons covered, unique venues, and overall runs and wickets at a glance.
  * **Interactive Season Filtering:** Analyze data for specific IPL seasons or across a range of years using a user-friendly slider in the sidebar.
  * **Match Trends Pivot Table:** Create custom pivot tables to uncover how match outcomes vary based on different criteria like winner, toss winner, and venue across seasons.
  * **Team Performance Visualization:** See how individual teams have performed season by season with an interactive chart showing matches won.
  * **All-Time Top Scorers:** Discover the IPL's leading run-getters with both a detailed table and a compelling bar chart.
  * **All-Time Top Wicket-Takers:** Identify the most successful bowlers in IPL history through a clear table and a striking bar chart.
  * **Engaging UI/UX:** Enjoy a visually appealing blue-themed interface with custom styling, clear headings, tooltips, and insightful text designed for cricket fans.
  * **Team Logos:** Browse and admire all IPL team logos directly from the sidebar.

-----

## Data

This dashboard utilizes two primary datasets:

  * `matches.csv`: Contains information about each IPL match, including date, teams, winner, venue, toss details, and match ID.
  * `deliveries.csv`: Provides ball-by-ball data for all matches, detailing runs scored, wickets taken, bowlers, batsmen, and dismissal types.

-----

## Getting Started

Follow these instructions to set up and run the IPL Data Dashboard locally on your machine.

### Prerequisites

Make sure you have Python 3.7+ installed.

### 1\. Clone the Repository

First, clone the `iplt20-stats` repository to your local machine:

```bash
git clone https://github.com/Eshaan-14/iplt20-stats.git
cd iplt20-stats
```

### 2\. Prepare Your Data

Ensure your `matches.csv` and `deliveries.csv` files are placed directly within the `iplt20-stats` directory (the same directory as `app.py`).

### 3\. Set Up Team Logos

Create a directory named `images` inside your `iplt20-stats` folder, and inside `images`, create another folder named `teams`. Place your IPL team logos (e.g., `RCB.png`, `MI.png`, `CSK.png`, `IPLlogo.jpg`) in the `iplt20-stats/images/teams/` directory.

**Important:** The application expects team logos to be named according to their short forms used in the `team_map` (e.g., `RCB.png`, `PBKS.png`, `SRH.png`, `RPS.png`, `DC.png`, `GT.png`, `LSG.png`, `KKR.png`, `MI.png`, `RR.png`, `CSK.png`, `KTK.png`, `PW.png`). Also, ensure you have an `IPLlogo.jpg` for the main header.

### 4\. Install Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can create one with the following content:

```
streamlit
pandas
altair
```

Then run:

```bash
pip install streamlit pandas altair
```

### 5\. Run the Application

Once all prerequisites are met and data/images are in place, run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

Your browser will automatically open a new tab displaying the IPL Data Dashboard.

-----

## Code Structure

  * `app.py`: The main Streamlit application script containing all the dashboard logic, data loading, preprocessing, and UI/UX elements.
  * `matches.csv`: Dataset containing IPL match details.
  * `deliveries.csv`: Dataset containing ball-by-ball IPL match details.
  * `images/teams/`: Directory to store IPL team logo images.

-----

## Contributing

Feel free to fork this repository, suggest improvements, or contribute to making this dashboard even better\!

-----

## Author

Eshaan-14

-----
