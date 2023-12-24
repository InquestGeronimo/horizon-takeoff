import os
import yaml
from typing import Dict, Any

from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.markup import escape

from .aws.titan_ec2 import TitanEC2
from .utils.ec2_utils import EC2ConfigHandler
from .utils.docker_utils import DockerHandler
from .utils.checks import EnvChecker as env
from .utils.banner import print_banner
from .utils.yaml_utils import add_instance_id_to_yaml

shell = Console()
ec2 = EC2ConfigHandler()


current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, "scripts")

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
    return os.path.exists(f"{name}_config.yaml")


def intro() -> None:
    shell.print(
        "\n[magenta]Let's generate your YAML config file for your AWS cloud environment[/magenta]"
    )


def select_aws_service() -> None:
    choice: str = Prompt.ask(
        "\n[magenta]Choose the AWS service:[/magenta] [yellow]ec2[/yellow] or [yellow]sagemaker[/yellow]",
        choices=["ec2", "sagemaker"],
        show_choices=False,
    )
    return choice

def provision_ec2(choice):
    if config_exists(choice):
        warning_message = "\n[bold red]Warning:[/bold red] EC2 configuration file already exists. Do you want to override it? [yellow](yes/no)[/yellow]"
        override_choice = Prompt.ask(
            warning_message, choices=["yes", "no"], show_choices=False
        )
        if override_choice == "yes":
            config_file = create_ec2_config_file()
            deploy_docker(config_file)
            instance_id = create_ec2_instance(config_file)
            return instance_id, config_file
        else:
            print("[bold red]Aborting YAML configuration![/bold red]")
    else:
        config_name = create_ec2_config_file()
        deploy_docker(config_name)
        create_ec2_instance(config_name)
            
def provision_sagemaker(choice):
    if config_exists(choice):
        warning_message = "[bold red]Warning: Sagemaker configuration file already exists. Do you want to override it? (yes/no)[/bold red]"
        override_choice = Prompt.ask(
            warning_message, choices=["yes", "no"], show_choices=False
        )
        if override_choice == "yes":
            create_sagemaker_config_file()
        else:
            print("[bold red]Aborting YAML configuration![/bold red]")
    else:
        create_sagemaker_config_file()


def create_ec2_config_file() -> None:
    ec2_config = ec2.create_ec2_config_dict()

    ec2_config["EC2"]["region_name"] = Prompt.ask(
        f"\n[magenta] 1. Enter EC2 Region Name[/magenta] (current configured region: [yellow]{ec2.get_aws_region()}[/yellow])"
    )

    ec2_config["EC2"]["ami_id"] = Prompt.ask(
        "\n[magenta] 2. Enter EC2 AMI ID[/magenta] (e.g. for Ubuntu 22.04 x86 [yellow]ami-0c7217cdde317cfec[/yellow])"
    )

    ec2_config["EC2"]["instance_type"] = Prompt.ask(
        "\n[magenta] 3. Enter EC2 Instance Type[/magenta] (e.g. for 1 V100 GPU: [yellow]p3.2xlarge[/yellow])"
    )

    ec2.list_key_pairs()
    ec2_config["EC2"]["key_name"] = Prompt.ask(
        "\n[magenta] 4. Enter EC2 Key Name[/magenta]"
    )

    ec2.list_security_groups()
    security_group_ids: str = Prompt.ask(
        "\n[magenta] 5. Enter EC2 Security Group ID(s) (if multiple, comma-separated)[/magenta]"
    )

    ec2_config["EC2"]["security_group_ids"] = [
        sg.strip() for sg in security_group_ids.split(",")
    ]

    with open(ec2.config_filename, "w") as config_file:
        yaml.dump(ec2_config, config_file, default_flow_style=False)

    shell.print(
        f"\n[bold green]EC2 config file '{config_file.name}' has been created in your working directory.[/bold green]"
    )

    return config_file


def deploy_docker(config_file):
    deploy = Prompt.ask(
        "\n[magenta] 6. Ready to deploy Docker image to ECR and instantiate your EC2 instance?[/magenta] [yellow](yes,no)[/yellow]",
        choices=["yes", "no"],
        show_choices=False,
    )

    if deploy.lower() == "yes":
        ecr_repo_name = Prompt.ask(
            "\n[magenta] - Enter your ECR repository name, if it doesn't exist, it will be created"
        )

        handler = DockerHandler(config_file.name)
        handler.check_or_create_repository(ecr_repo_name)
        handler.pull_takeoff_image(script_dir)
        handler.push_takeoff_image(script_dir, ecr_repo_name)

    else:
        print(
            "Your configuration is almost complete. To launch your EC2 instance manually etc etc."
        )
        # TODO write out manual flow using DockerHandler Class and TitanEC2/TitanSagemaker class


def create_ec2_instance(config_file):
    ec2 = TitanEC2.load_config(config_file.name)
    instance_id, instance_meta_data = ec2.create_instance()
    shell.print(
        f"\n[bold green] Created EC2 instance: {instance_meta_data}[/bold green]"
    )
    return instance_id


def create_sagemaker_config_file() -> None:
    sagemaker_config: Dict[str, Any] = {}
    sagemaker_config["account_id"] = Prompt.ask(
        "[magenta]Enter Sagemaker Account ID[/magenta]: "
    )
    sagemaker_config["model_name"] = Prompt.ask(
        "[magenta]Enter Sagemaker Model Name[/magenta]: "
    )
    sagemaker_config["instance_type"] = Prompt.ask(
        "[magenta]Enter Sagemaker Instance Type[/magenta]: "
    )
    sagemaker_config["endpoint_name"] = Prompt.ask(
        "[magenta]Enter Sagemaker Endpoint Name[/magenta]: "
    )

    with open("sagemaker_config.yaml", "w") as config_file:
        yaml.dump(sagemaker_config, config_file, default_flow_style=False)

    shell.print(
        "[bold green]Sagemaker configuration file 'sagemaker_config.yaml' has been created and filled.[/bold green]"
    )


def main():
    print_banner()
    check_requirements()
    intro()
    choice = select_aws_service()
    if choice == "ec2":
        instance_id, config_file = provision_ec2(choice)
        add_instance_id_to_yaml(config_file.name, instance_id)
    else:
        provision_sagemaker()

if __name__ == "__main__":
    main()
