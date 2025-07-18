# My Python AI Sandbox

This is a Python 3.13 project based on Poetry and other Python tools.

# What is included

- [MCP sample Tools](./docs/mcp.md) - add your MCP tools to VSCode and other clients

# Requirements

Note that you will need a Dockerized environment to start containers or activate the dev container.

- Tested with Docker desktop (tested with 4.42.0)

Note: use the SSH URL to access clone this repository, not a HTTPS one (otherwise the Git client included in the devcontainer will complain) (e.g., for example this is fine: `git@github.com:scalasm/my-python-ai-kata.git`).

# How to run

While you can run this with whatever IDE you prefer, a [DevContainer configuration](https://hub.docker.com/r/microsoft/devcontainers-python) is included so that you can use [VSCode support for DevContainers](https://code.visualstudio.com/docs/devcontainers/containers).

- Folders on your computer that will mounted inside the DevContainer:
  - `$HOME/.ssh` - SSH keys (required if cloned this repository using SSH)
  - `$HOME/.gitconfig` - shared configuration files
  - `$HOME/.cache` - for your Hugging Face models (and Python package caches)

The DevContainer will also spin up a Python virtual even with all the required dependencies installed. You use [Poetry commands](https://python-poetry.org/docs/cli/) to add or update dependencies later on.

So, after first spinning up your dev environment, you will immediately be able to run the application main entrypoint through the command `my-python-ai-kata`:

```bash
my-python-ai-kata-py3.13vscode ➜ /workspaces/my-python-ai-kata (main) $ clai
My Python AI Sandbox is ready.
```

# Command refences

Using nox with venv is a bit tricky, so I wrapped recurring commands in the following since I always forget about them!

## Run tests

```bash
./tests.sh
```

## Run pre-commit checks

This will run all code quality checks:

```bash
./pre-commit.sh
```

## Type checking

We use [Pyright](https://github.com/microsoft/pyright) for static type checking. To run type checks:

```bash
npx pyright
```

Or use the VSCode Pyright extension for inline feedback.

# Instructions

If you are a developer (or an AI coding agent!) looking for guidance about the project organization, goals, and conventions, read [docs](./docs/instructions.md).

# Docker support

See [running-postgres-in-docker.md](./docs/running-postgres-in-docker.md) - it is useful if you want to spin up a postgres database quickly.
