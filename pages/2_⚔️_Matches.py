import streamlit as st
from datetime import datetime, timedelta

def show_matches_page():
    st.markdown('<div class="main-header">All Matches</div>', unsafe_allow_html=True)
    
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Create two columns - left for matches list, right for scheduling
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_status = st.selectbox("Filter by Status", ["All", "Upcoming", "Completed"])
        with col2:
            all_teams = list(set([team for match in st.session_state.matches for team in match['teams']]))
            filter_team = st.selectbox("Filter by Team", ["All Teams"] + all_teams)
        with col3:
            st.write("")  # Spacer for layout
        
        # Apply filters
        filtered_matches = st.session_state.matches.copy()
        if filter_status != "All":
            filtered_matches = [m for m in filtered_matches if m['status'] == filter_status]
        if filter_team != "All Teams":
            filtered_matches = [m for m in filtered_matches if filter_team in m['teams']]
        
        # Display matches
        if not filtered_matches:
            st.info("No matches found with the selected filters.")
        else:
            for match in filtered_matches:
                with st.container():
                    st.markdown('<div class="match-card">', unsafe_allow_html=True)
                    
                    # Header with match ID and status
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        status_color = "🟢" if match['status'] == 'Upcoming' else "🔵"
                        st.markdown(f'<div class="subsection-header">Match #{match["id"]} {status_color} {match["status"]}</div>', unsafe_allow_html=True)
                    with col2:
                        st.write(f"**Date:** {match['date'].strftime('%B %d, %Y')}")
                    
                    # Match details
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Teams**")
                        for team in match['teams']:
                            team_style = "🟦" if team == user_info['team'] else "⬜"
                            st.markdown(f'<div class="team-info">{team_style} {team}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.write("**Match Info**")
                        st.write(f"📍 {match['location']}")
                        st.write(f"📊 Handicap: {match['handicap']}")
                        if 'course_par' in match:
                            st.write(f"⛳ Course Par: {match['course_par']}")
                        
                        if match['status'] == 'Completed' and 'scores' in match:
                            st.write("**Final Scores**")
                            for team in match['teams']:
                                st.write(f"{team}: {match['scores'][team]}")
                    
                    with col3:
                        st.write("**Actions**")
                        if match['status'] == 'Upcoming':
                            if user_info['team'] in match['teams']:
                                if st.button("Enter Scores", key=f"enter_{match['id']}"):
                                    st.session_state.selected_match = match
                                    st.switch_page("pages/3_📊_Score_Entry.py")
                            
                            if st.button("View Course", key=f"course_{match['id']}"):
                                st.session_state.selected_course = match['location']
                                st.switch_page("pages/6_📍_GPS_Tracking.py")
                        else:
                            if 'scores' in match:
                                winning_team = min(match['teams'], key=lambda x: match['scores'][x])
                                st.success(f"🏆 Winner: {winning_team}")
                            
                            if st.button("View Summary", key=f"summary_{match['id']}"):
                                show_match_summary(match)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Schedule New Match Section
        st.markdown('<div class="section-header">Schedule New Match</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        with st.form("schedule_match_form"):
            st.subheader("Create New Match")
            
            # Fixed list of available opponents (site members)
            available_opponents = ['Omkar Pol', 'Mayank Rai', 'Nitesh Devadiga', 'Dinesh Rambade', 'Mayank Saxena']
            
            # Remove current user from opponents list if they exist
            current_user_name = user_info.get('name', '')
            available_opponents = [opponent for opponent in available_opponents if opponent != current_user_name]
            
            if not available_opponents:
                st.warning("No other players available to schedule a match with.")
            else:
                # Opponent selection
                opponent = st.selectbox(
                    "Select Opponent",
                    options=available_opponents,
                    help="Choose the player you want to play against"
                )
                
                # Date selection
                match_date = st.date_input(
                    "Match Date",
                    min_value=datetime.now().date(),
                    value=datetime.now().date() + timedelta(days=7),
                    help="Select the date for the match"
                )
                
                # Time selection
                match_time = st.time_input(
                    "Match Time",
                    value=datetime.strptime("10:00", "%H:%M").time(),
                    help="Select the time for the match"
                )
                
                # Course selection
                available_courses = [
                    "Pebble Beach Golf Links",
                    "St. Andrews Links", 
                    "Augusta National Golf Club",
                    "TPC Sawgrass",
                    "Bethpage Black Course",
                    "Royal Melbourne Golf Club"
                ]
                
                course = st.selectbox(
                    "Select Course",
                    options=available_courses,
                    help="Choose the golf course for the match"
                )
                
                # Handicap adjustment
                handicap = st.slider(
                    "Match Handicap",
                    min_value=0.0,
                    max_value=36.0,
                    value=user_info['handicap'],
                    step=0.1,
                    help="Set the handicap for this match"
                )
                
                # Match format
                match_format = st.selectbox(
                    "Match Format",
                    options=["Stroke Play", "Match Play", "Stableford", "Scramble"],
                    help="Select the format for this match"
                )
                
                # Additional notes
                notes = st.text_area(
                    "Match Notes (Optional)",
                    placeholder="Any special instructions or notes for the match...",
                    help="Add any additional information about the match"
                )
                
                # Submit button
                submitted = st.form_submit_button("Schedule Match", use_container_width=True)
                
                if submitted:
                    # Create new match
                    new_match = create_new_match(
                        user_info['name'],  # Use user's name instead of team
                        opponent,
                        match_date,
                        match_time,
                        course,
                        handicap,
                        match_format,
                        notes
                    )
                    
                    # Add to session state
                    st.session_state.matches.append(new_match)
                    
                    st.success("🎉 Match scheduled successfully!")
                    st.balloons()
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Stats in Sidebar
        st.markdown("---")
        st.markdown("### 📊 Match Statistics")
        
        user_matches = [m for m in st.session_state.matches if user_info['team'] in m.get('teams', [])]
        upcoming_count = len([m for m in user_matches if m['status'] == 'Upcoming'])
        completed_count = len([m for m in user_matches if m['status'] == 'Completed'])
        
        wins = 0
        for match in user_matches:
            if match['status'] == 'Completed' and 'scores' in match:
                user_score = match['scores'][user_info['team']]
                other_team = [t for t in match['teams'] if t != user_info['team']][0]
                if user_score < match['scores'][other_team]:
                    wins += 1
        
        win_rate = (wins / completed_count * 100) if completed_count > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Upcoming", upcoming_count)
            st.metric("Completed", completed_count)
        with col2:
            st.metric("Wins", wins)
            st.metric("Win Rate", f"{win_rate:.1f}%")

def create_new_match(player1, player2, match_date, match_time, course, handicap, match_format, notes):
    """Create a new match object between two players"""
    # Combine date and time
    match_datetime = datetime.combine(match_date, match_time)
    
    # Generate new match ID
    existing_ids = [m['id'] for m in st.session_state.matches]
    new_id = max(existing_ids) + 1 if existing_ids else 1
    
    return {
        'id': new_id,
        'date': match_datetime,
        'players': [player1, player2],  # Using players instead of teams
        'status': 'Upcoming',
        'location': course,
        'handicap': handicap,
        'format': match_format,
        'course_par': 72,  # Default course par
        'created_by': st.session_state.current_user,
        'created_date': datetime.now(),
        'notes': notes
    }

def show_match_summary(match):
    st.markdown("---")
    st.markdown('<div class="subsection-header">Match Summary</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Match Details**")
        st.write(f"Date: {match['date'].strftime('%B %d, %Y')}")
        st.write(f"Location: {match['location']}")
        st.write(f"Course Par: {match.get('course_par', 'N/A')}")
        st.write(f"Handicap: {match['handicap']}")
        
        if 'weather' in match:
            st.write(f"Weather: {match['weather']}")
        if 'course_condition' in match:
            st.write(f"Course Condition: {match['course_condition']}")
    
    with col2:
        st.write("**Final Results**")
        if 'scores' in match:
            # Handle both old teams structure and new players structure
            if 'teams' in match:
                for team in match['teams']:
                    score = match['scores'][team]
                    par_diff = score - match.get('course_par', 72)
                    par_text = f" ({par_diff:+d})" if par_diff != 0 else " (E)"
                    st.write(f"{team}: {score}{par_text}")
                
                winning_team = min(match['teams'], key=lambda x: match['scores'][x])
                st.success(f"**Winner: {winning_team}**")
            elif 'players' in match:
                for i, player in enumerate(match['players']):
                    score = match['scores'][i]
                    par_diff = score - match.get('course_par', 72)
                    par_text = f" ({par_diff:+d})" if par_diff != 0 else " (E)"
                    st.write(f"{player}: {score}{par_text}")
                
                # Find winner
                min_score = min(match['scores'])
                winning_index = match['scores'].index(min_score)
                winning_player = match['players'][winning_index]
                st.success(f"**Winner: {winning_player}**")

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to view matches.")
else:
    show_matches_page()