from typing import Any
from fastmcp import FastMCP
from src.config import settings
from src.yahoo.client import YahooFantasyClient

mcp = FastMCP("Yahoo Fantasy Football MCP")
client = YahooFantasyClient()


@mcp.tool()
def get_team_roster(team_key: str) -> list[dict[str, Any]]:
    """Fetch current roster, starting slots, and injury status for a Yahoo Fantasy team."""
    return client.get_roster(team_key)


@mcp.tool()
def get_top_waiver_players(position: str, count: int = 10) -> list[dict[str, Any]]:
    """Fetch top available free agents on the waiver wire for a position (e.g. 'RB', 'WR', 'TE')."""
    return client.get_free_agents(position=position, count=count)


@mcp.tool()
def get_league_matchups() -> list[dict[str, Any]]:
    """Fetch weekly fantasy matchups, live scores, and projected point totals."""
    return client.get_matchups()


@mcp.tool()
def get_league_standings() -> list[dict[str, Any]]:
    """Fetch overall league standings, records, and points for/against."""
    return client.get_standings()


if __name__ == "__main__":
    # Expose SSE transport for scale-to-zero Cloud Run HTTP invocations
    mcp.run(transport="sse", host="0.0.0.0", port=settings.port)
