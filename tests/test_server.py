from unittest.mock import MagicMock, patch
from src.yahoo.client import YahooFantasyClient


@patch("src.yahoo.client.get_authenticated_session")
@patch("yahoo_fantasy_api.Game")
def test_get_roster(mock_game, mock_auth):
    mock_league = MagicMock()
    mock_team = MagicMock()
    mock_team.roster.return_value = [
        {"name": "Christian McCaffrey", "position_type": "RB", "status": "Healthy"}
    ]
    mock_league.to_team.return_value = mock_team
    mock_game.return_value.to_league.return_value = mock_league

    client = YahooFantasyClient()
    roster = client.get_roster("team_1")

    assert len(roster) == 1
    assert roster[0]["name"] == "Christian McCaffrey"
    assert roster[0]["status"] == "Healthy"


@patch("src.yahoo.client.get_authenticated_session")
@patch("yahoo_fantasy_api.Game")
def test_get_free_agents(mock_game, mock_auth):
    mock_league = MagicMock()
    mock_league.free_agents.return_value = [
        {"name": "Player A", "position": "WR"},
        {"name": "Player B", "position": "WR"},
    ]
    mock_game.return_value.to_league.return_value = mock_league

    client = YahooFantasyClient()
    waivers = client.get_free_agents("WR", count=2)

    assert len(waivers) == 2
    assert waivers[0]["name"] == "Player A"
