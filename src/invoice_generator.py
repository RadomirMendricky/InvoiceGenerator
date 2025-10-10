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
                        mode: str = 'pdf',
                        template: str = 'classic') -> dict:
        """
        Vygeneruje jednu fakturu.
        
        Args:
            invoice: Instance faktury (pokud None, vygeneruje se náhodná)
            mode: Režim generování ('pdf', 'qr', 'isdoc')
            template: Název šablony ('classic', 'modern', 'minimal')
            
        Returns:
            Slovník s cestami k vygenerovaným souborům
        """
        # Pokud není faktura zadána, vygeneruj náhodnou
        if invoice is None:
            invoice = data_utils.generate_invoice()
        
        # Získání třídy šablony
        template_class = get_template(template)
        
        # Generování podle režimu
        result = {}
        
        if mode == 'pdf':
            # Standardní PDF
            pdf_path = self.output_dir / generate_filename('invoice', 'pdf', invoice.invoice_number)
            template_instance = template_class()
            template_instance.generate(invoice, str(pdf_path))
            result['pdf'] = str(pdf_path)
            
        elif mode == 'qr':
            # PDF s QR kódem
            pdf_path = self.output_dir / generate_filename('invoice_qr', 'pdf', invoice.invoice_number)
            generate_invoice_with_qr(invoice, template_class, str(pdf_path))
            result['pdf'] = str(pdf_path)
            
        elif mode == 'isdoc':
            # PDF s embedovaným ISDOC XML
            pdf_path = self.output_dir / generate_filename('invoice_isdoc', 'pdf', invoice.invoice_number)
            generate_invoice_with_isdoc(invoice, template_class, str(pdf_path))
            result['pdf'] = str(pdf_path)
            result['note'] = 'ISDOC XML embedováno v PDF'
            
        else:
            raise ValueError(f"Neznámý režim: {mode}. Podporované: pdf, qr, isdoc")
        
        return result
    
    def generate_batch(self, count: int, mode: str = 'pdf', 
                      template: str = 'classic') -> List[dict]:
        """
        Vygeneruje více faktur najednou.
        
        Args:
            count: Počet faktur k vygenerování
            mode: Režim generování
            template: Název šablony
            
        Returns:
            Seznam slovníků s cestami k vygenerovaným souborům
        """
        results = []
        
        print(f"Generuji {count} faktur v režimu '{mode}' se šablonou '{template}'...")
        
        for i in range(count):
            try:
                result = self.generate_invoice(mode=mode, template=template)
                results.append(result)
                print(f"  [{i+1}/{count}] Vygenerováno: {result.get('pdf', 'N/A')}")
            except Exception as e:
                print(f"  [{i+1}/{count}] Chyba: {e}")
        
        print(f"\nCelkem vygenerováno: {len(results)}/{count} faktur")
        print(f"Umístění: {self.output_dir}")
        
        return results
    
    def generate_demo(self) -> List[dict]:
        """
        Vygeneruje ukázkové faktury ve všech režimech a šablonách.
        
        Returns:
            Seznam slovníků s cestami k vygenerovaným souborům
        """
        results = []
        
        print("=== DEMO REŽIM ===")
        print("Generuji ukázkové faktury...\n")
        
        modes = ['pdf', 'qr', 'isdoc']
        templates = ['classic', 'modern', 'minimal']
        
        # Pro každou kombinaci režimu a šablony (kromě ISDOC, který generujeme jen jednou)
        for template in templates:
            for mode in modes:
                # ISDOC generujeme jen s jednou šablonou (classic)
                if mode == 'isdoc' and template != 'classic':
                    continue
                
                try:
                    print(f"Generuji: {mode} / {template}")
                    result = self.generate_invoice(mode=mode, template=template)
                    results.append(result)
                    
                    for file_type, file_path in result.items():
                        print(f"  ✓ {file_type.upper()}: {file_path}")
                    
                except Exception as e:
                    print(f"  ✗ Chyba: {e}")
                
                print()
        
        print(f"=== KONEC DEMO ===")
        print(f"Vygenerováno celkem {len(results)} ukázek")
        print(f"Umístění: {self.output_dir}")
        
        return results

