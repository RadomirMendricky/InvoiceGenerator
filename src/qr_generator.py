"""Generátor QR kódů pro české platební QR kódy."""

import qrcode
from io import BytesIO
from PIL import Image

from models.invoice import Invoice


class QRGenerator:
    """
    Generátor QR kódů pro faktury podle českého standardu.
    
    Podporuje Short Payment Descriptor (SPD) formát používaný v ČR.
    """
    
    @staticmethod
    def _generate_cz_bban():
        """
        Generuje realistický 20místný český BBAN (Basic Bank Account Number)
        ve formátu: Předčíslí (max 6) + Číslo účtu (10) + Kód banky (4).
        """
        import random
        # Seznam reálných kódů bank v ČR pro větší realističnost
        bank_codes = [
            "0100",  # Komerční banka
            "0800",  # Česká spořitelna
            "2010",  # Fio banka
            "3030",  # Air Bank
            "5500",  # Raiffeisenbank
            "6210",  # mBank
        ]
        
        # 1. Kód banky (4 číslice) - vybíráme ze seznamu
        bank_code = random.choice(bank_codes)
        
        # 2. Předčíslí účtu (2 až 6 číslic) - v CZ BBANu se často doplňuje nulami na 6 pozic
        # Abychom zjednodušili, generujeme 6 náhodných číslic.
        prefix_account = "".join([str(random.randint(0, 9)) for _ in range(6)])
        
        # 3. Číslo účtu (vždy 10 číslic)
        main_account = "".join([str(random.randint(0, 9)) for _ in range(10)])
        
        # BBAN má celkem 20 číslic. V CZ IBANu je uspořádání PŘEDČÍSLÍ + ČÍSLO ÚČTU + KÓD BANKY.
        # POZOR: Struktura BBANu pro IBAN je pevně daná a liší se od obvyklého formátu SPREAD (kde je kód banky na konci).
        # CZ IBAN BBAN struktura (dle standardu ČNB): 
        #   A6 (Předčíslí) + B10 (Číslo účtu) + C4 (Kód banky) -> dohromady 20 číslic.
        
        # Správné pořadí pro BBAN, jak se používá ve výpočtu IBANu:
        bban = prefix_account + main_account + bank_code
        
        return bban

    @staticmethod
    def _char_to_int(char):
        """Převádí písmena na číslice (A=10, B=11, ..., Z=35)."""
        if '0' <= char <= '9':
            return char
        elif 'A' <= char <= 'Z':
            return str(ord(char) - ord('A') + 10)
        else:
            # Tady by se nemělo nic spustit pro CZ IBAN, který používá jen číslice.
            raise ValueError(f"Neplatný znak: {char}")

    @staticmethod
    def _calculate_mod97(s):
        """
        Vypočítá zbytek po dělení 97 pro dlouhý číselný řetězec (iterativní Modulo 97).
        """
        remainder = 0
        for digit in s:
            # Vytvoří nové číslo spojením zbytku a další číslice
            remainder = (remainder * 10 + int(digit)) % 97
        return remainder

    @staticmethod
    def _generate_valid_cz_iban():
        """
        Generuje validní český IBAN s realistickou strukturou BBAN.
        """
        country_code = "CZ"
        
        # 1. Generování realistického českého BBANu (20 číslic)
        bban = QRGenerator._generate_cz_bban()

        # 2. Sestavení dočasného řetězce pro kontrolní součet
        # Formát pro výpočet: BBAN + Kód Země + '00'
        temp_string_alpha = bban + country_code + "00"

        # 3. Převod písmen na číslice
        # CZ = 1235 (C=12, Z=35)
        temp_string_numeric = "".join(QRGenerator._char_to_int(char) for char in temp_string_alpha)

        # 4. Výpočet zbytku R (MOD 97)
        remainder = QRGenerator._calculate_mod97(temp_string_numeric)

        # 5. Výpočet kontrolních číslic K
        # K = 98 - R
        check_digits = 98 - remainder

        # Musí být vždy dvoumístné (doplní nulu zepředu, pokud je menší než 10)
        final_check_digits = str(check_digits).zfill(2)

        # 6. Sestavení finálního validního IBANu
        # Formát: Kód Země + Kontrolní číslice + BBAN
        valid_iban = country_code + final_check_digits + bban

        return valid_iban

    @staticmethod
    def generate_payment_string(invoice: Invoice) -> str:
        """
        Generuje platební řetězec pro QR kód podle českého standardu SPD 1.0.
        
        Formát: SPD*1.0*ACC:<IBAN>*AM:<částka>*CC:<měna>*MSG:<zpráva>*X-VS:<variabilní symbol>
        
        Args:
            invoice: Instance faktury
            
        Returns:
            Platební řetězec pro QR kód podle SPD 1.0
        """
        # Generování validního českého IBAN
        iban = QRGenerator._generate_valid_cz_iban()
        
        # Částka k úhradě - převést na formát s tečkou a max. dvě desetinná místa
        amount = round(float(invoice.total_with_vat), 2)
        
        # Zpráva (zkrácená na max 60 znaků, odstranění nepovolených znaků)
        message = f"Faktura {invoice.invoice_number}"[:60]
        # Odstranění nepovolených znaků ze zprávy
        message = message.replace("*", "").replace(":", "").replace(";", "")
        
        # Variabilní symbol - max. 10 číslic
        vs = str(invoice.variable_symbol)[:10]
        # Zajistit, že obsahuje pouze číslice
        vs = ''.join(filter(str.isdigit, vs))
        
        # Sestavení platebního řetězce podle SPD 1.0 standardu
        # Správné pořadí: SPD*1.0*ACC:<IBAN>*AM:<částka>*CC:<měna>*MSG:<zpráva>*X-VS:<vs>
        payment_string = (
            f"SPD*1.0*"
            f"ACC:{iban}*"
            f"AM:{amount:.2f}*"
            f"CC:CZK*"
            f"MSG:{message}*"
            f"X-VS:{vs}"
        )
        
        return payment_string
    
    @staticmethod
    def generate_qr_code(invoice: Invoice, output_path: str = None) -> Image:
        """
        Generuje QR kód pro platbu faktury.
        
        Args:
            invoice: Instance faktury
            output_path: Cesta k výstupnímu souboru (pokud None, vrátí Image objekt)
            
        Returns:
            PIL Image objekt s QR kódem
        """
        payment_string = QRGenerator.generate_payment_string(invoice)
        
        # Vytvoření QR kódu
        qr = qrcode.QRCode(
            version=None,  # Automatická velikost
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        
        qr.add_data(payment_string)
        qr.make(fit=True)
        
        # Vytvoření obrázku
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Uložení, pokud je zadána cesta
        if output_path:
            img.save(output_path)
        
        return img
    
    @staticmethod
    def get_qr_bytes(invoice: Invoice) -> bytes:
        """
        Vrací QR kód jako bajty (pro vložení do PDF).
        
        Args:
            invoice: Instance faktury
            
        Returns:
            Bajty PNG obrázku s QR kódem
        """
        img = QRGenerator.generate_qr_code(invoice)
        
        # Konverze na bajty
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @staticmethod
    def add_qr_to_template(template_instance, canvas_obj, invoice: Invoice, 
                          x: float, y: float, size: float = 50):
        """
        Přidá QR kód přímo do PDF šablony.
        
        Args:
            template_instance: Instance PDF šablony
            canvas_obj: Canvas objekt z reportlab
            invoice: Instance faktury
            x, y: Pozice QR kódu v mm
            size: Velikost QR kódu v mm
        """
        from reportlab.lib.units import mm
        import tempfile
        import os
        
        # Vytvoření dočasného souboru pro QR kód
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            # Získání QR jako obrázek a uložení do dočasného souboru
            img = QRGenerator.generate_qr_code(invoice)
            img.save(temp_path, format='PNG')
            
            # Vložení do PDF
            canvas_obj.drawImage(
                temp_path,
                x * mm,
                y * mm,
                width=size * mm,
                height=size * mm,
                preserveAspectRatio=True
            )
        finally:
            # Smazání dočasného souboru
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def add_qr_to_existing_pdf(invoice: Invoice, pdf_path: str):
    """
    Přidá QR kód do existujícího PDF souboru.
    
    Args:
        invoice: Instance faktury
        pdf_path: Cesta k existujícímu PDF (bude přepsáno)
    """
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    import PyPDF2
    import tempfile
    import os
    
    # 1. Vytvoření dočasného PDF pouze s QR kódem
    temp_qr_pdf = tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False)
    temp_qr_path = temp_qr_pdf.name
    temp_qr_pdf.close()
    
    c = pdf_canvas.Canvas(temp_qr_path, pagesize=A4)
    page_width, page_height = A4
    
    # Pozice QR kódu (vpravo dole)
    qr_x = page_width - 70 * mm
    qr_y = 35 * mm
    qr_size = 40  # mm
    
    # Vykreslení QR kódu
    QRGenerator.add_qr_to_template(None, c, invoice, qr_x / mm, qr_y / mm, qr_size)
    
    # Popisek QR kódu
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(qr_x + (qr_size * mm / 2), qr_y - 5 * mm, "Naskenujte pro platbu")
    
    c.showPage()
    c.save()
    
    # 2. Sloučení původního PDF a PDF s QR kódem
    try:
        with open(pdf_path, 'rb') as original_file, open(temp_qr_path, 'rb') as qr_file:
            original_reader = PyPDF2.PdfReader(original_file)
            qr_reader = PyPDF2.PdfReader(qr_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            
            if len(original_reader.pages) > 0:
                page = original_reader.pages[0]
                # Sloučení stránky s QR kódem
                page.merge_page(qr_reader.pages[0])
                pdf_writer.add_page(page)
                
                for i in range(1, len(original_reader.pages)):
                    pdf_writer.add_page(original_reader.pages[i])
            
            # Uložení do dočasného souboru
            temp_out_pdf = tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False)
            temp_out_path = temp_out_pdf.name
            pdf_writer.write(temp_out_pdf)
            temp_out_pdf.close()
            
        # Přepsání původního souboru
        import shutil
        shutil.move(temp_out_path, pdf_path)
        
    finally:
        # Úklid
        if os.path.exists(temp_qr_path):
            os.unlink(temp_qr_path)


def generate_invoice_with_qr(invoice: Invoice, template_class, output_path: str):
    """
    Generuje fakturu s QR kódem.
    (Zachováno pro zpětnou kompatibilitu)
    
    Args:
        invoice: Instance faktury
        template_class: Třída šablony (ClassicTemplate, ModernTemplate, atd.)
        output_path: Cesta k výstupnímu PDF
    """
    # Standardní generování faktury
    template = template_class()
    template.generate(invoice, output_path)
    
    # Přidání QR kódu
    add_qr_to_existing_pdf(invoice, output_path)

