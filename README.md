<h1 align="center">
Horizon Takeoff
</h1>

<div align="center">
    <img width="400" height="350" src="./img/rocket.png">
</div>

Horizon Takeoff is a Python library for simplifying the deployment of TitanML's Takeoff server on AWS, with a specific focus on EC2 and SageMaker. This toolkit offers a streamlined approach to setting up cloud instances and containers. It does so through an interactive terminal-based User Interface (TUI) that enhances the ease of configuring your cloud environment.


You have two workflows for launching your AWS service:

**1. Text-based User Interface (TUI):**

This involves using a step-by-step guide within the TUI to enter various variables, which in turn, initiates the process of spinning up an EC2/Sagemaker instance. This will automatically configure your cloud environment settings, pull and push Takeoff Server image to ECR, and launch the instance.

**2. Manual Deployment:**

For manual deployment, you will need to configure a YAML configuration file. After configuration, you can launch the TitanEC2 instance deployer object to deploy your service. 

> Currently, only EC2 instance deployment is stable, Sagemaker is under development.

# Install <img align="center" width="30" height="29" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install horizon-takeoff
```

# Launching the TUI <img align="center" width="30" height="29" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

After installation, launch the entrypoint to get your TUI launched. Enter `horizon-takeoff <service>`:


```py
horizon-takeoff ec2
```

Launch:

<div style="display: flex; justify-content: center;">
  <video muted controls src="https://private-user-images.githubusercontent.com/79061523/293062674-cd626c61-4397-4498-91d3-f11e2e4ea540.mp4" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px"></video>
</div>

# Calling API Endpoint

```py
from horizon import EC2Endpoint

endpoint = EC2Endpoint()
generation = endpoint('List 3 things to do in London.')

print(generation)
```


# Manual Configuration

Your 

```yaml
EC2:
  ami_id: ami-0c7217cdde317cfec             # The ID of the Amazon Machine Image (AMI) to use for EC2 instances.
  ecr_repo_name: takeoff                    # The name of the Elastic Container Registry (ECR) repository.
  hardware: cpu                             # The hardware type: 'cpu' or 'gpu'
  hf_model_name: tiiuae/falcon-7b-instruct  # The name of the Hugging Face (HF) model to use.
  instance_ids:                             # List of EC2 instance ID.
    - i-0234f3336b2ccd78a                   
  instance_role_arn: arn:aws:iam::^^^:path  # The ARN of the IAM instance profile role.
  instance_type: c5.2xlarge                 # The EC2 instance type.
  key_name: aws                             # The name of the AWS key pair.
  region_name: us-east-1                    # The AWS region name.
  security_group_ids:                       # List of security group ID(s) associated with the instances.
    - sg-0fefe7b366b0c0843                  

  ```