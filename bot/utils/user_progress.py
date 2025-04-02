user_progress = {}

DEFAULT_DATA = {"exercise": -1, "step": -1, "done": False}

def reset_progress(user_id):
    """Reset progress for a new day"""
    user_progress[user_id] = DEFAULT_DATA


def get_progress(user_id):
    """Get user's current exercise step"""
    return user_progress.get(user_id, DEFAULT_DATA)


def update_progress(user_id, exercise_idx, step_idx):
    """Increment user's progress to the next exercise"""
    if user_id in user_progress:
        user_progress[user_id]["exercise"] = exercise_idx
        user_progress[user_id]["step"] = step_idx


def mark_done(user_id):
    """Mark that the final exercise has been completed"""
    if user_id in user_progress:
        user_progress[user_id]["done"] = True
