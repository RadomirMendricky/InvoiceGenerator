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

ASSIGNMENT_CLAUSE_4TRANS = """Dodavatel tímto neodvolatelně oznamuje odběrateli, že pohledávku, vyúčtovanou tímto 
daňovým dokladem včetně jejího příslušenství a souvisejících práv, postoupil obchodní 
společnosti 4Trans IČO: 06760881, se sídlem: Karmelitská 379/18, Praha 1, 118 00, Česká republika. Z 
toho důvodu je nutné poukázat veškeré platby na pohledávku vyúčtovanou tímto daňovým 
dokladem výhradně na bankovní účet společnosti 4Trans uvedený na tomto daňovém dokladu. 
Závazek odběratele zaniká pouze splněním dluhu obchodní společnosti Malcom Finance s.r.o., 
nebude-li společností Malcom Finance s.r.o. odběrateli oznámeno jinak."""


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


def load_from_json(path: str) -> Invoice:
    """
    Načte fakturu z JSON souboru.
    
    Args:
        path: Cesta k JSON souboru
        
    Returns:
        Instance Invoice
    """
    import json
    from datetime import datetime

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Helper pro parsování data
    def parse_date(d_str):
        if not d_str: return date.today()
        try:
            return datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            return date.today()

    # Validace strict_mode (pokud není definováno, default je True)
    strict_validation = data.get('strict_validation', True)

    # Načtení firem
    supplier_data = data.get('supplier', {})
    customer_data = data.get('customer', {})
    
    # Fallback pro chybějící data firmy - generuj náhodně, ale použij co je k dispozici
    # Zde předpokládáme, že pokud je JSON zadán, uživatel chce specifikovat konkrétní data
    # Ale pro zjednodušení, pokud chybí celá sekce, vygenerujeme náhodnou
    
    if not supplier_data:
        supplier = generate_czech_company()
        supplier.strict_validation = strict_validation
    else:
        supplier = Company(**supplier_data, strict_validation=strict_validation)
        
    if not customer_data:
        customer = generate_czech_company()
        customer.strict_validation = strict_validation
    else:
        customer = Company(**customer_data, strict_validation=strict_validation)
        
    # Načtení položek
    items_data = data.get('items', [])
    items = []
    if items_data:
        for item_d in items_data:
            items.append(Item(**item_d))
    else:
        items = generate_items()

    # Zpracování data vystavení
    issue_date_raw = data.get('issue_date')
    if isinstance(issue_date_raw, str):
        if issue_date_raw.lower() == "today":
            issue_date = date.today()
        elif issue_date_raw.lower().startswith("today-"):
            try:
                days = int(issue_date_raw.split("-")[1])
                issue_date = date.today() - timedelta(days=days)
            except ValueError:
                issue_date = parse_date(issue_date_raw)
        else:
             issue_date = parse_date(issue_date_raw)
    else:
        issue_date = parse_date(issue_date_raw)

    # Zpracování data splatnosti
    due_date_raw = data.get('due_date')
    if due_date_raw:
        due_date = parse_date(due_date_raw)
    else:
        # Pokud není due_date, zkusíme payment_terms_days
        payment_terms = data.get('payment_terms_days')
        if payment_terms is not None:
             due_date = issue_date + timedelta(days=int(payment_terms))
        else:
             # Default 14 dní
             due_date = issue_date + timedelta(days=14)

    # Ostatní pole

    # Cestní doložka
    assignment_clause = data.get('assignment_clause', "")
    if data.get('use_assignment_clause', False):
        custom_text = data.get('assignment_clause_text')
        if custom_text:
             assignment_clause = custom_text
        else:
             assignment_clause = ASSIGNMENT_CLAUSE_4TRANS

    return Invoice(
        invoice_number=data.get('invoice_number', generate_invoice_number()),
        supplier=supplier,
        customer=customer,
        items=items,
        issue_date=issue_date,
        due_date=due_date,
        variable_symbol=data.get('variable_symbol', ""),
        payment_method=data.get('payment_method', "bankovní převod"),
        note=data.get('note', ""),
        assignment_clause=assignment_clause,
        currency=data.get('currency', "CZK")
    )

