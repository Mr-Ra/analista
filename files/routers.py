from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from db.models import CSVCreate, EventCreate, EventFilter
from files.service import FileService
from events.service import EventService
from sqlmodel.ext.asyncio.session import AsyncSession
from db.db_engine import get_session
from pprint import pprint



from fastapi import (
    APIRouter,
    status,
    Depends,
    UploadFile,
    File,
    Form
)

from auth.dependencies import (
    ValidateAccessTokenBearer,
    RoleTokenBearer

)

from files.utils import (
    get_csv_file_validations,
    serialize_csv_data,
)



files_router = APIRouter()
file_service = FileService()
event_service = EventService()

role_checker = Depends(RoleTokenBearer(["admin"]))


@files_router.post("/upload_csv", dependencies=[role_checker], description="Procesar archivo CSV")
async def upload_csv_file(
    csv_file: UploadFile = File(..., description="Archivo CSV a cargar"),
    source: str = Form(..., description="Fuente del archivo CSV"),
    category: str = Form(..., description="Categoría del archivo CSV"),   
    token_details: dict = Depends(ValidateAccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
    ):

    csv_data = await serialize_csv_data(uploaded_csv=csv_file)  

    csv_file.file.seek(0)

    file_validations = await get_csv_file_validations(uploaded_csv=csv_file)
    

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():

        # file_validations = get_csv_file_validations(uploaded_csv=csv_file)
        # csv_data = await serialize_csv_data(uploaded_csv=csv_file)     

        user_id = token_details["user"]["user_id"]
        
        filename = csv_file.filename

        csv_payload = CSVCreate(
            user_id = user_id,
            file_name = filename,
            source = source,
            category = category,
            csv_data = csv_data
        )

        csv_file.file.seek(0)
        await file_service.create_csv_file_record(csv_payload=csv_payload, session=session)

        await file_service.upload_to_s3_bucket(uploaded_file=csv_file, filename=filename)

        event_payload = EventCreate(
            event_type="CSV Upload",
            event_description="New csv file on S3 bucket and inner data processed"
        )
        await event_service.create_event(event_payload=event_payload, session=session)        

        return JSONResponse(content={"validations":file_validations})




    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )    




@files_router.post("/analyze", dependencies=[role_checker], description="Analizar archivos PDFs o imagénes con Ai")
async def upload_any_file(
    file: UploadFile = File(..., description="Archivo CSV a cargar"),
    token_details: dict = Depends(ValidateAccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
    ):

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():

        await file_service.save_temp_file(uploaded_file=file, filename=file.filename)

        if "image" in file.content_type:
            vision_inference = await file_service.get_vision_inference(filename=file.filename)

            event_payload = EventCreate(
                event_type="AI",
                event_description="Vision inference"
            )
            

            try:
                await event_service.create_event(event_payload=event_payload, session=session)
            
                return vision_inference            

            except:
                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inténtelo de nuevo"
                )
        

            
        
        elif "pdf" in file.content_type:
            pdf_inference = await file_service.get_rag_inference(filename=file.filename)

            event_payload = EventCreate(
                event_type="AI",
                event_description="PDF inference"
            )

            try:
                await event_service.create_event(event_payload=event_payload, session=session)
                
                return pdf_inference
            
            except:

                raise HTTPException(
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Inténtelo de nuevo"
                )                
        
        else:

            return HTTPException(
                status_code=status.WS_1003_UNSUPPORTED_DATA,
                detail="Formato de archivo no soportado"
            )


    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )



