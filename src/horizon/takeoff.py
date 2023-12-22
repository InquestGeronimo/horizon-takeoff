import os
import yaml
import subprocess
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.markup import escape
from typing import Dict, Any

from .ec2_utils import EC2ConfigHandler
from .checks import EnvChecker as env
from .banner import print_banner


shell = Console()
ec2 = EC2ConfigHandler()

print_banner()

requirements = [
    (env.check_aws_account_id, "AWS account ID exists."),
    (env.check_aws_cli_installed, "AWS CLI is installed."),
    (env.check_docker_installed, "Docker is installed."),
]

def check_requirements():
    emoji_checkmark = ":heavy_check_mark:"
    emoji_cross = ":x:"
    for condition, message in requirements:
        if condition is None:
            error_message = f"[bold red]{escape(emoji_cross)}[/] {message} is missing."
            shell.print(error_message)
            return  # Stop execution if any condition is None
        if condition:
            formatted_message = f"[bold green]{escape(emoji_checkmark)}[/] {message}"
            shell.print(formatted_message)

def config_exists(name) -> bool:
    return os.path.exists(f'{name}_config.yaml')

def create_ec2_config_file() -> None:
    ec2_config: Dict[str, Any] = {}
    ec2_config['EC2'] = {
        'region_name': Prompt.ask(
            f"[magenta] 1. Enter EC2 Region Name[/magenta] (current configured region: [yellow]{ec2.get_aws_region()}[/yellow])"
        ),
        'ami_id': Prompt.ask(
            "\n[magenta] 2. Enter EC2 AMI ID[/magenta] (e.g. for Ubuntu 22.04 x86 [yellow]ami-0c7217cdde317cfec[/yellow])"
        ),
        'instance_type': Prompt.ask(
            "\n[magenta] 3. Enter EC2 Instance Type[/magenta] (e.g. for 1 V100 GPU: [yellow]p3.2xlarge[/yellow])"
        )
    }
    ec2.list_key_pairs()
    key_name: str = Prompt.ask("\n[magenta] 4. Enter EC2 Key Name[/magenta]")
    ec2_config['EC2']['key_name'] = key_name
    ec2.list_security_groups()
    security_group_ids: str = Prompt.ask("\n[magenta] 5. Enter EC2 Security Group ID(s) (if multiple, comma-separated)[/magenta]")
    ec2_config['EC2']['security_group_ids'] = [sg.strip() for sg in security_group_ids.split(',')]
    
    with open('ec2_config.yaml', 'w') as config_file:
        yaml.dump(ec2_config, config_file, default_flow_style=False)
    
    deploy = Prompt.ask("""[bold green]EC2 configuration file 'ec2_config.yaml' has been created in your working directory.[/bold green]
    \n[magenta]Ready to deploy Docker image to ECR? (yes,no)[/magenta]""")
    
    if deploy.lower() == "yes":
        try:
            # Run the first Bash script
            subprocess.run(["bash", "./horizon/scripts/pull_takeoff_image.sh"])
            
            # Run the second Bash script
            subprocess.run(["bash", "./horizon/scripts/push_takeoff_ecr.sh"])
            
            print("Docker image of the Takeoff Server pushed sucessfully to ECR.")
        except Exception as e:
            print(f"Error during deployment: {e}")
    else:
        print("Your configuration is completed. You can now launch your EC2 instance manually.")  #TODO write out manual flow using Docker Class and TitanEC2/TitanSagemaker class
        
    
def create_sagemaker_config_file() -> None:
    sagemaker_config: Dict[str, Any] = {}
    sagemaker_config['account_id'] = Prompt.ask("[magenta]Enter Sagemaker Account ID[/magenta]: ")
    sagemaker_config['model_name'] = Prompt.ask("[magenta]Enter Sagemaker Model Name[/magenta]: ")
    sagemaker_config['instance_type'] = Prompt.ask("[magenta]Enter Sagemaker Instance Type[/magenta]: ")
    sagemaker_config['endpoint_name'] = Prompt.ask("[magenta]Enter Sagemaker Endpoint Name[/magenta]: ")

    with open('sagemaker_config.yaml', 'w') as config_file:
        yaml.dump(sagemaker_config, config_file, default_flow_style=False)
    
    print("[bold green]Sagemaker configuration file 'sagemaker_config.yaml' has been created and filled.[/bold green]")

check_requirements()
shell.print("\n[magenta]Let's generate your YAML config file for your AWS cloud environment[/magenta]\n")
choice: str = Prompt.ask("[magenta]Choose the AWS service: [yellow]ec2[/yellow] or [yellow]sagemaker[/yellow][/magenta]")

if choice == 'ec2':
    if config_exists(choice):
        warning_message = "[bold yellow]Warning:[/bold yellow] EC2 configuration file already exists. Do you want to override it? (yes/no)"
        override_choice = Prompt.ask(warning_message)
        if override_choice == 'yes':
            create_ec2_config_file()
        else:
            print("[bold red]Aborting YAML configuration![/bold red]")
    else:
        create_ec2_config_file()
elif choice == 'sagemaker':
    if config_exists(choice):
        warning_message = "[bold yellow]Warning: Sagemaker configuration file already exists. Do you want to override it? (yes/no)[/bold yellow]"
        override_choice = Prompt.ask(warning_message)
        if override_choice == 'yes':
            create_sagemaker_config_file()
        else:
            print("[bold red]Aborting YAML configuration![/bold red]")
    else:
        create_sagemaker_config_file()
else:
    print("Invalid choice. Choose either 'ec2' or 'sagemaker'.")
