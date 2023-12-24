from rich.panel import Panel
from rich import print


def print_banner():
    style = "yellow"
    subtitle = "Deploying LLMs with the Takeoff Server on AWS"
    banner = """ 

   ████████╗ ██╗ ████████╗  █████╗  ███╗   ██╗ ███╗   ███╗ ██╗     
   ╚══██╔══╝ ██║ ╚══██╔══╝ ██╔══██╗ ████╗  ██║ ████╗ ████║ ██║     
      ██║    ██║    ██║    ███████║ ██╔██╗ ██║ ██╔████╔██║ ██║     
      ██║    ██║    ██║    ██╔══██║ ██║╚██╗██║ ██║╚██╔╝██║ ██║     
      ██║    ██║    ██║    ██║  ██║ ██║ ╚████║ ██║ ╚═╝ ██║ ███████╗
      ╚═╝    ╚═╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝     ╚═╝ ╚══════╝  
                                                         
    """
    print(Panel.fit(banner, subtitle=subtitle, style=style))
    print()
