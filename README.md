# AutomatComposeDeploy - CD Tool

## Overview
This Tool automates the deployment of Dockerized applications by monitoring updates in Git repositories, pulling those updates, and managing Docker containers through Docker Compose. It is designed to run continuously, checking for updates only on the docket compose file in all the configured repositories.
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
├── docker-compose.yaml                  
│
└── gitcloner.sh                 # Main Python script for deployment
└── deployment_script.py
```
## Initial Setup

1. **Clone the Deployment Script Repository**: Start by cloning this deployment script repository to your local machine.
    ```bash
    git clone [URL-to-this-repository] AutomatComposeDeploy
    cd AutomatComposeDeploy

    ```

2. **Create the Autodeploy Folder**: Within the cloned repository, create an `autodeploy` folder. This will serve as the central point for all your Application git repositories for Auto deployment-related activities.

    ```bash
    mkdir autodeploy
    ```

3. **Clone Repositories**: Clone each of your Applicatio Git repositories into the `autodeploy` folder. Ensure each repository contains a Docker Compose file configured as needed for deployment.
    #### NOTE: You can use gitcloner to clone multiple repositries.
    ```bash
    cd autodeploy
    git clone [URL-to-your-repository] example_repo1
    git clone [URL-to-your-repository] example_repo2
    # Repeat for other repositories as needed
    # Setup the .env for the necessary respected repository that used by docker-compose (Optional)
    ```

4. **Configure Docker Compose**: In the Docker Compose file specify the full path to the `autodeploy` directory of the **Host** . In which the cloned repository is there for autodeploy . It Must needed to Mounted as volumes.

    ```yaml
    services:
      app:
        volumes:
          - /full/path/to/AutomatComposeDeploy/autodeploy:/app/autodeploy
    ```
5. **Configure config.yaml**: Create and edit the config.yaml file located in the deployment-script folder. which contains information about Git repository paths, success conditions, and exception conditions.
   
6. **Modifiy the Dockerfile.autodeploy** (Optional): Arguments to define UID, GID, and Docker group GID SameAS -> Host user ids (use `id` command). To Avoid git conflicts.
   
7. `**Setup is Compleated**` Now You can run the 'docker compose up -d' to run the AutomatComposeDeploy Service and check the logs (The Initial logs appear after schedule interval_minutes). First time you need to run your application containers manually because new git changes has already pulled when you cloned.


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

## Git Cloner Script Guide:

The Git Cloner script automates the cloning of Git repositories into a specified directory, handling both public and private repositories by optionally using authentication tokens. This is useful for setting up deployment environments or when managing multiple project repositories.

### Steps to Use the Git Cloner:

1. **Set the Authentication Token**: If you are cloning private repositories that require authentication, you need to provide a personal access token. Replace the `TOKEN=""` line in the script with your personal access token enclosed in quotes.

2. **Configure Repository Details**: List each repository you want to clone in the repos array. Each element should include the repository URL, the branch you want to clone, and a boolean flag indicating whether the token should be used (true for private repositories, false for public repositories).
    `"https://github.com/aditya-verp/example.git main true"`  

3. **Set the Target Directory**: Define the directory where the repositories will be cloned into with TARGET_DIR. This path can be adjusted to any directory where you wish to organize the cloned repositories.





#### Note :
Ensure that all paths in gitrepo_path and compose_path are specified as relative paths, to maintain the script's flexibility and ease of configuration across different environments.
The config.yaml file must be located in the deployment-script directory to be properly read by the script.
- **doker login auth error (solution)**: While doing docker login in the container need to mount the docker socket for non-root user.
   - Example: `"docker run -v /run/user/1001/docker.sock:/var/run/docker.sock:ro -v /usr/bin/docker:/usr/bin/docker --rm -i public.ecr.aws/aws-cli/aws-cli ecr get-login-password --region eu-west-3 | docker login -u AWS --password-stdin 880947752174.dkr.ecr.eu-west-3.amazonaws.com"`
- Always check the Logs and if you found any error related to file not found please recheck the directory structure which you have configured
- **Example Logs** -
![image](https://github.com/aditya-verp/AutomatComposeDeploy/assets/124437522/2cf2c49d-d0d5-44ed-b6be-64d50fb49fbb)







