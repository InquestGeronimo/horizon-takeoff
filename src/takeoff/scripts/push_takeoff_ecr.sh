#!/bin/bash

: '
This script pushes a Docker image to Amazon Elastic Container Registry (ECR).

It performs the following steps:
1. Authenticates Docker with ECR.
2. Tags the locally pulled Docker image with the ECR repository URI.
3. Pushes the tagged image to ECR.

Usage:
- Ensure that Docker is authenticated with ECR before running this script.
- Modify the AWS region, ECR repository name, and image name/tag as needed.
- Run the script to push the Docker image to ECR.
'

# AWS Account ID and Region
account=$(aws sts get-caller-identity --query Account | sed -e 's/^"//' -e 's/"$//')
region=$(aws configure get region)

# ECR Repository URL
ecr_account=${account}.dkr.ecr.${region}.amazonaws.com

# Tag the locally pulled image with the ECR repository URI
fullname=$ecr_account/fabulinus:latest

# Push the tagged image to ECR
docker push $fullname
# Optionally, customize the image name/tag if necessary
# docker push <custom-image-name>:<custom-tag>
