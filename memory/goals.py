import yaml
import os

GOALS_PATH = os.path.join(os.path.dirname(__file__), 'GOALS.yaml')

def load_goals():
    if not os.path.exists(GOALS_PATH):
        print("⚠️  GOALS.yaml not found. Returning empty goal list.")
        return []
    with open(GOALS_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('goals', [])

def save_goals(goals):
    with open(GOALS_PATH, 'w') as f:
        yaml.dump({'goals': goals}, f, sort_keys=False)
    print("✅ GOALS.yaml updated successfully.")

def update_goal_status(goal_name, new_status):
    goals = load_goals()
    for goal in goals:
        if goal['goal'] == goal_name:
            goal['status'] = new_status
            break
    save_goals(goals)
    return goals