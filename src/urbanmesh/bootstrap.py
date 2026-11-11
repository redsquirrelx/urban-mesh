"""Composition root for the local application deployment."""
from dataclasses import dataclass
from datetime import datetime, date, timedelta, timezone
from urbanmesh.domain.models import (Route, Bicycle, Boarding, StockItem, SensorReading)
from urbanmesh.domain.policies.pricing import MinuteFarePolicy
from urbanmesh.domain.policies.quality import ThresholdQualityRule
from urbanmesh.infrastructure.storage.memory import (MemoryRouteSource, MemoryBikeCatalog,
    MemoryRideRepository,MemoryTicketStore,MemoryAuditSink,MemoryCampaignQueue,
    MemoryMessages,MemoryRepairQueue,MemoryBoardingStore,MemoryShiftFlags,
    MemoryQualityStore,MemoryCustodySink,MemoryTelemetryStore,
    MemoryInventoryCatalog,MemorySupplyOrders)
from urbanmesh.infrastructure.gateways.locks import MemoryLockGateway
from urbanmesh.infrastructure.gateways.payments import ProcessorPaymentAdapter
from urbanmesh.infrastructure.gateways.sensors import FleetSensorReader
from urbanmesh.application.journeys.planner import JourneyPlanner
from urbanmesh.application.fares.quote import FareQuoteService
from urbanmesh.application.ticketing.issuer import TicketIssuer
from urbanmesh.application.alerts.dispatcher import AlertDispatcher
from urbanmesh.application.schedules.boards import DepartureBoardService
from urbanmesh.application.reporting.ridership import RidershipReportService
from urbanmesh.application.rides.service import RideService
from urbanmesh.application.payments.settlement import SettlementService
from urbanmesh.application.maintenance.triage import MaintenanceTriage
from urbanmesh.application.telemetry.processing import TelemetryProcessor
from urbanmesh.application.telemetry.quality import QualityReviewService
from urbanmesh.application.telemetry.custody import CustodyExportService
from urbanmesh.application.telemetry.notifications import TelemetryNoticeService
from urbanmesh.application.reporting.telemetry import TelemetryReportService
from urbanmesh.application.operations.retention import RetentionService
from urbanmesh.application.operations.audits import RegulatoryAuditService
from urbanmesh.application.operations.crew import CrewCompliance
from urbanmesh.application.operations.work_orders import WorkOrderService
from urbanmesh.application.engagement.campaigns import CampaignService
from urbanmesh.application.inventory.catalog import InventoryService
from urbanmesh.application.inventory.allocator import StockAllocator
from urbanmesh.application.procurement.checkout import SupplyCheckout
from urbanmesh.application.users.accounts import RiderAccounts
from urbanmesh.application.workflows import BookCommute, CompleteRental
from urbanmesh.application.procurement.quote import SupplyQuoteService
from urbanmesh.infrastructure.gateways.quote_support import (LocalPromotionSource,
    LocalDeliveryRateProvider,SequentialQuoteIds)
from urbanmesh.infrastructure.storage.quotes import MemorySupplyQuotes

@dataclass
class Services:
    journeys: JourneyPlanner
    fares: FareQuoteService
    tickets: TicketIssuer
    alerts: AlertDispatcher
    boards: DepartureBoardService
    ridership: RidershipReportService
    rides: RideService
    payments: SettlementService
    maintenance: MaintenanceTriage
    telemetry: TelemetryProcessor
    quality: QualityReviewService
    custody: CustodyExportService
    notices: TelemetryNoticeService
    telemetry_report: TelemetryReportService
    retention: RetentionService
    audits: RegulatoryAuditService
    crew: CrewCompliance
    work_orders: WorkOrderService
    campaigns: CampaignService
    inventory: InventoryService
    allocator: StockAllocator
    checkout: SupplyCheckout
    accounts: RiderAccounts
    commute: BookCommute
    rental: CompleteRental
    routes_store: MemoryRouteSource
    bikes_store: MemoryBikeCatalog
    rides_store: MemoryRideRepository
    ticket_store: MemoryTicketStore
    audit_store: MemoryAuditSink
    campaign_store: MemoryCampaignQueue
    messages_store: MemoryMessages
    repairs_store: MemoryRepairQueue
    boardings_store: MemoryBoardingStore
    shifts_store: MemoryShiftFlags
    quality_store: MemoryQualityStore
    custody_store: MemoryCustodySink
    telemetry_store: MemoryTelemetryStore
    inventory_store: MemoryInventoryCatalog
    orders_store: MemorySupplyOrders
    lock_gateway: MemoryLockGateway
    supply_quotes: SupplyQuoteService
    quote_store: MemorySupplyQuotes

def build_services(reference_day: date | None = None) -> Services:
    now = reference_day or date.today()
    routes_store = MemoryRouteSource([
        Route("R-01",("CENTRO","MUSEO","PUERTO"),(12,18),280),
        Route("R-02",("CENTRO","MERCADO","PUERTO"),(10,25),320),
        Route("R-03",("MUSEO","UNIVERSIDAD"),(14,),210),
        Route("R-04",("PUERTO","ESTACION","HOSPITAL"),(15,20),360),
    ])
    bikes_store = MemoryBikeCatalog([
        Bicycle("B-01","CENTRO"), Bicycle("B-02","CENTRO"),
        Bicycle("B-03","PUERTO"), Bicycle("B-04","MERCADO",False),
    ])
    rides_store=MemoryRideRepository(); tickets_store=MemoryTicketStore()
    audit_store=MemoryAuditSink(); campaigns_store=MemoryCampaignQueue()
    messages_store=MemoryMessages(); repairs_store=MemoryRepairQueue()
    boardings_store=MemoryBoardingStore([
        Boarding("u-001","R-01",now-timedelta(days=3)),
        Boarding("u-002","R-01",now-timedelta(days=12)),
        Boarding("u-003","R-02",now-timedelta(days=42)),
    ])
    shifts_store=MemoryShiftFlags(); quality_store=MemoryQualityStore()
    custody_store=MemoryCustodySink()
    telemetry_store=MemoryTelemetryStore([
        SensorReading("S-001",13.0,"ug/m3",datetime.now(timezone.utc)-timedelta(days=2)),
        SensorReading("S-002",70.0,"ug/m3",datetime.now(timezone.utc)-timedelta(days=190)),
    ])
    inventory_store=MemoryInventoryCatalog([
        StockItem("CHAIN-01","Bicycle chain",1299,8,[4.0,5.0]),
        StockItem("BRAKE-02","Brake pads",1900,5,[3.0,4.0]),
        StockItem("FILTER-01","Cabin filter",2400,9,[]),
    ])
    orders_store=MemorySupplyOrders(); lock_gateway=MemoryLockGateway()
    journeys=JourneyPlanner(routes_store)
    fares=FareQuoteService(routes_store,audit_store)
    tickets=TicketIssuer(tickets_store,campaigns_store)
    alerts=AlertDispatcher(messages_store,repairs_store)
    boards=DepartureBoardService(routes_store,shifts_store)
    ridership=RidershipReportService(boardings_store)
    rides=RideService(rides_store,bikes_store,lock_gateway)
    payments=SettlementService(rides_store,MinuteFarePolicy(),ProcessorPaymentAdapter())
    maintenance=MaintenanceTriage(repairs_store)
    telemetry=TelemetryProcessor(FleetSensorReader())
    quality=QualityReviewService(ThresholdQualityRule(),quality_store)
    custody=CustodyExportService(custody_store)
    notices=TelemetryNoticeService(messages_store)
    telemetry_report=TelemetryReportService(telemetry_store)
    retention=RetentionService(telemetry_store)
    audits=RegulatoryAuditService(audit_store)
    crew=CrewCompliance(shifts_store)
    work_orders=WorkOrderService(repairs_store)
    campaigns=CampaignService(campaigns_store)
    inventory=InventoryService(inventory_store)
    allocator=StockAllocator(inventory_store)
    checkout=SupplyCheckout(orders_store,ProcessorPaymentAdapter())
    accounts=RiderAccounts()
    commute=BookCommute(journeys,fares,tickets)
    rental=CompleteRental(rides,payments)
    quote_store=MemorySupplyQuotes()
    supply_quotes=SupplyQuoteService(inventory_store,LocalPromotionSource(),
        LocalDeliveryRateProvider(),quote_store,SequentialQuoteIds())
    return Services(journeys,fares,tickets,alerts,boards,ridership,rides,payments,
        maintenance,telemetry,quality,custody,notices,telemetry_report,retention,
        audits,crew,work_orders,campaigns,inventory,allocator,checkout,accounts,
        commute,rental,routes_store,bikes_store,rides_store,tickets_store,
        audit_store,campaigns_store,messages_store,repairs_store,boardings_store,
        shifts_store,quality_store,custody_store,telemetry_store,inventory_store,
        orders_store,lock_gateway,supply_quotes,quote_store)
