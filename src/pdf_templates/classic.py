"""Klasická šablona faktury."""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from models.invoice import Invoice
from .base import BaseTemplate


class ClassicTemplate(BaseTemplate):
    """
    Klasická (tradiční) šablona faktury.
    
    Charakteristika:
    - Modrá barevná schéma
    - Tradiční layout
    - Přehledné oddělení sekcí
    """
    
    def get_colors(self) -> dict:
        """Vrací modrošedé barevné schéma."""
        return {
            'primary': colors.HexColor('#2C3E50'),      # Tmavě modrošedá
            'secondary': colors.HexColor('#3498DB'),    # Modrá
            'accent': colors.HexColor('#ECF0F1'),       # Světle šedá
            'text': colors.black,
            'light_text': colors.HexColor('#7F8C8D')
        }
    
    def draw_header(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí hlavičku s dodavatelem a odběratelem."""
        colors_scheme = self.get_colors()
        y_pos = self.page_height - self.margin
        
        # Nadpis FAKTURA
        c.setFont(self.font_bold, 24)
        c.setFillColor(colors_scheme['primary'])
        c.drawString(self.margin, y_pos, "FAKTURA")
        
        # Číslo faktury napravo
        c.setFont(self.font_regular, 10)
        c.drawRightString(self.page_width - self.margin, y_pos, 
                         f"č. {invoice.invoice_number}")
        
        y_pos -= 15 * mm
        
        # Oddělení
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=2, color=colors_scheme['secondary'])
        
        y_pos -= 10 * mm
        
        # Dodavatel (vlevo)
        c.setFont(self.font_bold, 11)
        c.setFillColor(colors_scheme['text'])
        c.drawString(self.margin, y_pos, "Dodavatel:")
        
        c.setFont(self.font_regular, 10)
        y_pos -= 5 * mm
        c.drawString(self.margin, y_pos, invoice.supplier.name)
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, invoice.supplier.street)
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, f"{invoice.supplier.zip_code} {invoice.supplier.city}")
        y_pos -= 5 * mm
        c.drawString(self.margin, y_pos, f"IČO: {invoice.supplier.ico}")
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, f"DIČ: {invoice.supplier.dic}")
        
        # Odběratel (vpravo)
        y_pos_right = self.page_height - self.margin - 25 * mm
        x_right = self.page_width / 2 + 10 * mm
        
        c.setFont(self.font_bold, 11)
        c.drawString(x_right, y_pos_right, "Odběratel:")
        
        c.setFont(self.font_regular, 10)
        y_pos_right -= 5 * mm
        c.drawString(x_right, y_pos_right, invoice.customer.name)
        y_pos_right -= 4 * mm
        c.drawString(x_right, y_pos_right, invoice.customer.street)
        y_pos_right -= 4 * mm
        c.drawString(x_right, y_pos_right, f"{invoice.customer.zip_code} {invoice.customer.city}")
        y_pos_right -= 5 * mm
        c.drawString(x_right, y_pos_right, f"IČO: {invoice.customer.ico}")
        y_pos_right -= 4 * mm
        c.drawString(x_right, y_pos_right, f"DIČ: {invoice.customer.dic}")
        
        # Informace o faktuře
        y_pos = y_pos_right - 10 * mm
        
        # Box s informacemi
        box_height = 25 * mm
        self.draw_rect(c, self.margin, y_pos - box_height, 
                      self.page_width - 2 * self.margin, box_height,
                      fill_color=colors_scheme['accent'])
        
        y_pos -= 5 * mm
        c.setFillColor(colors_scheme['text'])
        
        # Levý sloupec
        c.drawString(self.margin + 5 * mm, y_pos, f"Datum vystavení:")
        c.drawString(self.margin + 45 * mm, y_pos, self.format_date(invoice.issue_date))
        
        y_pos -= 5 * mm
        c.drawString(self.margin + 5 * mm, y_pos, f"Datum splatnosti:")
        c.drawString(self.margin + 45 * mm, y_pos, self.format_date(invoice.due_date))
        
        # Pravý sloupec
        y_pos_right = y_pos + 5 * mm
        x_right_col = self.page_width / 2 + 10 * mm
        
        c.drawString(x_right_col, y_pos_right, f"Variabilní symbol:")
        c.drawString(x_right_col + 40 * mm, y_pos_right, invoice.variable_symbol)
        
        y_pos_right -= 5 * mm
        c.drawString(x_right_col, y_pos_right, f"Způsob platby:")
        c.drawString(x_right_col + 40 * mm, y_pos_right, invoice.payment_method)
        
        self.current_y = y_pos - 10 * mm
    
    def draw_body(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí tabulku s položkami."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y
        
        # Tabulka položek
        table_y = y_pos - 5 * mm
        
        # Hlavička tabulky
        header_height = 8 * mm
        self.draw_rect(c, self.margin, table_y - header_height,
                      self.page_width - 2 * self.margin, header_height,
                      fill_color=colors_scheme['secondary'])
        
        c.setFillColor(colors.white)
        c.setFont(self.font_bold, 9)
        
        # Pozice sloupců
        col_desc = self.margin + 2 * mm
        col_qty = self.page_width - 110 * mm
        col_unit = self.page_width - 95 * mm
        col_price = self.page_width - 75 * mm
        col_vat = self.page_width - 50 * mm
        
        header_y = table_y - 5 * mm
        c.drawString(col_desc, header_y, "Popis")
        c.drawString(col_qty, header_y, "Množ.")
        c.drawString(col_unit, header_y, "Jedn.")
        c.drawString(col_price, header_y, "Cena/j.")
        c.drawString(col_vat, header_y, "DPH")
        c.drawRightString(self.page_width - self.margin, header_y, "Celkem")
        
        y_pos = table_y - header_height - 3 * mm
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_regular, 9)
        
        # Položky
        for item in invoice.items:
            if y_pos < 50 * mm:  # Kontrola, zda máme místo
                c.showPage()
                y_pos = self.page_height - self.margin
            
            c.drawString(col_desc, y_pos, item.description[:40])
            c.drawString(col_qty, y_pos, str(item.quantity))
            c.drawString(col_unit, y_pos, item.unit)
            c.drawRightString(col_price + 20 * mm, y_pos, invoice.format_price(item.unit_price))
            c.drawString(col_vat, y_pos, f"{item.vat_rate}%")
            c.drawRightString(self.page_width - self.margin, y_pos, 
                            invoice.format_price(item.total_price_with_vat))
            
            y_pos -= 5 * mm
        
        # Oddělení před součty
        y_pos -= 2 * mm
        self.draw_line(c, self.margin, y_pos, self.page_width - self.margin, y_pos,
                      width=1, color=colors_scheme['secondary'])
        
        self.current_y = y_pos
    
    def draw_footer(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí součty a bankovní údaje."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y - 10 * mm
        
        # Souhrn DPH
        vat_summary = invoice.get_vat_summary()
        x_label = self.page_width - 110 * mm
        x_value = self.page_width - self.margin
        
        c.setFont(self.font_regular, 9)
        
        for vat_rate, amounts in vat_summary.items():
            c.drawString(x_label, y_pos, f"Základ DPH {vat_rate}%:")
            c.drawRightString(x_value, y_pos, invoice.format_price(amounts['base']))
            y_pos -= 4 * mm
            
            c.drawString(x_label, y_pos, f"DPH {vat_rate}%:")
            c.drawRightString(x_value, y_pos, invoice.format_price(amounts['vat']))
            y_pos -= 5 * mm
        
        # Celková částka
        y_pos -= 2 * mm
        self.draw_rect(c, self.page_width - 120 * mm, y_pos - 8 * mm,
                      100 * mm, 8 * mm, fill_color=colors_scheme['primary'])
        
        c.setFillColor(colors.white)
        c.setFont(self.font_bold, 11)
        c.drawString(self.page_width - 115 * mm, y_pos - 5 * mm, "K úhradě:")
        c.setFont(self.font_bold, 13)
        c.drawRightString(self.page_width - self.margin, y_pos - 5 * mm, 
                         invoice.format_price(invoice.total_with_vat))
        
        # Cestní doložka
        y_clause = y_pos - 10 * mm
        y_clause = self.draw_assignment_clause(c, invoice, y_clause)
        
        # Bankovní údaje
        y_pos = y_clause - 5 * mm
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_bold, 10)
        c.drawString(self.margin, y_pos, "Bankovní spojení:")
        
        y_pos -= 5 * mm
        c.setFont(self.font_regular, 9)
        c.drawString(self.margin, y_pos, f"Číslo účtu: {invoice.supplier.iban}")
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, f"Banka: {invoice.supplier.bank_name}")
        y_pos -= 4 * mm
        c.drawString(self.margin, y_pos, f"Variabilní symbol: {invoice.variable_symbol}")
        
        # Poznámka
        if invoice.note:
            y_pos -= 8 * mm
            c.setFont(self.font_bold, 9)
            c.drawString(self.margin, y_pos, "Poznámka:")
            y_pos -= 4 * mm
            c.setFont(self.font_regular, 9)
            c.drawString(self.margin, y_pos, invoice.note)
        
        # Patička
        y_pos = 20 * mm
        c.setFont(self.font_regular, 8)
        c.setFillColor(colors_scheme['light_text'])
        c.drawCentredString(self.page_width / 2, y_pos,
                           "Faktura vystavena elektronicky a je platná bez podpisu a razítka.")

