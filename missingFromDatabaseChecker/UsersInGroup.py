import requests
import time

def getGroupRoles(target):
  url = f"https://groups.roblox.com/v1/groups/{target}/roles"
  response = requests.get(url)
  if response.status_code != 200:
    print(f"Error fetching roles: {response.status_code}")
    return None
  data = response.json()
  return {role['rank']: role['name'] for role in data['roles']}

def getGroupMembers(target):
  members = []
  cursor = None
  role_map = getGroupRoles(target)
  if not role_map:
    return None
  print("Fetching group members...")
  while True:
    url = f"https://groups.roblox.com/v1/groups/{target}/users"
    params = {
      'limit': 100,
      'sortOrder': 'Asc'
    }
    if cursor:
      params['cursor'] = cursor
    response = requests.get(url, params=params)
    if response.status_code != 200:
      print(f"Error fetching members: {response.status_code}")
      break
    data = response.json()
    batch_members = data['data']
    for member in batch_members:
      try:
        if 'role' in member and isinstance(member['role'], dict) and 'rank' in member['role']:
          rank = member['role']['rank']
        elif 'rank' in member:
          rank = member['rank']
        else:
          print(f"Unexpected member structure: {members.keys()}")
          rank = 0
        member['rank'] = rank
        member['roleName'] = role_map.get(rank, "Unknown")
      except Exception as e:
        print(f"Error processing member: {e}")
        print(f"Member data: {member}")
        continue
    members.extend(batch_members)
    if not data.get('nextPageCursor'):
      break
    cursor = data['nextPageCursor']
    print(f"Fetched {len(members)} members so far...")
    time.sleep(0.1)  # To avoid hitting rate limits
  return members

def organizeMembersByRole(members):
  organized = {}
  for member in members:
    role = member['roleName']
    if role not in organized:
      organized[role] = []
    organized[role].append({
      'userId': member['user']['userId'],
      'username': member['user']['username'],
      'displayName': member['user']['displayName'],
      'rank': member['rank'],
      'roleName': role
    })
  return organized

def mainIGroup(target):
  print(f"Target Group ID: {target}")
  print("Starting member fetch...")

  members = getGroupMembers(target)
  if not members:
    print("Failed to retrieve group data.")
    return

  print("Organizing members by role...")

  organized_members = organizeMembersByRole(members)

  result = {
    "groupId": target,
    "totalMembers": len(members),
    "membersByRole": organized_members
  }

  print("\nSummary by Role:")
  for role, members in organized_members.items():
    print(f"    {role}: {len(members)} members")
  return result