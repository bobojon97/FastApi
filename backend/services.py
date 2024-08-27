from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Device, BatteryData
from .utils import adapt_device_name

async def update_battery_data(session: AsyncSession, selected_region=None):
    devices = await session.execute(select(Device))
    devices = devices.scalars().all()

    latest_entries = []
    regions = set()

    controller_names = sum([adapt_device_name(device.name, device.supports_multiple_batteries) for device in devices], [])

    latest_entries_qs = await session.execute(
        select(BatteryData).filter(BatteryData.controller_name.in_(controller_names)).order_by(BatteryData.controller_name, BatteryData.timestamp.desc())
    )
    latest_entries_qs = latest_entries_qs.scalars().all()

    latest_entries_map = {}
    for entry in latest_entries_qs:
        if entry.controller_name not in latest_entries_map:
            latest_entries_map[entry.controller_name] = entry

    for device in devices:
        controller_names = adapt_device_name(device.name, device.supports_multiple_batteries)
        details = [latest_entries_map[cn] for cn in controller_names if cn in latest_entries_map]

        if details:
            sum_batt_curr = sum(entry.Batt_Curr for entry in details)
            sum_full_capacity = sum(entry.Full_Capacity for entry in details)
            sum_remaining_capacity = sum(entry.Remaining_Capacity for entry in details)
            regions.update(entry.region for entry in details)

            aggregated_data = {
                'Avg_Batt_Volt': sum(entry.Batt_Volt for entry in details) / len(details),
                'Sum_Batt_Curr': sum_batt_curr,
                'Avg_SOC': sum(entry.SOC for entry in details) / len(details),
                'Avg_SOH': sum(entry.SOH for entry in details) / len(details),
                'Avg_Cycle': sum(entry.Cycle for entry in details) / len(details),
                'Avg_Mos_Temp': sum(entry.Mos_Temp for entry in details) / len(details),
                'Avg_Env_Temp': sum(entry.Env_Temp for entry in details) / len(details),
                'Avg_Full_Capacity': sum(entry.Full_Capacity for entry in details) / len(details),
                'Sum_Full_Capacity': sum_full_capacity,
                'Avg_Remaining_Capacity': sum(entry.Remaining_Capacity for entry in details) / len(details),
                'Sum_Remaining_Capacity': sum_remaining_capacity,
                'Avg_Temp_Max_Cell': sum(entry.Temp_Max_Cell for entry in details) / len(details),
                'Avg_Temp_Min_Cell': sum(entry.Temp_Min_Cell for entry in details) / len(details),
            }
            latest_entry = details[-1]
            latest_entries.append({
                'controller_name': device.name,
                'data': aggregated_data,
                'timestamp': latest_entry.timestamp,
                'region': latest_entry.region,
                'dga': 'Да' if device.dga else 'Нет',
                'details': details,
                'is_grouped': device.supports_multiple_batteries
            })

    if selected_region:
        latest_entries = [entry for entry in latest_entries if entry['region'] == selected_region]

    data = {
        'battery_data': latest_entries,
        'regions': sorted(regions),
        'selected_region': selected_region,
    }

    return data