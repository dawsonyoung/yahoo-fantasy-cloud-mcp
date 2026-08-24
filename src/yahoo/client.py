from typing import Any
import yahoo_fantasy_api as yfa
from src.config import settings
from src.yahoo.auth import get_authenticated_session


class YahooFantasyClient:
    def __init__(self):
        self._sc = None
        self._league = None

    @property
    def league(self) -> yfa.League:
        if self._league is None:
            self._sc = get_authenticated_session()
            gm = yfa.Game(self._sc, "nfl")
            self._league = gm.to_league(settings.yahoo_league_id)
        return self._league

    def get_roster(self, team_key: str) -> list[dict[str, Any]]:
        """Fetch current roster and status for a team."""
        team = self.league.to_team(team_key)
        return team.roster()

    def get_free_agents(self, position: str, count: int = 10) -> list[dict[str, Any]]:
        """Fetch top available free agents by position (e.g., 'RB', 'WR', 'TE')."""
        return self.league.free_agents(position)[:count]

    def get_matchups(self) -> list[dict[str, Any]]:
        """Fetch weekly matchups and projected scores."""
        return self.league.matchups()

    def get_standings(self) -> list[dict[str, Any]]:
        """Fetch current league standings and records."""
        return self.league.standings()
