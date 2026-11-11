from datetime import datetime,timedelta,timezone
from urbanmesh.domain.models import Ride,SensorReading
from urbanmesh.domain.policies.pricing import bus_fare,FlatFarePolicy,MinuteFarePolicy
from urbanmesh.domain.policies.quality import ThresholdQualityRule,AlwaysClearQualityRule
from urbanmesh.domain.policies.validation import validate_password


def ride(minutes=5):
    t=datetime(2026,11,11,tzinfo=timezone.utc)
    return Ride("ride-p","user-p","bike-p",t,t+timedelta(minutes=minutes))

def test_bus_fare_basic(): assert bus_fare(280,False,False)==280

def test_bus_fare_peak(): assert bus_fare(280,True,False)==355

def test_bus_fare_concession(): assert bus_fare(280,False,True)==190

def test_flat_fare(): assert FlatFarePolicy().quote(ride()).amount_cents==250

def test_minute_fare_exact_minutes(): assert MinuteFarePolicy().quote(ride(5)).amount_cents==200

def test_threshold_clear():
    reading=SensorReading("S",15,"ug/m3",datetime.now(timezone.utc))
    assert ThresholdQualityRule().assess(reading)=="accepted"

def test_always_clear():
    reading=SensorReading("S",5,"ug/m3",datetime.now(timezone.utc))
    assert AlwaysClearQualityRule().assess(reading)=="accepted"

def test_password_short(): assert validate_password("abc") is False
