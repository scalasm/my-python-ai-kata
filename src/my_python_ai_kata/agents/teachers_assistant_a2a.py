"""Teacher's Assistant (A2A)"""

import logging
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider  # type: ignore

from my_python_ai_kata.agents.staff.english_assistant import get_english_assistant
from my_python_ai_kata.agents.staff.math_assistant import get_math_assistant
from my_python_ai_kata.agents.staff.computer_science_assistant import get_computer_science_assistant
from my_python_ai_kata.agents.staff.language_assistant import get_language_assistant
from my_python_ai_kata.agents.staff.no_expertise import get_general_assistant

from my_python_ai_kata.agents.teachers_assistant import get_teacher_agent, start_interactive_session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_english_assistant() -> None:
    english_assistant = A2AServer(agent=get_english_assistant(), serve_at_root=True)
    english_assistant.serve(port=9000, app_type="fastapi")


def start_math_assistant() -> None:
    math_assistant = A2AServer(agent=get_math_assistant(), serve_at_root=True)
    math_assistant.serve(port=9001, app_type="fastapi")


def start_computer_science_assistant() -> None:
    computer_science_assistant = A2AServer(agent=get_computer_science_assistant(), serve_at_root=True)
    computer_science_assistant.serve(port=9002, app_type="fastapi")


def start_language_assistant() -> None:
    language_assistant = A2AServer(agent=get_language_assistant(), serve_at_root=True)
    language_assistant.serve(port=9003, app_type="fastapi")


def start_general_assistant() -> None:
    general_assistant = A2AServer(agent=get_general_assistant(), serve_at_root=True)
    general_assistant.serve(port=9004, app_type="fastapi")


if __name__ == "__main__":
    # Step 1. Start the individual assistants using CLI
    # start_english_assistant()
    # start_math_assistant()
    # start_computer_science_assistant()
    # start_language_assistant()
    # start_general_assistant()

    # Step 2. Run this client
    provider = A2AClientToolProvider(known_agent_urls=[
        "http://localhost:9000",
        "http://localhost:9001",
        "http://localhost:9002",
        "http://localhost:9003",
        "http://localhost:9004"
    ])

    # Use local Strands Agents as tools for the main Teacher Assistant
    teacher_agent = get_teacher_agent(provider.tools)
    start_interactive_session(teacher_agent)
