"""Minimalistická šablona faktury."""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from models.invoice import Invoice
from .base import BaseTemplate


class MinimalTemplate(BaseTemplate):
    """
    Minimalistická šablona faktury.
    
    Charakteristika:
    - Černobílé schéma
    - Čistý, jednoduchý design
    - Minimum grafických prvků
    - Zaměření na čitelnost
    """
    
    def get_colors(self) -> dict:
        """Vrací minimalistické barevné schéma (odstíny šedi)."""
        return {
            'primary': colors.black,
            'secondary': colors.HexColor('#333333'),
            'accent': colors.HexColor('#F5F5F5'),
            'text': colors.HexColor('#2C2C2C'),
            'light_text': colors.HexColor('#999999'),
            'line': colors.HexColor('#DDDDDD')
        }
    
    def draw_header(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí minimalistickou hlavičku."""
        colors_scheme = self.get_colors()
        y_pos = self.page_height - self.margin
        
        # Jednoduchý nadpis
        c.setFont(self.font_bold, 32)
        c.setFillColor(colors_scheme['primary'])
        c.drawString(self.margin, y_pos, "FAKTURA")
        
        # Číslo faktury pod ním
        c.setFont(self.font_regular, 10)
        c.setFillColor(colors_scheme['light_text'])
        y_pos -= 8 * mm
        c.drawString(self.margin, y_pos, f"Číslo: {invoice.invoice_number}")
        
        # Tenká oddělovací čára
        y_pos -= 5 * mm
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=0.5, color=colors_scheme['line'])
        
        y_pos -= 10 * mm
        
        # Základní informace v jednoduchém layoutu
        c.setFont(self.font_regular, 9)
        c.setFillColor(colors_scheme['text'])
        
        info_y = y_pos
        c.drawString(self.margin, info_y, "Datum vystavení:")
        c.drawString(self.margin + 40 * mm, info_y, self.format_date(invoice.issue_date))
        
        info_y -= 5 * mm
        c.drawString(self.margin, info_y, "Datum splatnosti:")
        c.drawString(self.margin + 40 * mm, info_y, self.format_date(invoice.due_date))
        
        info_y -= 5 * mm
        c.drawString(self.margin, info_y, "Variabilní symbol:")
        c.drawString(self.margin + 40 * mm, info_y, invoice.variable_symbol)
        
        y_pos -= 20 * mm
        
        # Dodavatel a odběratel - jednoduchý text bez rámečků
        # Dodavatel
        c.setFont(self.font_bold, 9)
        c.setFillColor(colors_scheme['secondary'])
        c.drawString(self.margin, y_pos, "OD:")
        
        c.setFont(self.font_regular, 9)
        c.setFillColor(colors_scheme['text'])
        y_pos -= 5 * mm
        c.drawString(self.margin, y_pos, invoice.supplier.name)
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, invoice.supplier.street)
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, 
                    f"{invoice.supplier.zip_code} {invoice.supplier.city}")
        y_pos -= 4 * mm
        c.setFillColor(colors_scheme['light_text'])
        c.drawString(self.margin, y_pos, 
                    f"IČO: {invoice.supplier.ico}  |  DIČ: {invoice.supplier.dic}")
        
        # Odběratel
        y_customer = y_pos + 21 * mm
        x_right = self.page_width / 2 + 10 * mm
        
        c.setFont(self.font_bold, 9)
        c.setFillColor(colors_scheme['secondary'])
        c.drawString(x_right, y_customer, "PRO:")
        
        c.setFont(self.font_regular, 9)
        c.setFillColor(colors_scheme['text'])
        y_customer -= 5 * mm
        c.drawString(x_right, y_customer, invoice.customer.name)
        y_customer -= 4 * mm
        c.drawString(x_right, y_customer, invoice.customer.street)
        y_customer -= 4 * mm
        c.drawString(x_right, y_customer, 
                    f"{invoice.customer.zip_code} {invoice.customer.city}")
        y_customer -= 4 * mm
        c.setFillColor(colors_scheme['light_text'])
        c.drawString(x_right, y_customer, 
                    f"IČO: {invoice.customer.ico}  |  DIČ: {invoice.customer.dic}")
        
        self.current_y = y_pos - 15 * mm
    
    def draw_body(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí minimalistickou tabulku položek."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y
        
        # Oddělovací čára
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=0.5, color=colors_scheme['line'])
        
        y_pos -= 8 * mm
        
        # Hlavička tabulky - pouze text, žádné pozadí
        c.setFont(self.font_bold, 8)
        c.setFillColor(colors_scheme['secondary'])
        
        col_desc = self.margin
        col_qty = self.page_width - 100 * mm
        col_unit = self.page_width - 85 * mm
        col_price = self.page_width - 65 * mm
        col_vat = self.page_width - 40 * mm
        col_total = self.page_width - 25 * mm
        
        c.drawString(col_desc, y_pos, "Popis")
        c.drawString(col_qty, y_pos, "Množství")
        c.drawString(col_unit, y_pos, "J.")
        c.drawString(col_price, y_pos, "Cena/j.")
        c.drawString(col_vat, y_pos, "DPH")
        c.drawString(col_total, y_pos, "Celkem")
        
        y_pos -= 2 * mm
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=0.5, color=colors_scheme['line'])
        
        y_pos -= 5 * mm
        c.setFont(self.font_regular, 8)
        c.setFillColor(colors_scheme['text'])
        
        # Položky - jednoduché řádky
        for item in invoice.items:
            if y_pos < 50 * mm:
                c.showPage()
                y_pos = self.page_height - self.margin
            
            c.drawString(col_desc, y_pos, item.description[:50])
            c.drawString(col_qty, y_pos, str(item.quantity))
            c.drawString(col_unit, y_pos, item.unit)
            c.drawRightString(col_price + 20 * mm, y_pos, 
                            self.format_price(item.unit_price))
            c.drawString(col_vat, y_pos, f"{item.vat_rate}%")
            c.drawRightString(col_total + 20 * mm, y_pos, 
                            self.format_price(item.total_price_with_vat))
            
            y_pos -= 5 * mm
        
        # Oddělovací čára
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=0.5, color=colors_scheme['line'])
        
        self.current_y = y_pos - 5 * mm
    
    def draw_footer(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí minimalistický footer."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y
        
        # Souhrn - vpravo, jednoduché
        x_label = self.page_width - 90 * mm
        x_value = self.page_width - 25 * mm
        
        c.setFont(self.font_regular, 9)
        c.setFillColor(colors_scheme['text'])
        
        vat_summary = invoice.get_vat_summary()
        for vat_rate, amounts in vat_summary.items():
            c.drawString(x_label, y_pos, f"Základ DPH {vat_rate}%")
            c.drawRightString(x_value, y_pos, self.format_price(amounts['base']))
            y_pos -= 4 * mm
            
            c.drawString(x_label, y_pos, f"DPH {vat_rate}%")
            c.drawRightString(x_value, y_pos, self.format_price(amounts['vat']))
            y_pos -= 5 * mm
        
        # Celková částka - pouze čára a zvětšené písmo
        y_pos -= 2 * mm
        self.draw_line(c, x_label - 5 * mm, y_pos, self.page_width - self.margin, y_pos,
                      width=1, color=colors_scheme['primary'])
        
        y_pos -= 7 * mm
        c.setFont(self.font_bold, 10)
        c.setFillColor(colors_scheme['primary'])
        c.drawString(x_label, y_pos, "K úhradě")
        c.setFont(self.font_bold, 14)
        c.drawRightString(self.page_width - self.margin, y_pos, self.format_price(invoice.total_with_vat))
        
        # Bankovní údaje - vlevo dole
        y_bank = y_pos - 5 * mm
        c.setFont(self.font_regular, 8)
        c.setFillColor(colors_scheme['text'])
        
        c.drawString(self.margin, y_bank, "Platba bankovním převodem:")
        y_bank -= 4 * mm
        c.drawString(self.margin, y_bank, f"Číslo účtu: {invoice.supplier.iban}")
        y_bank -= 3.5 * mm
        c.drawString(self.margin, y_bank, f"Banka: {invoice.supplier.bank_name}")
        y_bank -= 3.5 * mm
        c.drawString(self.margin, y_bank, f"Variabilní symbol: {invoice.variable_symbol}")
        
        # Poznámka
        if invoice.note:
            y_bank -= 5 * mm
            c.setFillColor(colors_scheme['light_text'])
            c.drawString(self.margin, y_bank, invoice.note)
        
        # Minimální patička
        c.setFont(self.font_regular, 7)
        c.setFillColor(colors_scheme['light_text'])
        c.drawCentredString(self.page_width / 2, 20 * mm,
                           "Elektronická faktura - platná bez podpisu")

