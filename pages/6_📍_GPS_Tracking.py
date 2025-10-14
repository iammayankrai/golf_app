import streamlit as st
import pandas as pd
import numpy as np

def show_gps_page():
    st.markdown('<div class="main-header">Course GPS & Tracking</div>', unsafe_allow_html=True)
    
    # Course selection
    courses = [
        "Pebble Beach Golf Links",
        "St. Andrews Links", 
        "Augusta National Golf Club",
        "TPC Sawgrass",
        "Bethpage Black Course",
        "Royal Melbourne Golf Club"
    ]
    
    selected_course = st.selectbox("Select Course", courses)
    
    if selected_course:
        st.markdown(f'<div class="section-header">{selected_course}</div>', unsafe_allow_html=True)
        
        # Course overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Par", "72")
        with col2:
            st.metric("Total Yardage", "6,800 yds")
        with col3:
            st.metric("Course Rating", "74.2")
        
        # Course layout
        st.markdown('<div class="subsection-header">Course Layout</div>', unsafe_allow_html=True)
        
        # Generate sample hole data
        holes_data = generate_hole_data(selected_course)
        holes_df = pd.DataFrame(holes_data)
        
        # Display hole information
        st.dataframe(holes_df, use_container_width=True)
        
        # GPS visualization placeholder
        st.markdown('<div class="subsection-header">Course Map</div>', unsafe_allow_html=True)
        
        # Create a simple course visualization using columns and metrics
        st.info(f"📡 Live GPS tracking for {selected_course}")
        
        # Show first 9 holes
        st.subheader("Front 9")
        front_9 = holes_data[:9]
        
        cols = st.columns(9)
        for i, hole in enumerate(front_9):
            with cols[i]:
                st.metric(f"Hole {hole['Hole']}", f"Par {hole['Par']}")
                st.write(f"{hole['Distance']} yds")
        
        # Distance calculator
        st.markdown('<div class="subsection-header">Distance Calculator</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            from_hole = st.selectbox("From Hole", range(1, 19), key="from_hole")
        
        with col2:
            to_hole = st.selectbox("To Hole", range(1, 19), key="to_hole")
        
        with col3:
            st.write("")  # Spacer
            if st.button("Calculate Distance", use_container_width=True):
                distance = calculate_distance(from_hole, to_hole, holes_data)
                st.success(f"📍 Distance: {distance} yards")
        
        # Current position simulation
        st.markdown('<div class="subsection-header">Current Position</div>', unsafe_allow_html=True)
        
        current_hole = st.slider("Select your current hole", 1, 18, 1)
        current_position = st.selectbox("Position on hole", ["Tee Box", "Fairway", "Green", "Hazard"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Hole Information**")
            current_hole_data = holes_data[current_hole - 1]
            st.write(f"**Hole {current_hole_data['Hole']}**")
            st.write(f"Par: {current_hole_data['Par']}")
            st.write(f"Distance: {current_hole_data['Distance']} yards")
            st.write(f"Handicap: {current_hole_data['Handicap']}")
        
        with col2:
            st.write("**GPS Data**")
            st.write("Latitude: 36.5653° N")
            st.write("Longitude: 121.9500° W")
            st.write("Elevation: 25 ft")
            st.write("Distance to pin: 145 yds")
        
        # Shot tracking
        st.markdown('<div class="subsection-header">Shot Tracking</div>', unsafe_allow_html=True)
        
        with st.form("shot_tracking_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                club_used = st.selectbox("Club Used", [
                    "Driver", "3 Wood", "5 Wood", "3 Iron", "4 Iron", "5 Iron",
                    "6 Iron", "7 Iron", "8 Iron", "9 Iron", "Pitching Wedge",
                    "Sand Wedge", "Lob Wedge", "Putter"
                ])
            
            with col2:
                shot_distance = st.number_input("Shot Distance (yards)", min_value=1, max_value=400, value=150)
            
            with col3:
                shot_result = st.selectbox("Shot Result", [
                    "Fairway", "Green", "Rough", "Bunker", "Water", "Out of Bounds"
                ])
            
            if st.form_submit_button("Track Shot", use_container_width=True):
                st.success(f"✅ Shot tracked: {shot_distance} yards with {club_used}")

def generate_hole_data(course_name):
    # Generate sample hole data based on course
    holes = []
    for i in range(1, 19):
        # Vary par and distance based on hole number
        if i % 4 == 0:  # Par 5 on every 4th hole
            par = 5
            distance = np.random.randint(480, 550)
        elif i % 2 == 0:  # Par 4 on even holes
            par = 4
            distance = np.random.randint(350, 420)
        else:  # Par 3 on odd holes
            par = 3
            distance = np.random.randint(150, 220)
        
        holes.append({
            "Hole": i,
            "Par": par,
            "Distance": distance,
            "Handicap": i,
            "Description": f"Hole #{i} - {par} par"
        })
    
    return holes

def calculate_distance(from_hole, to_hole, holes_data):
    # Simple distance calculation between holes
    if from_hole == to_hole:
        return holes_data[from_hole - 1]['Distance']
    
    # Calculate walking distance between holes
    base_distance = 100  # Base walking distance between holes
    hole_gap = abs(to_hole - from_hole)
    return holes_data[from_hole - 1]['Distance'] + (base_distance * hole_gap)

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access GPS tracking.")
else:
    show_gps_page()