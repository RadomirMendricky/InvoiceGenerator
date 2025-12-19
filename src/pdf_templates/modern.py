"""Moderní šablona faktury."""

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from models.invoice import Invoice
from .base import BaseTemplate


class ModernTemplate(BaseTemplate):
    """
    Moderní šablona faktury.
    
    Charakteristika:
    - Živé barvy (zelená/oranžová)
    - Čisté linie
    - Moderní typografie
    - Větší akcent na vizuální hierarchii
    """
    
    def get_colors(self) -> dict:
        """Vrací moderní barevné schéma."""
        return {
            'primary': colors.HexColor('#27AE60'),      # Zelená
            'secondary': colors.HexColor('#E67E22'),    # Oranžová
            'accent': colors.HexColor('#ECF0F1'),       # Světle šedá
            'dark': colors.HexColor('#2C3E50'),         # Tmavá
            'text': colors.HexColor('#34495E'),
            'light_text': colors.HexColor('#95A5A6')
        }
    
    def draw_header(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí moderní hlavičku."""
        colors_scheme = self.get_colors()
        y_pos = self.page_height - self.margin
        
        # Barevný pruh nahoře
        self.draw_rect(c, 0, self.page_height - 15 * mm,
                      self.page_width, 15 * mm, fill_color=colors_scheme['primary'])
        
        # FAKTURA text
        c.setFillColor(colors.white)
        c.setFont(self.font_bold, 28)
        c.drawString(self.margin, y_pos - 10 * mm, "FAKTURA")
        
        # Číslo faktury
        c.setFont(self.font_regular, 11)
        c.drawRightString(self.page_width - self.margin, y_pos - 10 * mm,
                         invoice.invoice_number)
        
        y_pos -= 25 * mm
        
        # Datum a splatnost v boxech
        box_width = 45 * mm
        box_height = 18 * mm
        gap = 5 * mm
        
        # Box datum vystavení
        self.draw_rect(c, self.margin, y_pos - box_height, box_width, box_height,
                      fill_color=colors_scheme['accent'])
        
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_regular, 8)
        c.drawString(self.margin + 2 * mm, y_pos - 5 * mm, "DATUM VYSTAVENÍ")
        c.setFont(self.font_bold, 12)
        c.drawString(self.margin + 2 * mm, y_pos - 12 * mm, 
                    self.format_date(invoice.issue_date))
        
        # Box datum splatnosti
        box_x = self.margin + box_width + gap
        self.draw_rect(c, box_x, y_pos - box_height, box_width, box_height,
                      fill_color=colors_scheme['accent'])
        
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_regular, 8)
        c.drawString(box_x + 2 * mm, y_pos - 5 * mm, "DATUM SPLATNOSTI")
        c.setFont(self.font_bold, 12)
        c.setFillColor(colors_scheme['secondary'])
        c.drawString(box_x + 2 * mm, y_pos - 12 * mm, 
                    self.format_date(invoice.due_date))
        
        # Variabilní symbol
        box_x = self.margin + 2 * (box_width + gap)
        self.draw_rect(c, box_x, y_pos - box_height, box_width, box_height,
                      fill_color=colors_scheme['accent'])
        
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_regular, 8)
        c.drawString(box_x + 2 * mm, y_pos - 5 * mm, "VAR. SYMBOL")
        c.setFont(self.font_bold, 12)
        c.drawString(box_x + 2 * mm, y_pos - 12 * mm, invoice.variable_symbol)
        
        y_pos -= box_height + 10 * mm
        
        # Dodavatel a Odběratel vedle sebe
        col_width = (self.page_width - 2 * self.margin - 10 * mm) / 2
        
        # Dodavatel
        self.draw_rect(c, self.margin, y_pos - 35 * mm, col_width, 35 * mm,
                      stroke_color=colors_scheme['primary'], line_width=2)
        
        c.setFillColor(colors_scheme['primary'])
        c.setFont(self.font_bold, 10)
        c.drawString(self.margin + 3 * mm, y_pos - 6 * mm, "DODAVATEL")
        
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_bold, 11)
        c.drawString(self.margin + 3 * mm, y_pos - 12 * mm, invoice.supplier.name)
        
        c.setFont(self.font_regular, 9)
        c.drawString(self.margin + 3 * mm, y_pos - 17 * mm, invoice.supplier.street)
        c.drawString(self.margin + 3 * mm, y_pos - 21 * mm, 
                    f"{invoice.supplier.zip_code} {invoice.supplier.city}")
        c.drawString(self.margin + 3 * mm, y_pos - 26 * mm, 
                    f"IČO: {invoice.supplier.ico}")
        c.drawString(self.margin + 3 * mm, y_pos - 30 * mm, 
                    f"DIČ: {invoice.supplier.dic}")
        
        # Odběratel
        x_right = self.margin + col_width + 10 * mm
        self.draw_rect(c, x_right, y_pos - 35 * mm, col_width, 35 * mm,
                      stroke_color=colors_scheme['secondary'], line_width=2)
        
        c.setFillColor(colors_scheme['secondary'])
        c.setFont(self.font_bold, 10)
        c.drawString(x_right + 3 * mm, y_pos - 6 * mm, "ODBĚRATEL")
        
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_bold, 11)
        c.drawString(x_right + 3 * mm, y_pos - 12 * mm, invoice.customer.name)
        
        c.setFont(self.font_regular, 9)
        c.drawString(x_right + 3 * mm, y_pos - 17 * mm, invoice.customer.street)
        c.drawString(x_right + 3 * mm, y_pos - 21 * mm, 
                    f"{invoice.customer.zip_code} {invoice.customer.city}")
        c.drawString(x_right + 3 * mm, y_pos - 26 * mm, 
                    f"IČO: {invoice.customer.ico}")
        c.drawString(x_right + 3 * mm, y_pos - 30 * mm, 
                    f"DIČ: {invoice.customer.dic}")
        
        self.current_y = y_pos - 40 * mm
    
    def draw_body(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí moderní tabulku položek."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y
        
        # Nadpis sekce
        c.setFillColor(colors_scheme['primary'])
        c.setFont(self.font_bold, 11)
        c.drawString(self.margin, y_pos, "POLOŽKY")
        
        y_pos -= 8 * mm
        
        # Tabulka
        # Pozice sloupců
        col_desc = self.margin + 2 * mm
        col_qty = self.page_width - 105 * mm
        col_unit = self.page_width - 90 * mm
        col_price = self.page_width - 70 * mm
        col_vat = self.page_width - 45 * mm
        
        # Hlavička - barevná
        header_height = 7 * mm
        self.draw_rect(c, self.margin, y_pos - header_height,
                      self.page_width - 2 * self.margin, header_height,
                      fill_color=colors_scheme['dark'])
        
        c.setFillColor(colors.white)
        c.setFont(self.font_bold, 8)
        header_y = y_pos - 4.5 * mm
        c.drawString(col_desc, header_y, "POPIS")
        c.drawString(col_qty, header_y, "MNŽ")
        c.drawString(col_unit, header_y, "J.")
        c.drawString(col_price, header_y, "CENA/J")
        c.drawString(col_vat, header_y, "DPH")
        c.drawRightString(self.page_width - self.margin, header_y, "CELKEM")
        
        y_pos -= header_height + 3 * mm
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_regular, 8)
        
        # Položky se střídavým pozadím
        alternate = True
        for item in invoice.items:
            if y_pos < 50 * mm:
                c.showPage()
                y_pos = self.page_height - self.margin
            
            # Střídavé pozadí
            if alternate:
                self.draw_rect(c, self.margin, y_pos - 5 * mm,
                             self.page_width - 2 * self.margin, 5 * mm,
                             fill_color=colors_scheme['accent'])
            
            c.setFillColor(colors_scheme['text'])
            c.drawString(col_desc, y_pos - 3.5 * mm, item.description[:45])
            c.drawString(col_qty, y_pos - 3.5 * mm, str(item.quantity))
            c.drawString(col_unit, y_pos - 3.5 * mm, item.unit)
            c.drawRightString(col_price + 20 * mm, y_pos - 3.5 * mm, 
                            invoice.format_price(item.unit_price))
            c.drawString(col_vat, y_pos - 3.5 * mm, f"{item.vat_rate}%")
            c.drawRightString(self.page_width - self.margin, y_pos - 3.5 * mm, 
                            invoice.format_price(item.total_price_with_vat))
            
            y_pos -= 5 * mm
            alternate = not alternate
        
        self.current_y = y_pos - 5 * mm
    
    def draw_footer(self, c: canvas.Canvas, invoice: Invoice):
        """Vykreslí moderní footer se součty."""
        colors_scheme = self.get_colors()
        y_pos = self.current_y
        
        # Souhrn na pravé straně
        x_label = self.page_width - 100 * mm
        x_value = self.page_width - self.margin
        
        c.setFont(self.font_regular, 9)
        c.setFillColor(colors_scheme['text'])
        
        vat_summary = invoice.get_vat_summary()
        for vat_rate, amounts in vat_summary.items():
            c.drawString(x_label, y_pos, f"Základ DPH {vat_rate}%:")
            c.drawRightString(x_value, y_pos, invoice.format_price(amounts['base']))
            y_pos -= 4 * mm
            
            c.drawString(x_label, y_pos, f"DPH {vat_rate}%:")
            c.drawRightString(x_value, y_pos, invoice.format_price(amounts['vat']))
            y_pos -= 5 * mm
        
        # Celkem - velký box
        y_pos -= 3 * mm
        box_height = 12 * mm
        self.draw_rect(c, self.page_width - 110 * mm, y_pos - box_height,
                      90 * mm, box_height, fill_color=colors_scheme['primary'])
        
        c.setFillColor(colors.white)
        c.setFont(self.font_bold, 11)
        c.drawString(self.page_width - 105 * mm, y_pos - 7 * mm, "K ÚHRADĚ")
        c.setFont(self.font_bold, 14)
        c.drawRightString(self.page_width - self.margin, y_pos - 7 * mm, 
                         invoice.format_price(invoice.total_with_vat))
        
        # Cestní doložka 
        y_clause = y_pos - 15 * mm
        y_clause = self.draw_assignment_clause(c, invoice, y_clause)
        
        # Bankovní údaje vlevo
        y_bank = y_clause - 5 * mm
        c.setFillColor(colors_scheme['text'])
        c.setFont(self.font_bold, 9)
        c.drawString(self.margin, y_bank, "PLATEBNÍ ÚDAJE")
        
        y_bank -= 5 * mm
        c.setFont(self.font_regular, 8)
        c.drawString(self.margin, y_bank, f"Účet: {invoice.supplier.iban}")
        y_bank -= 3.5 * mm
        c.drawString(self.margin, y_bank, f"Banka: {invoice.supplier.bank_name}")
        y_bank -= 3.5 * mm
        c.drawString(self.margin, y_bank, f"VS: {invoice.variable_symbol}")
        
        # Poznámka
        if invoice.note:
            y_bank -= 6 * mm
            c.setFont(self.font_regular, 8)
            c.drawString(self.margin, y_bank, invoice.note)
        
        # Patička
        c.setFont(self.font_regular, 7)
        c.setFillColor(colors_scheme['light_text'])
        c.drawCentredString(self.page_width / 2, 25 * mm,
                           "Faktura vystavena elektronicky a je platná bez podpisu.")

