from missingFromDatabaseChecker.Comparer import Comparer

possible_ids = {
  1346784451455356948: {
    "sheet": "1Skmq67lBY-opuAZQKCjMt6o7RBHGOZYuPa-UNtqMRw8",
    "group": 10421433,
    "parameters": "C7:D200",
    "start_row": 7
  }, 
  1362187563238035506: {
    "sheet": "1hzRzEdmCUdktzFXEhiM3JeTBDCOEwoTw8Bx2PZavL9M",
    "group": 5267416,
    "parameters": "D10:E200",
    "start_row": 10
  }, 
  475965830295715840: {
    "sheet": "1Skmq67lBY-opuAZQKCjMt6o7RBHGOZYuPa-UNtqMRw8",
    "group": 10421433,
    "parameters": "C7:D200",
    "start_row": 7
  }
}

async def Comparison(guild_id: int):
  if guild_id is None:
    return None, None
  guild = possible_ids.get(guild_id)
  if guild is None:
    return None, None
  notInDatabase, duplicates = await Comparer(guild)
  result = []
  resultNames = []
  for role, users in notInDatabase.items():
    print(f"\nRole: {role} - Users not in database:")
    for user in users:
      print(f"{user['roleName']} - {user['username']}")
      result.append(f"{user['roleName']} - {user['username']}")
      resultNames.append(user['username'])
  print(f"\nOverall total not in database: {len(result)}")
  if not result:
    result.append("All users are in the database.")
  result.append("-"*40)
  result.append("**Duplicates found in sheet data:**")
  for dup in duplicates:
    result.append(dup)
  joined = "\n".join(result)
  joinedNames = ", ".join(resultNames)
  return joined, joinedNames