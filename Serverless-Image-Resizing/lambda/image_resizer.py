import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')
size = int(os.environ['THUMBNAIL_SIZE'])

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Get image from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        image = Image.open(io.BytesIO(image_data))
        
        # Resize
        image.thumbnail((size, size))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        
        # Upload resized image
        resized_key = f"resized/{key}"
        s3.put_object(
            Bucket=os.environ['DEST_BUCKET'],
            Key=resized_key,
            Body=buffer,
            ContentType='image/jpeg'
        )
    return {'statusCode': 200}