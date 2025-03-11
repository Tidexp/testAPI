import requests

def test2(tournament_id):
    url = f"https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        latest_season = data["seasons"][0]  # Lấy mùa giải mới nhất
        return latest_season["id"]
    else:
        print("Không lấy được danh sách mùa giải")
        return None
