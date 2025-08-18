# General guidelines
- Stick to the goal of the task - do not try to do wide refactorings of the codebase, only modify what is strictly in scope for change.
- if you don't know a good answer, just do nothing, and say you don't know the answer.

# Version control
When creating a new PR on GitHub, please ensure that you follow these steps:

- create the local branch from the `main` branch
- ensure that the branch name is descriptive and follows the naming conventions (e.g., `feature/description`, `bugfix/description`, `hotfix/description`)
- commit your changes with a clear and concise commit message
- push your branch to the remote repository
- create a pull request against the `main` branch
- ensure that the PR description is clear and provides context for the changes made

# Python standards
- You are a Python software engineer, and you are building AI-powered applications.
- Apply modern python conventions and coding idioms (Python >= 3.11).
- OpenAI and Amazon Strands Agents are the main libraries we use.
- Use Type hints for local variables, as well as function parameters, return types, and class attributes
- Prefer f-strings over other string formatting methods.
- Use dataclasses for simple data containers.
- ensure code is linted and styled according to PEP8 standard - also include the settings specifics to this project, see `pyproject.toml`
- Create unit tests using `pytest`
  - Create parameterized tests using `pytest.mark.parametrize`
  - unit tests are to be created in the same package name as the original code but under `test/` directory
  - test files should be named `test_*.py` to ensure they are recognized by pytest
  - for example, the test file for `src/my_python_ai_kata/agents/model.py` should be located at `test/agents/test_model.py`
  - ensure code coverage according to project settings
  - for test classes and functions, add a succinct docstring to explain the purpose of the test.
  - use Python type hints when writing test code as well.
