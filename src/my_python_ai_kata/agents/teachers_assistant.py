#!/usr/bin/env python3
"""
# 📁 Teacher's Assistant Strands Agent

A specialized Strands agent that is the orchestrator to utilize sub-agents and tools at its disposal to answer a user query.

## What This Example Shows

"""
import os
import logging
import tomllib
from typing import Any

from strands import Agent
from strands.types.tools import AgentTool
from strands.agent.conversation_manager import ConversationManager

from my_python_ai_kata.agents.staff.english_assistant import english_assistant
from my_python_ai_kata.agents.staff.math_assistant import math_assistant
from my_python_ai_kata.agents.staff.computer_science_assistant import computer_science_assistant
from my_python_ai_kata.agents.staff.language_assistant import language_assistant
from my_python_ai_kata.agents.staff.no_expertise import general_assistant

from my_python_ai_kata.agents.model import ModelConfig, get_or_create_ai_model

logger = logging.getLogger(__name__)

# Define a focused system prompt for file operations
TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, a sophisticated educational orchestrator designed to coordinate educational support across multiple subjects. Your role is to:

1. Analyze incoming student queries and determine the most appropriate specialized agent to handle them:
   - Math Agent: For mathematical calculations, problems, and concepts
   - English Agent: For writing, grammar, literature, and composition
   - Language Agent: For translation and language-related queries
   - Computer Science Agent: For programming, algorithms, data structures, and code execution
   - General Assistant: For all other topics outside these specialized domains

2. Key Responsibilities:
   - Accurately classify student queries by subject area
   - Route requests to the appropriate specialized agent
   - Maintain context and coordinate multi-step problems
   - Ensure cohesive responses when multiple agents are needed

3. Decision Protocol:
   - If query involves calculations/numbers → Math Agent
   - If query involves writing/literature/grammar → English Agent
   - If query involves translation → Language Agent
   - If query involves programming/coding/algorithms/computer science → Computer Science Agent
   - If query is outside these specialized areas → General Assistant
   - For complex queries, coordinate multiple agents as needed

Always confirm your understanding before routing to ensure accurate assistance.
"""


def get_teacher_agent(tools: list[AgentTool], conversation_manager: ConversationManager | None) -> Agent:
    """This agent coordinates between various subject-specific agents to provide comprehensive assistance.

    Args:
        tools (list[AgentTool]): A list of tools (agents) to be used by the teacher agent.
        conversation_manager (ConversationManager): The conversation manager instance.

    Returns:
        Agent: The teacher agent instance.
    """
    model = get_or_create_ai_model(ModelConfig.from_environment())

    # Create a file-focused agent with selected tools
    teacher_agent = Agent(
        name="Teacher's Assistant",
        description="A specialized assistant that routes queries to the appropriate subject-specific agents.",
        system_prompt=TEACHER_SYSTEM_PROMPT,
        callback_handler=None,
        tools=tools,
        model=model,
        conversation_manager=conversation_manager,
    )

    return teacher_agent


def load_config() -> dict[str, Any]:
    """Load configuration from config/config.toml.

    Returns:
        dict[str, Any]: The loaded configuration.
    """
    config_dir: str = os.environ.get("CONFIG_DIR", "./config")
    config_path: str = os.path.join(config_dir, "config.toml")
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def configure_logging() -> None:
    """Configure logging from config/config.toml."""
    try:
        config = load_config()
        log_level = config.get("logging", {}).get("level", "INFO").upper()
        logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
        logging.getLogger().setLevel(getattr(logging, log_level))
    except Exception:
        logging.basicConfig(level=logging.INFO)


def start_interactive_session(teacher_assistant_agent: Agent) -> None:
    """Starts an interactive session with the Teacher's Assistant agent.

    Args:
        teacher_assistant_agent (Agent): The Teacher's Assistant agent instance.
    """
    configure_logging()

    print("\n📁 Teacher's Assistant Strands Agent 📁\n")
    print("✅ Ask a question in any subject area, and I'll route it to the appropriate specialist.")
    print("✅ Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\n✅ Goodbye! 👋")
                break

            response = teacher_assistant_agent(
                user_input,
            )

            # Extract and print only the relevant content from the specialized agent's response
            # content = response.message
            logger.debug(f"Response from {teacher_assistant_agent.name}: {str(response)}")
            # all_text = ''.join(
            #     item.get('text', '') for item in content['content']
            # )
            # logger.info(f"✅ {all_text}")
            # print(all_text)

        except KeyboardInterrupt:
            print("\n\n✅ Execution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"❌ An error occurred in {teacher_assistant_agent.name}. Please, try asking a different question: {str(e)}")


def start_teacher_agent() -> None:
    """Starts the Teacher's Assistant agent with local specialist agents."""
    tools: list[AgentTool] = [math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant]
    teacher_agent = get_teacher_agent(tools, conversation_manager=None)
    start_interactive_session(teacher_agent)


# Example usage
if __name__ == "__main__":
    start_teacher_agent()
