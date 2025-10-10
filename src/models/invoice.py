"""Model pro fakturu."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List

from .company import Company
from .item import Item


@dataclass
class Invoice:
    """
    Reprezentuje fakturu.
    
    Attributes:
        invoice_number: Číslo faktury (formát: YYYYMMDD001)
        supplier: Dodavatel (firma vystavující fakturu)
        customer: Odběratel (firma přijímající fakturu)
        items: Seznam položek na faktuře
        issue_date: Datum vystavení
        due_date: Datum splatnosti
        variable_symbol: Variabilní symbol pro platbu
        payment_method: Způsob platby (bankovní převod, hotově, atd.)
        note: Poznámka k faktuře
    """
    invoice_number: str
    supplier: Company
    customer: Company
    items: List[Item] = field(default_factory=list)
    issue_date: date = field(default_factory=date.today)
    due_date: date = field(default_factory=lambda: date.today() + timedelta(days=14))
    variable_symbol: str = ""
    payment_method: str = "bankovní převod"
    note: str = ""

    def __post_init__(self):
        """Inicializace a validace dat."""
        if not self.variable_symbol:
            # Pokud není VS zadán, použij číslo faktury bez lomítek
            self.variable_symbol = self.invoice_number.replace("/", "")
        
        if not self.items:
            raise ValueError("Faktura musí obsahovat alespoň jednu položku")
        
        if self.due_date < self.issue_date:
            raise ValueError("Datum splatnosti nemůže být před datem vystavení")

    @property
    def total_without_vat(self) -> int:
        """Celková cena bez DPH."""
        return sum(item.total_price_without_vat for item in self.items)

    @property
    def total_vat(self) -> int:
        """Celková částka DPH."""
        return sum(item.vat_amount for item in self.items)

    @property
    def total_with_vat(self) -> int:
        """Celková cena včetně DPH."""
        return self.total_without_vat + self.total_vat

    def get_vat_summary(self) -> dict:
        """
        Vrátí souhrn DPH podle sazeb.
        
        Returns:
            Dict s klíči jako sazbami DPH a hodnotami jako tuple (základ, DPH, celkem)
        """
        vat_summary = {}
        
        for item in self.items:
            rate = item.vat_rate
            if rate not in vat_summary:
                vat_summary[rate] = {
                    'base': 0,
                    'vat': 0,
                    'total': 0
                }
            
            vat_summary[rate]['base'] += item.total_price_without_vat
            vat_summary[rate]['vat'] += item.vat_amount
            vat_summary[rate]['total'] += item.total_price_with_vat
        
        return vat_summary

    def format_price(self, amount: int) -> str:
        """
        Formátuje částku v Kč.
        
        Args:
            amount: Částka v celých korunách
            
        Returns:
            Formátovaný řetězec s měnou (např. "1 234 Kč")
        """
        return f"{amount:,} Kč".replace(",", " ")

