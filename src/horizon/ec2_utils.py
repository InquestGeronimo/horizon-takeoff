import boto3
from typing import List, Dict, Any

class EC2ConfigHandler:
    """
    A class for handling EC2 configurations and listing security groups.
    """

    def __init__(self) -> None:
        """
        Initializes an EC2ConfigHandler object with an EC2 client based on the AWS region from the current session.
        """
        self.session = boto3.Session()
        self.ec2_client = self.session.client('ec2')

    def get_aws_region(self):
        
        """
        Get the AWS region using boto3's Session object.

        Returns:
            str: The AWS region name, or an error message if not configured.
        """
        try:
            aws_region = self.session.region_name
            return aws_region if aws_region else "AWS region is not configured."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def list_security_groups(self) -> List[Dict[str, Any]]:
        """
        Lists security groups in your AWS EC2 environment.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing security group information.
        """
        response = self.ec2_client.describe_security_groups()
        security_groups = response['SecurityGroups']

        print("\nList of your Security Groups:")
        for group in security_groups:
            print(f"Name: {group['GroupName']}")
            print(f"ID: {group['GroupId']}")
            
        return security_groups
    
    def list_key_pairs(self) -> List[Dict[str, str]]:
        """
        Lists the key pairs available in your AWS account.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing key pair information.
                Each dictionary contains a 'KeyName' key with the name of the key pair.
        """
        response = self.ec2_client.describe_key_pairs()
        key_pairs = response['KeyPairs']

        print("\nList of your Key Pairs:")
        for key in key_pairs:
            print(f"Name: {key['KeyName']}")

        return key_pairs

# Usage
# if __name__ == "__main__":
#     ec2 = EC2ConfigHandler()
#     reg = ec2.get_aws_region()
#     security_groups = ec2.list_security_groups()
#     print(security_groups)
#     key_pairs = ec2.list_key_pairs()
#     print(key_pairs)
