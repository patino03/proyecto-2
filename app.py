import streamlit as st
import pandas as pd
from database import DatabaseOperations

def handle_team_upload(db):
    st.subheader("Upload Teams Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:", df)
            
            if st.button("Upload Teams"):
                success, message = db.insert_teams(df)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")

def handle_player_upload(db):
    st.subheader("Upload Players Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:", df)
            
            if st.button("Upload Players"):
                success, message = db.insert_players(df)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")

def handle_player_form(db):
    st.subheader("Add New Player")
    
    with st.form("player_form"):
        player_name = st.text_input("Player Name")
        age = st.number_input("Age", min_value=16, max_value=45, value=20)
        
        # Get positions for dropdown
        positions = db.get_all_positions()
        position_names = [pos['position_name'] for pos in positions]
        selected_position = st.selectbox("Select Position", position_names)
        
        # Get teams for dropdown
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_names)
        
        submitted = st.form_submit_button("Add Player")
        
        if submitted and player_name and selected_position and selected_team:
            # Get position_id from selected position_name
            position_id = next(pos['position_id'] for pos in positions if pos['position_name'] == selected_position)
            
            # Get team_id from selected team_name
            team_id = next(team['team_id'] for team in teams if team['team_name'] == selected_team)
            
            # Insert player
            success, message = db.insert_player(player_name, age, position_id, team_id)
            
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def handle_coach_upload(db):
    st.subheader("Upload Coaches Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:", df)
            
            if st.button("Upload Coaches"):
                success, message = db.insert_coaches(df)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")

def handle_coach_form(db):
    st.subheader("Add New Coach")
    
    with st.form("coach_form"):
        coach_name = st.text_input("Coach Name")
        age = st.number_input("Age", min_value=30, max_value=80, value=45)
        
        # Get teams for dropdown
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_names)
        
        submitted = st.form_submit_button("Add Coach")
        
        if submitted and coach_name and selected_team:
            # Get team_id from selected team_name
            team_id = next(team['team_id'] for team in teams if team['team_name'] == selected_team)
            
            # Insert coach
            success, message = db.insert_coach(coach_name, age, team_id)
            
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def handle_team_form(db):
    st.subheader("Add New Team")
    
    with st.form("team_form"):
        team_name = st.text_input("Team Name")
        city = st.text_input("City")
        stadium_name = st.text_input("Stadium Name")
        
        submitted = st.form_submit_button("Add Team")
        
        if submitted and team_name and city and stadium_name:
            success, message = db.insert_team(team_name, city, stadium_name)
            
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def main():
    st.title("Football Team Management System")
    
    # Initialize database connection
    db = DatabaseOperations()
    
    # Navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choose an option",
        ["Teams", "Players", "Coaches"]
    )
    
    if option == "Teams":
        st.header("Team Management")
        tab1, tab2 = st.tabs(["Add Team", "Upload Excel"])
        
        with tab1:
            handle_team_form(db)
        
        with tab2:
            handle_team_upload(db)
            
        # Display teams
        teams = db.get_all_teams()
        if teams:
            st.write("Current Teams:")
            st.write(pd.DataFrame(teams))
    
    elif option == "Players":
        st.header("Player Management")
        tab1, tab2 = st.tabs(["Add Player", "Upload Excel"])
        
        with tab1:
            handle_player_form(db)
        
        with tab2:
            handle_player_upload(db)
            
        # Display players
        players = db.get_all_players()
        if players:
            st.write("Current Players:")
            st.write(pd.DataFrame(players))
    
    elif option == "Coaches":
        st.header("Coach Management")
        tab1, tab2 = st.tabs(["Add Coach", "Upload Excel"])
        
        with tab1:
            handle_coach_form(db)
        
        with tab2:
            handle_coach_upload(db)
            
        # Display coaches
        coaches = db.get_all_coaches()
        if coaches:
            st.write("Current Coaches:")
            st.write(pd.DataFrame(coaches))

if __name__ == "__main__":
    main()