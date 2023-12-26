import boto3
import botocore.exceptions  # Import for more specific exceptions

class IAMHandler:
    def __init__(self):
        # Create an IAM client
        self.iam_client = boto3.client('iam')

    def get_aws_account_id(self):
        try:
            # Get the AWS account ID
            response = self.iam_client.get_user()
            account_id = response['User']['Arn'].split(':')[4]
            return account_id
        except botocore.exceptions.ClientError as e:
            print(f"Error retrieving AWS account ID: {e}")
            return None

    def attach_policy_to_role(self, role_name, policy_arn):
        try:
            # Attach a managed policy to an IAM role
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"Policy '{policy_arn}' attached to IAM Role '{role_name}' successfully.")
        except botocore.exceptions.ClientError as e:
            print(f"Error attaching policy '{policy_arn}' to IAM role '{role_name}': {e}")

    def create_instance_profile_and_associate_role(self, role_name):
        try:
            # Create an instance profile
            self.iam_client.create_instance_profile(InstanceProfileName=role_name)

            # Add the IAM role to the instance profile
            self.iam_client.add_role_to_instance_profile(InstanceProfileName=role_name, RoleName=role_name)

            print(f"Instance profile '{role_name}' created and associated with IAM role '{role_name}' successfully.")
        except botocore.exceptions.ClientError as e:
            print(f"Error creating instance profile and associating it with IAM role '{role_name}': {e}")

    def list_roles(self, count):
        """
        Lists the specified number of roles for the account.

        :param count: The number of roles to list.
        """
        try:
            roles = self.iam_client.list_roles(MaxItems=count)['Roles']
            for role in roles:
                print("Role:", role['RoleName'])
        except botocore.exceptions.ClientError as e:
            print("Couldn't list roles for the account:", e)
            raise
        else:
            return roles