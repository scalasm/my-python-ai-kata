# School Staff 

This is a collection of specialized agents for a school staff.

It is based on the [Amazon Strands Multi-Agent example](https://github.com/strands-agents/docs/blob/main/docs/examples/python/multi_agent_example/index.md), which has been adapted to my needs.

The idea is to have to enough agents for playing with multi-agent workflows.


## Quick refs

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


# Example prompts

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