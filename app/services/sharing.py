from app.models.draw import Draw
from app.models.match import Match


def format_whatsapp_draw(match: Match, draw: Draw) -> str:
    lines: list[str] = []
    if match.notes:
        lines.extend([f"{match.notes} - {match.scheduled_at.strftime('%d/%m/%Y %H:%M')}", ""])

    result = draw.normalized_result or {}
    for team in result.get("teams", []):
        team_name = team.get("team_name") or "Time"
        lines.append(str(team_name))
        lines.append("")
        for player in team.get("players", []):
            name = player.get("name") if isinstance(player, dict) else player
            if name:
                lines.append(f"* {name}")
        lines.append("")

    leftovers = result.get("leftovers") or []
    if leftovers:
        lines.append("Sobras")
        lines.append("")
        for player in leftovers:
            name = player.get("name") if isinstance(player, dict) else player
            if name:
                lines.append(f"* {name}")

    return "\n".join(lines).strip()
