import streamlit as st
import pandas as pd
from datetime import datetime

def show_profile_page():
    st.markdown('<div class="main-header">Your Profile</div>', unsafe_allow_html=True)
    
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Personal information form
        st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
        
        with st.form("profile_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                name = st.text_input("Full Name", value=user_info['name'])
                email = st.text_input("Email", value=st.session_state.current_user, disabled=True)
            
            with col_b:
                phone = st.text_input("Phone Number", value=user_info['phone'])
                country = st.selectbox(
                    "Country", 
                    ["United States", "United Kingdom", "Canada", "Australia", "India", "Other"],
                    index=get_country_index(user_info['country'])
                )
            
            handicap = st.slider(
                "Handicap", 
                0.0, 
                36.0, 
                float(user_info['handicap']), 
                0.1,
                help="Your current golf handicap"
            )
            
            # Submit button
            submitted = st.form_submit_button("Update Profile", use_container_width=True)
            
            if submitted:
                # Update user info
                st.session_state.users[st.session_state.current_user].update({
                    'name': name,
                    'phone': phone,
                    'country': country,
                    'handicap': handicap
                })
                
                # Update leaderboard handicap
                update_leaderboard_handicap(name, handicap)
                
                # Save to persistent storage
                from app import save_users
                save_users(st.session_state.users)
                
                st.success("✅ Profile updated successfully!")
        
        # Change password section
        st.markdown('<div class="section-header">Change Password</div>', unsafe_allow_html=True)
        
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            password_submitted = st.form_submit_button("Change Password", use_container_width=True)
            
            if password_submitted:
                if current_password != user_info['password']:
                    st.error("Current password is incorrect")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    st.session_state.users[st.session_state.current_user]['password'] = new_password
                    save_users(st.session_state.users)
                    st.success("✅ Password changed successfully!")
    
    with col2:
        # Player statistics
        st.markdown('<div class="section-header">Player Statistics</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        # Calculate player statistics
        player_stats = calculate_player_statistics(user_info['name'])
        
        st.write(f"**Player:** {user_info['name']}")
        st.write(f"**Member Since:** {get_member_since()}")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Matches Played", player_stats['total_matches'])
            st.metric("Current Handicap", user_info['handicap'])
        with col_stat2:
            st.metric("Wins", player_stats['wins'])
            st.metric("Win Rate", f"{player_stats['win_rate']}%")
        
        # Performance metrics
        st.markdown("**Performance Metrics**")
        st.write(f"• Average Score: {player_stats['avg_score']}")
        st.write(f"• Best Score: {player_stats['best_score']}")
        st.write(f"• Average Putts: {player_stats['avg_putts']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Match history
        st.markdown('<div class="section-header">Recent Matches</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        recent_matches = get_recent_matches(user_info['name'])
        
        if recent_matches:
            for match in recent_matches[:3]:  # Show last 3 matches
                with st.container():
                    # Determine match result
                    user_index = match['players'].index(user_info['name'])
                    user_score = match['scores'][user_index]
                    opponent_index = 1 - user_index
                    opponent_score = match['scores'][opponent_index]
                    
                    if user_score < opponent_score:
                        result = "🏆 Win"
                        result_color = "green"
                    elif user_score == opponent_score:
                        result = "🤝 Tie"
                        result_color = "orange"
                    else:
                        result = "❌ Loss"
                        result_color = "red"
                    
                    st.write(f"**vs {match['players'][opponent_index]}**")
                    st.write(f"Score: {user_score} - {opponent_score}")
                    st.write(f"Result: {result}")
                    st.write(f"Date: {match['date'].strftime('%m/%d/%Y')}")
                    st.markdown("---")
        else:
            st.info("No recent matches played")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick actions
        st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        if st.button("📅 Schedule New Match", use_container_width=True):
            st.switch_page("pages/2_⚔️_Matches.py")
        
        if st.button("📊 View Leaderboard", use_container_width=True):
            st.switch_page("pages/4_🏆_Leaderboard.py")
        
        if st.button("📍 Course GPS", use_container_width=True):
            st.switch_page("pages/6_📍_GPS_Tracking.py")
        
        st.markdown('</div>', unsafe_allow_html=True)

def get_country_index(country):
    """Get the index for the country selectbox"""
    countries = ["United States", "United Kingdom", "Canada", "Australia", "India", "Other"]
    return countries.index(country) if country in countries else 5

def calculate_player_statistics(player_name):
    """Calculate statistics for the player"""
    # Get player's matches
    player_matches = [m for m in st.session_state.matches 
                     if player_name in m.get('players', []) and m['status'] == 'Completed']
    
    total_matches = len(player_matches)
    wins = 0
    scores = []
    total_putts = 0
    putts_count = 0
    
    for match in player_matches:
        if 'scores' in match:
            # Find player's score
            player_index = match['players'].index(player_name)
            player_score = match['scores'][player_index]
            scores.append(player_score)
            
            # Determine win/loss
            opponent_index = 1 - player_index
            opponent_score = match['scores'][opponent_index]
            if player_score < opponent_score:
                wins += 1
            
            # Calculate putts if available
            if 'player_stats' in match and player_name in match['player_stats']:
                total_putts += match['player_stats'][player_name].get('total_putts', 30)
                putts_count += 1
    
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    best_score = min(scores) if scores else 0
    avg_putts = round(total_putts / putts_count, 1) if putts_count > 0 else 30.0
    
    return {
        'total_matches': total_matches,
        'wins': wins,
        'win_rate': round(win_rate, 1),
        'avg_score': avg_score,
        'best_score': best_score,
        'avg_putts': avg_putts
    }

def get_recent_matches(player_name):
    """Get recent matches for the player"""
    player_matches = [m for m in st.session_state.matches 
                     if player_name in m.get('players', []) and m['status'] == 'Completed']
    
    # Sort by date descending and return
    return sorted(player_matches, key=lambda x: x['date'], reverse=True)

def get_member_since():
    """Get member since date (simulated for now)"""
    # In a real app, this would come from user registration date
    return "January 2024"

def update_leaderboard_handicap(player_name, new_handicap):
    """Update player's handicap in the leaderboard"""
    for player in st.session_state.leaderboard:
        if player['name'] == player_name:
            player['handicap'] = new_handicap
            break

def save_users(users):
    """Save users to persistent storage"""
    try:
        import json
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
    except:
        st.error("Error saving user data")

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to view your profile.")
else:
    show_profile_page()
