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

class TitanEC2:
    
    """Initialize a TitanEC2 instance.

    Args:
        config_path (str): Path to the YAML configuration file.
        min_count (int): The minimum number of instances to create.
        max_count (int): The maximum number of instances to create.
    """
    
    def __init__(
        self, 
        config_path: str = "./ec2_config.yaml", 
        min_count: int = 1, 
        max_count: int = 1
    ):
    
        params = parse_yaml_file(config_path)
        self.min_count = min_count
        self.max_count = max_count
        self.ec2_client = boto3.client('ec2', region_name=params["EC2"]["region_name"])
        self.ami_id = params["EC2"]["ami_id"]
        self.instance_type = params["EC2"]["instance_type"]
        self.key_name = params["EC2"]["key_name"]
        self.security_group_ids = params["EC2"]["security_group_ids"]
 

    def create_instance(self) -> str:
        """Create an EC2 instance based on the configured parameters.

        Returns:
            str: The ID of the created EC2 instance.
        """
        instance_params = {
            'ImageId': self.ami_id,
            'InstanceType': self.instance_type,
            'KeyName': self.key_name,
            'SecurityGroupIds': self.security_group_ids,  # Wrap it in a list if it's a single ID
            'MinCount': self.min_count,
            'MaxCount': self.max_count
        }

        return self.ec2_client.run_instances(**instance_params)
     