'''

Module bin.lovecalc (lovecalc command)
1 Function : lovecalc ; Takes in 2 user ids and returns a calculated love percentage and an associated comment.

'''

def lovecalc(user1, user2):
    user1n = int(user1[2:-1]) 
    user2n = int(user2[2:-1])
    love = int(user1n / user2n * 31415 % 100)  # Lovecalc formula

    # Custom lovecalc results
    love_results = {
        frozenset({481998330549764106, 1185973996055965799}): 100,
        frozenset({415974992308862977, 481998330549764106}): 100,
        frozenset({415974992308862977, 1185973996055965799}): 0,
        frozenset({1170434322453504093, 1186799421636231208}): 100,
        
        # frozenset({user_id1, user_id2}): love_amount, # Template to add a custom lovecalc result
    }
    
    
    users_pair = frozenset({user1n, user2n})
    reverse_users_pair = frozenset({user2n, user1n})
    if users_pair in love_results:
        love = love_results[users_pair]
    elif reverse_users_pair in love_results:
        love = love_results[reverse_users_pair]
    
    if 1170434322453504093 in users_pair or 1170434322453504093 in reverse_users_pair:
        love = 0
        comment = "Nobody loves Crystal SMHH (Besides me ,-, >.<)"
        print("[PNH Logs] (lovecalc) love is estimated to", love)  # Log
        return love, comment

    # Lovecalc comments section
    love_comments = [
        (lambda l: l < 10 and user1n != 1170434322453504093 and user2n != 1170434322453504093, "I may be wrong but uhh love may not be compatible with these two-"),
        (lambda l: users_pair == {1170434322453504093, 1186799421636231208}, "AAAAAAAAAAAAAAA AAAAAARGJOJRTOHTJO I love Crystal so much 💀💀 it's so true <3 ..."),
        (lambda l: 10 <= l < 30, "Not that high but doesn't mean it's impossible. Wait and see lol"),
        (lambda l: 30 <= l < 40, "Can feel something between em, still very decent"),
        (lambda l: 40 <= l < 60, "Pretty average, y'all got all your chances"),
        (lambda l: 60 <= l < 70, "Eyyy this is starting to be some good score ngl"),
        (lambda l: 70 <= l < 80, "Awww, you both have to make up fr"),
        (lambda l: 80 <= l < 100, "<3 DAMN if you want intimacy, just let us know and we'll let you be"),
        (lambda l: l == 100, "You are made for each other... <3"),
    ]

    comment = next((msg for condition, msg in love_comments if condition(love)), "")
    print("[PNH Logs] (lovecalc) love is estimated to", love)  # Log
    return love, comment







