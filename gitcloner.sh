#!/bin/bash
# NOTE: Read the Readme To use the git cloner.

# Token used for Git authentication, used only for private repositories
TOKEN=""

# Define an array with the repository URLs, branches, and token usage flag
declare -a repos=(
    "https://github.com/aditya-verp/example.git main true"  # Private repo, token required
    "https://github.com/example.git main false"  # Public repo, no token required
    # Add more repositories as needed
)

# Directory where repositories will be cloned
TARGET_DIR="./autodeploy"

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

clone_repo() {
    local repo_url=$1
    local branch=$2
    local use_token=$3
    
    if [ "$use_token" = "true" ]; then
        
        repo_url=$(echo $repo_url | sed "s|://|://oauth2:$TOKEN@|")
    fi

    echo "Cloning branch $branch of $repo_url into $TARGET_DIR..."
    git clone $repo_url --depth 1 --single-branch --branch $branch
}

for repo in "${repos[@]}"; do
    # Parse the repository information
    repo_url=$(echo $repo | cut -d' ' -f1)
    branch=$(echo $repo | cut -d' ' -f2)
    use_token=$(echo $repo | cut -d' ' -f3)
    
    clone_repo $repo_url $branch $use_token
done

echo "Cloning complete."

