"""Pomocné funkce pro práci se soubory."""

import os
from pathlib import Path
from datetime import datetime


def ensure_output_dir(base_dir: str = "output") -> Path:
    """
    Zajistí, že výstupní adresář existuje.
    
    Args:
        base_dir: Název základního adresáře (výchozí: "output")
        
    Returns:
        Path objekt výstupního adresáře
    """
    output_path = Path(base_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def generate_filename(prefix: str, extension: str, invoice_number: str = None, output_dir: Path = None) -> str:
    """
    Generuje unikátní název souboru.
    
    Args:
        prefix: Prefix souboru (např. "invoice", "qr", "isdoc")
        extension: Přípona souboru bez tečky (např. "pdf", "xml")
        invoice_number: Číslo faktury (pokud None, použije se timestamp)
        output_dir: Výstupní adresář pro kontrolu existence souboru
        
    Returns:
        Název souboru
    """
    if invoice_number:
        # Odstranění lomítek a speciálních znaků
        safe_number = invoice_number.replace("/", "_").replace(" ", "_")
        filename = f"{prefix}_{safe_number}.{extension}"
        
        # Kontrola existence a případné přidání timestampu
        if output_dir:
            file_path = output_dir / filename
            if file_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"{prefix}_{safe_number}_{timestamp}.{extension}"
                
        return filename
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"


def get_font_path(font_name: str) -> str:
    """
    Vrací cestu k fontu nebo None, pokud se použije výchozí font.
    
    Args:
        font_name: Název fontu
        
    Returns:
        Cesta k fontu nebo prázdný řetězec
    """
    # Pro Windows - fonty jsou v system složce
    if os.name == 'nt':
        system_fonts = Path(os.environ.get('WINDIR', 'C:\\Windows')) / 'Fonts'
        font_map = {
            'DejaVuSans': 'DejaVuSans.ttf',
            'Arial': 'arial.ttf',
            'Roboto': 'Roboto-Regular.ttf'
        }
        font_file = font_map.get(font_name)
        if font_file:
            font_path = system_fonts / font_file
            if font_path.exists():
                return str(font_path)
    
    # Pro Linux
    else:
        linux_fonts = [
            Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
            Path('/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf'),
        ]
        for font_path in linux_fonts:
            if font_path.exists():
                return str(font_path)
    
    return ""

