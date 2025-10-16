import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Golf Match Manager",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a5c;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2e5a87;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .subsection-header {
        font-size: 1.4rem;
        color: #3e6b9a;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    .match-card {
        background-color: #f5f9ff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #4a7eb9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .team-info {
        background-color: #e8f1fc;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #5d8cc9;
    }
    .sidebar .sidebar-content {
        background-color: #f0f7ff;
    }
    .profile-container {
        background-color: #f5f9ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #d1e0f0;
    }
    .success-box {
        background-color: #e7f7ed;
        border: 1px solid #28a745;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #e7f1ff;
        border: 1px solid #007bff;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence functions
def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)
    except:
        st.error("Error saving user data")

def load_matches():
    """Load matches from JSON file"""
    try:
        if os.path.exists('matches.json'):
            with open('matches.json', 'r') as f:
                matches_data = json.load(f)
                # Convert date strings back to datetime objects
                for match in matches_data:
                    if 'date' in match:
                        match['date'] = datetime.fromisoformat(match['date'])
                    if 'created_date' in match:
                        match['created_date'] = datetime.fromisoformat(match['created_date'])
                    if 'completed_date' in match:
                        match['completed_date'] = datetime.fromisoformat(match['completed_date'])
                return matches_data
    except:
        pass
    return []

def save_matches(matches):
    """Save matches to JSON file"""
    try:
        matches_data = []
        for match in matches:
            match_copy = match.copy()
            # Convert datetime objects to strings for JSON
            if 'date' in match_copy:
                match_copy['date'] = match_copy['date'].isoformat()
            if 'created_date' in match_copy:
                match_copy['created_date'] = match_copy['created_date'].isoformat()
            if 'completed_date' in match_copy:
                match_copy['completed_date'] = match_copy['completed_date'].isoformat()
            matches_data.append(match_copy)
        
        with open('matches.json', 'w') as f:
            json.dump(matches_data, f, indent=2)
    except:
        st.error("Error saving match data")

# Initialize session state for user authentication and data
def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Load persistent data
    if 'users' not in st.session_state:
        st.session_state.users = load_users()
        
        # If no users exist, create sample users
        if not st.session_state.users:
            st.session_state.users = {
                'craig@portfreyly.co': {
                    'name': 'Craig Roberts',
                    'phone': '440-0034-5078',
                    'country': 'England',
                    'handicap': 16,
                    'password': 'password'
                },
                'omkar@example.com': {
                    'name': 'Omkar Pol',
                    'phone': '440-1111-2222',
                    'country': 'India',
                    'handicap': 12,
                    'password': 'password'
                },
                'mayank@example.com': {
                    'name': 'Mayank Rai',
                    'phone': '440-2222-3333',
                    'country': 'India',
                    'handicap': 14,
                    'password': 'password'
                },
                'nitesh@example.com': {
                    'name': 'Nitesh Devadiga',
                    'phone': '440-3333-4444',
                    'country': 'India',
                    'handicap': 18,
                    'password': 'password'
                },
                'dinesh@example.com': {
                    'name': 'Dinesh Rambade',
                    'phone': '440-4444-5555',
                    'country': 'India',
                    'handicap': 15,
                    'password': 'password'
                },
                'mayank_s@example.com': {
                    'name': 'Mayank Saxena',
                    'phone': '440-5555-6666',
                    'country': 'India',
                    'handicap': 13,
                    'password': 'password'
                }
            }
            save_users(st.session_state.users)
    
    if 'matches' not in st.session_state:
        st.session_state.matches = load_matches()
        
        # If no matches exist, create sample matches
        if not st.session_state.matches:
            st.session_state.matches = [
                {
                    'id': 1,
                    'date': datetime.now() + timedelta(days=2),
                    'players': ['Craig Roberts', 'Omkar Pol'],
                    'status': 'Upcoming',
                    'location': 'Bombay Presidency Golf Club',
                    'handicap': 16,
                    'course_par': 72,
                    'format': 'Stroke Play'
                },
                {
                    'id': 2,
                    'date': datetime.now() - timedelta(days=5),
                    'players': ['Mayank Rai', 'Nitesh Devadiga'],
                    'status': 'Completed',
                    'location': 'Juhu Vile Parle Gymkhana Club',
                    'handicap': 12,
                    'course_par': 72,
                    'format': 'Stroke Play',
                    'scores': [72, 75],
                    'weather': 'Sunny',
                    'course_condition': 'Excellent'
                }
            ]
            save_matches(st.session_state.matches)
    
    if 'leaderboard' not in st.session_state:
        # Sample leaderboard data
        st.session_state.leaderboard = [
            {'name': 'Craig Roberts', 'handicap': 16, 'points': 120, 'matches_played': 8},
            {'name': 'Omkar Pol', 'handicap': 12, 'points': 115, 'matches_played': 7},
            {'name': 'Mayank Rai', 'handicap': 14, 'points': 110, 'matches_played': 6},
            {'name': 'Nitesh Devadiga', 'handicap': 18, 'points': 105, 'matches_played': 5},
            {'name': 'Dinesh Rambade', 'handicap': 15, 'points': 95, 'matches_played': 5},
            {'name': 'Mayank Saxena', 'handicap': 13, 'points': 90, 'matches_played': 4}
        ]

# Authentication functions
def authenticate_user(email, password):
    if email in st.session_state.users and st.session_state.users[email]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.current_user = email
        return True
    return False

def register_user(email, name, phone, country, handicap, password):
    if email not in st.session_state.users:
        st.session_state.users[email] = {
            'name': name,
            'phone': phone,
            'country': country,
            'handicap': handicap,
            'password': password
        }
        # Add to leaderboard
        st.session_state.leaderboard.append({
            'name': name,
            'handicap': handicap,
            'points': 0,
            'matches_played': 0
        })
        # Save to persistent storage
        save_users(st.session_state.users)
        return True
    return False

# Login/Registration page
def show_auth_page():
    st.markdown('<div class="main-header">⛳ Golf Match Manager</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Sign In")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_submitted = st.form_submit_button("Sign In")
            
            if login_submitted:
                if authenticate_user(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with col2:
        st.subheader("Sign Up")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            country = st.selectbox("Country", ["United States", "United Kingdom", "Canada", "Australia", "India", "Other"])
            handicap = st.slider("Handicap", 0, 36, 18)
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_submitted = st.form_submit_button("Sign Up")
            
            if register_submitted:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif register_user(email, name, phone, country, handicap, password):
                    st.success("Registration successful! Please sign in.")
                else:
                    st.error("Email already registered")

# Main application layout
def main_app():
    # Sidebar navigation
    st.sidebar.title("⛳ Golf Match Manager")
    
    # User info in sidebar
    user_info = st.session_state.users[st.session_state.current_user]
    st.sidebar.markdown(f"**Welcome, {user_info['name']}**")
    st.sidebar.markdown(f"**Handicap:** {user_info['handicap']}")
    
    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    
    user_matches = [m for m in st.session_state.matches 
                   if user_info['name'] in m.get('players', [])]
    upcoming_count = len([m for m in user_matches if m['status'] == 'Upcoming'])
    completed_count = len([m for m in user_matches if m['status'] == 'Completed'])
    
    st.sidebar.markdown(f"**Upcoming Matches:** {upcoming_count}")
    st.sidebar.markdown(f"**Completed Matches:** {completed_count}")
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

# Main function
def main():
    initialize_session_state()
    
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        main_app()
        # The actual page content will be handled by Streamlit's multi-page architecture

if __name__ == "__main__":
    main()


