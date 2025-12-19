# 📄 Invoice Generator

Python aplikace pro generování českých faktur s realistickými nebo vlastními daty. Ideální pro testování a vývoj.

## 🚀 Rychlý start

### 1. Instalace
```bash
pip install -r requirements.txt
```

### 2. Generování faktury
```bash
cd src
python main.py generate
```
Tento příkaz vygeneruje jednu náhodnou fakturu do složky `output`.

## 🎮 Příklady použití

```bash
# Vygeneruje 5 faktur s QR kódem a ISDOC přílohou
python main.py generate --count 5 --qr --isdoc

# Použití moderní šablony
python main.py generate --template modern

# Generování na základě vlastních dat (JSON)
python main.py generate --config mojefaktura.json
```

## ⚙️ Parametry příkazové řádky

| Přepínač | Popis |
| :--- | :--- |
| `--count N` | Počet generovaných faktur (výchozí: 1). |
| `--qr` | Přidá QR kód pro platbu (SPD formát). |
| `--isdoc` | Vloží ISDOC XML jako přílohu do PDF. |
| `--template X` | Šablona faktury: `classic` (výchozí), `modern`, `minimal`. |
| `--config FILE` | Cesta k JSON souboru s definicí dat. |

## 🛠️ Konfigurace (JSON)

Pro plnou kontrolu nad obsahem faktury vytvořte JSON soubor.

### Základní struktura
```json
{
  "invoice_number": "2025001",
  "variable_symbol": "1234567890",
  "issue_date": "today",
  "payment_terms_days": 14,
  "currency": "CZK",
  "strict_validation": true,
  "supplier": { ... },
  "customer": { ... },
  "items": [ ... ]
}
```

### Možnosti konfigurace

| Klíč | Typ | Popis |
| :--- | :--- | :--- |
| `strict_validation` | `bool` | `true` (default) zapne kontrolu formátu IČO/DIČ/IBAN. `false` povolí neplatné hodnoty pro testování. |
| `currency` | `string` | Měna faktury, např. `"CZK"` nebo `"EUR"`. Ovlivní symboly měny i QR kód. |
| `issue_date` | `string` | Datum vystavení. Může být `YYYY-MM-DD`, `"today"` nebo `"today-N"` (např. `"today-5"`). |
| `payment_terms_days` | `int` | Počet dní splatnosti. Automaticky dopočítá `due_date`. |
| `variable_symbol` | `string` | Pokud není zadán, použije se číslo faktury (bez lomítek). |
| `assignment_clause_text`| `string`| Text pro factoringovou doložku (pokud je `use_assignment_clause: true`). |

### Příklad kompletní konfigurace
```json
{
  "invoice_number": "FA-2025-001",
  "issue_date": "today",
  "currency": "EUR",
  "strict_validation": false,
  "supplier": {
    "name": "Moje Firma s.r.o.",
    "ico": "12345678",
    "dic": "CZ12345678",
    "street": "Hlavní 1",
    "city": "Praha",
    "zip_code": "11000",
    "iban": "CZ0000000000000012345678"
  },
  "customer": {
    "name": "Testovací s.r.o."
  },
  "items": [
    {
      "description": "Konzultace",
      "quantity": 10,
      "unit": "hod",
      "unit_price": 50,
      "vat_rate": 21
    }
  ]
}
```
Pokud některé údaje firem (dodavatel/odběratel) vynecháte, budou **doplněny náhodnými realistickými daty**.

