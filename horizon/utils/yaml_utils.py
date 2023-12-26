import os
import yaml
from typing import Dict, Optional
from io import TextIOWrapper
from ..aws.models import EC2Config


class YamlFileManager:
    @staticmethod
    def parse_yaml_file(yaml_file_path: str) -> Optional[EC2Config]:
        try:
            with open(yaml_file_path, "r") as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)
            return EC2Config(**yaml_content["EC2"])
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error parsing YAML file: {e}")
            return None

    @staticmethod
    def add_instance_id_to_yaml(yaml_file_path, instance_id_to_add):
        ec2_config = YamlFileManager.parse_yaml_file(yaml_file_path)

        try:
            if ec2_config is not None:
                if ec2_config.instance_ids is None:
                    ec2_config.instance_ids = []

                ec2_config.instance_ids.append(instance_id_to_add)

                updated_data = {"EC2": ec2_config.model_dump()}

                YamlFileManager.write_yaml_to_file(yaml_file_path, updated_data)

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error updating YAML file: {e}")

    @staticmethod
    def yaml_config_exists(name: str) -> bool:
        """Check if a YAML configuration file exists.

        Args:
            name (str): Name of the configuration.

        Returns:
            bool: True if the configuration file exists, False otherwise.
        """
        return os.path.exists(f"{name}_config.yaml")

    @staticmethod
    def write_yaml_to_file(filename: str, data: Dict) -> TextIOWrapper:
        """Write YAML data to a file.

        Args:
            filename (str): The name of the file to write to.
            data (dict): The YAML data to write.

        Returns:
            None
        """
        with open(filename, "w") as config_file:
            yaml.dump(data, config_file, default_flow_style=False)

        return config_file
