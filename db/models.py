from typing import Optional
from sqlmodel import Field, SQLModel, Column, Text
from sqlalchemy.dialects import mssql
import uuid
from datetime import datetime
from pydantic import BaseModel





class UserCreate(BaseModel):
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)



class UserLogin(BaseModel):
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)



class CSVUpload(BaseModel):
   source: str = Field(..., description="Fuente del archivo, por ejemplo: 'sistema_externo'")
   category: str = Field(..., description="Categoría del archivo, por ejemplo: 'facturas'")


class CSVCreate(BaseModel):
    user_id: str = Field()
    file_name: str = Field(max_length=25)
    source: str = Field(max_length=25)
    category: str = Field(max_length=25)
    csv_data: dict = Field()



class EventCreate(BaseModel):
    event_type: str
    event_description :str


class EventFilter(BaseModel):
    event_type: str = Field()
    start_date: str = Field()
    end_date: str = Field()

"""
DB TABLES
"""   

class User(SQLModel, table=True):
    __tablename__ = "user"
    user_id:uuid.UUID = Field(sa_column=Column(
            mssql.UNIQUEIDENTIFIER,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)    
    role: str = Field(sa_column=Column(mssql.VARCHAR, nullable=False, server_default="user"))
    created_at: datetime = Field(sa_column=Column(mssql.DATETIME, default=datetime.now))
    is_verified: bool = False
    password_hash: str


    def __repr__(self) -> str:
        return f"<User {self.username}>"    



class DataCSV(SQLModel, table=True):
    __tablename__ = "csv"

    id: uuid.UUID = Field(
        sa_column=Column(mssql.UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(mssql.UNIQUEIDENTIFIER, nullable=False)
    )
    # s3_file_id: str = Field(
    #     sa_column=Column(mssql.VARCHAR(255), nullable=False),
    # )
    file_name: str = Field(
        sa_column=Column(mssql.VARCHAR(255), nullable=False),
    )
    source: str = Field(
        sa_column=Column(mssql.VARCHAR(255), nullable=False),
    )    
    category: str = Field(
        sa_column=Column(mssql.VARCHAR(255), nullable=False),
    )    
    upload_date: datetime = Field(
        sa_column=Column(mssql.DATETIME, default=datetime.now, nullable=False)
    )
    csv_data: dict = Field(
        sa_column=Column(mssql.JSON, nullable=False),
    )    




class Event(SQLModel, table=True):
    __tablename__ = "event"

    event_id: uuid.UUID = Field(
        sa_column=Column(mssql.UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    )

    event_type: str = Field(
        sa_column=Column(mssql.VARCHAR(255), nullable=False),
    )    

    event_description: str = Field(
        sa_column=Column(mssql.TEXT, nullable=False)
    )

    event_date: datetime = Field(
        sa_column=Column(mssql.DATETIME, default=datetime.now, nullable=False)
    )



