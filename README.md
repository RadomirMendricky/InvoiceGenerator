# 📄 Invoice Generator

Python aplikace pro generování českých faktur s realistickými náhodnými údaji.

## 🚀 Rychlý start

### 1. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 2. Spuštění
# 📄 Invoice Generator

Python aplikace pro generování českých faktur s realistickými náhodnými údaji.

## 🚀 Rychlý start

### 1. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 2. Spuštění
```bash
cd src
python main.py generate --count 1
```

## 📋 Funkce

- **Flexibilní generování:**
  - Standardní PDF faktura
  - Možnost přidat **QR kód** pro platbu (`--qr`)
  - Možnost připojit **ISDOC XML** (`--isdoc`)
  - Lze kombinovat obojí najednou!

- **3 šablony:**
  - `classic` - Modrý tradiční design
  - `modern` - Zelený moderní design
  - `minimal` - Černobílý minimalistický design

- **Realistická data:**
  - České firmy s IČO, DIČ, IBAN
  - Náhodné položky v češtině
  - Rozumné ceny (100-2000 Kč)
  - Správné výpočty DPH

## 💡 Příklady použití

```bash
# 1 standardní faktura
python main.py generate --count 1

# 10 faktur s QR kódem
python main.py generate --count 10 --qr

# 5 faktur s ISDOC a QR kódem (vše v jednom PDF)
python main.py generate --count 5 --isdoc --qr

# Moderní šablona s QR kódem
python main.py generate --template modern --qr
```

## 🛠️ Pokročilé funkce: Vlastní data

### Konfigurace pomocí JSON
Můžete nahrát vlastní data faktury pomocí souboru JSON. Umožňuje plně přizpůsobit dodavatele, odběratele, položky a další údaje.

1. Vytvořte soubor `my_invoice.json`:
```json
{
  "invoice_number": "2025001",
  "supplier": {
    "name": "Moje Firma s.r.o.",
    "street": "Hlavní 123",
    "city": "Praha",
    "zip_code": "110 00",
    "ico": "12345678",
    "dic": "CZ12345678",
    "country": "Česká republika",
    "iban": "CZ1234000000000012345678",
    "bank_name": "Moje Banka"
  },
  "customer": {
    "name": "Zákazník a.s.",
    "street": "Vedlejší 456",
    "city": "Brno",
    "zip_code": "602 00",
    "ico": "87654321",
    "dic": "CZ87654321",
    "country": "Česká republika"
  },
  "items": [
    {
      "description": "Konzultace",
      "quantity": 10,
      "unit": "hod",
      "unit_price": 1000,
      "vat_rate": 21
    }
  ],
  "note": "Děkujeme za spolupráci."
}
```

2. Spusťte generátor s parametrem `--config`:
```bash
python main.py generate --config my_invoice.json
```

### Cestní doložka (Factoring 4Trans)
Pro automatické přidání cestní doložky 4Trans do faktury použijte přepínač `--assignment-clause`.
Doložka bude umístěna na spodní části faktury.

```bash
python main.py generate --config my_invoice.json --assignment-clause
```
