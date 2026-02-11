import requests
from collections import Counter
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

async def timer():
  cooldown = 60
  while cooldown > 0:
    print(f"Rate limited. Retrying in {cooldown} seconds...", end='\r')
    await asyncio.sleep(1)
    cooldown -= 1
  print("Retrying now...            ")

async def fetchSheetData(spreadsheet_id, api_key, sheet_name: str, parameters: str, start_row: int):
  range_name = f"{sheet_name}!{parameters}"
  url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}?key={api_key}"
  print(f"Fetching data from URL: {url}")
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    usersAndRoles = []
    duplicates = []
    if 'values' in data:
      print("Data fetched successfully. Processing rows...")
      for i, row in enumerate(data['values'], start=start_row):
        if len(row) >= 1 and row[0] and row[0].strip():
          username = row[0].strip()
          role = row[1].strip() if len(row) > 1 and row[1] else "Guest"
          for entry in usersAndRoles:
            if entry['username'] == username:
              print(f"Duplicate username found: {username} at row {i}. Skipping entry.")
              duplicates.append(f"In {sheet_name}: Duplicate {username} at row '{i}'")
              continue
            elif entry['username'] == "" or entry['username'] is None:
              print(f"Empty username found at row {i}. Skipping entry.")
              duplicates.append(f"In {sheet_name}: Empty username at row '{i}'")
              continue
          usersAndRoles.append({
            "row": i,
            "username": username, 
            "role": role
          })
      print(f"Total valid entries found: {len(usersAndRoles)}")
      print(f"Duplicates found: {duplicates}")
      return usersAndRoles, duplicates
    else:
      print("No 'values' key found in the response.")
      return None
  elif response.status_code == 429:  # Rate limited
    print("Rate limited! Waiting 60 seconds before retry...")
    await timer()
    return await fetchSheetData(spreadsheet_id, api_key, sheet_name)  # Retry
  else:
    print(f"Error {response.status_code}: {response.text}")
    return None
    
async def mainISheet(spreadsheet_id: str, parameters: str, start_row: int):
  sheet_names = [
    "Personnel | Database",
    "Staff | Database",
  ]
  api_key = os.getenv("API_KEY")
  data = []
  duplicates = []
  for sheet_name in sheet_names:
    print(f"Fetching data from sheet: {sheet_name}")
    sheet_data, sheet_duplicates = await fetchSheetData(spreadsheet_id, api_key, sheet_name, parameters, start_row)
    if sheet_data:
      data.extend(sheet_data)
    if sheet_duplicates:
      duplicates.extend(sheet_duplicates)
  if data is not None:
    role_counts = Counter(entry['role'] for entry in data)
    print("\nRole Distribution:")
    for role, count in role_counts.items():
      print(f"{role}: {count}")
    print("\nFirst 5 Entries:")
    for entry in data[:5]:
      print(f"Row {entry['row']}: Username: {entry['username']}, Role: {entry['role']}")
    return data, duplicates
  else:
    print("Failed to retrieve data from the Google Sheet.")