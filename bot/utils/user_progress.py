user_progress = {}

def reset_progress(user_id):
    """Reset progress for a new day"""
    user_progress[user_id] = {"step": 0, "done": False}

def get_progress(user_id):
    """Get user's current exercise step"""
    return user_progress.get(user_id, {"step": 0, "done": False})

def inc_progress(user_id):
    """Move user to the next exercise"""
    if user_id in user_progress:
        user_progress[user_id]["step"] += 1

def mark_done(user_id):
    """Mark that the final exercise has been completed"""
    if user_id in user_progress:
        user_progress[user_id]["done"] = True
