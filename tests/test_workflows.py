from datetime import date,datetime,timezone
from urbanmesh.domain.models import Disruption


def test_commute_wiring(services):
    receipt=services.commute.execute("CENTRO","PUERTO","u-001",0,date(2026,11,11))
    assert receipt.journey.route_id=="R-01"
    assert receipt.ticket.amount_cents==receipt.fare.amount_cents

def test_rental_wiring(services):
    reference=services.rental.run("ride-workflow","u-001","B-01",
                                  datetime(2026,11,11,9,0,tzinfo=timezone.utc))
    assert reference.startswith("PROC-")

def test_dispatch_subscribers(services):
    event=Disruption("R-01","BUS-4","Heavy traffic","low")
    result=services.alerts.dispatch(event,{"u-001":{"R-01"},"u-002":{"R-04"}})
    assert result==1 and len(services.messages_store.sent)==1

def test_maintenance_queue(services):
    task=services.maintenance.report("B-01","Brake inspection")
    assert task in services.repairs_store.tickets

def test_work_order_policy(services):
    event=Disruption("R-01","BUS-1","Engine overheat","critical")
    assert services.work_orders.from_disruption(event).asset_id=="BUS-1"

def test_crew_compliance(services):
    assert services.crew.check("DRIVER-1",3)=="covered"
    assert services.crew.check("DRIVER-2",9)=="excess_hours"

def test_retention_explicit(services):
    assert services.retention.prune(date(2025,1,1))==0

def test_campaign_separate(services):
    assert services.campaigns.schedule("u-001",5)=="RETURN10"
