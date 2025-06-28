import yaml
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from echo_logger import log_agent_activation

PRESSURE_PATH = os.path.join(os.path.dirname(__file__), '../memory/MOTIF_PRESSURE.yaml')
GOALS_PATH = os.path.join(os.path.dirname(__file__), '../memory/GOALS.yaml')

class CuriosityAgent:
    def __init__(self, pressure_threshold=3):
        self.pressure_threshold = pressure_threshold
        self.motif_pressure = self.load_yaml(PRESSURE_PATH).get('motif_pressure', {})
        self.goals = self.load_yaml(GOALS_PATH).get('goals', [])
        self.active_goal_tags = self.get_active_goal_tags()

    def load_yaml(self, path):
        if not os.path.exists(path):
            print(f"⚠️  Missing file: {path}")
            return {}
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def get_active_goal_tags(self):
        tags = []
        for goal in self.goals:
            if goal.get('status') == 'active':
                tags.extend(goal.get('trigger_tags', []))
        return set(tags)

    def generate_questions(self):
        questions = []
        for tag, count in self.motif_pressure.items():
            if count >= self.pressure_threshold and tag not in self.active_goal_tags:
                questions.append(
                    f"You've engaged frequently with the motif '{tag}'. "
                    f"What unresolved insight or tension might it represent?"
                )
        return questions

if __name__ == '__main__':
    agent = CuriosityAgent()
    questions = agent.generate_questions()
    if questions:
        print("\n🤔 CuriosityAgent — Symbolic Questions:")
        for q in questions:
            print(f"• {q}")
    else:
        print("\n✅ No unresolved high-pressure motifs outside active goals.")
