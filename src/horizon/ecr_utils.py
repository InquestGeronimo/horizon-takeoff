import boto3

class ECRManager:
    def __init__(self, region_name):
        self.ecr_client = boto3.client('ecr', region_name=region_name)

    def check_or_create_repository(self, repository_name):
        try:
            response = self.ecr_client.describe_repositories(repositoryNames=[repository_name])
            repository_exists = len(response['repositories']) > 0
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            repository_exists = False

        if not repository_exists:
            try:
                self.ecr_client.create_repository(repositoryName=repository_name)
                print(f"ECR repository '{repository_name}' created successfully.")
            except Exception as e:
                print(f"Error creating ECR repository: {e}")
        else:
            print(f"ECR repository '{repository_name}' already exists.")


ecr = ECRManager("us-east-1")
ecr.check_or_create_repository("fabulinus")