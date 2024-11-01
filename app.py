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
        age = st.number_input("Age", min_value=16, max_value=45)
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_names)
        positions = db.get_all_positions()
        position_names = [pos['position_name'] for pos in positions]
        selected_position = st.selectbox("Select Position", position_names)
        submitted = st.form_submit_button("Add Player")
        if submitted:
            team_id = next(team['team_id'] for team in teams if team['team_name'] == selected_team)
            position_id = next(pos['position_id'] for pos in positions if pos['position_name'] == selected_position)
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
        age = st.number_input("Age", min_value=30, max_value=80)
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_names)
        submitted = st.form_submit_button("Add Coach")
        if submitted:
            team_id = next(team['team_id'] for team in teams if team['team_name'] == selected_team)
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
        if submitted:
            success, message = db.insert_team(team_name, city, stadium_name)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def handle_search_page(db):
    st.header("Search Database")
    search_type = st.tabs(["Search Players", "Search Teams", "Search Coaches"])
    
    with search_type[0]:
        st.subheader("Search Players")
        player_id = st.number_input("Enter Player ID", min_value=1, step=1)
        if st.button("Search Player"):
            player = db.get_player_by_id(player_id)
            if player:
                st.write("Player Details:")
                st.json({
                    "Player Name": player['player_name'],
                    "Age": player['age'],
                    "Team": player['team_name'],
                    "Position": player['position_name']
                })
            else:
                st.error("Player not found")
    
    with search_type[1]:
        st.subheader("Search Teams")
        team_id = st.number_input("Enter Team ID", min_value=1, step=1, key="team_search")
        if st.button("Search Team"):
            team = db.get_team_by_id(team_id)
            if team:
                st.write("Team Details:")
                st.json({
                    "Team Name": team['team_name'],
                    "City": team['city'],
                    "Stadium": team['stadium_name']
                })
            else:
                st.error("Team not found")
    
    with search_type[2]:
        st.subheader("Search Coaches")
        coach_id = st.number_input("Enter Coach ID", min_value=1, step=1, key="coach_search")
        if st.button("Search Coach"):
            coach = db.get_coach_by_id(coach_id)
            if coach:
                st.write("Coach Details:")
                st.json({
                    "Coach Name": coach['coach_name'],
                    "Age": coach['age'],
                    "Team": coach['team_name']
                })
            else:
                st.error("Coach not found")

def handle_advanced_queries(db):
    st.header("Advanced Database Queries")
    
    query_options = [
        "1. Average age by team (players and coaches)",
        "2. Youngest and oldest players per team",
        "3. Teams with their players and coaches (INNER JOIN)",
        "4. Teams without players (LEFT JOIN)",
        "5. Players without teams (RIGHT JOIN)",
        "6. Number of players per position in each team",
        "7. Teams with coaches above average age",
        "8. Top 5 teams with most players",
        "9. Position distribution across teams",
        "10. Complete team statistics"
    ]
    
    selected_query = st.selectbox("Select Query", query_options)
    
    if st.button("Execute Query"):
        if selected_query.startswith("1."):
            result = db.get_avg_age_by_team()
            if result:
                st.write("Average age of players and coaches by team:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("2."):
            result = db.get_youngest_oldest_players()
            if result:
                st.write("Youngest and oldest players in each team:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("3."):
            result = db.get_teams_players_coaches()
            if result:
                st.write("Teams with their players and coaches (INNER JOIN):")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("4."):
            result = db.get_teams_without_players()
            if result:
                st.write("Teams without players (LEFT JOIN):")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("5."):
            result = db.get_players_without_teams()
            if result:
                st.write("Players without teams (RIGHT JOIN):")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("6."):
            result = db.get_players_by_position_team()
            if result:
                st.write("Number of players per position in each team:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("7."):
            result = db.get_teams_coaches_above_avg()
            if result:
                st.write("Teams with coaches above average age:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("8."):
            result = db.get_top_teams_by_players()
            if result:
                st.write("Top 5 teams with most players:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("9."):
            result = db.get_position_distribution()
            if result:
                st.write("Position distribution across teams:")
                st.dataframe(pd.DataFrame(result))
                
        elif selected_query.startswith("10."):
            result = db.get_team_statistics()
            if result:
                st.write("Complete team statistics:")
                st.dataframe(pd.DataFrame(result))

def main():
    st.title("Football Team Management System")
    
    db = DatabaseOperations()
    
    # Navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choose an option",
        ["Teams", "Players", "Coaches", "Search Database", "Advanced Queries"]
    )
    
    if option == "Search Database":
        handle_search_page(db)
    
    elif option == "Teams":
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
    
    elif option == "Advanced Queries":
        handle_advanced_queries(db)

if __name__ == "__main__":
    main()