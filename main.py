from fastapi import FastAPI, HTTPException, File, UploadFile
from minio import Minio
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logs

# Load .env file
load_dotenv()

client = Minio(
    "localhost:9000",
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False  
)

class FileDetails(BaseModel):
    objectName: str
    fileName: str
    contentType: str
     

app = FastAPI()

@app.post('/buckets/{bucket_name}')
def addBucket(bucket_name: str):
    logs.logger.info(f"Adding bucket '{bucket_name}' if not exists")

    try:
        if client.bucket_exists(bucket_name):
            return {"message": f"Bucket '{bucket_name}' already exists"}
        else:
            client.make_bucket(bucket_name)
            return {"message": f"Bucket '{bucket_name}' created successfully"}
    except Exception as e:
        logs.logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create bucket")


@app.post('/buckets/{bucket_name}/upload')
async def addFileToBucket(bucket_name: str, file: UploadFile = File(...)):
    logs.logger.info(f"Adding file '{file.filename}' to bucket: {bucket_name}")

    try:
        # Check if the bucket exists
        if not client.bucket_exists(bucket_name):
            logs.logger.info(f"Bucket '{bucket_name}' does not exist, creating it")
            client.make_bucket(bucket_name)

        # Save the file temporarily to disk
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # Upload the file to MinIO
        client.fput_object(bucket_name, file.filename, temp_file_path)

        # Clean up the temporary file
        os.remove(temp_file_path)

        return {"message": f"File '{file.filename}' uploaded to bucket '{bucket_name}' successfully"}

    except Exception as e:
        logs.logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload file: {str(e)}")
