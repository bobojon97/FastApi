import re
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from backend.utils import adapt_device_name
from .database import get_db
from .services import update_battery_data
from .models import AggregatedBatteryData, BatteryData, DGAStatus, DGAStatusHistory, Device

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

@app.get("/battery-data/detail/{controller_name}")
async def battery_data_detail(controller_name: str, db: AsyncSession = Depends(get_db)):
    match = re.match(r'^(\d*.*?)(B\d+)?$', controller_name)
    if match:
        base_name = match.group(1)
    else:
        raise HTTPException(status_code=404, detail="Invalid controller name format.")
    
    result = await db.execute(
        select(Device).where(Device.name.ilike(base_name))
    )
    devices = result.scalars().all()
    
    if not devices:
        raise HTTPException(status_code=404, detail="No Device matches the given query.")
    
    if len(devices) > 1:
        device = sorted(devices, key=lambda d: d.name)[0]
    else:
        device = devices[0]

    controller_names = adapt_device_name(device.name, device.supports_multiple_batteries)

    result = await db.execute(
        select(AggregatedBatteryData)
        .where(AggregatedBatteryData.controller_name == controller_name)
        .order_by(AggregatedBatteryData.timestamp.desc())
    )
    aggregated_data = result.scalars().all()
    
    if aggregated_data:
        battery_data = aggregated_data
        is_aggregated = True
    else:
        if device.supports_multiple_batteries:
            result = await db.execute(
                select(BatteryData)
                .where(BatteryData.controller_name == controller_name)
                .order_by(BatteryData.timestamp.desc())
            )
        else:
            result = await db.execute(
                select(BatteryData)
                .where(BatteryData.controller_name.in_(controller_names))
                .order_by(BatteryData.timestamp.desc())
            )
        battery_data = result.scalars().all()
        is_aggregated = False
    
    result = await db.execute(
        select(DGAStatusHistory)
        .where(DGAStatusHistory.controller_name == controller_name)
        .order_by(DGAStatusHistory.timestamp)
    )
    dga_status_history = result.scalars().all()

    battery_data_with_status = []
    last_status = None
    last_timestamp = None

    for data in battery_data:
        status_entry = next((entry for entry in dga_status_history if entry.timestamp <= data.timestamp), None)
        if status_entry:
            last_status = status_entry.dga_status
            last_timestamp = str(status_entry.timestamp)
        battery_data_with_status.append({
            "controller_name": data.controller_name,
            "Batt_Volt": data.Batt_Volt,
            "Batt_Curr": data.Batt_Curr,
            "SOC": data.SOC,
            "SOH": data.SOH,
            "Cycle": data.Cycle,
            "Mos_Temp": data.Mos_Temp,
            "Env_Temp": data.Env_Temp,
            "Full_Capacity": data.Full_Capacity,
            "Remaining_Capacity": data.Remaining_Capacity,
            "Temp_Max_Cell": data.Temp_Max_Cell,
            "Temp_Min_Cell": data.Temp_Min_Cell,
            "region": data.region,
            "timestamp": str(data.timestamp),
            "status": last_status,
            "status_timestamp": last_timestamp,
            "is_aggregated": is_aggregated
        })

    return {
        "battery_data": battery_data_with_status,
    }