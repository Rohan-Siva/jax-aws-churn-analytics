import os
import boto3
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ModelStorage:
\
\
       
    
    def __init__(self, storage_type: str = "local", **kwargs):
        self.storage_type = storage_type
        
        if storage_type == "local":
            self.local_path = Path(kwargs.get('local_path', './models'))
            self.local_path.mkdir(parents=True, exist_ok=True)
        elif storage_type == "s3":
            self.s3_client = boto3.client('s3')
            self.bucket_name = kwargs.get('bucket_name')
            self.s3_prefix = kwargs.get('s3_prefix', 'models/')
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
    
    def upload(self, local_file: str, remote_key: str):
\
\
\
\
\
\
           
        if self.storage_type == "local":
                                     
            logger.info(f"Model stored locally at {local_file}")
        
        elif self.storage_type == "s3":
            try:
                self.s3_client.upload_file(
                    local_file,
                    self.bucket_name,
                    f"{self.s3_prefix}{remote_key}"
                )
                logger.info(f"Uploaded to s3://{self.bucket_name}/{self.s3_prefix}{remote_key}")
            except Exception as e:
                logger.error(f"S3 upload failed: {e}")
                raise
    
    def download(self, remote_key: str, local_file: str):
\
\
\
\
\
\
           
        if self.storage_type == "local":
                           
            pass
        
        elif self.storage_type == "s3":
            try:
                self.s3_client.download_file(
                    self.bucket_name,
                    f"{self.s3_prefix}{remote_key}",
                    local_file
                )
                logger.info(f"Downloaded from s3://{self.bucket_name}/{self.s3_prefix}{remote_key}")
            except Exception as e:
                logger.error(f"S3 download failed: {e}")
                raise
    
    def list_models(self) -> list:
\
\
           
        if self.storage_type == "local":
            return [f.name for f in self.local_path.glob("model_*.pkl")]
        
        elif self.storage_type == "s3":
            try:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=self.s3_prefix
                )
                return [obj['Key'] for obj in response.get('Contents', [])]
            except Exception as e:
                logger.error(f"S3 list failed: {e}")
                return []
