import streamlit as st
import pandas as pd
import requests
import io
from bs4 import BeautifulSoup

# Dictionary of available leagues per country
leagues_dict = {
        "England": ["UK1", "UK2", "UK3", "UK4", "UK5", "UK6N", "UK6S", "UK7N"],
        "Germany": ["DE1", "DE2", "DE3", "DE4SW", "DE4W", "DE4N", "DE4NO", "DE4B"],
        "Italy": ["IT1", "IT2", "IT3C", "IT3B", "IT3A"],
        "Spain": ["ES1", "ES2", "ES3G1", "ES3G2", "ES3G3", "ES3G4", "ES3G5"],
        "France": ["FR1", "FR2", "FR3"],
        "Sweden": ["SW1", "SW2", "SW3S", "SW3N"],
        "Netherlands": ["NL1", "NL2", "NL3"],
        "Russia": ["RU1", "RU2"],
        "Portugal": ["PT1", "PT2"],
        "Austria": ["AT1", "AT2", "AT3O", "AT3T", "AT3M", "AT3W", "AT3V"],
        "Denmark": ["DK1", "DK2", "DK3G1", "DK3G2"],
        "Greece": ["GR1", "GR2"],
        "Norway": ["NO1", "NO2", "NO3G1", "NO3G2"],
        "Czech Republic": ["CZ1", "CZ2"],
        "Turkey": ["TU1", "TU2", "TU3B", "TU3K"],
        "Belgium": ["BE1", "BE2"],
        "Scotland": ["SC1", "SC2", "SC3", "SC4"],
        "Switzerland": ["CH1", "CH2"],
        "Finland": ["FI1", "FI2", "FI3A", "FI3B", "FI3C"],
        "Ukraine": ["UA1", "UA2"],
        "Romania": ["RO1", "RO2"],
        "Poland": ["PL1", "PL2", "PL3"],
        "Croatia": ["HR1", "HR2"],
        "Belarus": ["BY1", "BY2"],
        "Israel": ["IL1", "IL2"],
        "Iceland": ["IS1", "IS2", "IS3", "IS4"],
        "Cyprus": ["CY1", "CY2"],
        "Serbia": ["CS1", "CS2"],
        "Bulgaria": ["BG1", "BG2"],
        "Slovakia": ["SK1", "SK2"],
        "Hungary": ["HU1", "HU2"],
        "Kazakhstan": ["KZ1", "KZ2"],
        "Bosnia-Herzegovina": ["BA1"],
        "Slovenia": ["SI1", "SI2"],
        "Azerbaijan": ["AZ1"],
        "Ireland": ["IR1", "IR2"],
        "Latvia": ["LA1", "LA2"],
        "Georgia": ["GE1", "GE2"],
        "Kosovo": ["XK1"],
        "Albania": ["AL1"],
        "Lithuania": ["LT1", "LT2"],
        "North Macedonia": ["MK1"],
        "Armenia": ["AM1"],
        "Estonia": ["EE1", "EE2"],
        "Northern Ireland": ["NI1", "NI2"],
        "Malta": ["MT1"],
        "Luxembourg": ["LU1"],
        "Wales": ["WL1"],
        "Montenegro": ["MN1"],
        "Moldova": ["MD1"],
        "Färöer": ["FA1"],
        "Gibraltar": ["GI1"],
        "Andorra": ["AD1"],
        "San Marino": ["SM1"],
        "Brazil": ["BR1", "BR2", "BR3", "BRC", "BRGA"],
        "Mexico": ["MX1", "MX2"],
        "Argentina": ["AR1", "AR2", "AR3F", "AR5", "AR3", "AR4"],
        "USA": ["US1", "US2", "US3"],
        "Colombia": ["CO1", "CO2"],
        "Ecuador": ["EC1", "EC2"],
        "Paraguay": ["PY1", "PY2"],
        "Chile": ["CL1", "CL2"],
        "Uruguay": ["UY1", "UY2"],
        "Costa-Rica": ["CR1", "CR2"],
        "Bolivia": ["BO1"],
        "Guatemala": ["GT1", "GT2"],
        "Dominican Rep.": ["DO1"],
        "Honduras": ["HN1"],
        "Venezuela": ["VE1"],
        "Peru": ["PE1", "PE2"],
        "Panama": ["PA1"],
        "El-Salvador": ["SV1"],
        "Japan": ["JP1", "JP2", "JP3"],
        "South-Korea": ["KR1", "KR2", "KR3"],
        "China": ["CN1", "CN2", "CN3"],
        "Iran": ["IA1", "IA2"],
        "Australia": ["AU1", "AU2V", "AU2NSW", "AU2Q", "AU2S", "AU2W"],
        "Saudi-Arabia": ["SA1", "SA2"],
        "Thailand": ["TH1", "TH2"],
        "Qatar": ["QA1", "QA2"],
        "United Arab Emirates": ["AE1", "AE2"],
        "Indonesia": ["ID1", "ID2"],
        "Jordan": ["JO1"],
        "Syria": ["SY1"],
        "Uzbekistan": ["UZ1"],
        "Malaysia": ["MY1", "MY2"],
        "Vietnam": ["VN1", "VN2"],
        "Iraq": ["IQ1"],
        "Kuwait": ["KW1"],
        "Bahrain": ["BH1"],
        "Myanmar": ["MM1"],
        "Palestine": ["PS1"],
        "India": ["IN1", "IN2"],
        "New Zealand": ["NZ1"],
        "Hong Kong": ["HK1", "HK2"],
        "Oman": ["OM1"],
        "Taiwan": ["TW1"],
        "Tajikistan": ["TJ1"],
        "Turkmenistan": ["TM1"],
        "Lebanon": ["LB1"],
        "Bangladesh": ["BD1"],
        "Singapore": ["SG1"],
        "Egypt": ["EG1", "EG2"],
        "Algeria": ["DZ1", "DZ2"],
        "Tunisia": ["TN1", "TN2"],
        "Morocco": ["MA1", "MA2"],
        "South-Africa": ["ZA1", "ZA2"],
        "Kenya": ["KE1", "KE2"],
        "Zambia": ["ZM1"],
        "Ghana": ["GH1"],
        "Nigeria": ["NG1"],
        "Uganda": ["UG1"],
        "Burundi": ["BI1"],
        "Rwanda": ["RW1"],
        "Cameroon": ["CM1"],
        "Tanzania": ["TZ1"],
        "Gambia": ["GM1"],
        "Sudan": ["SD1"]
}

def fetch_table(country, league, table_type="home"):
    url = f"https://www.soccer-rating.com/{country}/{league}/{table_type}/"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        html_io = io.StringIO(str(soup))
        tables = pd.read_html(html_io, flavor="lxml")
        # Assumes the desired table is at index 14 as per your earlier snippet
        return tables[14] if tables else None
    except Exception as e:
        return None
def prob_to_odds(prob):
    """Convert a probability to decimal odds (rounded to 2 decimals)."""
    return round(1 / prob, 2) if prob > 0 else None

st.title("⚽ Odds Wizard")

# Sidebar for country and league selection
selected_country = st.sidebar.selectbox("Select Country:", list(leagues_dict.keys()), index=0)
selected_league = st.sidebar.selectbox("Select League:", leagues_dict[selected_country], index=0)

# Initialize session state for matches and ratings if league changes or on first load
if "selected_league" not in st.session_state or st.session_state.selected_league != selected_league:
    st.session_state.matches = [("", "")]  # default one match
    st.session_state.selected_league = selected_league
    st.session_state.home_table = fetch_table(selected_country, selected_league, "home")
    st.session_state.away_table = fetch_table(selected_country, selected_league, "away")
    # Drop unwanted columns if table structure is as expected
    if st.session_state.home_table is not None and st.session_state.home_table.shape[1] >= 4:
        st.session_state.home_table = st.session_state.home_table.drop(st.session_state.home_table.columns[[0, 2, 3]], axis=1)
    if st.session_state.away_table is not None and st.session_state.away_table.shape[1] >= 4:
        st.session_state.away_table = st.session_state.away_table.drop(st.session_state.away_table.columns[[0, 2, 3]], axis=1)

# Button to add a new match
if st.button("➕ Add Match"):
    st.session_state.matches.append(("", ""))

# Display match selections and corresponding ratings
if st.session_state.home_table is not None and st.session_state.away_table is not None:
    st.subheader("Select Matches")
    home_team_list = st.session_state.home_table.iloc[:, 0].tolist()
    away_team_list = st.session_state.away_table.iloc[:, 0].tolist()

    for i, _ in enumerate(st.session_state.matches):
        st.markdown(f"#### Match {i+1}")
        col_home, col_away = st.columns(2)
        with col_home:
            home_team = st.selectbox("Home Team", home_team_list, key=f"home_{i}")
            # Retrieve rating for the selected home team (assumed to be in the second column)
            home_row = st.session_state.home_table[st.session_state.home_table.iloc[:, 0] == home_team]
            if not home_row.empty:
                home_rating = home_row.iloc[0, 1]
                st.write(f"Rating: {home_rating}")
            else:
                home_rating = None
                st.write("Rating: N/A")
        with col_away:
            away_team = st.selectbox("Away Team", away_team_list, key=f"away_{i}")
            # Retrieve rating for the selected away team (assumed to be in the second column)
            away_row = st.session_state.away_table[st.session_state.away_table.iloc[:, 0] == away_team]
            if not away_row.empty:
                away_rating = away_row.iloc[0, 1]
                st.write(f"Rating: {away_rating}")
            else:
                away_rating = None
                st.write("Rating: N/A")
        
        # Only calculate probabilities if ratings are available
        if home_rating is not None and away_rating is not None:
            # Convert ratings to float (if they are not already)
            try:
                home_rating = float(home_rating)
                away_rating = float(away_rating)
            except ValueError:
                st.error("Ratings are not in a numeric format.")
                continue

            home_val = 10**(home_rating / 400)
            away_val = 10**(away_rating / 400)
            home_win_prob = home_val / (home_val + away_val)
            away_win_prob = away_val / (home_val + away_val)
            
            # Determine default draw probability based on home_win_prob
            if 0.01 <= home_win_prob <= 0.10:
                default_draw_prob = 0.14
            elif 0.11 <= home_win_prob <= 0.19:
                default_draw_prob = 0.19
            elif 0.20 <= home_win_prob <= 0.25:
                default_draw_prob = 0.22
            elif 0.26 <= home_win_prob <= 0.35:
                default_draw_prob = 0.26
            elif 0.36 <= home_win_prob <= 0.45:
                default_draw_prob = 0.28
            elif 0.46 <= home_win_prob <= 0.70:
                default_draw_prob = 0.26
            elif 0.71 <= home_win_prob <= 0.75:
                default_draw_prob = 0.22
            elif 0.76 <= home_win_prob <= 0.80:
                default_draw_prob = 0.18
            elif 0.81 <= home_win_prob <= 0.90:
                default_draw_prob = 0.16
            elif 0.91 <= home_win_prob <= 0.95:
                default_draw_prob = 0.14
            elif 0.96 <= home_win_prob <= 0.99:
                default_draw_prob = 0.11
            else:
                default_draw_prob = 0.26  # Default value if no conditions are met
            
            remaining_prob = 1 - default_draw_prob 
            adjusted_home_win = home_win_prob * remaining_prob
            adjusted_away_win = away_win_prob * remaining_prob
            
            # Convert adjusted probabilities to decimal odds
            home_odds = prob_to_odds(adjusted_home_win)
            draw_odds = prob_to_odds(default_draw_prob)
            away_odds = prob_to_odds(adjusted_away_win)
            
            # Create columns for displaying odds in the same row with custom colors
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div style='color: green; font-size: 20px;'>Home: {home_odds:.2f}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='color: orange; font-size: 20px;'>Draw: {draw_odds:.2f}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div style='color: red; font-size: 20px;'>Away: {away_odds:.2f}</div>", unsafe_allow_html=True)
else:
    st.error("Error fetching team ratings. Please try again.")
    