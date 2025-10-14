import streamlit as st
from datetime import datetime

def show_score_entry_page():
    st.markdown('<div class="main-header">Score Entry</div>', unsafe_allow_html=True)
    
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Select match to score
    upcoming_matches = [m for m in st.session_state.matches 
                       if m['status'] == 'Upcoming' and user_info['team'] in m['teams']]
    
    if not upcoming_matches:
        st.info("No upcoming matches available for scoring.")
        return
    
    selected_match = st.selectbox(
        "Select Match to Score",
        options=upcoming_matches,
        format_func=lambda x: f"{x['teams'][0]} vs {x['teams'][1]} - {x['date'].strftime('%m/%d/%Y')}",
        key="score_match_select"
    )
    
    if selected_match:
        st.markdown(f'<div class="section-header">Scoring: {selected_match["teams"][0]} vs {selected_match["teams"][1]}</div>', unsafe_allow_html=True)
        
        # Match information
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Date:** {selected_match['date'].strftime('%B %d, %Y')}")
            st.write(f"**Location:** {selected_match['location']}")
        with col2:
            st.write(f"**Course Par:** {selected_match.get('course_par', 72)}")
            st.write(f"**Handicap:** {selected_match['handicap']}")
        
        st.markdown("---")
        
        # Score entry form
        with st.form("score_entry_form"):
            st.markdown('<div class="subsection-header">Enter Match Scores</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'**{selected_match["teams"][0]}**')
                team1_score = st.number_input(
                    f"Score for {selected_match['teams'][0]}",
                    min_value=50,
                    max_value=150,
                    value=selected_match.get('course_par', 72),
                    key="team1_score"
                )
                
            with col2:
                st.markdown(f'**{selected_match["teams"][1]}**')
                team2_score = st.number_input(
                    f"Score for {selected_match['teams'][1]}",
                    min_value=50,
                    max_value=150,
                    value=selected_match.get('course_par', 72),
                    key="team2_score"
                )
            
            # Additional match details
            st.markdown('<div class="subsection-header">Match Conditions</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                weather = st.selectbox(
                    "Weather Conditions",
                    ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Windy", "Stormy"],
                    key="weather_select"
                )
            
            with col2:
                course_condition = st.selectbox(
                    "Course Condition",
                    ["Excellent", "Good", "Fair", "Poor", "Wet"],
                    key="course_condition_select"
                )
            
            with col3:
                match_duration = st.selectbox(
                    "Match Duration",
                    ["< 3 hours", "3-4 hours", "4-5 hours", "> 5 hours"],
                    key="duration_select"
                )
            
            notes = st.text_area("Additional Notes", placeholder="Enter any additional match notes...")
            
            # Submit button
            submitted = st.form_submit_button("Submit Scores", use_container_width=True)
            
            if submitted:
                # Update match with scores and mark as completed
                for i, match in enumerate(st.session_state.matches):
                    if match['id'] == selected_match['id']:
                        st.session_state.matches[i]['scores'] = {
                            selected_match['teams'][0]: team1_score,
                            selected_match['teams'][1]: team2_score
                        }
                        st.session_state.matches[i]['status'] = 'Completed'
                        st.session_state.matches[i]['weather'] = weather
                        st.session_state.matches[i]['course_condition'] = course_condition
                        st.session_state.matches[i]['duration'] = match_duration
                        st.session_state.matches[i]['notes'] = notes
                        st.session_state.matches[i]['completed_date'] = datetime.now()
                        break
                
                # Update leaderboard points (simplified)
                update_leaderboard(selected_match['teams'][0], team1_score)
                update_leaderboard(selected_match['teams'][1], team2_score)
                
                st.success("✅ Scores submitted successfully!")
                st.balloons()

def update_leaderboard(team_name, score):
    # Simplified leaderboard update - in real app, this would be more complex
    # Award points based on score (lower is better in golf)
    points_earned = max(0, 100 - score)  # Simple points calculation
    
    # Find players in the team and update their points
    for player in st.session_state.leaderboard:
        # This is simplified - in real app, you'd have team-player mapping
        if player['name'].startswith(team_name.split(' ')[0]):  # Simple matching
            player['points'] += points_earned
            player['matches_played'] = player.get('matches_played', 0) + 1

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to enter scores.")
else:
    show_score_entry_page()