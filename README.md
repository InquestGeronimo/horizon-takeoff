<h1 align="center">
Horizon Takeoff
</h1>

<div align="center">
    <img width="400" height="350" src="./img/rocket.png">
</div>

**Horizon Takeoff** is a Python library for simplifying the cloud deployment of LLMs with TitanML's [Takeoff Server](https://github.com/titanml/takeoff-community) on AWS, with a specific focus on EC2 and SageMaker. The deployment process is facilitated through an interactive terminal-based User Interface (TUI), enhancing the ease and efficiency of configuring your cloud environment. To gain a deeper understanding of the features offered by the Takeoff Server, one should refer to [TitanML's documentation](https://docs.titanml.co/docs/intro).

With Horizon-Takeoff, you have the flexibility to choose between two distinct workflows for launching your AWS service:

**1. Terminal User Interface (TUI):** This approach guides you through a step-by-step process within the terminal. This procedure configures and preserves your cloud environment settings in a YAML file, handles pulling, tagging, and pushing of the Takeoff Server image to AWS's Elastic Container Registry (ECR), and initiates the instance launch.

**2. Manual Deployment:** Alternatively, you can can configure the YAML config file according to your specific requirements without the TUI. Further details found in the `YAML Configuration` section.

## Requirements

**1.** AWS CLI installed and configured on local machine.

**2.** Docker installed.

**3.** Own an AWS account with the following configurations:

* Have an instance profile role with access to `AmazonEC2ContainerRegistryReadOnly`. This will allow access to Docker pulls from ECR within an instance.

* Own a security group allowing inboud traffic for `port 8000` (community edition), `port 3000` (pro edition). This will expose the Docker endpoint for API calling.

> Currently, only EC2 instance deployment on the Community edition server is stable, Sagemaker and/or Takeoff Server with Pro features is under development.

# Install <img align="center" width="30" height="29" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install horizon-takeoff
```

# Launching the TUI <img align="center" width="30" height="29" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

After installation, launch the entrypoint to get your TUI launched. Enter `horizon-takeoff <service>`:


```bash
horizon-takeoff ec2
```

<div style="display: flex; justify-content: center;">
  <video muted controls src="https://private-user-images.githubusercontent.com/79061523/293062674-cd626c61-4397-4498-91d3-f11e2e4ea540.mp4" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px"></video>
</div>

# Staging

After you've finished the TUI workflow, a YAML configuration file will be automatically stored in your working directory. This file will trigger the staging process of your deployment and you will receive a notification in terminal of your instance launch. 

Wait a few minutes as the instance downloads the LLM model and initiates the Docker container containing the Takeoff Server. To keep track of the progress and access your instance's initialization logs, you can SSH into your instance using the following command:

```bash
ssh -i ~/<pem.key> <user>@<public-ipv4-dns>  # e.g. ssh -i ~/aws.pem ubuntu@ec2-44-205-255-59.compute-1.amazonaws.com
```

To view your instance logs and confirm that your container is up and running, run:

```bash
cat /var/log/cloud-init-output.log
```

if you find the Uvicorn URL endpoint displayed in the logs, it indicates that your Docker container is running, and you are now prepared to start making API calls to the inference endpoint.

# Calling the Inference Endpoint

Once you've initialized the EC2Endpoint class, you can effortlessly invoke your LLM in the cloud with just a single line of code.

```py
from horizon import EC2Endpoint

endpoint = EC2Endpoint()
generation = endpoint('List 3 things to do in London.')
print(generation)
```

# Deleting Instance

To delete your working instance via the terminal, run:

```bash
horizon-del
```

# YAML Configuration

If you prefer to bypass the TUI, you can enter your YAML configuration manually. Make sure to add the following EC2-related variables and save them in a `ec2_config.yaml` file:

```yaml
EC2:
  ami_id: ami-0c7217cdde317cfec             # The ID of the Amazon Machine Image (AMI) to use for EC2 instances.
  ecr_repo_name: takeoff                    # The name of the Elastic Container Registry (ECR) repository.
  hardware: cpu                             # The hardware type: 'cpu' or 'gpu'
  hf_model_name: tiiuae/falcon-7b-instruct  # The name of the Hugging Face model to use.
  instance_ids:                             # List of EC2 instance ID.
    - i-0234f3336b2ccd78a                   
  instance_role_arn: arn:aws:iam::^^^:path  # The ARN of the IAM instance profile role.
  instance_type: c5.2xlarge                 # The EC2 instance type.
  key_name: aws                             # The name of the AWS key pair.
  region_name: us-east-1                    # The AWS region name.
  security_group_ids:                       # List of security group ID(s) associated with the instances.
    - sg-0fefe7b366b0c0843                  
```

# Launch in Python

Upon configuring the YAML file, you'll need use the `DockerHandler` and `TitanEC2` classes to handle Docker image flows and instance launch.

### Docker 

Load the YAML file into the `DockerHandler` class. These commands will pull the Takeoff Docker image, tag it, and push it to ECR:

```py
from horizon import DockerHandler, TitanEC2

docker = DockerHandler("ec2_config.yaml")

docker.pull_takeoff_image()
docker.push_takeoff_image()
```

### Create Instance

Launch the EC2 instance:

```py
titan = TitanEC2("ec2_config.yaml")
instance = titan.create_instance()
print(instance)
```
Revisit the `Staging` and 'Calling the Inference Endpoint` section for final steps