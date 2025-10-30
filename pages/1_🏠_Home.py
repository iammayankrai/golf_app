import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def show_home_page():
    # st.markdown('<div class="main-header">🏌️ Golf Dashboard</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style='
        font-size: 36px;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 10px;
    '>
        🏌️ Golf Dashboard
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p style='font-size:16px; text-align:center; color:#555;'>
            Use this form to record completed match results, opponents, and notes.
        </p>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state.users[st.session_state.current_user]
    
    # Generate enhanced analytics data
    analytics_data = generate_analytics_data(user_info)
    
    # Top metrics row
    st.markdown("### 📊 Performance Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Handicap", 
            f"{user_info['handicap']}",
            f"{analytics_data['handicap_change']:+g}",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Win Rate", 
            f"{analytics_data['win_rate']}%",
            f"{analytics_data['win_rate_change']:+g}%"
        )
    
    with col3:
        st.metric(
            "Avg Score", 
            f"{analytics_data['avg_score']}",
            f"{analytics_data['score_change']:+g}"
        )
    
    with col4:
        st.metric(
            "Leaderboard Rank", 
            f"#{analytics_data['current_rank']}",
            f"{analytics_data['rank_change']:+g}"
        )
    
    # Main content - Two columns
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Performance Charts Section
        st.markdown("### 📈 Performance Analytics")
        
        # Tabbed charts
        tab1, tab2, tab3, tab4 = st.tabs(["Score Trend", "Handicap History", "Course Performance", "Performance Indicators"])
        
        with tab1:
            # Score trend chart using Streamlit
            st.markdown("#### Score Trend (Last 6 Rounds)")
            if analytics_data['recent_scores']:
                score_data = pd.DataFrame({
                    'Date': analytics_data['recent_dates'],
                    'Score': analytics_data['recent_scores']
                })
                score_data = score_data.set_index('Date')
                st.line_chart(score_data)
            else:
                st.info("No score data available yet. Play some matches to see your trends!")
        
        with tab2:
            # Handicap history chart using Streamlit
            st.markdown("#### Handicap Progression (Last 6 Months)")
            handicap_data = pd.DataFrame(analytics_data['handicap_history'])
            handicap_data = handicap_data.set_index('month')
            st.area_chart(handicap_data)
        
        with tab3:
            # Course performance chart using Streamlit
            st.markdown("#### Performance by Course")
            course_data = pd.DataFrame(analytics_data['course_performance'])
            course_data = course_data.set_index('course')
            st.bar_chart(course_data['avg_score'])
        
        with tab4:
            # Performance indicators using Streamlit components
            st.markdown("#### Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Greens in Regulation**")
                st.metric("GIR", f"{analytics_data['gir_percentage']}%")
            
            with col2:
                st.markdown("**Driving Accuracy**")
                st.metric("Fairways", f"{analytics_data['fairway_percentage']}%")
            
            with col3:
                st.markdown("**Scrambling**")
                st.metric("Saves", f"{analytics_data['scrambling_percentage']}%")
            
            with col4:
                st.markdown("**Putts per Round**")
                st.metric("Putts", f"{analytics_data['avg_putts']}")
            
            # Club accuracy as a horizontal bar chart
            st.markdown("#### Club Accuracy")
            club_data = pd.DataFrame({
                'Club': analytics_data['clubs'],
                'Accuracy': analytics_data['shot_accuracy']
            })
            club_data = club_data.set_index('Club')
            st.bar_chart(club_data)
        
        # Recent matches with enhanced visualization
        st.markdown("### 🎯 Recent Matches & Performance")
        show_enhanced_recent_matches(user_info, analytics_data)
    
    with col_right:
        # Quick actions with icons
        st.markdown("### ⚡ Quick Actions")
        quick_action_col1, quick_action_col2 = st.columns(2)
        
        with quick_action_col1:
            if st.button("📝 Enter Scores", use_container_width=True):
                st.switch_page("pages/3_📊_Score_Entry.py")
            if st.button("🏆 Leaderboard", use_container_width=True):
                st.switch_page("pages/4_🏆_Leaderboard.py")
        
        with quick_action_col2:
            if st.button("⚔️ Matches", use_container_width=True):
                st.switch_page("pages/2_⚔️_Matches.py")
            if st.button("📍 GPS Tracking", use_container_width=True):
                st.switch_page("pages/6_📍_GPS_Tracking.py")
        
        # Player stats card
        st.markdown("### 👤 Player Stats")
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Matches Played", analytics_data['total_matches'])
            st.metric("Best Score", analytics_data['best_score'])
        with col_stat2:
            st.metric("Avg Putts", analytics_data['avg_putts'])
            st.metric("Fairways Hit", f"{analytics_data['fairway_percentage']}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Performance indicators
        st.markdown("### 🎯 Skill Progress")
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        # Greens in Regulation
        st.write("**Greens in Regulation:**")
        gir = analytics_data['gir_percentage']
        st.progress(gir/100, text=f"{gir}%")
        
        # Driving Accuracy
        st.write("**Driving Accuracy:**")
        driving_acc = analytics_data['driving_accuracy']
        st.progress(driving_acc/100, text=f"{driving_acc}%")
        
        # Scrambling
        st.write("**Scrambling:**")
        scrambling = analytics_data['scrambling_percentage']
        st.progress(scrambling/100, text=f"{scrambling}%")
        
        # Putting
        st.write("**Putting Efficiency:**")
        putting_eff = max(0, min(100, 100 - (analytics_data['avg_putts'] - 28) * 5))  # Scale to 28-36 putts
        st.progress(putting_eff/100, text=f"{putting_eff}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upcoming matches widget
        st.markdown("### 📅 Upcoming Matches")
        show_upcoming_matches_widget(user_info)

def generate_analytics_data(user_info):
    """Generate comprehensive analytics data for the user"""
    
    # Get user's matches
    user_matches = [m for m in st.session_state.matches 
                   if user_info['name'] in m.get('players', []) and m['status'] == 'Completed']
    
    # Calculate basic stats
    total_matches = len(user_matches)
    wins = 0
    scores = []
    dates = []
    
    for match in user_matches:
        if 'scores' in match:
            # Find user's score
            user_index = match['players'].index(user_info['name'])
            user_score = match['scores'][user_index]
            scores.append(user_score)
            dates.append(match['date'])
            
            # Determine win/loss
            opponent_index = 1 - user_index  # Since there are only 2 players
            opponent_score = match['scores'][opponent_index]
            if user_score < opponent_score:
                wins += 1
    
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
    avg_score = np.mean(scores) if scores else user_info['handicap'] + 72
    
    # Generate historical handicap data (last 6 months)
    months = pd.date_range(end=datetime.now(), periods=6, freq='M')
    handicap_history = []
    base_handicap = user_info['handicap']
    
    for i, month in enumerate(months):
        # Simulate handicap progression
        variation = np.random.uniform(-2, 2)
        handicap = max(0, min(36, base_handicap + (6-i-1)*1 + variation))
        handicap_history.append({
            'month': month.strftime('%b %Y'),
            'handicap': round(handicap, 1)
        })
    
    # Course performance data
    courses = ['Bombay Presidency Golf Club (BPGC)', 'Willingdon Sports Club', 'Kharghar Valley Golf Course', 'Royal Palms Golf & Country Club']
    course_performance = []
    for course in courses:
        course_scores = [72 + np.random.normal(0, 3) for _ in range(4)]
        course_performance.append({
            'course': course,
            'avg_score': round(np.mean(course_scores), 1),
            'best_score': int(min(course_scores)),
            'rounds_played': 4
        })
    
    # Shot analysis data
    clubs = ['Driver', '3-Wood', '5-Iron', '7-Iron', '9-Iron', 'PW', 'SW', 'Putter']
    shot_accuracy = [np.random.randint(60, 95) for _ in clubs]
    
    # Leaderboard position
    current_rank = next((i+1 for i, p in enumerate(st.session_state.leaderboard) 
                        if p['name'] == user_info['name']), len(st.session_state.leaderboard) + 1)
    
    return {
        'total_matches': total_matches,
        'win_rate': round(win_rate, 1),
        'win_rate_change': round(np.random.uniform(-5, 5), 1),
        'avg_score': round(avg_score, 1),
        'score_change': round(np.random.uniform(-2, 2), 1),
        'handicap_change': round(np.random.uniform(-1, 1), 1),
        'current_rank': current_rank,
        'rank_change': np.random.randint(-3, 4),
        'handicap_history': handicap_history,
        'course_performance': course_performance,
        'shot_accuracy': shot_accuracy,
        'clubs': clubs,
        'best_score': min(scores) if scores else 68,
        'avg_putts': round(np.random.uniform(28, 34), 1),
        'fairway_percentage': np.random.randint(55, 85),
        'gir_percentage': np.random.randint(50, 80),
        'driving_accuracy': np.random.randint(60, 90),
        'scrambling_percentage': np.random.randint(40, 70),
        'recent_scores': scores[-6:] if len(scores) >= 6 else scores,
        'recent_dates': [d.strftime('%m/%d') for d in dates[-6:]] if len(dates) >= 6 else [d.strftime('%m/%d') for d in dates]
    }

def show_enhanced_recent_matches(user_info, analytics_data):
    """Show recent matches with enhanced visualization"""
    user_matches = [m for m in st.session_state.matches 
                   if user_info['name'] in m.get('players', []) and m['status'] == 'Completed']
    
    recent_matches = user_matches[-3:]  # Last 3 matches
    
    if not recent_matches:
        st.info("No recent matches to display. Complete some matches to see your performance analytics!")
        return
    
    for match in recent_matches:
        with st.container():
            st.markdown('<div class="match-card">', unsafe_allow_html=True)
            
            # Match header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{match['players'][0]} vs {match['players'][1]}**")
            with col2:
                st.write(f"📅 {match['date'].strftime('%m/%d/%Y')}")
            
            # Scores and performance
            if 'scores' in match:
                user_index = match['players'].index(user_info['name'])
                user_score = match['scores'][user_index]
                opponent_index = 1 - user_index
                opponent_score = match['scores'][opponent_index]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(f"{user_info['name']}", user_score, 
                             delta=f"{user_score - match.get('course_par', 72):+d} vs Par")
                
                with col2:
                    opponent_name = match['players'][opponent_index]
                    st.metric(f"{opponent_name}", opponent_score,
                             delta=f"{opponent_score - match.get('course_par', 72):+d} vs Par")
                
                with col3:
                    result = "🏆 Win" if user_score < opponent_score else "🤝 Tie" if user_score == opponent_score else "❌ Loss"
                    st.metric("Result", result)
            
            # Performance indicators for the match
            if st.checkbox(f"Show match details", key=f"details_{match['id']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Course:**", match.get('location', 'Unknown'))
                    st.write("**Conditions:**", match.get('weather', 'Unknown'))
                
                with col2:
                    st.write("**Course Par:**", match.get('course_par', 72))
                    st.write("**Condition:**", match.get('course_condition', 'Unknown'))
                
                with col3:
                    # Simulated performance stats
                    st.write("**Fairways:**", f"{np.random.randint(60, 90)}%")
                    st.write("**Greens:**", f"{np.random.randint(50, 80)}%")
                    st.write("**Putts:**", np.random.randint(28, 36))
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_upcoming_matches_widget(user_info):
    """Show upcoming matches in a compact widget"""
    upcoming_matches = [m for m in st.session_state.matches 
                       if m['status'] == 'Upcoming' and user_info['name'] in m['players']]
    
    if not upcoming_matches:
        st.info("No upcoming matches")
        return
    
    for match in upcoming_matches[:2]:  # Show max 2 upcoming matches
        with st.container():
            st.markdown('<div style="background: #f0f8ff; padding: 10px; border-radius: 8px; margin: 5px 0;">', unsafe_allow_html=True)
            
            days_until = (match['date'] - datetime.now()).days
            st.write(f"**{match['players'][0]} vs {match['players'][1]}**")
            st.write(f"📍 {match['location']}")
            st.write(f"⏰ {match['date'].strftime('%b %d')} ({days_until} days)")
            
            if st.button("View Details", key=f"upcoming_{match['id']}", use_container_width=True):
                st.session_state.selected_match = match
            
            st.markdown('</div>', unsafe_allow_html=True)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access the dashboard.")
else:
    show_home_page()



