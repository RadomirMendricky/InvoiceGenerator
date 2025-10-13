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

