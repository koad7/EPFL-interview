# resslab-tools

## Development

### Prerequisites

Prerequisites:

- [Python](https://www.python.org/) 3.9
- [Make](https://www.gnu.org/software/make/)
- [Poetry](https://python-poetry.org/)
- [Node.js](https://nodejs.org/) 16.x
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/) 1.27.0+

### Secrets

An environment file should be created (see all available keys in `backend/resslab_tools/config.py`):

```bash
mkdir -p secrets && echo POSTGRES_PASSWORD=changeit > secrets/.env
```

### Installation

```bash
make install
```

### Run for development

#### CLI

```bash
make run-database
# postgresql://127.0.0.1:5432

make run-backend
# http://127.0.0.1:8000

make run-frontend
# http://127.0.0.1:8080
```

#### Visual Studio Code

Run configurations are in `.vscode`: https://code.visualstudio.com/docs/editor/debugging

### Data

Populate data to database

```bash
make upload-data
```

## Generate API for frontend

Folder frontend/src/backend is generated from backend API. It should be updated when the backend api changes.

```bash
# update generated files (requires Java installed)
make generate-api
```

## Deployment

### Locally with Docker Compose

```bash
make deploy-local
```

### Server

Deployed on http://enacvm0070.xaas.epfl.ch/

Prerequisites:

- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

```bash
# Install on new server
make install-server

# Deploy
make deploy-prod
```
