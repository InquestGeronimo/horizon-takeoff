from rich.panel import Panel
from rich import print


def print_banner():
    style = "yellow"
    subtitle = "Deploying the Takeoff Server on AWS for LLMs Inference"
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
