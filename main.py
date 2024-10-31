from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Football Management System",
    description="API for managing season stats, contracts, and matches",
    version="1.0.0"
)

# Modelos Pydantic para validación de datos
class SeasonStats(BaseModel):
    player_id: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    minutes_played: int

class Contract(BaseModel):
    player_id: int
    start_date: date
    end_date: date
    player_value: float

class Match(BaseModel):
    home_team_id: int
    away_team_id: int
    match_date: date
    score_home_team: int
    score_away_team: int

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'equipo_futbol')
    )

# Endpoints para insertar datos
@app.post("/season_stats/", response_model=dict)
async def create_season_stats(stats: SeasonStats):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO season_stats 
            (player_id, goals, assists, yellow_cards, red_cards, minutes_played)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            stats.player_id,
            stats.goals,
            stats.assists,
            stats.yellow_cards,
            stats.red_cards,
            stats.minutes_played
        ))
        conn.commit()
        return {"message": "Season stats created successfully", "stat_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/contracts/", response_model=dict)
async def create_contract(contract: Contract):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO contracts 
            (player_id, start_date, end_date, player_value)
            VALUES (%s, %s, %s, %s)
        """, (
            contract.player_id,
            contract.start_date,
            contract.end_date,
            contract.player_value
        ))
        conn.commit()
        return {"message": "Contract created successfully", "contract_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/matches/", response_model=dict)
async def create_match(match: Match):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO matches 
            (home_team_id, away_team_id, match_date, score_home_team, score_away_team)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            match.home_team_id,
            match.away_team_id,
            match.match_date,
            match.score_home_team,
            match.score_away_team
        ))
        conn.commit()
        return {"message": "Match created successfully", "match_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()