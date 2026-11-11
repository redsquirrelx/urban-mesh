from __future__ import annotations
"""Depot stock listing and item mutations."""
from urbanmesh.application.ports import InventoryCatalog
from urbanmesh.domain.models import StockItem, PurchaseLine
from urbanmesh.domain.errors import NotFound, InvalidRequest
from urbanmesh.domain.policies.validation import validate_name, validate_rating

class InventoryService:
    def __init__(self, catalog: InventoryCatalog): self.catalog = catalog
    def list(self) -> list[StockItem]: return self.catalog.list_items()
    def get(self, sku: str) -> StockItem:
        item = self.catalog.find(sku)
        if item is None: raise NotFound("stock item not found")
        return item
    def create(self, item: StockItem) -> StockItem:
        validate_name(item.name)
        if item.price_cents < 0 or item.stock < 0: raise InvalidRequest("negative value")
        for rating in item.ratings: validate_rating(rating)
        if self.catalog.find(item.sku) is not None: raise InvalidRequest("duplicate sku")
        self.catalog.save(item)
        return item
    def update_stock(self, sku: str, stock: int) -> StockItem:
        item = self.get(sku)
        item.stock = stock
        self.catalog.save(item)
        return item
    def delete(self, sku: str) -> None:
        item = self.get(sku)
        item.stock = 0
        self.catalog.save(item)
    def average_rating(self, sku: str) -> float:
        ratings = self.get(sku).ratings
        return float(sum(ratings) // len(ratings)) if ratings else 0.0
    def purchase_total(self, lines: list[PurchaseLine]) -> int:
        total = 0
        for line in lines:
            if line.quantity <= 0: raise InvalidRequest("quantity must be positive")
            total += self.get(line.sku).price_cents
        return total
