import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_home_page():
    st.markdown('<div class="main-header">🏌️ Golf Dashboard</div>', unsafe_allow_html=True)
    
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
        tab1, tab2, tab3, tab4 = st.tabs(["Score Trend", "Handicap History", "Course Performance", "Shot Analysis"])
        
        with tab1:
            # Score trend chart
            fig_score_trend = create_score_trend_chart(analytics_data)
            st.plotly_chart(fig_score_trend, use_container_width=True)
        
        with tab2:
            # Handicap history chart
            fig_handicap = create_handicap_chart(analytics_data)
            st.plotly_chart(fig_handicap, use_container_width=True)
        
        with tab3:
            # Course performance chart
            fig_course = create_course_performance_chart(analytics_data)
            st.plotly_chart(fig_course, use_container_width=True)
        
        with tab4:
            # Shot analysis chart
            fig_shots = create_shot_analysis_chart(analytics_data)
            st.plotly_chart(fig_shots, use_container_width=True)
        
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
        st.markdown("### 🎯 Performance Indicators")
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upcoming matches widget
        st.markdown("### 📅 Upcoming Matches")
        show_upcoming_matches_widget(user_info)

def generate_analytics_data(user_info):
    """Generate comprehensive analytics data for the user"""
    
    # Get user's matches
    user_matches = [m for m in st.session_state.matches 
                   if user_info['team'] in m.get('teams', []) and m['status'] == 'Completed']
    
    # Calculate basic stats
    total_matches = len(user_matches)
    wins = 0
    scores = []
    dates = []
    
    for match in user_matches:
        if 'scores' in match:
            user_score = match['scores'][user_info['team']]
            scores.append(user_score)
            dates.append(match['date'])
            
            # Determine win/loss
            other_team = [t for t in match['teams'] if t != user_info['team']][0]
            if user_score < match['scores'][other_team]:
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
        handicap = max(0, min(36, base_handicap + (6-i-1)*0.5 + variation))
        handicap_history.append({
            'month': month.strftime('%b %Y'),
            'handicap': round(handicap, 1)
        })
    
    # Course performance data
    courses = ['Pebble Beach', 'St. Andrews', 'Augusta National', 'TPC Sawgrass']
    course_performance = []
    for course in courses:
        course_scores = [72 + np.random.normal(0, 3) for _ in range(4)]
        course_performance.append({
            'course': course,
            'avg_score': np.mean(course_scores),
            'best_score': min(course_scores),
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

def create_score_trend_chart(analytics_data):
    """Create a line chart showing score trends"""
    if not analytics_data['recent_scores']:
        # Create sample data if no real data
        dates = ['01/01', '01/15', '02/01', '02/15', '03/01', '03/15']
        scores = [72 + np.random.normal(0, 2) for _ in range(6)]
    else:
        dates = analytics_data['recent_dates']
        scores = analytics_data['recent_scores']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Scores',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8, color='#1f77b4')
    ))
    
    # Add par line
    fig.add_hline(y=72, line_dash="dash", line_color="red", annotation_text="Par")
    
    fig.update_layout(
        title="Score Trend (Last 6 Rounds)",
        xaxis_title="Date",
        yaxis_title="Score",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_handicap_chart(analytics_data):
    """Create a line chart showing handicap progression"""
    handicap_data = analytics_data['handicap_history']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[h['month'] for h in handicap_data],
        y=[h['handicap'] for h in handicap_data],
        mode='lines+markers',
        name='Handicap',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=8, color='#2ca02c'),
        fill='tozeroy',
        fillcolor='rgba(44, 160, 44, 0.1)'
    ))
    
    fig.update_layout(
        title="Handicap Progression (Last 6 Months)",
        xaxis_title="Month",
        yaxis_title="Handicap",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_course_performance_chart(analytics_data):
    """Create a bar chart showing performance by course"""
    course_data = analytics_data['course_performance']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[c['course'] for c in course_data],
        y=[c['avg_score'] for c in course_data],
        name='Average Score',
        marker_color='#ff7f0e',
        text=[f"{c['avg_score']:.1f}" for c in course_data],
        textposition='auto',
    ))
    
    fig.add_hline(y=72, line_dash="dash", line_color="red", annotation_text="Par")
    
    fig.update_layout(
        title="Performance by Course",
        xaxis_title="Course",
        yaxis_title="Average Score",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_shot_analysis_chart(analytics_data):
    """Create a radar chart for shot analysis"""
    clubs = analytics_data['clubs']
    accuracy = analytics_data['shot_accuracy']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=accuracy + [accuracy[0]],  # Close the circle
        theta=clubs + [clubs[0]],    # Close the circle
        fill='toself',
        name='Accuracy %',
        line=dict(color='#9467bd'),
        fillcolor='rgba(148, 103, 189, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Club Accuracy Analysis",
        template="plotly_white",
        height=300,
        showlegend=False
    )
    
    return fig

def show_enhanced_recent_matches(user_info, analytics_data):
    """Show recent matches with enhanced visualization"""
    user_matches = [m for m in st.session_state.matches 
                   if user_info['team'] in m.get('teams', []) and m['status'] == 'Completed']
    
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
                st.write(f"**{match['teams'][0]} vs {match['teams'][1]}**")
            with col2:
                st.write(f"📅 {match['date'].strftime('%m/%d/%Y')}")
            
            # Scores and performance
            if 'scores' in match:
                user_score = match['scores'][user_info['team']]
                other_team = [t for t in match['teams'] if t != user_info['team']][0]
                other_score = match['scores'][other_team]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(f"{user_info['team']}", user_score, 
                             delta=f"{user_score - match.get('course_par', 72):+d} vs Par")
                
                with col2:
                    st.metric(f"{other_team}", other_score,
                             delta=f"{other_score - match.get('course_par', 72):+d} vs Par")
                
                with col3:
                    result = "🏆 Win" if user_score < other_score else "🤝 Tie" if user_score == other_score else "❌ Loss"
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
                       if m['status'] == 'Upcoming' and user_info['team'] in m['teams']]
    
    if not upcoming_matches:
        st.info("No upcoming matches")
        return
    
    for match in upcoming_matches[:2]:  # Show max 2 upcoming matches
        with st.container():
            st.markdown('<div style="background: #f0f8ff; padding: 10px; border-radius: 8px; margin: 5px 0;">', unsafe_allow_html=True)
            
            days_until = (match['date'] - datetime.now()).days
            st.write(f"**{match['teams'][0]} vs {match['teams'][1]}**")
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