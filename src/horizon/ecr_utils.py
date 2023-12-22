import boto3
import yaml
from typing import Dict, Union

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

class ECRManager:
    def __init__(self, config_path: str):
        params = parse_yaml_file(config_path)
        self.ecr_client = boto3.client('ecr', region_name=params["EC2"]["region_name"])

    def check_or_create_repository(self, repository_name):
        try:
            response = self.ecr_client.describe_repositories(repositoryNames=[repository_name])
            repository_exists = len(response['repositories']) > 0
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            repository_exists = False

        if not repository_exists:
            try:
                self.ecr_client.create_repository(repositoryName=repository_name)
                print(f"ECR repository '{repository_name}' created successfully.")
            except Exception as e:
                print(f"Error creating ECR repository: {e}")
        else:
            print(f"ECR repository '{repository_name}' already exists.")
