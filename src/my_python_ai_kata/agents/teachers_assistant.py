#!/usr/bin/env python3
"""
# 📁 Teacher's Assistant Strands Agent

A specialized Strands agent that is the orchestrator to utilize sub-agents and tools at its disposal to answer a user query.

## What This Example Shows

"""

from strands import Agent
from strands.types.tools import AgentTool

from my_python_ai_kata.agents.staff.english_assistant import english_assistant
from my_python_ai_kata.agents.staff.math_assistant import math_assistant
from my_python_ai_kata.agents.staff.computer_science_assistant import computer_science_assistant
from my_python_ai_kata.agents.staff.language_assistant import language_assistant
from my_python_ai_kata.agents.staff.no_expertise import general_assistant

from my_python_ai_kata.agents.model import ModelConfig, get_or_create_ai_model


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


def get_teacher_agent(tools: list[AgentTool]) -> Agent:
    """This agent coordinates between various subject-specific agents to provide comprehensive assistance.

    Args:
        tools (list[AgentTool]): A list of tools (agents) to be used by the teacher agent.

    Returns:
        Agent: The teacher agent instance.
    """

    model = get_or_create_ai_model(ModelConfig.from_environment())

    # Create a file-focused agent with selected tools
    teacher_agent = Agent(
        system_prompt=TEACHER_SYSTEM_PROMPT,
        callback_handler=None,
        tools=tools,
        model=model
    )

    return teacher_agent


def start_interactive_session(teacher_agent: Agent) -> None:
    """Starts an interactive session with the Teacher's Assistant agent.

    Args:
        teacher_agent (Agent): The Teacher's Assistant agent instance.
    """
    print("\n📁 Teacher's Assistant Strands Agent 📁\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate specialist.")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = teacher_agent(
                user_input,
            )

            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")


# Example usage
if __name__ == "__main__":
    # Use local Strands Agents as tools for the main Teacher Assistant
    tools: list[AgentTool] = [math_assistant, language_assistant, english_assistant, computer_science_assistant, general_assistant]
    teacher_agent = get_teacher_agent(tools)
    start_interactive_session(teacher_agent)
