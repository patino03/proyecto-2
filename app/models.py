from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TeamCreate(BaseModel):
    team_name: str = Field(..., description="Nombre del equipo (campo requerido)")
    city: str = Field(..., description="Ciudad del equipo (campo requerido)")
    stadium_name: str = Field(..., description="Nombre del estadio (campo requerido)")

class Team(TeamCreate):
    team_id: int

class PlayerCreate(BaseModel):
    player_name: str = Field(..., description="Nombre del jugador (campo requerido)")
    age: int = Field(..., description="Edad del jugador (campo requerido)")
    position_id: int = Field(..., description="ID de la posición del jugador (campo requerido)")
    team_id: Optional[int] = Field(None, description="ID del equipo del jugador (opcional)")

class Player(PlayerCreate):
    player_id: int

class CoachCreate(BaseModel):
    coach_name: str = Field(..., description="Nombre del entrenador (campo requerido)")
    age: int = Field(..., description="Edad del entrenador (campo requerido)")
    team_id: Optional[int] = Field(None, description="ID del equipo del entrenador (opcional)")

class Coach(CoachCreate):
    coach_id: int

class MatchCreate(BaseModel):
    home_team_id: int = Field(..., description="ID del equipo local (campo requerido)")
    away_team_id: int = Field(..., description="ID del equipo visitante (campo requerido)")
    match_date: date = Field(..., description="Fecha del partido (campo requerido)")
    score_home_team: int = Field(..., description="Goles del equipo local (campo requerido)")
    score_away_team: int = Field(..., description="Goles del equipo visitante (campo requerido)")

class Match(MatchCreate):
    match_id: int

class ContractCreate(BaseModel):
    player_id: int = Field(..., description="ID del jugador (campo requerido)")
    start_date: date = Field(..., description="Fecha de inicio del contrato (campo requerido)")
    end_date: date = Field(..., description="Fecha de fin del contrato (campo requerido)")
    player_value: float = Field(..., description="Valor del jugador (campo requerido)")

class Contract(ContractCreate):
    contract_id: int

class SeasonStatCreate(BaseModel):
    player_id: int = Field(..., description="ID del jugador (campo requerido)")
    goals: int = Field(..., description="Número de goles (campo requerido)")
    assists: int = Field(..., description="Número de asistencias (campo requerido)")
    yellow_cards: int = Field(..., description="Tarjetas amarillas (campo requerido)")
    red_cards: int = Field(..., description="Tarjetas rojas (campo requerido)")
    minutes_played: int = Field(..., description="Minutos jugados (campo requerido)")

class SeasonStat(SeasonStatCreate):
    stat_id: int

# Ejemplos para la documentación
class Config:
    schema_extra = {
        "example": {
            "TeamCreate": {
                "team_name": "Real Madrid",
                "city": "Madrid",
                "stadium_name": "Santiago Bernabéu"
            },
            "PlayerCreate": {
                "player_name": "Lionel Messi",
                "age": 34,
                "position_id": 1,
                "team_id": 1
            },
            "ContractCreate": {
                "player_id": 1,
                "start_date": "2024-01-01",
                "end_date": "2025-01-01",
                "player_value": 1000000.00
            }
        }
    } 