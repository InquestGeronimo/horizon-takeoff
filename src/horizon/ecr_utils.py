import boto3

# Specify the AWS region where you want to create the ECR repository
region = 'your-region'  # Replace with your desired region

# Initialize the ECR client
ecr_client = boto3.client('ecr', region_name=region)

# Define the repository name
repository_name = 'fabulinus'

try:
    # Create the ECR repository
    response = ecr_client.create_repository(
        repositoryName=repository_name
    )
    
    # Check if the repository creation was successful
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"ECR repository '{repository_name}' created successfully.")
    else:
        print(f"Failed to create ECR repository '{repository_name}'.")

except Exception as e:
    print(f"Error creating ECR repository: {str(e)}")
