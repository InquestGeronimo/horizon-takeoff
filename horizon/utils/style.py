def banner():
	
	return """ 

██╗  ██╗  ██████╗  ██████╗  ██╗ ███████╗  ██████╗  ███╗   ██╗
██║  ██║ ██╔═══██╗ ██╔══██╗ ██║ ╚══███╔╝ ██╔═══██╗ ████╗  ██║
███████║ ██║   ██║ ██████╔╝ ██║   ███╔╝  ██║   ██║ ██╔██╗ ██║
██╔══██║ ██║   ██║ ██╔══██╗ ██║  ███╔╝   ██║   ██║ ██║╚██╗██║
██║  ██║ ╚██████╔╝ ██║  ██║ ██║ ███████╗ ╚██████╔╝ ██║ ╚████║
╚═╝  ╚═╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝ ╚══════╝  ╚═════╝  ╚═╝  ╚═══╝
    
	"""

class PromptHandler:
    subtitle = "Deploying the Takeoff Server on AWS for LLMs Inference"
    intro = "\n[magenta]Let's generate your YAML config file for your AWS cloud environment[/magenta]"
    emoji_checkmark = ":heavy_check_mark:"
    emoji_cross = ":x:"
    aws_id_exists = "AWS account ID exists."
    aws_cli_exists = "AWS CLI is installed."
    docker_exists = "Docker is installed."
    
    select_aws_feature = "\n[magenta]Choose the AWS service:[/magenta] [yellow]ec2[/yellow] or [yellow]sagemaker[/yellow]"
    aws_feature_choices = ["ec2", "sagemaker"]
    ec2_warning_msg = "\n[bold red]Warning:[/bold red] EC2 configuration file already exists. \
						Do you want to override it? [yellow](yes/no)[/yellow]"
    boolean_choices = ["yes", "no"]
    abort_config = "[bold red]Aborting YAML configuration![/bold red]"
    sagemaker_warning_msg = "[bold red]Warning: Sagemaker configuration file already exists. Do you want to override it? (yes/no)[/bold red]"
    
    enter_ami = "\n[magenta] 2. Enter EC2 AMI ID[/magenta] (e.g. for Ubuntu 22.04 x86 [yellow]ami-0c7217cdde317cfec[/yellow])"
    enter_instance_type = "\n[magenta] 3. Enter EC2 Instance Type[/magenta] (e.g. for 1 V100 GPU: [yellow]p3.2xlarge[/yellow])"
    enter_key_name = "\n[magenta] 4. Enter EC2 Key Name[/magenta]"
    enter_security_group = "\n[magenta] 5. Enter EC2 Security Group ID(s) (if multiple, comma-separated)[/magenta]"
    
    docker_flow = "\n[magenta] 6. Ready to deploy Docker image to ECR and instantiate your EC2 instance?[/magenta] [yellow](yes,no)[/yellow]"
    enter_ecr_name = "\n[magenta] - Enter your ECR repository name, if it doesn't exist, it will be created"
    
    @staticmethod
    def dependency_not_exists(escape, message):
        return f"[bold red]{escape}[/] {message} is missing."
    
    @staticmethod
    def dependency_exists(escape, message):
        return f"[bold green]{escape}[/] {message}"
    
    @staticmethod
    def enter_region(region):
        return f"\n[magenta] 1. Enter EC2 Region Name[/magenta] (current configured region: [yellow]{region}[/yellow])"
    
    @staticmethod
    def config_created(config_file):
        return f"\n[bold green]EC2 config file '{config_file}' has been created in your working directory.[/bold green]"
    
    @staticmethod
    def instance_created(instance_meta_data):
        return f"\nCreated EC2 instance: [bold green] {instance_meta_data}[/bold green]"
    
    @staticmethod
    def instance_id_added(instance_id, config_file):
        return f"Instance ID '{instance_id}' added to the YAML file '{config_file}'."
	

	
	
