# FastAPI: framework tạo API
# HTTPException: xử lý lỗi về HTTP trong API
from fastapi import FastAPI, HTTPException
import sys
sys.path.append('d:/Python/testFolder')
import requests
import testFolder
from test2 import test2

# gọi api: uvicorn test:app --reload
app = FastAPI()

def get_standing(tournament_id: int):
    """
    Lấy bảng xếp hạng
    """
    season_id = test2(tournament_id)  # Lấy ID mùa giải mới nhất
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/standings/total"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if "standings" in data and len(data["standings"]) > 0:
            standings_type = data["standings"][0]["type"]
            standings_rows = data["standings"][0]["rows"]

            teams_rank = []
            teams_info = []

            for index, row in enumerate(standings_rows):
                team_name = row["team"]["name"]
                rank = index + 1
                teams_rank.append({"rank": rank, "team": team_name})

            for team in standings_rows[:20]:  # Giới hạn từ 0 đến 19
                team_info = {
                    "position": team.get("position"),
                    "matches": team.get("matches"),
                    "wins": team.get("wins"),
                    "draws": team.get("draws"),
                    "losses": team.get("losses"),
                    "points": team.get("points"),
                    "scoresFor": team.get("scoresFor"),
                    "scoresAgainst": team.get("scoresAgainst"),
                    "scoreDiffFormatted": team.get("scoreDiffFormatted"),
                }
                teams_info.append(team_info)

            return {
                "type": standings_type,
                "teams_rank": teams_rank,
                "teams_info": teams_info
            }
        else:
            return None
    else:
        return None

@app.get("/standings")
async def standings(tournament_id: int):
    result = get_standing(tournament_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=500, detail="Không thể lấy dữ liệu standings")

# truy cập http://127.0.0.1:8000/docs  (mùa giải hiện tại là 17)

