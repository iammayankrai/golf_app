import streamlit as st
import pandas as pd

def show_leaderboard_page():
    # st.markdown('<div class="main-header">Leaderboard</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style='
        font-size: 36px;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 10px;
    '>
        Leaderboard
    </h1>
    """, unsafe_allow_html=True)
    
    # Leaderboard type selection
    leaderboard_type = st.radio(
        "Select Leaderboard Type:",
        ["Player Rankings", "Team Rankings"],
        horizontal=True
    )
    
    if leaderboard_type == "Player Rankings":
        show_player_leaderboard()
    else:
        show_team_leaderboard()

def show_player_leaderboard():
    st.markdown('<div class="section-header">Player Rankings</div>', unsafe_allow_html=True)
    
    # Sort options
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort By", ["Points", "Handicap", "Matches Played"])
    with col2:
        sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
    
    # Sort data
    sorted_leaderboard = sorted(
        st.session_state.leaderboard,
        key=lambda x: x[sort_by.lower().replace(' ', '_')],
        reverse=(sort_order == "Descending")
    )
    
    # Create display data
    display_data = []
    for i, player in enumerate(sorted_leaderboard, 1):
        display_data.append({
            'Rank': i,
            'Player': player['name'],
            'Handicap': player['handicap'],
            'Points': player['points'],
            'Matches': player.get('matches_played', 0)
        })
    
    # Display as dataframe with styling
    df = pd.DataFrame(display_data)
    df = df.set_index('Rank')
    
    # Apply styling
    def style_leaderboard(row):
        if row.name == 1:  # First place
            return ['background-color: #FFD700; font-weight: bold'] * len(row)
        elif row.name == 2:  # Second place
            return ['background-color: #C0C0C0; font-weight: bold'] * len(row)
        elif row.name == 3:  # Third place
            return ['background-color: #CD7F32; font-weight: bold'] * len(row)
        elif row.name <= 10:  # Top 10
            return ['background-color: #e8f4f8'] * len(row)
        else:
            return [''] * len(row)
    
    styled_df = df.style.apply(style_leaderboard, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    # Current user's position
    user_info = st.session_state.users[st.session_state.current_user]
    user_rank = None
    for i, player in enumerate(sorted_leaderboard, 1):
        if player['name'] == user_info['name']:
            user_rank = i
            break
    
    if user_rank:
        st.markdown("---")
        st.markdown(f"**Your Position:** #{user_rank} out of {len(sorted_leaderboard)} players")
        
        # Progress to next rank
        if user_rank > 1:
            points_to_next = sorted_leaderboard[user_rank-2]['points'] - sorted_leaderboard[user_rank-1]['points'] + 1
            st.info(f"You need {points_to_next} more points to reach rank #{user_rank-1}")

def show_team_leaderboard():
    st.markdown('<div class="section-header">Team Rankings</div>', unsafe_allow_html=True)
    
    # Calculate team points
    teams = {}
    for match in st.session_state.matches:
        if match['status'] == 'Completed' and 'scores' in match:
            for team in match['teams']:
                if team not in teams:
                    teams[team] = {'points': 0, 'matches': 0, 'wins': 0}
                
                teams[team]['matches'] += 1
                # Award points: 3 for win, 1 for tie, 0 for loss
                other_team = [t for t in match['teams'] if t != team][0]
                if match['scores'][team] < match['scores'][other_team]:
                    teams[team]['points'] += 3
                    teams[team]['wins'] += 1
                elif match['scores'][team] == match['scores'][other_team]:
                    teams[team]['points'] += 1
    
    if not teams:
        st.info("No team data available yet. Complete some matches to see team rankings!")
        return
    
    # Create team ranking data
    team_data = []
    for team, stats in teams.items():
        win_rate = (stats['wins'] / stats['matches']) * 100 if stats['matches'] > 0 else 0
        team_data.append({
            'Team': team,
            'Points': stats['points'],
            'Matches': stats['matches'],
            'Wins': stats['wins'],
            'Win Rate': f"{win_rate:.1f}%"
        })
    
    # Sort by points
    team_data.sort(key=lambda x: x['Points'], reverse=True)
    
    # Display team rankings
    for i, team in enumerate(team_data, 1):
        with st.container():
            st.markdown('<div class="match-card">', unsafe_allow_html=True)
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**#{i} {team['Team']}**")
            with col2:
                st.write(f"**{team['Points']}** pts")
            with col3:
                st.write(f"{team['Matches']} matches")
            with col4:
                st.write(f"{team['Wins']} wins")
            with col5:
                st.write(team['Win Rate'])
            
            st.markdown('</div>', unsafe_allow_html=True)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to view the leaderboard.")
else:

    show_leaderboard_page()
