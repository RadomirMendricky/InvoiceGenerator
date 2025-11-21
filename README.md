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
