import boto3
import yaml
from .models import EC2Config


def parse_yaml_file(yaml_file_path: str) -> EC2Config:
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
        return EC2Config(**yaml_content['EC2'])
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error parsing YAML file: {e}")
        return None


class TitanEC2:
    def __init__(
        self, 
        ec2_config: EC2Config, 
        min_count: int = 1, 
        max_count: int = 1
    ):
        self.min_count = min_count
        self.max_count = max_count
        self.ec2_client = boto3.client('ec2', region_name=ec2_config.region_name)
        self.ami_id = ec2_config.ami_id
        self.instance_type = ec2_config.instance_type
        self.key_name = ec2_config.key_name
        self.security_group_ids = ec2_config.security_group_ids

    def create_instance(self) -> str:
        instance_params = {
            'ImageId': self.ami_id,
            'InstanceType': self.instance_type,
            'KeyName': self.key_name,
            'SecurityGroupIds': self.security_group_ids,
            'MinCount': self.min_count,
            'MaxCount': self.max_count
        }

        return self.ec2_client.run_instances(**instance_params)

    @classmethod
    def load_ec2_config(cls, config_file_path: str):
        ec2_config = parse_yaml_file(config_file_path)
        if ec2_config:
            return cls(ec2_config)
