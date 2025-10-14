import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# Initialize session state for user authentication and data
def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'matches' not in st.session_state:
        # Sample match data
        st.session_state.matches = [
            {
                'id': 1,
                'date': datetime.now() + timedelta(days=2),
                'teams': ['Team 1', 'Team 2'],
                'status': 'Upcoming',
                'location': 'Pebble Beach Golf Links',
                'handicap': 16.6,
                'course_par': 72
            },
            {
                'id': 2,
                'date': datetime.now() - timedelta(days=5),
                'teams': ['Team 3', 'Team 4'],
                'status': 'Completed',
                'location': 'St. Andrews Links',
                'handicap': 12.3,
                'course_par': 72,
                'scores': {'Team 3': 72, 'Team 4': 75},
                'weather': 'Sunny',
                'course_condition': 'Excellent'
            },
            {
                'id': 3,
                'date': datetime.now() + timedelta(days=7),
                'teams': ['Team 1', 'Team 5'],
                'status': 'Upcoming',
                'location': 'Augusta National',
                'handicap': 14.2,
                'course_par': 72
            }
        ]
    if 'users' not in st.session_state:
        # Sample user data
        st.session_state.users = {
            'craig@portfreyly.co': {
                'name': 'Craig Roberts',
                'phone': '440-0034-5078',
                'country': 'England',
                'handicap': 16.5,
                'team': 'Team 1',
                'password': 'password'
            },
            'alex@example.com': {
                'name': 'Alex Johnson',
                'phone': '440-1234-5678',
                'country': 'USA',
                'handicap': 12.3,
                'team': 'Team 2',
                'password': 'password'
            }
        }
    if 'leaderboard' not in st.session_state:
        # Sample leaderboard data
        st.session_state.leaderboard = [
            {'name': 'Mayank Rai', 'handicap': 16.5, 'points': 120, 'matches_played': 8},
            {'name': 'Omkar Pol', 'handicap': 12.3, 'points': 115, 'matches_played': 7},
            {'name': 'Nitesh Devadiga', 'handicap': 18.2, 'points': 110, 'matches_played': 6},
            {'name': 'Dinesh Rambade', 'handicap': 14.7, 'points': 105, 'matches_played': 5},
            {'name': 'Mayank Saxena', 'handicap': 15.8, 'points': 95, 'matches_played': 5}
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
            'team': 'Unassigned',
            'password': password
        }
        # Add to leaderboard
        st.session_state.leaderboard.append({
            'name': name,
            'handicap': handicap,
            'points': 0,
            'matches_played': 0
        })
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
                    st.experimental_rerun()
                else:
                    st.error("Invalid email or password")
    
    with col2:
        st.subheader("Sign Up")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            country = st.selectbox("Country", ["India", "United State", "Canada", "Australia", "Other"])
            handicap = st.slider("Handicap", 0.0, 36.0, 18.0)
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
    st.sidebar.markdown(f"**Team:** {user_info['team']}")
    
    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Stats")
    
    user_matches = [m for m in st.session_state.matches 
                   if user_info['team'] in m.get('teams', [])]
    upcoming_count = len([m for m in user_matches if m['status'] == 'Upcoming'])
    completed_count = len([m for m in user_matches if m['status'] == 'Completed'])
    
    st.sidebar.markdown(f"**Upcoming Matches:** {upcoming_count}")
    st.sidebar.markdown(f"**Completed Matches:** {completed_count}")
    
    # Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.experimental_rerun()

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