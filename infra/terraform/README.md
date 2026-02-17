# 🛰️ Terraform Deployment — AWS Uptime Monitor

> Infrastructure as Code implementation of the AWS Uptime Monitor project.

Unlike the manual AWS Console deployment described in the [root README](../../README.md), this version provisions the **entire monitoring architecture using Terraform** — declaratively, reproducibly, and cleanly.

---

## 📦 What This Terraform Configuration Creates

Running this configuration provisions the following AWS resources:

| Resource | Description |
|---|---|
| EC2 Instance | Amazon Linux 2023 with Apache installed via user data |
| Elastic IP | Static public IP attached to the EC2 instance |
| Security Group | Allows inbound HTTP traffic on port 80 |
| IAM Role + Profile | Grants Lambda permission to interact with AWS services |
| Lambda Function | Uptime-check function that polls the EC2 endpoint |
| EventBridge Rule | Scheduled trigger for the Lambda function |
| SNS Topic | Email alerts on detected downtime |
| CloudWatch Logs | Captures all Lambda execution output |

> All infrastructure is defined declaratively and can be recreated at any time with a single command.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                            │
│                                                             │
│   ┌─────────────┐     ┌──────────────┐     ┌───────────┐  │
│   │ EventBridge │────▶│    Lambda    │────▶│    EC2    │  │
│   │  (Schedule) │     │ Uptime Check │     │  Apache   │  │
│   └─────────────┘     └──────┬───────┘     └───────────┘  │
│                              │ on failure                   │
│                              ▼                              │
│                       ┌─────────────┐                      │
│                       │     SNS     │──▶ 📧 Email Alert    │
│                       └─────────────┘                      │
│                              │                              │
│                              ▼                              │
│                      ┌──────────────┐                      │
│                      │  CloudWatch  │                       │
│                      │     Logs     │                       │
│                      └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

**Flow:**
1. **EventBridge** triggers the Lambda function at a fixed interval
2. **Lambda** sends an HTTP request to the EC2 Elastic IP
3. On **failure**, Lambda publishes a message to SNS
4. **SNS** delivers an alert email to the subscribed address
5. **CloudWatch Logs** capture every execution for observability

---

## 📁 Directory Structure

```
infra/terraform/
│
├── main.tf          # Core infrastructure resources
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider & Terraform version constraints
├── user_data.sh     # EC2 bootstrap script (Apache install)
├── .gitignore       # Prevents state and local files from being committed
└── README.md        # This file
```

---

## ✅ Prerequisites

Before deploying, ensure you have the following:

- **Terraform** >= 1.4 — [Install guide](https://developer.hashicorp.com/terraform/install)
- **AWS CLI** configured with appropriate credentials
- An active **AWS account**
- An **email address** to receive SNS uptime alerts

Verify your AWS identity:

```bash
aws sts get-caller-identity
```

---

## 🚀 Deployment Steps

Run all commands from inside `infra/terraform/`:

### 1. Initialize Terraform

Downloads required providers and sets up the backend.

```bash
terraform init
```

### 2. Review the Execution Plan

Preview every resource that will be created before applying.

```bash
terraform plan
```

### 3. Apply Infrastructure

```bash
terraform apply
```

When prompted, confirm with:

```
yes
```

**Terraform will output:**
- `elastic_ip` — the EC2 instance's public IP
- `http_endpoint` — the monitored HTTP URL
- `sns_topic_arn` — the ARN of the SNS alert topic

> 📬 **Check your inbox** — AWS will send a subscription confirmation email. You must confirm it before alerts will be delivered.

---

## 🧪 Testing the System

To simulate a real downtime event:

**1. Connect to the EC2 instance** via SSH or AWS Session Manager.

**2. Stop Apache:**

```bash
sudo systemctl stop httpd
```

Within the next scheduled Lambda run:

- ✅ Lambda detects the failure
- 📧 SNS sends an alert email
- 📋 CloudWatch logs record the error

**3. Restart Apache to resume monitoring:**

```bash
sudo systemctl start httpd
```

Monitoring resumes automatically on the next scheduled execution — no manual intervention required.

---

## 🗑️ Destroying Infrastructure

To remove **all provisioned resources** and avoid ongoing AWS costs:

```bash
terraform destroy
```

> ⚠️ This action is irreversible. All resources defined in this configuration will be permanently deleted.

---

## 💡 Why Infrastructure as Code?

This Terraform implementation transitions the project from manual AWS Console configuration to **production-style DevOps practices**.

| Benefit | Description |
|---|---|
| **Reproducibility** | Recreate the entire stack in minutes, anywhere |
| **Version Control** | Infrastructure changes are tracked in Git like application code |
| **Predictability** | `terraform plan` shows exactly what will change before it happens |
| **Clean Teardown** | `terraform destroy` removes everything with zero leftover resources |
| **Self-Documenting** | The `.tf` files are the authoritative source of truth for the architecture |

---

<p align="center">
  <sub>Part of the <a href="../../README.md">AWS Uptime Monitor</a> project</sub>
</p>
