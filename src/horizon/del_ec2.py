from rich.console import Console

from .aws.titan_ec2 import TitanEC2
from .utils.ec2_utils import EC2ConfigHandler as handler


shell = Console()

def main():
    ec2 = TitanEC2.load_config(handler.config_filename)
    ec2.delete_instance(ec2.instance_ids)
    shell.print("\n[bold red]instance deleted[/bold red]")
if __name__ == "__main__":
    main()