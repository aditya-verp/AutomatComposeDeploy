# Automated Deployment Script README

## Overview
This script automates the deployment of Dockerized applications by monitoring updates in Git repositories, pulling those updates, and managing Docker containers through Docker Compose. It is designed to run continuously, checking for updates at configurable intervals.
## Features
- **Automated Pulls**: Automatically pulls the latest changes from the specified Git repositories.
- **Docker Compose Integration**: Utilizes Docker Compose to manage container deployments.
- **Change Detection**: Only redeploys if changes are detected in the `docker-compose.yml` or `.yaml` files within the repositories.
- **Exception Handling**: Attempts recovery actions if initial deployment fails, based on predefined exception conditions.
- **Configurable Schedule**: Runs deployment checks at intervals configured in `config.yaml`.
- **Secure**: Does not log sensitive information like Git URLs.

## Directory Structure
```deployment-script/
│
├── autodeploy/                  # Central folder for all deployment-related activities
│   ├── example_repo/            # Each cloned Git repository
│   │   ├── docker-compose.yml   # Docker Compose file for the repository
│   │   └── ...                  # Other repository files
│   │
│   ├── another_repo/            # Another repository
│   │   ├── docker-compose.yml
│   │   └── ...
│   │
├── config.yaml                  # Configuration file for the deployment script
│
└── gitcloner.sh         # Main Python script for deployment
└── deployment_script.py
```
## Initial Setup

1. **Clone the Deployment Script Repository**: Start by cloning this deployment script repository to your local machine.
    ## NOTE: You can use gitcloner to clone multiple repositories.
    ```bash
    git clone [URL-to-this-repository] deployment-script
    cd deployment-script
    ```

2. **Create the Autodeploy Folder**: Within the cloned repository, create an `autodeploy` folder. This will serve as the central point for all deployment-related activities.

    ```bash
    mkdir autodeploy
    ```

3. **Clone Repositories**: Clone each of your Git repositories into the `autodeploy` folder. Ensure each repository contains a Docker Compose file configured as needed for deployment.

    ```bash
    cd autodeploy
    git clone [URL-to-your-repository] example_repo
    # Repeat for other repositories as needed
    ```

4. **Configure Docker Compose**: In the Docker Compose file of each repository, specify the full path to the `autodeploy` directory in the volumes section. This ensures the script has the necessary access to manage Docker services.

    ```yaml
    services:
      app:
        volumes:
          - /full/path/to/deployment-script/autodeploy:/app
    ```
## Configuration Guide

### Config.yaml File
Create and edit the `config.yaml` file located in the `deployment-script` folder. This file controls various parameters of the script:

#### Schedule
Set the interval at which the script will check for updates in the repositories.
```yaml
schedule:
  interval_minutes: 5  # Example: checks every 5 minutes

#### Repositories
Define the paths to your local Git repositories and their respective Docker Compose files. Use the format ./autodeploy/git-repo-name for the repository paths to ensure proper directory referencing.
```gitrepo_path:
     example_repo:
      path: "./autodeploy/example_repo"  # Relative path to the Git repository within autodeploy
      compose_path: "./autodeploy/example_repo/docker-compose.yml"  # Relative path to the Docker Compose file 
```
#### Note (do not commit the autodeploy directory ):
Ensure that all paths in gitrepo_path and compose_path are specified as relative paths, to maintain the script's flexibility and ease of configuration across different environments.
The config.yaml file must be located in the deployment-script directory to be properly read by the script.




