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

- **3 režimy:**
  - `pdf` - Standardní PDF faktura
  - `qr` - PDF s QR kódem pro platbu
  - `isdoc` - PDF s embedovaným ISDOC XML (přímo v PDF)

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
# 1 faktura
python main.py generate --count 1

# 10 faktur s QR kódem
python main.py generate --count 10 --mode qr

# 5 faktur s ISDOC
python main.py generate --count 5 --mode isdoc

# Moderní šablona
python main.py generate --template modern
```

## 📁 Struktura

```
src/
├── main.py              # Hlavní aplikace
├── invoice_generator.py # Generování faktur
├── data_utils.py        # Generování dat
├── qr_generator.py      # QR kódy
├── isdoc_generator.py   # ISDOC XML
├── models/              # Datové modely
├── pdf_templates/       # PDF šablony
├── fonts/               # Fonty s diakritikou
└── utils/               # Pomocné funkce
```

## ✅ Vlastnosti

- ✅ Plná podpora české diakritiky (DejaVu Sans)
- ✅ Validace IČO, DIČ, IBAN
- ✅ QR kódy pro platby (SPD standard)
- ✅ ISDOC XML embedováno v PDF
- ✅ CLI rozhraní
- ✅ 30+ testů

## 📝 Licence

MIT License - volné použití pro komerční i nekomerční účely.