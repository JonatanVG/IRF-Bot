def check_friends_against_blacklist(friends, blacklist):
    flagged_friends = []
    for friend_name, friend_id in friends.items():
        lower_friend_name = friend_name.lower()
        if lower_friend_name in blacklist:
            accurate_name, list_type = blacklist[lower_friend_name]
            flagged_friends.append((accurate_name, list_type, friend_id))
    return flagged_friends