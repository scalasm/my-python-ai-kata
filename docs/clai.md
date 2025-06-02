# CLI for AI commands

There is a prototype CLI that allows to expose features on the command line.

# How to
In your environment your will have the `clai` command (yeah, we have a great sense of humour here!).

The commands should be self documented so feel free to use `--help` option:
```bash
arch-ai-sandoox-py3.12vscode ➜ /workspaces/my-python-ai-kata (main) $ clai
Usage: clai [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  images  AI Generated images
arch-ai-sandoox-py3.12vscode ➜ /workspaces/my-python-ai-kata (main) $ 
```

So far, `clai` offers the following command groups:
- `images` - to deal with image generation

Others will be added in the future.

# References

- [Click and Python: Build Extensible and Composable CLI Apps](https://realpython.com/python-click/)
- [Commands and Groups](https://click.palletsprojects.com/en/stable/commands/)