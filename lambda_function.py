import json
import boto3
import uuid

# Initialize DynamoDB resource and reference your table name
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('InvoiceRecords')

def lambda_handler(event, context):
    try:
        # Process records triggered by the S3 event notification
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            
            # Generate a unique transaction/invoice ID
            invoice_id = str(uuid.uuid4())
            
            # Structure the extracted metadata item
            item_data = {
                'InvoiceId': invoice_id,
                'Bucket': bucket_name,
                'FileKey': file_key,
                'Status': 'PROCESSED',
                'EstimatedTotal': '$45.00'
            }
            
            # Save the structured record into Amazon DynamoDB
            table.put_item(Item=item_data)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Invoice processed successfully serverlessly!')
        }
        
    except Exception as e:
        print(f"Error processing invoice: {str(e)}")
        raise e
