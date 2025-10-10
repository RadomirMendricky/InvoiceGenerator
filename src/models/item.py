"""Model pro položku faktury."""

from dataclasses import dataclass


@dataclass
class Item:
    """
    Reprezentuje položku na faktuře (zboží nebo služba).
    
    Attributes:
        description: Popis položky (název zboží/služby)
        quantity: Množství
        unit: Jednotka (ks, hod, m², atd.)
        unit_price: Jednotková cena bez DPH v Kč
        vat_rate: Sazba DPH v procentech (např. 21)
    """
    description: str
    quantity: int
    unit: str
    unit_price: int
    vat_rate: int = 21  # Výchozí sazba DPH 21%

    @property
    def total_price_without_vat(self) -> int:
        """Celková cena bez DPH."""
        return self.quantity * self.unit_price

    @property
    def vat_amount(self) -> int:
        """Částka DPH."""
        return int(self.total_price_without_vat * self.vat_rate / 100)

    @property
    def total_price_with_vat(self) -> int:
        """Celková cena včetně DPH."""
        return self.total_price_without_vat + self.vat_amount

    def __post_init__(self):
        """Validace dat po inicializaci."""
        if self.quantity <= 0:
            raise ValueError("Množství musí být kladné číslo")
        if self.unit_price <= 0:
            raise ValueError("Jednotková cena musí být kladné číslo")
        if self.vat_rate not in [0, 10, 15, 21]:
            raise ValueError(f"Neplatná sazba DPH: {self.vat_rate}%")

