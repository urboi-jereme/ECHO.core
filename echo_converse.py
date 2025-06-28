import sys
import os
import traceback

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agents.curiosity_agent import CuriosityAgent
from echo_logger import log_agent_activation

def main():
    print("\n🧠 [ECHO] Entering conversational mode...")
    try:
        log_agent_activation("CuriosityAgent", action="invoked", reason="user_requested_conversation")

        curiosity = CuriosityAgent()
        questions = curiosity.generate_questions()

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
                curiosity.log_user_response(questions[idx], insight)
                print("✅ Response logged.")

            except Exception as e:
                print(f"⚠️ Error during input: {e}")
                continue

    except Exception as e:
        print(f"🚨 Fatal error in ECHO conversation loop: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
