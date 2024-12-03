from db.models import (
    CSVCreate, 
    DataCSV,
    EventCreate,
    EventFilter,
    Event
)

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import UploadFile
import boto3
import os
from dotenv import load_dotenv
from sqlmodel import select
from llms.llm_providers import get_vision_inference, get_rag_inference


load_dotenv()


BUCKET_NAME = os.getenv("BUCKET_NAME")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")


class FileService:
    def __init__(self, s3_file_key: str = ""):
        self.uploads_dir = "./uploads/"
        self.s3_file_key:str = s3_file_key


    async def create_csv_file_record(self, csv_payload: CSVCreate, session: AsyncSession):
        csv_data_dict = csv_payload.model_dump()
        
        new_csv_file_record = DataCSV(**csv_data_dict)

        session.add(new_csv_file_record)

        await session.commit()

        self.s3_file_key = str(new_csv_file_record.id).upper()

        return new_csv_file_record
    
    
    async def upload_to_s3_bucket(self, uploaded_file: UploadFile, filename: str):
        #s3 client localstack
        s3_client = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,  # Usar las claves fake de LocalStack
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,  # Usar las claves fake de LocalStack
            region_name="us-east-1"
        )


        try:
            # Subir archivo a S3
            print(BUCKET_NAME)
            response = s3_client.upload_fileobj(
                Key=self.s3_file_key,
                Fileobj=uploaded_file.file,  # Stream del archivo cargado
                Bucket=BUCKET_NAME,
            )
            
            print(f"Document {filename} uploaded successfully with s3_key: {self.s3_file_key}")
            return

        except Exception as e:
            print(f"Error during file uploading {e}")
            raise    


    async def save_temp_file(self, uploaded_file: UploadFile, filename: str):
        file_location = os.path.join(self.uploads_dir, filename)
        with open(file_location, "wb") as file_object:
            file_object.write(await uploaded_file.read())  

        return      
            

    def get_s3_file_key(self):
        return self.s3_file_key
    
    
    async def get_vision_inference(self, filename):
        return get_vision_inference(filename=filename)
    
    async def get_rag_inference(self, filename):
        return get_rag_inference(filename=filename)




        


