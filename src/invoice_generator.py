"""Hlavní modul pro generování faktur."""

from pathlib import Path
from typing import List

from models.invoice import Invoice
from pdf_templates import get_template
from qr_generator import generate_invoice_with_qr
from isdoc_generator import generate_invoice_with_isdoc
from utils.file_utils import ensure_output_dir, generate_filename
import data_utils


class InvoiceGenerator:
    """
    Hlavní třída pro generování faktur v různých režimech.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Inicializace generátoru.
        
        Args:
            output_dir: Cesta k výstupnímu adresáři
        """
        self.output_dir = ensure_output_dir(output_dir)
    
    def generate_invoice(self, invoice: Invoice = None, 
                        template: str = 'classic',
                        with_qr: bool = False,
                        with_isdoc: bool = False) -> dict:
        """
        Vygeneruje jednu fakturu.
        
        Args:
            invoice: Instance faktury (pokud None, vygeneruje se náhodná)
            template: Název šablony ('classic', 'modern', 'minimal')
            with_qr: Zda přidat QR kód
            with_isdoc: Zda připojit ISDOC XML
            
        Returns:
            Slovník s cestami k vygenerovaným souborům
        """
        # Pokud není faktura zadána, vygeneruj náhodnou
        if invoice is None:
            invoice = data_utils.generate_invoice()
        
        # Získání třídy šablony
        template_class = get_template(template)
        
        # Základní název souboru
        suffix = ""
        if with_qr: suffix += "_qr"
        if with_isdoc: suffix += "_isdoc"
        
        pdf_filename = generate_filename('invoice' + suffix, 'pdf', invoice.invoice_number, self.output_dir)
        pdf_path = self.output_dir / pdf_filename
        pdf_path_str = str(pdf_path)
        
        # 1. Generování základního PDF
        template_instance = template_class()
        template_instance.generate(invoice, pdf_path_str)
        
        result = {'pdf': pdf_path_str}
        
        # 2. Přidání QR kódu
        if with_qr:
            from qr_generator import add_qr_to_existing_pdf
            add_qr_to_existing_pdf(invoice, pdf_path_str)
            
        # 3. Přidání ISDOC
        if with_isdoc:
            from isdoc_generator import attach_isdoc_to_pdf
            attach_isdoc_to_pdf(invoice, pdf_path_str)
            result['note'] = 'ISDOC XML embedováno v PDF'
            
        return result
    
    def generate_batch(self, count: int, template: str = 'classic',
                      with_qr: bool = False, with_isdoc: bool = False) -> List[dict]:
        """
        Vygeneruje více faktur najednou.
        
        Args:
            count: Počet faktur k vygenerování
            template: Název šablony
            with_qr: Zda přidat QR kód
            with_isdoc: Zda připojit ISDOC XML
            
        Returns:
            Seznam slovníků s cestami k vygenerovaným souborům
        """
        results = []
        
        print(f"Generuji {count} faktur (QR={with_qr}, ISDOC={with_isdoc}) se šablonou '{template}'...")
        
        for i in range(count):
            try:
                result = self.generate_invoice(template=template, with_qr=with_qr, with_isdoc=with_isdoc)
                results.append(result)
                print(f"  [{i+1}/{count}] Vygenerováno: {result.get('pdf', 'N/A')}")
            except Exception as e:
                print(f"  [{i+1}/{count}] Chyba: {e}")
        
        print(f"\nCelkem vygenerováno: {len(results)}/{count} faktur")
        print(f"Umístění: {self.output_dir}")
        
        return results
    


