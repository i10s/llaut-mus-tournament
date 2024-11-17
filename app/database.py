# Centralized database for shared state

# List of registered users (e.g., usernames)
registered_users = []

# List of pairs (e.g., tuples of two usernames)
pairs = []

# Dictionary to hold stats for each pair
pair_stats = {}

# Dictionary to hold stats for each user
user_stats = {}

# Tournament bracket (list of rounds, where each round contains match details)
tournament_bracket = []


# Helper functions for managing the shared state
def get_registered_users():
    """
    Get a copy of the current registered users list.
    
    Returns:
        list: A copy of the registered users.
    """
    return registered_users[:]


def add_registered_user(username):
    """
    Add a user to the registered users list.
    
    Args:
        username (str): The username to add.
    
    Raises:
        ValueError: If the username already exists.
    """
    if username in registered_users:
        raise ValueError(f"User '{username}' already exists.")
    registered_users.append(username)
    user_stats[username] = {"games_played": 0, "games_won": 0, "games_lost": 0}


def get_user_stats():
    """
    Get a copy of the current user stats.
    
    Returns:
        dict: A copy of the user stats.
    """
    return user_stats.copy()


def update_user_stats(username, games_played=0, games_won=0, games_lost=0):
    """
    Update stats for a specific user.
    
    Args:
        username (str): The username of the user.
        games_played (int): The number of games played to increment.
        games_won (int): The number of games won to increment.
        games_lost (int): The number of games lost to increment.
    
    Raises:
        ValueError: If the user does not exist in the stats.
    """
    if username not in user_stats:
        raise ValueError(f"User stats for '{username}' do not exist.")
    user_stats[username]["games_played"] += games_played
    user_stats[username]["games_won"] += games_won
    user_stats[username]["games_lost"] += games_lost


def get_pairs():
    """
    Get a copy of the current pairs list.
    
    Returns:
        list: A copy of the pairs.
    """
    return pairs[:]


def add_pair(pair):
    """
    Add a pair to the pairs list.
    
    Args:
        pair (tuple): A tuple representing the pair of usernames.
    
    Raises:
        ValueError: If the pair already exists.
    """
    if pair in pairs:
        raise ValueError(f"Pair {pair} already exists.")
    pairs.append(pair)


def get_pair_stats():
    """
    Get a copy of the current pair stats.
    
    Returns:
        dict: A copy of the pair stats.
    """
    return pair_stats.copy()


def update_pair_stats(pair_key, games_played=0, games_won=0, games_lost=0):
    """
    Update stats for a specific pair.
    
    Args:
        pair_key (str): The key representing the pair.
        games_played (int): The number of games played to increment.
        games_won (int): The number of games won to increment.
        games_lost (int): The number of games lost to increment.
    
    Raises:
        ValueError: If the pair does not exist in the stats.
    """
    if pair_key not in pair_stats:
        raise ValueError(f"Pair stats for '{pair_key}' do not exist.")
    pair_stats[pair_key]["games_played"] += games_played
    pair_stats[pair_key]["games_won"] += games_won
    pair_stats[pair_key]["games_lost"] += games_lost


def get_tournament_bracket():
    """
    Get a copy of the current tournament bracket.
    
    Returns:
        list: A copy of the tournament bracket.
    """
    return tournament_bracket[:]


def add_to_tournament_bracket(round_matches):
    """
    Add a round to the tournament bracket.
    
    Args:
        round_matches (list): A list of matches for the round.
    """
    tournament_bracket.append(round_matches)


def clear_database():
    """
    Clear all data from the database. This is typically used for testing or resetting.
    """
    registered_users.clear()
    user_stats.clear()
    pairs.clear()
    pair_stats.clear()
    tournament_bracket.clear()
