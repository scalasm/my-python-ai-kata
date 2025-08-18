"""Teacher's Assistant (A2A)"""

import asyncio
import logging
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider  # type: ignore
from strands.agent.conversation_manager import SlidingWindowConversationManager

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
    english_assistant.serve(host="localhost", port=9000, app_type="fastapi")


def start_math_assistant() -> None:
    math_assistant = A2AServer(agent=get_math_assistant(), serve_at_root=True)
    math_assistant.serve(host="localhost", port=9001, app_type="fastapi")


def start_computer_science_assistant() -> None:
    computer_science_assistant = A2AServer(agent=get_computer_science_assistant(), serve_at_root=True)
    computer_science_assistant.serve(host="localhost", port=9002, app_type="fastapi")


def start_language_assistant() -> None:
    language_assistant = A2AServer(agent=get_language_assistant(), serve_at_root=True)
    language_assistant.serve(host="localhost", port=9003, app_type="fastapi")


def start_general_assistant() -> None:
    general_assistant = A2AServer(agent=get_general_assistant(), serve_at_root=True)
    general_assistant.serve(host="localhost", port=9004, app_type="fastapi")


async def start_teacher_assistant() -> None:
    # Step 1. Start the individual assistants using CLI
    # TODO This could be automated by some manager to independently start each process
    # For now I manually need to start the different agents in a terminal.
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

    await provider._discover_known_agents()

    conversation_manager = SlidingWindowConversationManager(
        window_size=10,  # Limit history size
    )

    # Use local Strands Agents as tools for the main Teacher Assistant
    teacher_agent = get_teacher_agent(provider.tools, conversation_manager)
    start_interactive_session(teacher_agent)

if __name__ == "__main__":
    asyncio.run(start_teacher_assistant())
