# Terraform – Provision AWS Uptime Monitor

## Prereqs
- Terraform installed
- AWS CLI configured (`aws configure`)
- An EC2 key pair already exists in AWS (matches `var.key_name`)

## Setup
Create a tfvars file:

```hcl
alert_email = "YOUR_EMAIL"
Run

terraform init
terraform plan
terraform apply

Destroy

terraform destroy
