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
```
/AutomatComposeDeploy
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
    ```bash
    git clone [URL-to-this-repository] AutomatComposeDeploy
    cd AutomatComposeDeploy

    ```

2. **Create the Autodeploy Folder**: Within the cloned repository, create an `autodeploy` folder. This will serve as the central point for all deployment-related activities.

    ```bash
    mkdir autodeploy
    ```

3. **Clone Repositories**: Clone each of your Git repositories into the `autodeploy` folder. Ensure each repository contains a Docker Compose file configured as needed for deployment.
    ### NOTE: You can use gitcloner to clone multiple repositries.
    ```bash
    cd autodeploy
    git clone [URL-to-your-repository] example_repo
    # Repeat for other repositories as needed
    # Setup the .env as their respected repository
    ```

4. **Configure Docker Compose**: In the Docker Compose file of each repository, specify the full path to the `autodeploy` directory in the volumes section to avoid conflicts. This ensures the script has the necessary access to manage Docker services.

    ```yaml
    services:
      app:
        volumes:
          - /full/path/to/AutomatComposeDeploy/autodeploy:/app
    ```
5. **Configure config.yaml**: Create and edit the config.yaml file located in the deployment-script folder. which contains information about Git repository paths, success conditions, and exception conditions.

6. **Setup is Compleated** Now You can run the 'docker compose up -d' to run the AutomatComposeDeploy Service and check the logs.


## Configuration Guide - Config.yaml File: 
This file controls various parameters of the script:

- **Schedule**: Set the interval at which the script will check for updates in the repositories.
- **gitrepo_path**: Define the paths to your local Git repositories and their respective Docker Compose files. Use the format ./autodeploy/git-repo-name for the repository paths to ensure proper directory referencing. This is Must condition to script to fetch the repositories
```yaml
schedule:
  interval_minutes: 5  # Example: checks every 5 minutes

#### Repositories
```gitrepo_path:
     example_repo:
      path: "./autodeploy/example_repo"  # Relative path to the Git repository within autodeploy
      compose_path: "./autodeploy/example_repo/docker-compose.yml"  # Relative path to the Docker Compose file 
```

### Config - Conditions Logic
- **Check for Changes**: For each Git repository, it checks if there are any changes in the Docker Compose file.
- **Execute Docker Compose**: If changes are detected, it attempts to bring up the services defined in the Docker Compose file using docker-compose up .
- **Success Condition**: If the docker-compose up command succeeds and specific keywords are not found in the output, it considers the operation successful and moves to the next repository.
- **Exception Conditions**: If the docker-compose up command fails or specific keywords in Exception and it found in the output, it tries exception conditions command execution and retries docker-compose up and 
  success condition checks for each exception condition until either a condition succeeds or all conditions are exhausted.




#### Note :
Ensure that all paths in gitrepo_path and compose_path are specified as relative paths, to maintain the script's flexibility and ease of configuration across different environments.
The config.yaml file must be located in the deployment-script directory to be properly read by the script.

- Always check the Logs and if you found any error related to file not found please recheck the directory structure which you have configured
- **Example Logs** - (troubleshooting: In this Logs script can't find the docker compose file , now you need to correct the path in the config.yaml)
![image](https://github.com/aditya-verp/AutomatComposeDeploy/assets/124437522/88bece98-c5f5-4095-8fe3-44a25a525a56)






