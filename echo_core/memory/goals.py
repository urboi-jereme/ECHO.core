from pathlib import Path
from echo_core.utils.yaml_utils import load, dump

GOALS_PATH = Path(__file__).resolve().parent / 'GOALS.yaml'


def load_goals():
    data = load(GOALS_PATH, fallback={'goals': []})
    return data.get('goals', [])


def save_goals(goals):
    dump({'goals': goals}, GOALS_PATH)
    print("✅ GOALS.yaml updated successfully.")


def update_goal_status(goal_name, new_status):
    goals = load_goals()
    for goal in goals:
        if goal['goal'] == goal_name:
            goal['status'] = new_status
            break
    save_goals(goals)
    return goals
