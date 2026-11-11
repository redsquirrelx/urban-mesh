from datetime import date


def test_health(client):
    assert client.get("/health").json() == {"status":"ok"}

def test_route_list(client):
    result=client.get("/routes")
    assert result.status_code==200 and len(result.json())==4

def test_route_detail(client):
    response=client.get("/routes/R-01")
    assert response.json()["stops"][0]=="CENTRO"

def test_route_not_found(client):
    assert client.get("/routes/not-a-route").status_code==404

def test_journey_search(client):
    result=client.post("/journeys/search",json={"origin":"CENTRO","destination":"PUERTO",
        "rider_id":"u-001","rides_last_month":0,"travel_day":"2026-11-11"})
    assert result.status_code==200
    assert {x["route_id"] for x in result.json()}=={"R-01","R-02"}

def test_fare_quote(client):
    response=client.post("/fares/quote",json={"route_id":"R-01","rider_id":"u-001"})
    assert response.status_code==200
    assert response.json()["amount_cents"]==280

def test_missing_fare_route(client):
    response=client.post("/fares/quote",json={"route_id":"N/A","rider_id":"u-001"})
    assert response.status_code==404

def test_create_ticket(client):
    result=client.post("/tickets",json={"route_id":"R-01","rider_id":"u-001"})
    assert result.status_code==201
    assert client.get("/tickets/"+result.json()["ticket_id"]).status_code==200

def test_station_bikes(client):
    result=client.get("/stations/CENTRO/bicycles")
    assert result.status_code==200 and len(result.json())==2

def test_ride_happy_path(client):
    result=client.post("/rides",json={"ride_id":"ride-test-1","rider_id":"u-001",
      "bike_id":"B-01","started_at":"2026-11-11T09:00:00Z"})
    assert result.status_code==201
    assert result.json()["ended_at"] is None
    closed=client.patch("/rides/ride-test-1/finish",json={"ended_at":"2026-11-11T09:08:00Z"})
    assert closed.status_code==200
    assert closed.json()["ended_at"] is not None

def test_rider_list(client):
    assert client.get("/riders").status_code==200

def test_rider_get(client):
    assert client.get("/riders/u-001").json()["rider_id"]=="u-001"

def test_rider_create(client):
    result=client.post("/riders",json={"rider_id":"u-005","email":"new@example.com"})
    assert result.status_code==201
    assert client.get("/riders/u-005").status_code==200

def test_rider_duplicate(client):
    response=client.post("/riders",json={"rider_id":"u-001","email":"a@example.com"})
    assert response.status_code==409

def test_list_inventory(client):
    result=client.get("/inventory")
    assert result.status_code==200 and len(result.json())==3

def test_get_stock(client):
    assert client.get("/inventory/CHAIN-01").json()["stock"]==8

def test_create_stock(client):
    result=client.post("/inventory",json={"sku":"BOLT-01","name":"Bolt",
        "price_cents":100,"stock":6,"ratings":[5.0]})
    assert result.status_code==201
    assert client.get("/inventory/BOLT-01").json()["stock"]==6

def test_create_stock_invalid_name(client):
    result=client.post("/inventory",json={"sku":"BAD-01","name":"  ",
        "price_cents":100,"stock":1,"ratings":[]})
    assert result.status_code==422

def test_stock_not_found(client):
    assert client.get("/inventory/MISSING").status_code==404

def test_purchase_empty(client):
    assert client.post("/purchases/total",json={"lines":[]}).json()["total_cents"]==0

def test_password_long(client):
    assert client.post("/passwords/validate",json={"password":"abcdefgh"}).json()=={"valid":True}

def test_password_non_string(client):
    assert client.post("/passwords/validate",json={"password":123}).json()=={"valid":False}

def test_maintenance_create_and_read(client):
    payload={"asset_id":"B-02","description":"Wheel check","priority":"normal"}
    response=client.post("/maintenance/work-orders",json=payload)
    assert response.status_code==201
    assert client.get("/maintenance/work-orders").json()[0]["asset_id"]=="B-02"

def test_telemetry_factory_sensor(client):
    response=client.get("/telemetry/sensors/S-001")
    assert response.status_code==200 and response.json()["value"]==15.0

def test_quality_review(client):
    result=client.post("/telemetry/sensors/S-001/assess")
    assert result.status_code==200 and result.json()["classification"]=="accepted"
    assert client.get("/telemetry/quality/S-001").status_code==200

def test_custody_record(client):
    result=client.post("/telemetry/custody",json={"sensor_id":"S-001",
      "action":"inspected","actor":"operator","recorded_on":"2026-11-11"})
    assert result.status_code==201
    assert "S-001" in client.get("/telemetry/custody/export").json()["rows"][0]

def test_departures(client):
    result=client.get("/stops/CENTRO/departures",params={"minute":100})
    assert result.status_code==200 and len(result.json())==2

def test_retention_nothing(client):
    result=client.post("/operations/retention/run",params={"as_of":"2025-01-01"})
    assert result.status_code==200 and result.json()["deleted"]==0

def test_discount_preview(client):
    assert client.get("/procurement/discount-preview",params={"code":"CIVIC5",
      "subtotal_cents":1000}).json()["discount_cents"]==500
