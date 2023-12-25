from typing import Optional, Dict, List

import boto3
from ..utils.yaml_utils import parse_yaml_file
from .models import EC2Config


class TitanEC2:
    """Initialize a TitanEC2 instance.

    Args:
        ec2_config (EC2Config): A Pydantic model representing the EC2 configuration.
        min_count (int, optional): The minimum number of instances to create. Defaults to 1.
        max_count (int, optional): The maximum number of instances to create. Defaults to 1.
    """

    def __init__(self, ec2_config: EC2Config, min_count: int = 1, max_count: int = 1):
        """
        Initialize a TitanEC2 instance.

        Args:
            ec2_config (EC2Config): A Pydantic model representing the EC2 configuration.
            min_count (int, optional): The minimum number of instances to create. Defaults to 1.
            max_count (int, optional): The maximum number of instances to create. Defaults to 1.
        """
        self.min_count = min_count
        self.max_count = max_count
        self.ec2_client = boto3.client("ec2", region_name=ec2_config.region_name)
        self.ami_id = ec2_config.ami_id
        self.instance_type = ec2_config.instance_type
        self.key_name = ec2_config.key_name
        self.security_group_ids = ec2_config.security_group_ids
        self.instance_ids = ec2_config.instance_ids or []

    def create_instance(self) -> Dict:
        """Create an EC2 instance based on the configured parameters.

        Returns:
            str: The ID of the created EC2 instance.
        """
        instance_params = {
            "ImageId": self.ami_id,
            "InstanceType": self.instance_type,
            "KeyName": self.key_name,
            "SecurityGroupIds": self.security_group_ids,
            "MinCount": self.min_count,
            "MaxCount": self.max_count,
        }

        response = self.ec2_client.run_instances(**instance_params)
        return response["Instances"][0]["InstanceId"], response

    def delete_instance(self, instance_ids: List[str]) -> None:
        """Delete EC2 instances by providing a list of instance IDs.

        Args:
            instance_ids (List[str]): A list of EC2 instance IDs to delete.
        """
        if instance_ids:
            self.ec2_client.terminate_instances(InstanceIds=instance_ids)
            print(f"Instances {', '.join(instance_ids)} are being terminated.")
        else:
            print("No instance IDs provided. No instances will be terminated.")

    @classmethod
    def load_config(cls, config_file_path: str) -> Optional["TitanEC2"]:
        """Load EC2 configuration from a YAML file and create a TitanEC2 instance.

        Args:
            config_file_path (str): Path to the YAML configuration file.

        Returns:
            TitanEC2: An instance of TitanEC2 initialized with the loaded configuration.
        """
        ec2_config = parse_yaml_file(config_file_path)
        if ec2_config:
            return cls(ec2_config)
