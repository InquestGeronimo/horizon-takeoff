import os
import yaml
from typing import Dict, Optional
from io import TextIOWrapper
from ..aws.models import EC2Config


class YamlFileManager:
    @staticmethod
    def parse_yaml_file(yaml_file_path: str) -> Optional[EC2Config]:
        """Parse a YAML file and return an EC2Config object.

        Args:
            yaml_file_path (str): The path to the YAML file, or just the filename.

        Returns:
            Optional[EC2Config]: An EC2Config object representing the parsed YAML data, or None on error.
        """
        try:
            # If the input is just the filename, construct the full path
            if not os.path.isabs(yaml_file_path):
                yaml_file_path = os.path.join(os.getcwd(), yaml_file_path)

            with open(yaml_file_path, "r") as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)
            return EC2Config(**yaml_content["EC2"])
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error parsing YAML file: {e}")
            return None

    @staticmethod
    def add_instance_id_to_yaml(yaml_file_path: str, instance_id_to_add: str) -> None:
        # TODO change title to make it more generic
        """Add an instance ID to a YAML configuration file.

        Args:
            yaml_file_path (str): The path to the YAML file.
            instance_id_to_add (str): The instance ID to add.

        Returns:
            None
        """
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
    def add_ecr_repo_name_to_yaml(yaml_file_path: str, repo_name_to_add: str) -> None:
        # TODO change title to make it more generic
        """Add an instance ID to a YAML configuration file.

        Args:
            yaml_file_path (str): The path to the YAML file.
            repo_name_to_add (str): The ECR repo name to add.

        Returns:
            None
        """
        ec2_config = YamlFileManager.parse_yaml_file(yaml_file_path)

        try:
            if ec2_config is not None:
                ec2_config.ecr_repo_name = repo_name_to_add  # Assign the single string

                updated_data = {"EC2": ec2_config.model_dump()}

                YamlFileManager.write_yaml_to_file(yaml_file_path, updated_data)

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error updating YAML file: {e}")

    @staticmethod
    def add_model_name_to_yaml(yaml_file_path: str, model_name_to_add: str) -> None:
        # TODO change title to make it more generic
        """Add an instance ID to a YAML configuration file.

        Args:
            yaml_file_path (str): The path to the YAML file.
            repo_name_to_add (str): The ECR repo name to add.

        Returns:
            None
        """
        ec2_config = YamlFileManager.parse_yaml_file(yaml_file_path)

        try:
            if ec2_config is not None:
                ec2_config.hf_model_name = model_name_to_add

                updated_data = {"EC2": ec2_config.model_dump()}

                YamlFileManager.write_yaml_to_file(yaml_file_path, updated_data)

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error updating YAML file: {e}")

    @staticmethod
    def add_hardware_to_yaml(yaml_file_path: str, hardware_to_add: str) -> None:
        # TODO change title to make it more generic
        """Add a hardware specification to a YAML configuration file.

        Args:
            yaml_file_path (str): The path to the YAML file.
            hardware_to_add (str): The hardware specification to add (e.g., 'cpu' or 'gpu').

        Returns:
            None
        """
        ec2_config = YamlFileManager.parse_yaml_file(yaml_file_path)

        try:
            if ec2_config is not None:
                ec2_config.hardware = hardware_to_add

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
