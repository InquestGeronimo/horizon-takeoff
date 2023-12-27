<h1 align="center">
Horizon Takeoff
</h1>

<div align="center">
    <img width="400" height="350" src="./img/rocket.png">
</div>

**Horizon Takeoff** is a Python library for simplifying the cloud deployment of LLMs with TitanML's [Takeoff Server](https://github.com/titanml/takeoff-community) on AWS, with a specific focus on EC2 and SageMaker. It does so through an interactive terminal-based User Interface (TUI) that enhances the ease of configuring your cloud environment. View Titan's [Takeoff Server Docs](https://docs.titanml.co/docs/intro) to learn more about its commmunity and Pro features.

With this library, you have two workflows for launching your AWS service with the Takeoff Server:

**1. Text-based User Interface (TUI):** This involves following a step-by-step guide within the terminal to enter various variables. This will automatically configure and save your cloud environment settings in a YAML file, pull, tag and push the Takeoff Server image to ECR, and launch the instance.

**2. Manual Deployment:** For manual deployment, configure a YAML configuration file manually.

## Requirements

**1.** AWS CLI installed and configured on local machine.

**2.** Docker installed.

**3.** Own an AWS account with the following configurations:

* Have an instance profile role with access to `AmazonEC2ContainerRegistryReadOnly`. This will allow access to Docker pulls from ECR within an instance.

* Own a security group allowing inboud traffic for `port 8000` (community edition), `port 3000` (pro edition). This will expose the Docker endpoint for API calling.

> Currently, only EC2 instance deployment is stable, Sagemaker is under development. Also Pro Takeoff Server with Pro features is in the job queue.

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

After you've finished the TUI workflow, an automatically generated YAML configuration file will be stored in your working directory. This file will trigger the staging process for your instance on its own. Please be patient and wait for a few minutes as the instance downloads the LLM model and initiates the Docker container containing the Takeoff Server. To keep track of the progress and access cloud initialization logs, you can SSH into your instance using the following command:

```bash
ssh -i ~/<pem.key> <user>@<public-ipv4-dns>  # e.g. ssh -i ~/aws.pem ubuntu@ec2-44-205-255-59.compute-1.amazonaws.com
```

To view the cloud init logs and ensure that your container is up and running, run the following command:

```bash
cat /var/log/cloud-init-output.log
```

if you find the Uvicorn URL endpoint displayed within them, it indicates that your Docker container is up and running, and you are now prepared to start making API calls for LLM inference.

# Calling API Endpoint

```py
from horizon import EC2Endpoint

endpoint = EC2Endpoint()
generation = endpoint('List 3 things to do in London.')
print(generation)
```

# Deleting Instance

To delete your working instance, run:

```bash
del-instance
```

# YAML Configuration

To bypass the TUI, you can create your YAML config manually. Make sure to enter the following variables save it as `ec2_config.yaml`:

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

# Launch Manually
To launch an EC2 instance, load the YAML file. These commands will pull the Takeoff Docker image, tag it for ECR, and push it to ECR. An instance will be created, the Docker image from ECR will be pulled in the instance and the container will start automatically:

```py
titan = TitanEC2.load_config("ec2_config.yaml")
instance = titan.create_instance()
print(instance)
```
### Staging

You can keep up with the process as described in the `Staging` section.

### Calling API

Same process in the `Calling API` section.
