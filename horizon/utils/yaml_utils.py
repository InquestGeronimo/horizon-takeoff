import os
import yaml
from typing import Dict, Union


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
    
def add_instance_id_to_yaml(yaml_file_path: str, instance_id):
    try:
        # Read the existing YAML file
        with open(yaml_file_path, "r") as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)

        # Add the instance ID to the "EC2" section
        if "instance_ids" not in yaml_content["EC2"]:
            yaml_content["EC2"]["instance_ids"] = []
        yaml_content["EC2"]["instance_ids"].append(instance_id)

        # Write the updated content back to the YAML file
        with open(yaml_file_path, "w") as yaml_file:
            yaml.dump(yaml_content, yaml_file, default_flow_style=False)
        
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error updating YAML file: {e}")
        
def yaml_config_exists(name) -> bool:
    return os.path.exists(f"{name}_config.yaml")

def write_yaml_to_file(filename, data):
    """
    Write YAML data to a file.

    Args:
        filename (str): The name of the file to write to.
        data (dict): The YAML data to write.

    Returns:
        None
    """
    with open(filename, "w") as config_file:
        yaml.dump(data, config_file, default_flow_style=False)
        
    return config_file