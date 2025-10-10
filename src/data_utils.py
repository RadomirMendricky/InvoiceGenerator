"""Generátor realistických náhodných dat pro české faktury."""

import random
from datetime import date, timedelta
from faker import Faker

from models.company import Company
from models.item import Item
from models.invoice import Invoice


# Inicializace Faker s českou lokalizací
fake = Faker('cs_CZ')
Faker.seed()


# České názvy firem - přípony a typy
COMPANY_TYPES = ['s.r.o.', 'a.s.', 'v.o.s.']
COMPANY_PREFIXES = [
    'Český', 'Moravský', 'Slezský', 'Jiho', 'Severo', 'Západ', 'Východ',
    'Praha', 'Brno', 'Ostrava', 'Plzeň'
]
COMPANY_NAMES = [
    'Obchod', 'Trade', 'Market', 'Group', 'Systems', 'Tech', 'Digital',
    'Solutions', 'Holding', 'Company', 'Partners', 'Invest', 'Development',
    'Service', 'Center', 'House', 'Factory', 'Store', 'Shop', 'Works'
]

# České položky zboží a služeb
PRODUCT_ITEMS = [
    'Notebook Dell Latitude', 'Monitor Samsung 27"', 'Tiskárna HP LaserJet',
    'Klávesnice Logitech', 'Myš bezdrátová', 'Webkamera Full HD',
    'Headset s mikrofonem', 'USB flash disk 64GB', 'Extern. disk 2TB',
    'Kancelářská židle', 'Stůl kancelářský', 'Regál na dokumenty',
    'Skříň na spisy', 'Lampa stolní LED', 'Papír A4 5000 listů',
    'Tonery do tiskárny', 'Pero kuličkové', 'Blok linkovaný A4',
    'Obálky C5', 'Složky zakládací', 'Diář 2025', 'Pořadač pákový',
    'Sešívačka kovová', 'Razítko firemní', 'Nůžky kancelářské'
]

SERVICE_ITEMS = [
    'Vývoj webové aplikace', 'Správa IT infrastruktury', 'Grafické práce',
    'Konzultační služby', 'Účetní služby', 'Daňové poradenství',
    'Marketingové služby', 'SEO optimalizace', 'Správa sociálních sítí',
    'Tvorba textů', 'Překlad dokumentace', 'Školení zaměstnanců',
    'Technická podpora', 'Údržba softwaru', 'Hosting služby',
    'Cloud storage', 'Zálohovací služby', 'Bezpečnostní audit',
    'Právní poradenství', 'Architektonické služby', 'Projektová dokumentace',
    'Stavební dozor', 'Servis výpočetní techniky', 'Instalace sítě',
    'Konfigurace serveru'
]

UNITS = ['ks', 'hod', 'den', 'měsíc', 'balení', 'm²', 'služba']


def generate_ico() -> str:
    """
    Generuje náhodné IČO (8 číslic).
    
    Returns:
        Validní IČO jako string
    """
    return str(random.randint(10000000, 99999999))


def generate_dic(ico: str) -> str:
    """
    Generuje DIČ na základě IČO.
    
    Args:
        ico: IČO firmy
        
    Returns:
        DIČ ve formátu CZ + IČO
    """
    return f"CZ{ico}"


def _letters_to_digits(s: str) -> str:
    """Převede písmena na číslice (A -> 10, B -> 11, ..., Z -> 35)."""
    return ''.join(str(ord(ch) - 55) if ch.isalpha() else ch for ch in s)

def compute_iban_check_digits(country_code: str, bban: str) -> str:
    """Vrátí dvouciferné kontrolní číslice pro IBAN (řetězec)."""
    # Sestavíme řetězec pro výpočet: BBAN + country_code + "00"
    rearranged = bban + country_code + "00"
    # Převedeme písmena na čísla (A->10 ...)
    numeric = _letters_to_digits(rearranged)
    # Spočítáme zbytek po dělení 97
    remainder = int(numeric) % 97
    check_digits = 98 - remainder
    return f"{check_digits:02d}"

def generate_iban() -> str:
    """
    Vygeneruje náhodný syntakticky platný CZ IBAN (24 znaků).
    
    Returns:
        Validní český IBAN
    """
    country = "CZ"
    # BBAN v ČR - 20 číslic (pro účely syntaktické validity můžeme použít libovolných 20 číslic)
    bban = ''.join(str(random.randint(0, 9)) for _ in range(20))
    check = compute_iban_check_digits(country, bban)
    iban = f"{country}{check}{bban}"
    return iban


def generate_czech_company() -> Company:
    """
    Generuje náhodnou českou firmu s realistickými údaji.
    
    Returns:
        Instance třídy Company s náhodnými daty
    """
    ico = generate_ico()
    
    # Generování názvu firmy
    if random.random() > 0.3:
        # Složený název
        company_name = f"{random.choice(COMPANY_PREFIXES)} {random.choice(COMPANY_NAMES)}"
    else:
        # Jednoduchý název
        company_name = random.choice(COMPANY_NAMES)
    
    company_name += f" {random.choice(COMPANY_TYPES)}"
    
    # Banky v ČR
    banks = [
        'Česká spořitelna, a.s.',
        'Komerční banka, a.s.',
        'ČSOB, a.s.',
        'Raiffeisenbank a.s.',
        'UniCredit Bank Czech Republic',
        'Fio banka, a.s.',
        'Air Bank a.s.'
    ]
    
    return Company(
        name=company_name,
        ico=ico,
        dic=generate_dic(ico),
        street=fake.street_address(),
        city=fake.city(),
        zip_code=fake.postcode(),
        country="Česká republika",
        iban=generate_iban(),
        bank_name=random.choice(banks),
        email=fake.company_email(),
        phone=fake.phone_number()
    )


def generate_invoice_number() -> str:
    """
    Generuje číslo faktury ve formátu YYYYMMDD001.
    
    Returns:
        Číslo faktury
    """
    today = date.today()
    sequence = random.randint(1, 999)
    return f"{today.strftime('%Y%m%d')}{sequence:03d}"


def generate_items(count: int = None) -> list[Item]:
    """
    Generuje náhodné položky faktury.
    
    Args:
        count: Počet položek (pokud None, vybere se náhodně 1-8)
        
    Returns:
        Seznam položek
    """
    if count is None:
        count = random.randint(1, 8)
    
    items = []
    
    # Mix produktů a služeb
    all_items = PRODUCT_ITEMS + SERVICE_ITEMS
    selected_items = random.sample(all_items, min(count, len(all_items)))
    
    for item_name in selected_items:
        # Určení jednotky podle typu položky
        if item_name in SERVICE_ITEMS:
            unit = random.choice(['hod', 'den', 'měsíc', 'služba'])
        else:
            unit = random.choice(['ks', 'balení', 'm²'])
        
        # Množství závisí na jednotce
        if unit in ['měsíc', 'služba']:
            quantity = 1
        elif unit in ['den', 'hod']:
            quantity = random.randint(1, 10)  # Sníženo z 40
        else:
            quantity = random.randint(1, 5)  # Sníženo z 10
        
        # Cena v celých číslech 50-500 Kč
        # Pro služby obvykle vyšší ceny
        if item_name in SERVICE_ITEMS:
            unit_price = random.randint(10, 50) * 10  # 100-500
        else:
            unit_price = random.randint(5, 30) * 10   # 50-300
        
        # Sazba DPH
        vat_rate = random.choices([21, 15, 10], weights=[80, 15, 5])[0]
        
        items.append(Item(
            description=item_name,
            quantity=quantity,
            unit=unit,
            unit_price=unit_price,
            vat_rate=vat_rate
        ))
    
    return items


def generate_invoice(supplier: Company = None, customer: Company = None) -> Invoice:
    """
    Generuje kompletní fakturu s náhodnými údaji.
    
    Args:
        supplier: Dodavatel (pokud None, vygeneruje se náhodný)
        customer: Odběratel (pokud None, vygeneruje se náhodný)
        
    Returns:
        Instance třídy Invoice
    """
    if supplier is None:
        supplier = generate_czech_company()
    
    if customer is None:
        customer = generate_czech_company()
    
    issue_date = date.today() - timedelta(days=random.randint(0, 30))
    due_date = issue_date + timedelta(days=random.choice([14, 21, 30]))
    
    invoice_number = generate_invoice_number()
    variable_symbol = invoice_number.replace("/", "")
    
    items = generate_items()
    
    notes = [
        "Děkujeme za Vaši důvěru.",
        "Faktura vystavena elektronicky a je platná bez podpisu.",
        "V případě dotazů nás neváhejte kontaktovat.",
        "Platba bankovním převodem na uvedený účet.",
        "",  # Žádná poznámka
    ]
    
    return Invoice(
        invoice_number=invoice_number,
        supplier=supplier,
        customer=customer,
        items=items,
        issue_date=issue_date,
        due_date=due_date,
        variable_symbol=variable_symbol,
        payment_method="bankovní převod",
        note=random.choice(notes)
    )


def generate_invoices(count: int) -> list[Invoice]:
    """
    Generuje více faktur najednou.
    
    Args:
        count: Počet faktur k vygenerování
        
    Returns:
        Seznam faktur
    """
    return [generate_invoice() for _ in range(count)]

