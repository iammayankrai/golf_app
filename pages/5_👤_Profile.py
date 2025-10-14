import streamlit as st

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
                    ["United States", "United Kingdom", "Canada", "Australia", "Other"],
                    index=["United States", "United Kingdom", "Canada", "Australia", "Other"].index(user_info['country'])
                    if user_info['country'] in ["United States", "United Kingdom", "Canada", "Australia", "Other"]
                    else 4
                )
            
            handicap = st.slider("Handicap", 0.0, 36.0, float(user_info['handicap']), 0.1)
            
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
                else:
                    st.session_state.users[st.session_state.current_user]['password'] = new_password
                    st.success("✅ Password changed successfully!")
    
    with col2:
        # Team information
        st.markdown('<div class="section-header">Team Information</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        st.write(f"**Current Team:** {user_info['team']}")
        st.write(f"**Role:** Captain" if user_info['team'] == 'Team 1' else "**Role:** Player")
        
        # Team statistics
        team_matches = [m for m in st.session_state.matches if user_info['team'] in m['teams']]
        team_wins = 0
        for match in team_matches:
            if match['status'] == 'Completed' and 'scores' in match:
                if match['scores'][user_info['team']] < match['scores'][[t for t in match['teams'] if t != user_info['team']][0]]:
                    team_wins += 1
        
        st.write(f"**Team Record:** {team_wins}-{len(team_matches) - team_wins}")
        st.write(f"**Win Rate:** {team_wins/len(team_matches)*100:.1f}%" if team_matches else "**Win Rate:** N/A")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Team members
        st.markdown('<div class="section-header">Team Members</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        # Sample team members data
        team_members = [
            {"name": "Craig Roberts", "handicap": 16.5, "role": "Captain", "status": "Active"},
            {"name": "Alex Johnson", "handicap": 12.3, "role": "Player", "status": "Active"},
            {"name": "Sam Wilson", "handicap": 18.2, "role": "Player", "status": "Active"},
            {"name": "Taylor Smith", "handicap": 14.7, "role": "Reserve", "status": "Inactive"}
        ]
        
        for member in team_members:
            status_icon = "🟢" if member['status'] == 'Active' else "⚪"
            role_icon = "👑" if member['role'] == 'Captain' else "⛳"
            st.write(f"{status_icon} {role_icon} **{member['name']}**")
            st.write(f"   Handicap: {member['handicap']} | {member['role']}")
            st.write("---")
        
        # Invite player button
        if st.button("Invite Player", use_container_width=True):
            st.info("Player invitation feature would be implemented here")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to view your profile.")
else:
    show_profile_page()