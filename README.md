# AWS Uptime Monitor – DevOps Cloud Project

This project is a cloud-based uptime monitoring system built on AWS.  
Its purpose is simple: continuously check whether a public service is reachable, and notify me automatically when it is not.

I built this project to transition my existing local monitoring experience into a real cloud environment and to deeply understand how AWS services work together in a production-style setup.

The system was designed, deployed, broken, observed, and recovered intentionally, to validate the full DevOps feedback loop.

---

## What the system does

A Linux server running on AWS EC2 exposes a simple HTTP endpoint using Apache.  
A serverless AWS Lambda function periodically sends HTTP requests to that endpoint.  

If the request succeeds, the system logs the result and continues silently.  
If the request fails, the system automatically sends an email alert.

The checks run on a schedule without manual intervention, and all executions are logged for observability and troubleshooting.

---

## Architecture overview

The monitored service runs on an EC2 instance with Apache installed and a permanent Elastic IP attached. This instance represents a real, publicly reachable target that can fail and recover like a production system.

An EventBridge schedule acts as the time trigger. It invokes a Lambda function at a fixed interval.

The Lambda function performs the HTTP check against the EC2 endpoint. It does not maintain state and runs only for the duration of the check.

When a failure is detected, the Lambda function publishes a message to an SNS topic.  
SNS then delivers the alert to my email address.

All Lambda executions and outcomes are recorded in CloudWatch Logs, allowing inspection of latency, status codes, and errors.

---

## How I validated the system

The system was not considered complete until failure and recovery were proven.

Apache was intentionally stopped on the EC2 instance to simulate an outage.  
The monitoring function detected the failure and sent an alert email.

Apache was then restarted, the endpoint recovered, and subsequent checks returned to a healthy state without further alerts.

This confirmed that monitoring, alerting, and recovery all functioned correctly end-to-end.

---

## What I learned

This project helped solidify the mental separation between core AWS services:

EC2 as a long-running server that I manage directly.  
Lambda as a short-lived, stateless execution environment.  
EventBridge as a scheduling and orchestration mechanism.  
SNS as a decoupled notification delivery service.

Beyond individual services, the key learning was architectural: monitoring should be external to the system being monitored, automated, observable, and able to fail independently.

I also gained hands-on experience with IAM permissions, cloud networking concepts such as public IPs and ports, and CloudWatch as an operational visibility tool.

---

## Current state

The system is fully functional and deployed manually through the AWS Console.  
It successfully performs scheduled uptime checks, logs results, and sends alerts on failure.

At this stage, the focus has been understanding and validating the architecture rather than automation.

---

## Next steps

The next phase of this project is to convert the manual setup into Infrastructure as Code using Terraform or AWS SAM, allowing the entire system to be recreated predictably from source control.

Planned improvements also include reducing alert noise through failure thresholds and extending the monitor to support multiple targets.

---

## Why this project exists

This project is not a tutorial copy or a simulated exercise.  
It represents a deliberate transition from local automation tools into cloud-native DevOps practices, with an emphasis on understanding, observability, and operational correctness.
