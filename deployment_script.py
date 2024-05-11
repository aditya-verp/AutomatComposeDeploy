import os
import subprocess
import yaml
import re
import schedule
import time
from datetime import datetime
import pytz

# Define the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_config():
    """Reads the YAML configuration file, trying both .yaml and .yml extensions."""
    config_paths = [os.path.join(SCRIPT_DIR, 'config.yaml'), os.path.join(SCRIPT_DIR, 'config.yml')]
    for config_path in config_paths:
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                return config
    raise FileNotFoundError("🚫 No config file found with .yaml or .yml extension.")

def get_repo_url(git_path):
    """Gets the Git repository URL without logging sensitive information."""
    if not os.path.exists(git_path) or not os.path.isdir(os.path.join(git_path, '.git')):
        print(f"🚫 Failed to get Git URL or invalid repository at {git_path}. Moving to next repository...")
        return None
    try:
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], cwd=git_path, capture_output=True, text=True)
        return result.stdout.strip().split('@')[-1]
    except subprocess.CalledProcessError:
        print(f"🚫 Error retrieving Git URL for directory {git_path}.")
        return None

def detect_git_changes(git_path, compose_path):
    """Detects if there are changes in the Git repository affecting the docker-compose file."""
    try:
        temp_compose_path = os.path.join(git_path, 'docker-compose.tmp.yml')
        subprocess.run(['cp', compose_path, temp_compose_path], check=True)
        subprocess.run(['git', 'pull'], cwd=git_path, capture_output=True, text=True)
        cmp_result = subprocess.run(['cmp', compose_path, temp_compose_path], stdout=subprocess.PIPE)
        os.remove(temp_compose_path)
        if cmp_result.returncode != 0:
            print("🔄 Changes detected.")
            return True
        else:
            print(f"✅ No changes detected in the Docker Compose file at {git_path}.")
            return False
    except Exception as e:
        print("🚫 Error during Git operations:", e)
        return False

def execute_docker_compose_up(compose_path):
    """Executes 'docker compose up -d' and captures both stdout and stderr."""
    try:
        dir_path = os.path.dirname(compose_path)
        result = subprocess.run(['docker', 'compose', 'up', '-d'], cwd=dir_path, capture_output=True, text=True)
        if result.stderr:
            print("🐳 Docker Compose execution output (stderr):")
            print(result.stderr)
        return result.stdout + result.stderr, result.returncode == 0
    except subprocess.CalledProcessError as e:
        print("🚫 Error executing Docker Compose:", e.stderr)
        return e.stderr, False

def all_keywords_match(output, keywords):
    """Check if all keywords match the output as whole words."""
    return all(re.search(r'\b{}\b'.format(re.escape(keyword.strip('!'))), output) for keyword in keywords if not keyword.startswith('!'))

def deployment_cycle():
    config = read_config()
    success_keywords = config['Success_condition']['keywords']
    git_repo_paths = config['gitrepo_path']
    exception_conditions = config['exception_condition']

    print("🚀 Starting deployment script...")
    for repo_name, repo_config in git_repo_paths.items():
        git_path = repo_config['path']
        compose_path = repo_config['compose_path']

        repo_url = get_repo_url(git_path)
        if repo_url:
            print(f"🔍 Checking {repo_name} at {repo_url}...")
            if detect_git_changes(git_path, compose_path):
                output, success = execute_docker_compose_up(compose_path)
                if success and all_keywords_match(output, success_keywords):
                    print(f"✅ {datetime.now()} - Docker Compose up successful for {repo_name}")
                else:
                    print(f"❌ {datetime.now()} - Initial Docker Compose up failed for {repo_url}.")
                    for index, condition in enumerate(exception_conditions):
                        print(f"⚙️ Trying exception condition {index+1}/{len(exception_conditions)} for {repo_name}...")
                        if all_keywords_match(output, condition['search']['keywords']):
                            output, success = execute_docker_compose_up(compose_path)
                            if success and all_keywords_match(output, success_keywords):
                                print(f"✅ {datetime.now()} - Docker Compose up successful after exception for {repo_url}")
                                break
                            else:
                                print(f"❌ {datetime.now()} - Still failed after exception for {repo_url}")
                    else:
                        print(f"❌ {datetime.now()} - All exception conditions checked and none met for {repo_url}. Moving to next repository...")
            else:
                print(f"✅ No changes detected on {repo_name}, skipping...")
        else:
            print(f"🚫 Failed to get Git URL or invalid repository at {git_path}. Moving to next repository...")

    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')

    print(f"🏁 #### Deployment script finished at {current_time} IST ####.")


def main():
    interval_minutes = read_config().get('schedule', {}).get('interval_minutes', 5)
    schedule.every(interval_minutes).minutes.do(deployment_cycle)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()

