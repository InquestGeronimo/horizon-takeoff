import os
import boto3
import subprocess
import yaml
from typing import Dict, Union

PULL_SCRIPT = "pull_takeoff_image.sh"
PUSH_SCRIPT = "push_takeoff_ecr.sh"


def parse_yaml_file(yaml_file_path: str) -> Union[Dict, None]:
    """Parse the config YAML file containing AWS environment variables \
       and return its content as a dictionary.

    Args:
        yaml_file_path (str): Path to the YAML file.

    Returns:
        dict: A dictionary representing the YAML content or None if there's an issue.
    """
    try:
        with open(yaml_file_path, "r") as yaml_file:
            yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return yaml_content
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error parsing YAML file: {e}")
        return None


class DockerHandler:
    def __init__(self, config_path: str) -> None:
        """
        Initialize the Handler with the provided YAML config path.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        params = parse_yaml_file(config_path)
        self.ecr_client = boto3.client("ecr", region_name=params["EC2"]["region_name"])

    def check_or_create_repository(self, repo_name: str) -> None:
        """
        Check if an ECR repository exists; create it if not.

        Args:
            repo_name (str): The name of the ECR repository to check or create.
        """
        try:
            response = self.ecr_client.describe_repositories(
                repositoryNames=[repo_name]
            )
            repository_exists = len(response["repositories"]) > 0
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

    def pull_takeoff_image(self, script_dir: str) -> None:
        """
        Pulls the Takeoff Server Docker image to local machine.

        Args:
            script_dir (str): The directory containing the script for pulling Takeoff server.
        """
        pull_script = os.path.join(script_dir, PULL_SCRIPT)

        try:
            subprocess.run(["bash", pull_script])

        except Exception as e:
            print(f"Error during image pull: {e}")

    def push_takeoff_image(self, script_dir: str, ecr_repo_name: str) -> None:
        """
        Pushes the Takeoff Server Docker image to the ECR repository.

        Args:
            script_dir (str): The directory containing the Bash push script.
            repo_name (str): The name of the ECR repository.
        """
        push_script = os.path.join(script_dir, PUSH_SCRIPT)

        try:
            subprocess.run(["bash", push_script, ecr_repo_name])

        except Exception as e:
            print(f"Error during image push: {e}")
