# My Python AI Sandbox

This is a Python 3.12 project based on Poetry and other Python tools.

# Requirements

- Docker desktop (tested with 4.39.0)
- Folders on your computer that will mounted inside the DevContainer:
  - `$HOME/.ssh` - SSH keys (required if cloned this repository using SSH)
  - `$HOME/.gitconfig` - shared configuration files
  - `$HOME/.cache` - for your Hugging Face models (and Python package caches)

Note: use the SSH URL to access clone this repository, not a HTTPS one (otherwise the Git client included in the devcontainer will complain):
 - This  `git@github.com:scalasm/my-python-ai-kata.git`

# How to run

While you can run this with whatever IDE you prefer, a [DevContainer configuration](https://hub.docker.com/r/microsoft/devcontainers-python) is included so that you can use [VSCode support for DevContainers](https://code.visualstudio.com/docs/devcontainers/containers).

The DevContainer will also spin up a Python virtual even with all the required dependencies installed. You use [Poetry commands](https://python-poetry.org/docs/cli/) to add or update dependencies later on.

So, after first spinning up your dev environment, you will immediately be able to run the application main entrypoint through the command `my-python-ai-kata`:
```bash
arch-ai-sandoox-py3.12vscode ➜ /workspaces/my-python-ai-kata (main) $ my-python-ai-kata 
My pyAI Sandbox is ready.
```

# CL(A)I 
We also provide a basic CLI wrapper (which should be the standard way to run these simple features), see [the documentation](./docs/clai.md).

# Project structure

- `pyproject.toml` - this is Poetry configuration file, where names, scripts, runtime/build dependencies are needed
- `src` - it is the where the package source code is, with `my_python_ai_kata` being the root package
- `tests` - it is where the test source code goes
- `noxfile` - it is the test automation for different scenarios, including linting, precommit hooks, ... 
- other `dot files` required for tools configuration (e.g., code quality tools) 


# Docker support

See [running-postgres-in-docker.md](./docs/running-postgres-in-docker.md).
