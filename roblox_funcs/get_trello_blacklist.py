import requests

def get_trello_blacklist():
  url = "https://trello.com/b/ov7HU6Pv.json"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    blacklisted_names = {}
    active_card_ids = {card["id"] for card in data.get("cards", []) if not card.get("closed", False)}
    for card in data.get("cards", []):
      is_archived = card["id"] not in active_card_ids
      for list_item in data.get("lists", []):
        if card["idList"] == list_item["id"]:
          status_suffix = " (Archived/Inactive Punishment)" if is_archived else ""
          blacklisted_names[card["name"].strip().lower()] = (card["name"].strip(), list_item["name"] + status_suffix)
    return blacklisted_names
  return {}