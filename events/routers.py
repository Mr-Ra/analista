from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from auth.dependencies import ValidateAccessTokenBearer, RoleTokenBearer
from db.models import EventFilter
from db.db_engine import get_session
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from events.service import EventService

events_router = APIRouter()
event_service = EventService()
role_checker = Depends(RoleTokenBearer(["admin"]))



@events_router.post("/get_events", dependencies=[role_checker], description="Obtener registros de eventos")
async def get_event(
    filter_payload: EventFilter,
    token_details: dict = Depends(ValidateAccessTokenBearer()),
    session: AsyncSession = Depends(get_session)    
    ):


    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        events = await event_service.filter_events(filter_payload=filter_payload, session=session)

        return events

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )




@events_router.post("/export_events", dependencies=[role_checker], description="Generar reporte de eventos")
async def export_event(
    filter_payload: EventFilter,
    token_details: dict = Depends(ValidateAccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
    ):

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        excel_file = await event_service.create_excel_from_events(filter_payload, session=session)

        start_date = filter_payload.start_date.replace(":", "-").replace(" ", "_")
        end_date = filter_payload.end_date.replace(":", "-").replace(" ", "_")
        logs_filename = f"event_logs_{start_date}_to_{end_date}.xlsx"        

        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={logs_filename}"}
        )        


    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )    