import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "match_records.csv"

def load_match_data():
    """Load match data if CSV exists, otherwise create an empty DataFrame."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "User", "User Score", "Opponent", "Opponent Handicap", "Opponent Score",
            "Ground", "Match Type", "Match Date", "Match Time", "Notes"
        ])

def save_match_data(new_record):
    """Append a new record and save to CSV."""
    df = load_match_data()
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def show_match_details_page():
    st.markdown('<div class="main-header">🏌️‍♂️ Add Completed Match Details</div>', unsafe_allow_html=True)
    st.markdown("Use this form to record completed match results, opponents, and notes.")

    # Load existing match data
    existing_data = load_match_data()

    # Example existing opponents (from previous records or default list)
    existing_opponents = sorted(set(existing_data["Opponent"].dropna().tolist() + [
        "Omkar Pol", "Nitesh Devadiga", "Dinesh Rambade", "Mayank Saxena"
    ]))

    # Section 1: Opponent Details
    st.markdown('<div class="section-header">Opponent Details</div>', unsafe_allow_html=True)
    opponent_option = st.radio("Select Option:", ["Choose Existing Opponent", "Add New Opponent"])

    if opponent_option == "Choose Existing Opponent":
        opponent_name = st.selectbox("Select Opponent", existing_opponents)
        opponent_handicap = st.number_input("Opponent Handicap", min_value=0, max_value=54, value=12, key="existing_handicap")
    else:
        opponent_name = st.text_input("Enter Opponent Name")
        opponent_handicap = st.number_input("Enter Opponent Handicap", min_value=0, max_value=54, value=15, key="new_handicap")

    # Section 2: Match Details
    st.markdown('<div class="section-header">Match Details</div>', unsafe_allow_html=True)
    grounds = [
        "Bombay Presidency Golf Club (BPGC)",
        "Willingdon Sports Club",
        "Kharghar Valley Golf Course",
        "Royal Palms Golf & Country Club",
        "9 Aces Golf Greens & Academy",
        "Golden Swan Country Club"
    ]
    selected_ground = st.selectbox("Select Ground", grounds)
    match_type = st.selectbox("Match Type", ["Friendly", "Tournament", "Practice Round", "Club Match"])

    col1, col2 = st.columns(2)
    with col1:
        match_date = st.date_input("Match Date", datetime.now().date())
    with col2:
        match_time = st.time_input("Match Time", datetime.now().time())

    # Scores section
    st.markdown('<div class="section-header">Scores</div>', unsafe_allow_html=True)
    col_user, col_opponent = st.columns(2)
    with col_user:
        user_score = st.number_input("Your Final Score", min_value=0, max_value=200, value=70, key="user_score")
    with col_opponent:
        opponent_score = st.number_input("Opponent Final Score", min_value=0, max_value=200, value=75, key="opponent_score")

    match_notes = st.text_area("Match Notes (optional)", placeholder="Add any notes or remarks about the match...")

    st.markdown('<div class="section-header">Finalize Entry</div>', unsafe_allow_html=True)

    if st.button("✅ Save Match Details", use_container_width=True):
        if not opponent_name:
            st.warning("Please enter opponent name.")
        else:
            user_name = st.session_state.get("username", "Unknown User")
            new_record = {
                "User": user_name,
                "User Score": user_score,
                "Opponent": opponent_name,
                "Opponent Handicap": opponent_handicap,
                "Opponent Score": opponent_score,
                "Ground": selected_ground,
                "Match Type": match_type,
                "Match Date": match_date.strftime("%Y-%m-%d"),
                "Match Time": match_time.strftime("%H:%M"),
                "Notes": match_notes
            }

            save_match_data(new_record)
            st.success(f"🎉 Match details for **{opponent_name}** saved successfully!")
            st.dataframe(pd.DataFrame([new_record]), use_container_width=True)

    # Optional: Show previous match records for current user
    if st.checkbox("📋 Show My Past Matches", value=False):
        user_name = st.session_state.get("username", "Unknown User")
        user_matches = existing_data[existing_data["User"] == user_name]
        if not user_matches.empty:
            st.dataframe(user_matches.sort_values(by="Match Date", ascending=False), use_container_width=True)
        else:
            st.info("No previous matches found.")

# Authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access this page.")
else:
    show_match_details_page()
