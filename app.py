import streamlit as st
import pandas as pd
from database import DatabaseOperations
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="⚽ Football Management System",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database connection
@st.cache_resource
def init_connection():
    return DatabaseOperations()

def handle_manual_team_entry():
    st.subheader("Add New Team")
    with st.form("team_form"):
        team_name = st.text_input("Team Name")
        city = st.text_input("City")
        stadium = st.text_input("Stadium Name")
        
        submitted = st.form_submit_button("Add Team")
        if submitted and team_name and city and stadium:
            db = init_connection()
            df = pd.DataFrame([[team_name, city, stadium]], 
                            columns=['team_name', 'city', 'stadium_name'])
            success, message = db.insert_teams(df)
            if success:
                st.success(message)
                st.rerun()  # Cambiado de experimental_rerun a rerun
            else:
                st.error(message)

def handle_team_upload(db):
    st.subheader("Upload Teams Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview:", df)
            
            if st.button("Upload Teams"):
                success, message = db.insert_teams(df)
                if success:
                    st.success(message)
                    st.rerun()  # Cambiado de experimental_rerun a rerun
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"Error: {str(e)}")

def handle_player_form():
    st.subheader("Add New Player")
    with st.form("player_form"):
        player_name = st.text_input("Player Name")
        age = st.number_input("Age", min_value=15, max_value=45)
        
        # Get positions for dropdown
        db = init_connection()
        positions = db.get_all_positions()
        position_names = [pos['position_name'] for pos in positions]
        selected_position = st.selectbox("Position", position_names)
        
        # Get teams for dropdown
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        
        if not team_names:
            st.error("No teams available. Please add teams first.")
            return
            
        selected_team = st.selectbox("Select Team", team_names)
        
        submitted = st.form_submit_button("Add Player")
        if submitted and player_name and selected_team and selected_position:
            # Get IDs from names
            position_id = next(pos['position_id'] for pos in positions if pos['position_name'] == selected_position)
            team_id = next(team['team_id'] for team in teams if team['team_name'] == selected_team)
            
            success, message = db.insert_player(player_name, age, position_id, team_id)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def handle_coach_form():
    st.subheader("Add New Coach")
    with st.form("coach_form"):
        coach_name = st.text_input("Coach Name")
        age = st.number_input("Age", min_value=25, max_value=80)
        
        # Get teams for dropdown
        db = init_connection()
        teams = db.get_all_teams()
        team_names = [team['team_name'] for team in teams]
        selected_team = st.selectbox("Select Team", team_names)
        
        submitted = st.form_submit_button("Add Coach")
        if submitted:
            st.info("Coach functionality coming soon!")

def view_data(db):
    """Handle data visualization"""
    st.title("View Data")
    data_type = st.selectbox("Select data to view", ["Teams", "Players", "Coaches", "Matches"])
    
    if data_type == "Teams":
        teams = db.get_all_teams()
        if teams:
            st.write("Registered Teams:", pd.DataFrame(teams))
        else:
            st.info("No teams registered yet.")
    elif data_type == "Players":
        players = db.get_all_players()
        if players:
            df = pd.DataFrame(players)
            # Reordenar y renombrar columnas para mejor visualización
            columns = ['player_name', 'age', 'team_name', 'position_name']
            df = df[columns]
            df.columns = ['Name', 'Age', 'Team', 'Position']
            st.write("Registered Players:", df)
        else:
            st.info("No players registered yet.")

def main():
    try:
        # Create database instance
        db = init_connection()
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        option = st.sidebar.selectbox(
            "Choose an option",
            ["Home", "Teams", "Players", "Coaches", "View Data"]
        )

        if option == "Home":
            st.title("⚽ Football Management System")
            st.write("Welcome to the Football Management System")
            
            # Dashboard stats in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                teams = db.get_all_teams()
                st.metric("Total Teams", len(teams))
            with col2:
                st.metric("Total Players", "Coming soon")
            with col3:
                st.metric("Total Coaches", "Coming soon")
            
        elif option == "Teams":
            st.title("Team Management")
            tab1, tab2 = st.tabs(["Add Team", "Upload Excel"])
            
            with tab1:
                handle_manual_team_entry()
            with tab2:
                handle_team_upload(db)
                
        elif option == "Players":
            st.title("Player Management")
            handle_player_form()
            
        elif option == "Coaches":
            st.title("Coach Management")
            handle_coach_form()
                
        elif option == "View Data":
            view_data(db)

    except Exception as e:
        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
