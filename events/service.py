from db.models import Event, EventFilter, EventCreate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import pandas as pd
from io import BytesIO



class EventService:
    async def create_event(self, event_payload: EventCreate, session: AsyncSession):
        new_event = Event(
            event_type=event_payload.event_type,
            event_description=event_payload.event_description,
        )
        session.add(new_event)
        await session.commit()
        return new_event


    async def filter_events(self, filter_payload: EventFilter, session: AsyncSession):
        query = select(Event)
        start_date = datetime.fromisoformat(filter_payload.start_date)
        end_date = datetime.fromisoformat(filter_payload.end_date)
        
        query = query.where(Event.event_type.ilike(f"%{filter_payload.event_type}%"))        
    
        query = query.where(Event.event_date >= start_date)

        query = query.where(Event.event_date <= end_date)



        # Ejecutar la consulta
        result = await session.exec(query)

        events = result.all()

        for event in events:
            event.event_id = str(event.event_id)[:7]

        return events
    
        
    async def create_excel_from_events(self, filter_payload: EventFilter, session: AsyncSession):
        logs = await self.filter_events(
            filter_payload=filter_payload,
            session=session
        )

        formatted_logs = []
        for log in logs:
            formatted_log = {}
            for key, value in dict(log).items():
                if key == "event_date":
                    # Convertir fechas a string
                    try:
                        formatted_log[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                        formatted_log[key] = "Fecha inválida"
                else:
                    formatted_log[key] = value
            formatted_logs.append(formatted_log)

        
        



        df = pd.DataFrame(formatted_logs)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
            
        output.seek(0)

        return output