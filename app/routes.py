from fastapi import APIRouter, HTTPException
from typing import List
from .models import (Team, TeamCreate, Player, PlayerCreate, Coach, CoachCreate, 
                    Match, MatchCreate, Contract, ContractCreate, SeasonStat, SeasonStatCreate)
from .database import DatabaseOperations

router = APIRouter()
db = DatabaseOperations()

@router.get("/teams", response_model=List[Team])
async def get_teams():
    teams = db.get_all_teams()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    return teams

@router.post("/teams", response_model=Team)
async def create_team(team: TeamCreate):
    result = db.insert_team(team.team_name, team.city, team.stadium_name)
    if not result[0]:
        raise HTTPException(status_code=400, detail=result[1])
    return {"team_id": result[2], **team.dict()}

@router.get("/players", response_model=List[Player])
async def get_players():
    players = db.get_all_players()
    if not players:
        raise HTTPException(status_code=404, detail="No players found")
    return players

@router.post("/players", response_model=Player)
async def create_player(player: PlayerCreate):
    result = db.insert_player(player.player_name, player.age, player.position_id, player.team_id)
    if not result[0]:
        raise HTTPException(status_code=400, detail=result[1])
    return {"player_id": result[2], **player.dict()}

@router.get("/coaches", response_model=List[Coach])
async def get_coaches():
    coaches = db.get_all_coaches()
    if not coaches:
        raise HTTPException(status_code=404, detail="No coaches found")
    return coaches

@router.post("/coaches", response_model=Coach)
async def create_coach(coach: CoachCreate):
    result = db.insert_coach(coach.coach_name, coach.age, coach.team_id)
    if not result[0]:
        raise HTTPException(status_code=400, detail=result[1])
    return {"coach_id": result[2], **coach.dict()}