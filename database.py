import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseOperations:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseOperations, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                port=int(os.getenv('DB_PORT', 3306))
            )
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()

    def close(self):
        """Close the database connection"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def reconnect_if_needed(self):
        """Reconnect if connection is lost"""
        try:
            if not self.connection.is_connected():
                self.connection.reconnect()
                print("Reconnected to database")
        except Error as e:
            print(f"Error reconnecting: {e}")
            raise

    def insert_teams(self, df):
        """Insert teams in bulk"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO teams (team_name, city, stadium_name)
            VALUES (%s, %s, %s)
            """
            
            teams_data = df[['team_name', 'city', 'stadium_name']].values.tolist()
            
            cursor.executemany(insert_query, teams_data)
            self.connection.commit()
            return True, f"{cursor.rowcount} teams successfully inserted."
            
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def get_all_teams(self):
        """Get all teams"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM teams")
                return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_all_players(self):
        """Get all players with team and position information"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, t.team_name, pos.position_name 
                FROM players p
                LEFT JOIN teams t ON p.team_id = t.team_id
                LEFT JOIN positions pos ON p.position_id = pos.position_id
            """)
            players = cursor.fetchall()
            return players
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def get_all_positions(self):
        """Get all positions"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM positions")
            positions = cursor.fetchall()
            return positions
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def insert_players(self, df):
        """Insert players in bulk"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO players (player_name, age, position_id, team_id)
            VALUES (%s, %s, %s, %s)
            """
            players_data = df[['player_name', 'age', 'position_id', 'team_id']].values.tolist()
            cursor.executemany(insert_query, players_data)
            self.connection.commit()
            return True, f"{cursor.rowcount} players successfully inserted."
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def insert_player(self, player_name, age, position_id, team_id):
        """Insert a single player"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO players (player_name, age, position_id, team_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (player_name, age, position_id, team_id))
            self.connection.commit()
            return True, "Player successfully added"
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def insert_coaches(self, df):
        """Insert coaches in bulk"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO coaches (coach_name, age, team_id)
            VALUES (%s, %s, %s)
            """
            coaches_data = df[['coach_name', 'age', 'team_id']].values.tolist()
            cursor.executemany(insert_query, coaches_data)
            self.connection.commit()
            return True, f"{cursor.rowcount} coaches successfully inserted."
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def get_all_coaches(self):
        """Get all coaches with team information"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.*, t.team_name 
                FROM coaches c
                LEFT JOIN teams t ON c.team_id = t.team_id
            """)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            cursor.close()

    def insert_coach(self, coach_name, age, team_id):
        """Insert a single coach"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO coaches (coach_name, age, team_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (coach_name, age, team_id))
            self.connection.commit()
            return True, "Coach successfully added"
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def insert_team(self, team_name, city, stadium_name):
        """Insert a single team"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO teams (team_name, city, stadium_name)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (team_name, city, stadium_name))
            self.connection.commit()
            return True, "Team successfully added"
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()

    def insert_coach(self, coach_name, age, team_id):
        """Insert a single coach"""
        try:
            cursor = self.connection.cursor()
            insert_query = """
            INSERT INTO coaches (coach_name, age, team_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (coach_name, age, team_id))
            self.connection.commit()
            return True, "Coach successfully added"
        except Error as e:
            self.connection.rollback()
            return False, f"Database error: {e}"
        finally:
            cursor.close()