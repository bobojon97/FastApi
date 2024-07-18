from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .database import get_db
from .services import update_battery_data

app = FastAPI()

@app.get("/battery-data/")
async def battery_data_list(region: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    data = await update_battery_data(db, region)

    if data and 'battery_data' in data:
        battery_data = data['battery_data']
        sorted_battery_data = sorted(
            battery_data, 
            key=lambda x: (
                x['data']['Sum_Batt_Curr'] >= 0, 
                x['data']['Avg_SOC'] != 0
            )
        )
        data['battery_data'] = sorted_battery_data
    
    return data