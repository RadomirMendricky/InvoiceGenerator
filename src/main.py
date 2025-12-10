"""Hlavní vstupní bod aplikace - CLI rozhraní."""

import typer
from pathlib import Path
from typing import Optional

from invoice_generator import InvoiceGenerator


# Inicializace Typer aplikace
app = typer.Typer(
    help="Generator ceskych faktur - vytvari realisticke faktury pro testovani",
    add_completion=False
)


@app.command()
def generate(
    count: int = typer.Option(1, "--count", "-c", help="Počet faktur k vygenerování"),
    qr: bool = typer.Option(False, "--qr", "-q", help="Přidat QR kód"),
    isdoc: bool = typer.Option(False, "--isdoc", "-i", help="Připojit ISDOC XML"),
    template: str = typer.Option("classic", "--template", "-t", 
                                help="Šablona: classic, modern, minimal"),
    output_dir: str = typer.Option("output", "--output", "-o", 
                                  help="Výstupní adresář"),
    demo: bool = typer.Option(False, "--demo", "-d", 
                             help="Spustit demo režim (ignoruje ostatní parametry)"),
    config: str = typer.Option(None, "--config", "-C", help="Cesta k JSON konfiguraci dat"),
    assignment_clause: bool = typer.Option(False, "--assignment-clause", "-A", help="Přidat cestní doložku pro 4Trans")
):
    """
    Generuje české faktury s náhodnými nebo konfigurovatelnými daty.
    
    Příklady použití:
    
    # Vygenerovat 10 klasických faktur
    python main.py --count 10
    
    # Vygenerovat 5 faktur s QR kódem, moderní šablona
    python main.py --count 5 --qr --template modern
    
    # Vygenerovat faktury s ISDOC i QR kódem
    python main.py --count 3 --isdoc --qr
    
    # Spustit demo režim
    python main.py --demo
    """
    try:
        # Vytvoření generátoru
        generator = InvoiceGenerator(output_dir=output_dir)
        
        # Demo režim
        if demo:
            typer.echo("Spoustim DEMO rezim...\n")
            generator.generate_demo()
            typer.echo("\nDemo dokonceno!")
            return
            
        # Příprava faktury
        import data_utils
        if config:
            if not Path(config).exists():
                typer.echo(f"[!] Chyba: Konfiguracni soubor '{config}' neexistuje", err=True)
                raise typer.Exit(1)
            invoice = data_utils.load_from_json(config)
            typer.echo(f"Nactena data z: {config}")
        else:
            invoice = None 
            
        # Aplikace cestní doložky
        if assignment_clause:
            if invoice is None:
                 invoice = data_utils.generate_invoice()
            
            invoice.assignment_clause = data_utils.ASSIGNMENT_CLAUSE_4TRANS
            typer.echo("Pridana cestni dolozka (4Trans)")

        
        # Validace parametrů
        valid_templates = ['classic', 'modern', 'minimal']
        if template not in valid_templates:
            typer.echo(f"[!] Chyba: Neplatna sablona '{template}'", err=True)
            typer.echo(f"    Podporovane sablony: {', '.join(valid_templates)}", err=True)
            raise typer.Exit(1)
        
        if count < 1:
            typer.echo("[!] Chyba: Pocet faktur musi byt alespon 1", err=True)
            raise typer.Exit(1)
        
        # Generování
        typer.echo(f"QR kod: {'ANO' if qr else 'NE'}")
        typer.echo(f"ISDOC: {'ANO' if isdoc else 'NE'}")
        typer.echo(f"Sablona: {template}")
        typer.echo(f"Pocet: {count}")
        typer.echo(f"Vystup: {output_dir}\n")
        
        if count == 1:
            result = generator.generate_invoice(invoice=invoice, template=template, with_qr=qr, with_isdoc=isdoc)
            typer.echo("\n[OK] Faktura vygenerovana!")
            for file_type, file_path in result.items():
                typer.echo(f"     {file_type.upper()}: {file_path}")
        else:
            
            
            if config:
                 typer.echo("[WARN] Batch generovani s configem pouzije stejna data pro vsechny faktury.")
                 
            results = []
            print(f"Generuji {count} faktur (QR={with_qr}, ISDOC={with_isdoc}) se šablonou '{template}'...")
            
            for i in range(count):
                try:
                    current_invoice = None
                    if config:
                         current_invoice = data_utils.load_from_json(config)
                    
                    if assignment_clause:
                        if current_invoice is None:
                            current_invoice = data_utils.generate_invoice()
                        current_invoice.assignment_clause = data_utils.ASSIGNMENT_CLAUSE_4TRANS
                    
                    result = generator.generate_invoice(invoice=current_invoice, template=template, with_qr=qr, with_isdoc=isdoc)
                    results.append(result)
                    print(f"  [{i+1}/{count}] Vygenerováno: {result.get('pdf', 'N/A')}")
                except Exception as e:
                    print(f"  [{i+1}/{count}] Chyba: {e}")
            
            typer.echo(f"\n[OK] Vygenerovano {len(results)}/{count} faktur!")
        
    except KeyboardInterrupt:
        typer.echo("\n\n[!] Generovani preruseno uzivatelem", err=True)
        raise typer.Exit(130)
    
    except Exception as e:
        typer.echo(f"\n[!] Neocekavana chyba: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def info():
    """Zobrazí informace o aplikaci."""
    info_text = """
    Generator ceskych faktur
    ========================
    
    Verze: 1.0.0
    Autor: Invoice Generator Team
    
    Funkce:
    - Generovani PDF faktur (3 sablony)
    - QR kody pro platby (cesky standard SPD)
    - ISDOC XML export
    - Realisticka ceska data (firmy, adresy, ICO, DIC, IBAN)
    
    Podporovane moznosti:
    - --qr    - Prida QR kod pro platbu
    - --isdoc - Pripoji ISDOC XML soubor (embedovany v PDF)
    
    Dostupne sablony:
    - classic - Tradicni modry design
    - modern  - Moderni zeleno-oranzovy design
    - minimal - Cisty cernobily design
    
    Pro napovedu: python main.py --help
    """
    typer.echo(info_text)


@app.command()
def version():
    """Zobrazí verzi aplikace."""
    typer.echo("Invoice Generator v1.0.0")


@app.command()
def test_diakritika():
    """Otestuje správné zobrazení české diakritiky v PDF."""
    try:
        from test_diakritika import test_all_templates
        
        typer.echo("\n=== TEST CESKE DIAKRITIKY ===\n")
        success = test_all_templates()
        
        if success:
            typer.echo("\n[OK] Test dokoncen uspesne!")
            typer.echo("Zkontrolujte vygenerovane PDF v output/test_diakritika_*.pdf")
        else:
            typer.echo("\n[!] Test selhal!", err=True)
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"\n[!] Chyba behem testu: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

