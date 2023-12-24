import boto3
import botocore
from typing import List, Dict, Any


class EC2ConfigHandler:
    """
    A class for handling EC2 configurations and listing security groups.
    """

    config_filename = "ec2_config.yaml"

    def __init__(self) -> None:
        """
        Initializes an EC2ConfigHandler object with an EC2 client based on the AWS region from the current session.
        """
        self.session = boto3.Session()
        self.ec2_client = self.session.client("ec2")

    def get_aws_region(self):
        """
        Get the AWS region using boto3's Session object.

        Returns:
            str: The AWS region name, or an error message if not configured.
        """
        try:
            aws_region = self.session.region_name
            return aws_region if aws_region else "AWS region is not configured."
        except botocore.exceptions.NoRegionError as e:
            print(f"Error listing aws region: {e}")

    def list_security_groups(self) -> List[Dict[str, Any]]:
        """
        Lists security groups in your AWS EC2 environment.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing security group information.
        """
        try:
            response = self.ec2_client.describe_security_groups()
            security_groups = response["SecurityGroups"]

            print("\nList of your Security Groups:")
            for group in security_groups:
                print(f"Name: {group['GroupName']}")
                print(f"ID: {group['GroupId']}")

            return security_groups
        except botocore.exceptions.ClientError as e:
            print(f"Error listing security groups: {e}")

    def list_key_pairs(self) -> List[Dict[str, str]]:
        """
        Lists the key pairs available in your AWS account.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing key pair information.
                Each dictionary contains a 'KeyName' key with the name of the key pair.
        """
        try:
            response = self.ec2_client.describe_key_pairs()
            key_pairs = response["KeyPairs"]

            print("\nList of your Key Pairs:")
            for key in key_pairs:
                print(f"Name: {key['KeyName']}")

            return key_pairs
        except botocore.exceptions.ClientError as e:
            # Handle the exception here, e.g., print an error message
            print(f"Error listing key pairs: {e}")
            return []

    def create_ec2_config_dict(self) -> Dict[str, Any]:
        """
        Initialize an empty EC2 configuration dictionary.

        Returns:
            dict: An empty EC2 configuration dictionary with predefined keys.
        """
        ec2_config: Dict[str, Any] = {
            "EC2": {
                "region_name": "",
                "ami_id": "",
                "instance_type": "",
                "key_name": "",
                "security_group_ids": [],
            }
        }
        return ec2_config