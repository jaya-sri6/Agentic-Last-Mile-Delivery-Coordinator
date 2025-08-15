import argparse
import sys
import os

# Add the project root to the Python path to resolve import issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.coordinator import Coordinator

def main():
    """
    Main entry point for the Project Synapse application.
    This function parses command-line arguments and runs the coordinator agent.
    """
    parser = argparse.ArgumentParser(description="Project Synapse - Autonomous Last-Mile Disruption Resolution")
    parser.add_argument(
        "scenario",
        type=str,
        help="A natural language description of the disruption scenario to resolve.",
    )
    parser.add_argument(
        "--mock-llm",
        action="store_true",
        help="Use a mock LLM for testing without an API key.",
    )
    args = parser.parse_args()

    print("--- Starting Project Synapse ---")
    print(f"Received disruption scenario: '{args.scenario}'")
    if args.mock_llm:
        print("--- RUNNING IN MOCK LLM MODE ---")
    print("-" * 20)

    try:
        # Initialize the coordinator agent
        coordinator = Coordinator(use_mock_llm=args.mock_llm)

        # Handle the disruption
        result = coordinator.handle_disruption(args.scenario)

        print("-" * 20)
        print("--- Resolution Complete ---")
        print("Final output from the agent:")
        print(result.get("output"))

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure the OPENAI_API_KEY is set as an environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
