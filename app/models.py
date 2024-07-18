from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BatteryData(Base):
    __tablename__ = 'battery_data'

    id = Column(Integer, primary_key=True, index=True)
    controller_name = Column(String(50))
    Batt_Volt = Column(Float)
    Batt_Curr = Column(Float)
    SOC = Column(Float)
    SOH = Column(Float)
    Cycle = Column(Integer)
    Mos_Temp = Column(Float)
    Env_Temp = Column(Float)
    Full_Capacity = Column(Float)
    Remaining_Capacity = Column(Float)
    Temp_Max_Cell = Column(Float)
    Temp_Min_Cell = Column(Float)
    region = Column(String(50))
    timestamp = Column(DateTime)

class BatteryType(Base):
    __tablename__ = 'app_monitoring_batterytype'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(50), unique=True)
    oids = Column(JSON)

class Region(Base):
    __tablename__ = 'app_monitoring_region'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

class Device(Base):
    __tablename__ = 'app_monitoring_device'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    ip_address = Column(String(100))
    community_name = Column(String(100))
    region = Column(String(100))
    dga = Column(Boolean)
    supports_multiple_batteries = Column(Boolean)
    snmp_version = Column(Integer)

class DeviceBatteries(Base):
    __tablename__ = 'app_monitoring_devicebatteries'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    battery_type_id = Column(Integer, ForeignKey('battery_type.id'))
    quantity = Column(Integer)

class AggregatedBatteryData(Base):
    __tablename__ = 'app_monitoring_aggregatedbatterydata'

    id = Column(Integer, primary_key=True, index=True)
    controller_name = Column(String(255))
    Batt_Volt = Column(Float)
    Batt_Curr = Column(Float)
    SOC = Column(Float)
    SOH = Column(Float)
    Cycle = Column(Float)
    Mos_Temp = Column(Float)
    Env_Temp = Column(Float)
    Full_Capacity = Column(Float)
    Remaining_Capacity = Column(Float)
    Temp_Max_Cell = Column(Float)
    Temp_Min_Cell = Column(Float)
    timestamp = Column(DateTime)
    region = Column(String(255))
    is_grouped = Column(Boolean)