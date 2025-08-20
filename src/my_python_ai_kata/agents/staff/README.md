# School Staff with Strands Agents

This is a collection of specialized agents for a school staff.

It is based on the [Amazon Strands Multi-Agent example](https://github.com/strands-agents/docs/blob/main/docs/examples/python/multi_agent_example/index.md), which has been adapted to my needs.

The idea is to have to enough agents for playing with multi-agent workflows.

The teacher assistant can be run in two ways
 - **Pure Strands Agents** - see `teachers_assistant.py` - coordinator and specialist agents start within the same process.
 - **A2A and Strands Agents** - see `teachers_assistant_a2a.py`, like above abut the agents are separate processes and talk to each other through the A2A protocol.

# Quick refs for Pure Strands Agents

Just run `teachers_assistant.py` .

# Quick refs for A2A and Strands Agents

Each agent has a [agent-card.json](http://127.0.0.1:9000/.well-known/agent-card.json) available when started.

Agent servers need to be started separetely before you can run `Run TeachAssist (A2A)` (`teachers_assistant_a2a.py`) application. So open a terminal and launch each of them. For example: 
```shell
(my-python-ai-kata-py3.13) vscode ➜ /workspaces/my-python-ai-kata (agenti-ai-with-strands) $ math_assistant 
INFO:strands.multiagent.a2a.server:Strands' integration with A2A is experimental. Be aware of frequent breaking changes.
INFO:strands.multiagent.a2a.server:Starting Strands A2A server...
INFO:     Started server process [79019]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9001 (Press CTRL+C to quit)
INFO:     127.0.0.1:35102 - "GET /.well-known/agent-card.json HTTP/1.1" 200 OK
```

See `pyproject.toml` for the different startup scripts available to you (or you can run them in Debug mode).

Then you can run `teachers_assistant_a2a.py`.

# Example prompts

*Just some example prompts that will help routing messages to the specialists.*

This one will trigger the assistant to consult the English Language specialist agent:
```
What are the three most famous narrative poems by William Shakespeare, the famous english writer from the renaissance? Provide a summary of each within the 1000 characters each.
```

This prompt will involve the math agent:
```
Can you explain me the mathematical meaning of an equation, and give me two examples of real world applications? Stay under 2000 characters.
```

This will force the Teacher's Assistant to involve more tools available to it:
```
list the titles of up to 10 most famous narrative poems by William Shakespeare, and then suggest an efficient algorithm for sorting the titles, and implement a Python program that prints the sorted titled on the console.
Take advantage of the specialists available to you.
```

Some other prompts to try:

```
Use your math skills to compute the square root of 200?

explain me the geometric meaning of the the equation ax^2 + bx + c = 0

write a python "hello world" program - then translate it into javascript so that it can be run on nodejs 20+ runtime

use your computer science expert to write a python program called `my_adder.py` that can be run from the command line (linux) and print the sum of two integer numbers provided on the command line. An example execution: `python my_adder.py 5 5` must print `10`
```