# Running Postgres inside your Docker container

A `compose.yml` file is used for starting required services from within the Dev container.

```bash
docker compose up
```

(You could use `-d` if to start it as a daemon but do not forget to shut docker-compose down later)

# How it is implemented

We use [Docker-outside-Docker apprach](https://github.com/devcontainers/features/tree/main/src/docker-outside-of-docker) since we want to reuse the Docker desktop system.

This has issues about folders and paths to keep in synch between the container and the host operating system (see the documentation).

In addition, we require a Docker Desktop daemon (or equivalent) running - so maybe a better option would be to run an internal Docker daemon, using the [Docker-in-Docker](https://github.com/devcontainers/features/tree/main/src/docker-in-docker) approach instead.

Both approaches have pros and cons, so it will take some time to figure out what really works for us
