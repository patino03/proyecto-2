from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection = connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    def insert_team(self, team_name, city, stadium_name):
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

    def insert_player(self, player_name, age, position_id, team_id):
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

    def insert_coach(self, coach_name, age, team_id):
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

    def get_all_teams(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM teams")
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def get_all_players(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, t.team_name, pos.position_name 
                FROM players p
                LEFT JOIN teams t ON p.team_id = t.team_id
                LEFT JOIN positions pos ON p.position_id = pos.position_id
            """)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def get_all_positions(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM positions")
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def get_all_coaches(self):
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
            return None
        finally:
            cursor.close()

    def get_player_by_id(self, player_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, t.team_name, pos.position_name 
                FROM players p
                LEFT JOIN teams t ON p.team_id = t.team_id
                LEFT JOIN positions pos ON p.position_id = pos.position_id
                WHERE p.player_id = %s
            """, (player_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def get_team_by_id(self, team_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM teams WHERE team_id = %s
            """, (team_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def get_coach_by_id(self, coach_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.*, t.team_name 
                FROM coaches c
                LEFT JOIN teams t ON c.team_id = t.team_id
                WHERE c.coach_id = %s
            """, (coach_id,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()