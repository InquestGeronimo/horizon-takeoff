import os
import boto3
import subprocess
import yaml
from typing import Dict, Union

PULL_SCRIPT = "pull_takeoff_image.sh"
PUSH_SCRIPT = "push_takeoff_ecr.sh"


def parse_yaml_file(yaml_file_path: str) -> Union[Dict, None]:
    """Parse a YAML file and return its content as a dictionary.

    Args:
        yaml_file_path (str): Path to the YAML file.

    Returns:
        dict: A dictionary representing the YAML content or None if there's an issue.
    """
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return yaml_content
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error parsing YAML file: {e}")
        return None

class Manager:
    def __init__(self, config_path: str):
        params = parse_yaml_file(config_path)
        self.ecr_client = boto3.client('ecr', region_name=params["EC2"]["region_name"])

    def check_or_create_repository(self, repo_name):
        try:
            response = self.ecr_client.describe_repositories(repositoryNames=[repo_name])
            repository_exists = len(response['repositories']) > 0
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            repository_exists = False

        if not repository_exists:
            try:
                self.ecr_client.create_repository(repositoryName=repo_name)
                print(f"ECR repository '{repo_name}' created successfully.")
            except Exception as e:
                print(f"Error creating ECR repository: {e}")
        else:
            print(f"ECR repository '{repo_name}' already exists.")

    def deploy_takeoff_image(self, script_dir, repo_name):
        """
        Deploys the Takeoff Server Docker image.

        Args:
            script_directory (str): The directory containing the Bash scripts.
            repo_name (str): The name of the ECR repository.
        """

        pull_script = os.path.join(script_dir, PULL_SCRIPT)
        push_script = os.path.join(script_dir, PUSH_SCRIPT)

        try:
            # Run the first Bash script
            subprocess.run(["bash", pull_script])

            # Run the second Bash script with repo_name as an argument
            subprocess.run(["bash", push_script, repo_name])

        except Exception as e:
            print(f"Error during deployment: {e}")