from fastapi import APIRouter, HTTPException
from app.models import (ContractCreate, Contract, 
                       MatchCreate, Match,
                       SeasonStatCreate, SeasonStat)
from app.apidatabase import get_db_connection
from typing import List
from datetime import datetime

router = APIRouter()

# Endpoints para Contracts
@router.post("/contracts/", response_model=Contract, tags=["Contracts"])
def create_contract(contract: ContractCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO contracts (player_id, start_date, end_date, player_value)
        VALUES (%s, %s, %s, %s)
        """
        values = (contract.player_id, contract.start_date, 
                 contract.end_date, contract.player_value)
        
        cursor.execute(query, values)
        conn.commit()
        
        contract_id = cursor.lastrowid
        return Contract(contract_id=contract_id, **contract.dict())
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/contracts/", response_model=List[Contract], tags=["Contracts"])
def list_contracts():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contracts")
        contracts = cursor.fetchall()
        return [Contract(**contract) for contract in contracts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Endpoints para Matches
@router.post("/matches/", response_model=Match, tags=["Matches"])
def create_match(match: MatchCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO matches (home_team_id, away_team_id, match_date, 
                           score_home_team, score_away_team)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (match.home_team_id, match.away_team_id, match.match_date,
                 match.score_home_team, match.score_away_team)
        
        cursor.execute(query, values)
        conn.commit()
        
        match_id = cursor.lastrowid
        return Match(match_id=match_id, **match.dict())
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Endpoints para Season Stats
@router.post("/season-stats/", response_model=SeasonStat, tags=["Season Stats"])
def create_season_stat(stat: SeasonStatCreate):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO season_stats (player_id, goals, assists, 
                                yellow_cards, red_cards, minutes_played)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (stat.player_id, stat.goals, stat.assists,
                 stat.yellow_cards, stat.red_cards, stat.minutes_played)
        
        cursor.execute(query, values)
        conn.commit()
        
        stat_id = cursor.lastrowid
        return SeasonStat(stat_id=stat_id, **stat.dict())
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Queries específicas
@router.get("/stats/player/{player_id}", tags=["Queries"])
def get_player_stats(player_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT s.*, c.player_value, c.start_date, c.end_date
        FROM season_stats s
        LEFT JOIN contracts c ON s.player_id = c.player_id
        WHERE s.player_id = %s
        """
        cursor.execute(query, (player_id,))
        return cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close() 