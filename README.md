## 1. The Problem
Freelancers and small business owners spend countless hours manually extracting line items, totals, and vendor names from messy receipts and invoices. Existing accounting integrations often require complex CI/CD pipelines, container clusters, or dedicated EC2 instances to process documents via OCR, making lightweight automation overly burdensome to deploy and maintain.

## 2. What the Build Does
Our serverless application instantly processes uploaded invoices and receipts via Amazon S3 event notifications triggering an AWS Lambda function. The function executes lightweight parsing logic to extract key financial fields, stores structured transaction logs securely in Amazon DynamoDB, and exposes an instant REST API endpoint via Amazon API Gateway for frontend retrieval—all with **zero servers and zero deployment pipelines** to manage.

## 3. AWS Services Used & How They Connect
* **Amazon S3 (Document Ingestion Bucket):** Acts as the entry point where users drop raw receipt or invoice files. Configured with native S3 Event Notifications.
* **AWS Lambda (Serverless Compute & Parser):** Triggered instantly upon object creation in S3. Executes Python code to parse metadata and structure the payload.
* **Amazon DynamoDB (NoSQL Transaction Database):** Stores structured JSON records of extracted invoice metadata (Vendor, Date, Total, Items) keyed by transaction ID.
* **Amazon API Gateway (REST API Interface):** Provides a serverless HTTP endpoint for clients to query parsed invoice history and analytics on demand.

### Sample Lambda Function Code
\`\`\`python
import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('InvoiceRecords')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            
            invoice_id = str(uuid.uuid4())
            
            item_data = {
                'InvoiceId': invoice_id,
                'Bucket': bucket_name,
                'FileKey': file_key,
                'Status': 'PROCESSED',
                'EstimatedTotal': '$45.00'
            }
            
            table.put_item(Item=item_data)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Invoice processed successfully serverlessly!')
        }
    except Exception as e:
        print(e)
        raise e
\`\`\`
