"""Interactive conversation loop with the CuriosityAgent."""

import traceback
from echo_core.memory.alignments import log_alignment
from echo_core.agents.curiosity import CuriosityAgent
from echo_core.utils.echo_logger import log_agent_activation

import sys
import os
import traceback
from memory.alignments import log_alignment

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.curiosity import CuriosityAgent
from echo_logger import log_agent_activation

def main():
    print("\n🧠 [ECHO] Entering conversational mode...")
    try:
        log_agent_activation("CuriosityAgent", action="invoked", reason="user_requested_conversation")

        curiosity = CuriosityAgent()
        questions = curiosity.generate_questions()

        try:
            curiosity.log_questions(questions)
        except Exception as e:
            print(f"⚠️ Could not log questions: {e}")

        if not questions:
            print("❌ No questions generated.")
            return

        print("\n🤖 ECHO has some questions for you:\n")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")

        while True:
            response = input("\n✍️  Would you like to answer a question? (y/n): ").strip().lower()
            if response != 'y':
                break

            try:
                idx = int(input("Which question number? ").strip()) - 1
                if idx < 0 or idx >= len(questions):
                    print("⚠️ Invalid question number.")
                    continue

                insight = input("Enter your symbolic insight or reflection: ").strip()
                try:
                    curiosity.log_user_response(questions[idx], insight)
                except Exception as e:
                    print(f"⚠️ Failed to log response: {e}")
                else:
                    print("✅ Response logged to curiosity log.")
                log_alignment(
                    interaction={
                        'summary': 'Conversation answer',
                        'content': insight,
                    },
                    mirrored_tags=[questions[idx].get('motif')],
                    reasoning_path=['conversation', 'question_response'],
                    agent_activations=['CuriosityAgent'],
                    score=5.0,
                    notes='Logged from echo_converse'
                )

            except Exception as e:
                print(f"⚠️ Error during input: {e}")
                continue

    except Exception as e:
        print(f"🚨 Fatal error in ECHO conversation loop: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
