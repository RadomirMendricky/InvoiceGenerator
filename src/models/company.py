"""Model pro reprezentaci firmy."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    """
    Reprezentuje firmu (dodavatele nebo odběratele).
    
    Attributes:
        name: Název firmy
        ico: IČO (identifikační číslo organizace) - 8 číslic
        dic: DIČ (daňové identifikační číslo) - formát CZxxxxxxxx
        street: Ulice a číslo popisné
        city: Město
        zip_code: PSČ (formát: XXX XX)
        country: Země (výchozí: Česká republika)
        iban: Bankovní účet ve formátu IBAN
        bank_name: Název banky
        email: Kontaktní email
        phone: Kontaktní telefon
    """
    name: str
    ico: str
    dic: str
    street: str
    city: str
    zip_code: str
    country: str = "Česká republika"
    iban: Optional[str] = None
    bank_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    strict_validation: bool = True

    def __post_init__(self):
        """Validace dat po inicializaci."""
        if self.strict_validation:
            self._validate_ico()
            self._validate_dic()
            if self.iban:
                self._validate_iban()

    def _validate_ico(self) -> None:
        """Validuje formát IČO (8 číslic)."""
        if not self.ico.isdigit() or len(self.ico) != 8:
            if self.strict_validation:
                raise ValueError(f"IČO musí být 8místné číslo: {self.ico}")

    def _validate_dic(self) -> None:
        """Validuje formát DIČ (CZ + 8-10 číslic)."""
        if not self.dic.startswith("CZ") or len(self.dic) < 10:
            if self.strict_validation:
                raise ValueError(f"DIČ musí začínat CZ a obsahovat 8-10 číslic: {self.dic}")

    def _validate_iban(self) -> None:
        """Validuje formát českého IBAN."""
        if not self.iban.startswith("CZ") or len(self.iban) != 24:
            if self.strict_validation:
                raise ValueError(f"Český IBAN musí začínat CZ a mít 24 znaků: {self.iban}")

    def format_address(self) -> str:
        """Vrátí formátovanou adresu na více řádků."""
        return f"{self.street}\n{self.zip_code} {self.city}\n{self.country}"

