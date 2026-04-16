

# 🚀 KEDA + AWS SQS Autoscaling POC

This demo shows how to use **KEDA** to autoscale Kubernetes consumers based on **AWS SQS queue length**.  
Producer pushes messages → KEDA detects queue depth → consumer pods scale up → messages processed → pods scale back down to zero.

---

## 01
Create AWS SQS Queue
Set up an SQS queue in AWS that KEDA will monitor.

Go to AWS Console → SQS

Create a new queue (Standard)

Note down the Queue URL and Region

## 02
Create Kubernetes Secret for AWS Credentials
Store AWS access keys securely in your cluster.

kubectl apply -f aws-secret.yaml

Secret must contain AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

Namespace: kedademo

## 03
Create TriggerAuthentication
Tell KEDA how to use the AWS credentials.

kubectl apply -f trigger-auth.yaml

Reference the secret keys

Name it keda-aws-auth

Namespace: kedademo

## 04
Deploy Consumer
Deploy the consumer app that reads messages from SQS.

kubectl apply -f consumer-deploy.yaml

Set replicas: 0 so KEDA controls scaling

Mount aws-secrets via envFrom

## 05
Deploy ScaledObject
Configure KEDA to scale the consumer based on SQS queue length.

kubectl apply -f sqs-scaledobject.yaml

Set minReplicaCount: 0 and maxReplicaCount: 10

Use queueURLFromEnv or hardcoded URL

Reference keda-aws-auth

## 06
Run Producer
Send test messages to the SQS queue.

python src/producer.py

Produces 10 messages

Each message appears in SQS

## 07
Watch Scaling
Observe pods scaling up and down automatically.

kubectl get pods -n kedademo -w

Pods start at 0

Scale up when messages arrive

Scale back down after queue empties


---

## ✅ Expected Behavior
- Start: **0 pods**.  
- Producer sends messages → queue fills.  
- KEDA scales consumer pods up (e.g., 0 → 3).  
- Consumers process messages → queue empties.  
- After cooldown → pods scale back down to 0.

---

## 🧩 Files in This Demo
- `aws-secret.yaml` → Kubernetes Secret with AWS credentials.  
- `trigger-auth.yaml` → KEDA TriggerAuthentication referencing the secret.  
- `consumer-deploy.yaml` → Deployment for consumer app.  
- `sqs-scaledobject.yaml` → ScaledObject defining scaling rules.  
- `producer.py` → Python script to send messages to SQS.

---
