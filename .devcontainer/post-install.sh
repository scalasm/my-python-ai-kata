#!/bin/bash
set -ex

# Convenience workspace directory for later use
WORKSPACE_DIR=$(pwd)

##
## Create some aliases
##
echo 'alias ll="ls -alF"' >> ${HOME}/.bashrc
echo 'alias la="ls -A"' >> ${HOME}/.bashrc
echo 'alias l="ls -CF"' >> ${HOME}/.bashrc
# Create the postgres data dir symlink if needed
if [ ! -L "${WORKSPACE_DIR}/postgres-data" ]; then
  ln -s "${HOME}/.cache/postgres-data" "${WORKSPACE_DIR}/postgres-data"
fi

# Change some Poetry settings to better deal with working in a container
poetry config cache-dir ${HOME}/.cache
poetry config virtualenvs.in-project true

# Now install all dependencies
poetry install

# The inspector is a useful debugging tool for the Model Context Protocol
npm install @modelcontextprotocol/inspector -g

# Install Pyright for type checking
npm install -g pyright

echo "Done!"
