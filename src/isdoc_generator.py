"""Generátor ISDOC XML souborů pro české faktury."""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

from models.invoice import Invoice


class ISDOCGenerator:
    """
    Generátor ISDOC (Information System Data Output for Commerce) XML souborů.
    
    ISDOC je český standard pro elektronickou výměnu faktur.
    Verze: ISDOC 6.0.1
    """
    
    # Namespace definice
    NAMESPACES = {
        'isdoc': 'http://isdoc.cz/namespace/2013',
    }
    
    @staticmethod
    def _prettify_xml(elem: ET.Element) -> str:
        """
        Naformátuje XML s odsazením.
        
        Args:
            elem: Element k naformátování
            
        Returns:
            Formátovaný XML string
        """
        rough_string = ET.tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
    
    @staticmethod
    def _format_date(date_obj) -> str:
        """Formátuje datum do ISO formátu."""
        return date_obj.strftime("%Y-%m-%d")
    
    @staticmethod
    def generate(invoice: Invoice, output_path: str):
        """
        Generuje ISDOC XML soubor.
        
        Args:
            invoice: Instance faktury
            output_path: Cesta k výstupnímu XML souboru
        """
        # Hlavní element
        root = ET.Element('Invoice')
        root.set('xmlns', ISDOCGenerator.NAMESPACES['isdoc'])
        root.set('version', '6.0.1')
        
        # Metadata dokumentu
        doc_details = ET.SubElement(root, 'DocumentType')
        doc_details.text = '1'  # 1 = faktura
        
        # Číslo dokladu
        doc_number = ET.SubElement(root, 'ID')
        doc_number.text = invoice.invoice_number
        
        # UUID (pro reálné použití by mělo být unikátní)
        uuid_elem = ET.SubElement(root, 'UUID')
        uuid_elem.text = f"INV-{invoice.invoice_number}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Datum vystavení
        issue_date = ET.SubElement(root, 'IssueDate')
        issue_date.text = ISDOCGenerator._format_date(invoice.issue_date)
        
        # Datum splatnosti
        due_date = ET.SubElement(root, 'DueDate')
        due_date.text = ISDOCGenerator._format_date(invoice.due_date)
        
        # Měna
        currency = ET.SubElement(root, 'LocalCurrencyCode')
        currency.text = invoice.currency
        
        # Dodavatel (AccountingSupplierParty)
        ISDOCGenerator._add_party(root, 'AccountingSupplierParty', invoice.supplier)
        
        # Odběratel (AccountingCustomerParty)
        ISDOCGenerator._add_party(root, 'AccountingCustomerParty', invoice.customer)
        
        # Položky faktury
        ISDOCGenerator._add_invoice_lines(root, invoice)
        
        # Souhrn DPH
        ISDOCGenerator._add_tax_total(root, invoice)
        
        # Celkové částky
        ISDOCGenerator._add_totals(root, invoice)
        
        # Platební údaje
        ISDOCGenerator._add_payment_means(root, invoice)
        
        # Uložení do souboru
        xml_string = ISDOCGenerator._prettify_xml(root)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)
    
    @staticmethod
    def _add_party(parent: ET.Element, party_type: str, company):
        """
        Přidá informace o subjektu (dodavatel/odběratel).
        
        Args:
            parent: Rodičovský element
            party_type: Typ subjektu (AccountingSupplierParty/AccountingCustomerParty)
            company: Instance Company
        """
        party = ET.SubElement(parent, party_type)
        
        # Strana (Party)
        party_elem = ET.SubElement(party, 'Party')
        
        # Název
        party_name = ET.SubElement(party_elem, 'PartyName')
        name = ET.SubElement(party_name, 'Name')
        name.text = company.name
        
        # Adresa
        postal_address = ET.SubElement(party_elem, 'PostalAddress')
        
        street = ET.SubElement(postal_address, 'StreetName')
        street.text = company.street
        
        city = ET.SubElement(postal_address, 'CityName')
        city.text = company.city
        
        zip_code = ET.SubElement(postal_address, 'PostalZone')
        zip_code.text = company.zip_code
        
        country = ET.SubElement(postal_address, 'Country')
        country_code = ET.SubElement(country, 'IdentificationCode')
        country_code.text = 'CZ'
        country_name = ET.SubElement(country, 'Name')
        country_name.text = company.country
        
        # Identifikace
        party_identification = ET.SubElement(party_elem, 'PartyIdentification')
        id_elem = ET.SubElement(party_identification, 'ID')
        id_elem.text = company.ico
        
        # DIČ
        party_tax_scheme = ET.SubElement(party_elem, 'PartyTaxScheme')
        tax_id = ET.SubElement(party_tax_scheme, 'CompanyID')
        tax_id.text = company.dic
        
        tax_scheme = ET.SubElement(party_tax_scheme, 'TaxScheme')
        tax_scheme_id = ET.SubElement(tax_scheme, 'ID')
        tax_scheme_id.text = 'VAT'
    
    @staticmethod
    def _add_invoice_lines(parent: ET.Element, invoice: Invoice):
        """
        Přidá položky faktury.
        
        Args:
            parent: Rodičovský element
            invoice: Instance faktury
        """
        lines_container = ET.SubElement(parent, 'InvoiceLines')
        
        for idx, item in enumerate(invoice.items, start=1):
            line = ET.SubElement(lines_container, 'InvoiceLine')
            
            # ID řádku
            line_id = ET.SubElement(line, 'ID')
            line_id.text = str(idx)
            
            # Množství
            quantity = ET.SubElement(line, 'InvoicedQuantity')
            quantity.set('unitCode', item.unit)
            quantity.text = str(item.quantity)
            
            # Celková cena řádku
            line_extension = ET.SubElement(line, 'LineExtensionAmount')
            line_extension.text = str(item.total_price_without_vat)
            
            # Celková cena s DPH
            line_extension_tax = ET.SubElement(line, 'LineExtensionAmountTaxInclusive')
            line_extension_tax.text = str(item.total_price_with_vat)
            
            # DPH částka
            line_tax = ET.SubElement(line, 'LineExtensionTaxAmount')
            line_tax.text = str(item.vat_amount)
            
            # Jednotková cena
            unit_price = ET.SubElement(line, 'UnitPrice')
            unit_price.text = str(item.unit_price)
            
            # Sazba DPH
            class_tax = ET.SubElement(line, 'ClassifiedTaxCategory')
            percent = ET.SubElement(class_tax, 'Percent')
            percent.text = str(item.vat_rate)
            
            vat_calc = ET.SubElement(class_tax, 'VATCalculationMethod')
            vat_calc.text = '0'  # 0 = standardní výpočet
            
            # Popis položky
            item_elem = ET.SubElement(line, 'Item')
            description = ET.SubElement(item_elem, 'Description')
            description.text = item.description
    
    @staticmethod
    def _add_tax_total(parent: ET.Element, invoice: Invoice):
        """
        Přidá souhrn DPH.
        
        Args:
            parent: Rodičovský element
            invoice: Instance faktury
        """
        tax_total = ET.SubElement(parent, 'TaxTotal')
        
        # Celková DPH
        tax_amount = ET.SubElement(tax_total, 'TaxAmount')
        tax_amount.text = str(invoice.total_vat)
        
        # Rozpis podle sazeb
        vat_summary = invoice.get_vat_summary()
        
        for vat_rate, amounts in vat_summary.items():
            tax_subtotal = ET.SubElement(tax_total, 'TaxSubTotal')
            
            # Základ daně
            taxable_amount = ET.SubElement(tax_subtotal, 'TaxableAmount')
            taxable_amount.text = str(amounts['base'])
            
            # Částka daně
            tax_amount_sub = ET.SubElement(tax_subtotal, 'TaxAmount')
            tax_amount_sub.text = str(amounts['vat'])
            
            # Celkem s daní
            tax_inclusive = ET.SubElement(tax_subtotal, 'TaxInclusiveAmount')
            tax_inclusive.text = str(amounts['total'])
            
            # Kategorie
            tax_category = ET.SubElement(tax_subtotal, 'TaxCategory')
            percent = ET.SubElement(tax_category, 'Percent')
            percent.text = str(vat_rate)
    
    @staticmethod
    def _add_totals(parent: ET.Element, invoice: Invoice):
        """
        Přidá celkové částky.
        
        Args:
            parent: Rodičovský element
            invoice: Instance faktury
        """
        # Celkem bez DPH
        tax_exclusive = ET.SubElement(parent, 'TaxExclusiveAmount')
        tax_exclusive.text = str(invoice.total_without_vat)
        
        # Celkem s DPH
        tax_inclusive = ET.SubElement(parent, 'TaxInclusiveAmount')
        tax_inclusive.text = str(invoice.total_with_vat)
        
        # Částka k úhradě
        payable_amount = ET.SubElement(parent, 'PayableAmount')
        payable_amount.text = str(invoice.total_with_vat)
    
    @staticmethod
    def _add_payment_means(parent: ET.Element, invoice: Invoice):
        """
        Přidá platební údaje.
        
        Args:
            parent: Rodičovský element
            invoice: Instance faktury
        """
        payment_means = ET.SubElement(parent, 'PaymentMeans')
        
        # Platební instrukce
        payment_means_code = ET.SubElement(payment_means, 'PaymentMeansCode')
        payment_means_code.text = '42'  # 42 = bankovní převod
        
        # Detaily platby
        payment = ET.SubElement(payment_means, 'Payment')
        
        # Bankovní účet
        account = ET.SubElement(payment, 'PaidBy')
        iban = ET.SubElement(account, 'IBAN')
        iban.text = invoice.supplier.iban
        
        # Variabilní symbol
        details = ET.SubElement(payment, 'Details')
        id_elem = ET.SubElement(details, 'ID')
        id_elem.text = invoice.variable_symbol


def attach_isdoc_to_pdf(invoice: Invoice, pdf_path: str, output_xml: str = None):
    """
    Připojí ISDOC XML k existujícímu PDF souboru.
    
    Args:
        invoice: Instance faktury
        pdf_path: Cesta k existujícímu PDF (bude přepsáno)
        output_xml: Cesta k výstupnímu XML (volitelné, pro samostatný soubor)
    """
    import tempfile
    import os
    import pypdf
    
    # Vytvoření dočasného XML souboru
    temp_xml = tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8')
    temp_xml_path = temp_xml.name
    temp_xml.close()
    
    try:
        # Vygenerování ISDOC XML
        ISDOCGenerator.generate(invoice, temp_xml_path)
        
        # Přečtení XML obsahu
        with open(temp_xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Pokud je zadána cesta pro samostatný XML, zkopíruj ho tam
        if output_xml:
            import shutil
            shutil.copy(temp_xml_path, output_xml)
            
        # Přečtení PDF a přidání přílohy
        # Musíme načíst celý soubor do paměti nebo použít dočasný soubor pro výstup
        # PyPDF2 neumí číst a zapisovat do stejného souboru najednou
        
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = pypdf.PdfReader(pdf_file)
            pdf_writer = pypdf.PdfWriter()
            
            # Kopírování všech stránek
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            
            # Přidání XML jako attachment
            pdf_writer.add_attachment('isdoc.xml', xml_content.encode('utf-8'))
            
            # Uložení do dočasného souboru
            temp_pdf = tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False)
            temp_pdf_path = temp_pdf.name
            pdf_writer.write(temp_pdf)
            temp_pdf.close()
            
        # Přepsání původního souboru
        import shutil
        shutil.move(temp_pdf_path, pdf_path)
        
    finally:
        # Úklid
        if os.path.exists(temp_xml_path):
            os.unlink(temp_xml_path)

def generate_invoice_with_isdoc(invoice: Invoice, template_class, 
                                output_pdf: str, output_xml: str = None):
    """
    Generuje fakturu s ISDOC XML embedovaným přímo v PDF.
    (Zachováno pro zpětnou kompatibilitu, ale doporučuje se použít nový flow)
    
    Args:
        invoice: Instance faktury
        template_class: Třída PDF šablony
        output_pdf: Cesta k výstupnímu PDF
        output_xml: Cesta k výstupnímu XML (volitelné, pro samostatný soubor)
    """
    # Standardní vygenerování PDF
    template = template_class()
    template.generate(invoice, output_pdf)
    
    # Připojení ISDOC
    attach_isdoc_to_pdf(invoice, output_pdf, output_xml)
    
    print(f"[OK] ISDOC XML vloženo do PDF: {output_pdf}")

