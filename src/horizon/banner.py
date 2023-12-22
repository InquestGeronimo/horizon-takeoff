from rich.panel import Panel
from rich import print

def print_banner():
    subtitle = "Deploying LLMs with the Takeoff Server on AWS"
    banner = f""" 

   ████████╗ ██╗ ████████╗  █████╗  ███╗   ██╗ ███╗   ███╗ ██╗     
   ╚══██╔══╝ ██║ ╚══██╔══╝ ██╔══██╗ ████╗  ██║ ████╗ ████║ ██║     
      ██║    ██║    ██║    ███████║ ██╔██╗ ██║ ██╔████╔██║ ██║     
      ██║    ██║    ██║    ██╔══██║ ██║╚██╗██║ ██║╚██╔╝██║ ██║     
      ██║    ██║    ██║    ██║  ██║ ██║ ╚████║ ██║ ╚═╝ ██║ ███████╗
      ╚═╝    ╚═╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝     ╚═╝ ╚══════╝  
                                                         
    """
    print(Panel.fit(banner, subtitle=subtitle, style="yellow"))
    print()
