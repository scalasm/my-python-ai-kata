# Architecture guidelines

This is a Python project managed through poetry management tool - see `pyproject.toml` for dependency configuration, project metadata, and tools conflgurations like flake8.

nox and nox-poetry are used for running lifecycle operations like linting, tests, and pre-commit hooks:

- `noxfile` - it is the test automation for different scenarios, including linting, precommit hooks, ...
- other `dot files` required for tools configuration (e.g., code quality tools)

# Goal

The source code is a sandbox for dealing with AI agents using standard python libraries and best practices.

An important topic is MCP (Model context Protocol) - the functionalities we may develop here are to be exposed according to this standard using [fastmcp](https://github.com/modelcontextprotocol/python-sdk).

# Source code and folder structure

The git repository is https://github.com/scalasm/my-python-ai-kata - we use it for issue management and PR too.

Refer to `pyproject.toml` for source and test folders.

- Apply python best practices and follow source code linting configuration referred there and in other dedicated configuration files like `.flake8` or `.darglint`
- `my_python_ai_kata` is the root package
