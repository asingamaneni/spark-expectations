# Developer Setup Guide

This guide walks you through setting up a local development environment for spark-expectations.

---

## Prerequisites

### Python

| | |
|---|---|
| **Supported versions** | 3.9, 3.10, 3.11, 3.12, 3.13 |
| **Recommended** | Latest 3.12.x |

```sh
python3 --version
```

Install Python from [python.org](https://www.python.org/downloads/) or use a version manager such as [pyenv](https://github.com/pyenv/pyenv).

### Java

| | |
|---|---|
| **Supported versions** | 8, 11, 17 |
| **Recommended** | Latest 17.x |

Use a JDK version manager such as [SDKMAN!](https://sdkman.io/) or [OpenJDK](https://openjdk.org/) (Linux/macOS) to install and manage Java versions. If your tools require it, set the `JAVA_HOME` environment variable to point to your installed JDK.

### Hatch

[Hatch](https://hatch.pypa.io/latest/) is used for Python environment and dependency management.

```sh
# macOS
brew install hatch
```

### Docker

A container engine is required for running integration tests. You can use Docker, Podman, containerd, Rancher, or any equivalent container runtime.

### IDE

**Recommended:** [Visual Studio Code](https://code.visualstudio.com/) | **Alternative:** [PyCharm](https://www.jetbrains.com/pycharm/)

---

## GitHub Configuration

You need a GitHub account to access the source code and documentation.

### GPG and SSH Keys

- **GPG** — for signing commits and tags. See [GitHub Docs: Generate a GPG Key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key).
- **SSH** — for connecting to remote repositories. See [GitHub Docs: Generate an SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

### Clone the Repository

```sh
git clone git@github.com:Nike-Inc/spark-expectations.git
cd spark-expectations
```

---

## Environment Setup

We recommend using a version manager:

- [pyenv](https://github.com/pyenv/pyenv) — Python version manager
- [asdf](https://github.com/asdf-vm/asdf) — multi-language version manager ([supported plugins](https://github.com/asdf-vm/asdf-plugins))

### Install Python with pyenv

```sh
pyenv install -l | less       # List available versions
pyenv install 3.12.11         # Install a specific version
pyenv versions                # List installed versions
pyenv global <version>        # Set default for all shells
pyenv local <version>         # Set version for current directory (creates .python-version)
```

### Install Dependencies

All required and optional dependencies are managed via `pyproject.toml`. To initialize the dev environment and install dependencies:

```sh
# Configures Hatch dev environment
# Initializes Python virtual environments (3.10, 3.11, 3.12)
# Installs all dependencies
make dev
```

### Inspect Hatch Environments

View which environments are available and how they are configured:

```sh
hatch env show
```

Hatch creates multiple Python virtual environments under the project root at `.venv/env/virtual/<dev.py3.X>`.

### Troubleshooting Hatch Environments

If you encounter issues, clean and recreate the environment:

```sh
make env-remove-all
# Or manually delete <project_root>/.venv/ directory

# Recreate environments
make dev
```

---

## Running Tests

To execute all spark-expectations tests:

```bash
make cov
```

!!! warning "Docker Required"
    This command spins up Docker containers needed for some tests — make sure Docker is running.
    Check `./containers/kafka/scripts` and test fixtures to understand what is started.

    ```sh
    sh ./containers/kafka/scripts/docker_kafka_start_script.sh
    ```

    This script will build the required Docker image, start a Kafka service, and make it available for integration tests.

### IDE Debugging

??? note "VSCode Interpreter and Launch Config"

    ??? note "settings.json"

        Set the default Python interpreter to the project’s virtual environment:
        ```json
        {
            "python.testing.pytestEnabled": true,
            "python.testing.autoTestDiscoverOnSaveEnabled": true,
            "python.defaultInterpreterPath": ".venv/env/virtual/dev.py3.12/bin/python",
            "terminal.integrated.profiles.osx": {
                "Hatch Shell": {
                    "path": "hatch",
                    "args": ["shell"],
                    "icon": "terminal"
                }
            },
            "terminal.integrated.defaultProfile.osx": "zsh",
            "python.testing.pytestArgs": [
                "--maxfail=1",
                "--disable-warnings"
            ]
        }
        ```

    ??? note "launch.json"

        Debug launch configurations:
        ```json
        {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Coverage: Pytest (All files)",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "coverage",
                    "args": [
                        "run",
                        "--source=spark_expectations",
                        "--omit=examples/*",
                        "-m", "pytest",
                        "-v",
                        "-x"
                    ],
                    "console": "integratedTerminal",
                    "justMyCode": false
                },
                {
                    "name": "Coverage: Pytest (Selected File)",
                    "type": "debugpy",
                    "request": "launch",
                    "module": "coverage",
                    "args": [
                        "run",
                        "--source=spark_expectations",
                        "--omit=examples/*",
                        "-m", "pytest",
                        "-v",
                        "-x",
                        "${file}"
                    ],
                    "console": "integratedTerminal",
                    "justMyCode": false
                }
            ]
        }
        ```

---

## Adding Certificates

To enable trusted SSL/TLS communication during testing, place any required `.crt` files in the `containers/certs` directory. During test container startup, all certificates in this folder are automatically imported into the container’s trusted certificate store.

---

## Deploying Docs Locally

When updating the project documentation, test your changes locally:

```sh
# Install dependencies (if not already done)
make dev

# Deploy the docs server locally
make docs
```
