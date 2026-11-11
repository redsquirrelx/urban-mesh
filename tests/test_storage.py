from datetime import date
from urbanmesh.domain.models import Route,Boarding,StockItem
from urbanmesh.infrastructure.storage.memory import (MemoryRouteSource,
 MemoryInventoryCatalog,MemoryBoardingStore)


def test_routes_connected():
    catalog=MemoryRouteSource([Route("R",("A","B","C"),(4,7),100)])
    assert catalog.connecting("A","C")[0][1]==11

def test_routes_not_connected_reverse():
    catalog=MemoryRouteSource([Route("R",("A","B"),(7,),100)])
    assert catalog.connecting("B","A")==[]

def test_stock_save():
    catalog=MemoryInventoryCatalog([])
    catalog.save(StockItem("X","Part",100,5))
    assert catalog.find("X").stock==5

def test_stock_remove():
    catalog=MemoryInventoryCatalog([StockItem("X","Part",100,5)])
    assert catalog.remove("X") and catalog.find("X") is None

def test_boarding_read_snapshot():
    store=MemoryBoardingStore([Boarding("u","R",date(2026,11,11))])
    data=store.read_all();data.clear()
    assert len(store.read_all())==1
