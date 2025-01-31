from fastapi import FastAPI, HTTPException, Query
from requests import Session, RequestException
from datetime import datetime, timezone, timedelta

app = FastAPI()

class LolesportsAPI:
    def __init__(self):
        # All credits about the key and idea to Leo Lo in GitLab
        self.API_KEY = {'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'}
        self.API_URL = 'https://esports-api.lolesports.com/persisted/gw'
        self.LIVESTATS_API = 'https://feed.lolesports.com/livestats/v1'
        self.session = Session()
        self.session.headers.update(self.API_KEY)

    def get_latest_date(self):
        now = datetime.now(timezone.utc)
        now = now - timedelta(seconds=now.second, microseconds=now.microsecond)
        return now.isoformat().replace('+00:00', 'Z')

    def fetch_data(self, endpoint: str, params: dict):
        try:
            response = self.session.get(self.API_URL + endpoint, params=params)
            response.raise_for_status()
            return response.json().get('data', {})
        except RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching {endpoint}: {e}")

    def fetch_game_data(self, endpoint: str, params: dict):
        try:
            response = self.session.get(self.LIVESTATS_API + endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error fetching {endpoint}: {e}")

api_client = LolesportsAPI()

@app.get("/leagues")
def get_leagues(hl: str = "en-US"):
    return api_client.fetch_data("/getLeagues", {"hl": hl})

@app.get("/tournaments")
def get_tournaments(league_id: str, hl: str = "en-US"):
    return api_client.fetch_data("/getTournamentsForLeague", {"hl": hl, "leagueId": league_id})

@app.get("/standings")
def get_standings(tournament_id: str, hl: str = "en-US"):
    return api_client.fetch_data("/getStandings", {"hl": hl, "tournamentId": tournament_id})

@app.get("/schedule")
def get_schedule(league_id: str, hl: str = "en-US"):
    return api_client.fetch_data("/getSchedule", {"hl": hl, "leagueId": league_id})

@app.get("/live")
def get_live(hl: str = "en-US"):
    return api_client.fetch_data("/getLive", {"hl": hl})

@app.get("/completed_events")
def get_completed_events(tournament_id: str, hl: str = "en-US"):
    return api_client.fetch_data("/getCompletedEvents", {"hl": hl, "tournamentId": tournament_id})

@app.get("/teams")
def get_teams(hl: str = "en-US"):
    return api_client.fetch_data("/getTeams", {"hl": hl})

@app.get("/game/window")
def get_game_window(game_id: str, starting_time: str = Query(default=None)):
    if starting_time is None:
        starting_time = api_client.get_latest_date()
    return api_client.fetch_game_data(f"/window/{game_id}", {"startingTime": starting_time})

@app.get("/game/details")
def get_game_details(game_id: str, starting_time: str = Query(default=None), participant_ids: str = Query(default=None)):
    if starting_time is None:
        starting_time = api_client.get_latest_date()
    params = {"startingTime": starting_time}
    if participant_ids:
        params["participantIds"] = participant_ids
    return api_client.fetch_game_data(f"/details/{game_id}", params)

# LEC 98767991302996019