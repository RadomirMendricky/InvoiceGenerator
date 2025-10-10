"""Základní třída pro PDF šablony."""

from abc import ABC, abstractmethod
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

from models.invoice import Invoice


class BaseTemplate(ABC):
    """
    Abstraktní základní třída pro všechny PDF šablony.
    
    Definuje společné metody a rozhraní pro generování PDF faktur.
    """
    
    def __init__(self):
        """Inicializace šablony."""
        self.page_width, self.page_height = A4
        self.margin = 20 * mm
        self.current_y = self.page_height - self.margin
        
        # Registrace fontu s podporou diakritiky
        self._register_fonts()
    
    def _register_fonts(self):
        """Registruje fonty s podporou české diakritiky."""
        import os
        import sys
        
        # Určení cesty k fontům
        # Pokud je spuštěno z src/, použij fonts/
        # Pokud z root, použij src/fonts/
        possible_paths = [
            'fonts/DejaVuSans.ttf',  # Spuštěno z src/
            'src/fonts/DejaVuSans.ttf',  # Spuštěno z root
            os.path.join(os.path.dirname(__file__), '..', 'fonts', 'DejaVuSans.ttf'),  # Relativní k tomuto souboru
        ]
        
        font_path_regular = None
        font_path_bold = None
        
        # Najdi existující cestu
        for path in possible_paths:
            if os.path.exists(path):
                font_path_regular = path
                font_path_bold = path.replace('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf')
                break
        
        if font_path_regular and os.path.exists(font_path_regular):
            try:
                # Registrace DejaVu Sans s českou diakritikou
                pdfmetrics.registerFont(TTFont('DejaVuSans', font_path_regular))
                if os.path.exists(font_path_bold):
                    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))
                
                self.font_regular = 'DejaVuSans'
                self.font_bold = 'DejaVuSans-Bold'
                print(f"[OK] Font DejaVu Sans úspěšně zaregistrován: {font_path_regular}")
            except Exception as e:
                print(f"[WARN] Chyba při registraci fontu: {e}")
                print("[WARN] Používám výchozí font Helvetica (bez české diakritiky)")
                self.font_regular = 'Helvetica'
                self.font_bold = 'Helvetica-Bold'
        else:
            print("[WARN] DejaVu Sans font nebyl nalezen!")
            print("[WARN] Hledáno v:")
            for path in possible_paths:
                print(f"        - {path}")
            print("[WARN] Používám výchozí font Helvetica (bez české diakritiky)")
            self.font_regular = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'
    
    @abstractmethod
    def get_colors(self) -> dict:
        """
        Vrací barevné schéma šablony.
        
        Returns:
            Slovník s barvami pro různé prvky
        """
        pass
    
    @abstractmethod
    def draw_header(self, c: canvas.Canvas, invoice: Invoice):
        """
        Vykreslí hlavičku faktury.
        
        Args:
            c: Canvas objekt
            invoice: Instance faktury
        """
        pass
    
    @abstractmethod
    def draw_body(self, c: canvas.Canvas, invoice: Invoice):
        """
        Vykreslí tělo faktury (položky).
        
        Args:
            c: Canvas objekt
            invoice: Instance faktury
        """
        pass
    
    @abstractmethod
    def draw_footer(self, c: canvas.Canvas, invoice: Invoice):
        """
        Vykreslí patičku faktury (součty, poznámky).
        
        Args:
            c: Canvas objekt
            invoice: Instance faktury
        """
        pass
    
    def generate(self, invoice: Invoice, output_path: str):
        """
        Hlavní metoda pro generování PDF.
        
        Args:
            invoice: Instance faktury
            output_path: Cesta k výstupnímu souboru
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Metadata PDF
        c.setAuthor(invoice.supplier.name)
        c.setTitle(f"Faktura {invoice.invoice_number}")
        c.setSubject("Faktura - daňový doklad")
        
        # Vykreslení sekcí
        self.draw_header(c, invoice)
        self.draw_body(c, invoice)
        self.draw_footer(c, invoice)
        
        c.showPage()
        c.save()
    
    def format_price(self, amount: int) -> str:
        """
        Formátuje částku v Kč.
        
        Args:
            amount: Částka v celých korunách
            
        Returns:
            Formátovaný řetězec
        """
        return f"{amount:,} Kč".replace(",", " ")
    
    def format_date(self, date_obj) -> str:
        """
        Formátuje datum do českého formátu.
        
        Args:
            date_obj: Objekt datetime.date
            
        Returns:
            Formátované datum (DD.MM.YYYY)
        """
        return date_obj.strftime("%d.%m.%Y")
    
    def draw_text(self, c: canvas.Canvas, x: float, y: float, text: str, 
                  font: str = None, size: int = 10, color=colors.black):
        """
        Pomocná metoda pro vykreslení textu.
        
        Args:
            c: Canvas objekt
            x, y: Souřadnice
            text: Text k vykreslení
            font: Název fontu
            size: Velikost písma
            color: Barva textu
        """
        if font is None:
            font = self.font_regular
        
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(x, y, str(text))
    
    def draw_line(self, c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float,
                  width: float = 1, color=colors.black):
        """
        Pomocná metoda pro vykreslení čáry.
        
        Args:
            c: Canvas objekt
            x1, y1: Počáteční souřadnice
            x2, y2: Koncové souřadnice
            width: Šířka čáry
            color: Barva čáry
        """
        c.setStrokeColor(color)
        c.setLineWidth(width)
        c.line(x1, y1, x2, y2)
    
    def draw_rect(self, c: canvas.Canvas, x: float, y: float, width: float, height: float,
                  fill_color=None, stroke_color=None, line_width: float = 1):
        """
        Pomocná metoda pro vykreslení obdélníku.
        
        Args:
            c: Canvas objekt
            x, y: Souřadnice levého dolního rohu
            width, height: Rozměry
            fill_color: Barva výplně (None = bez výplně)
            stroke_color: Barva obrysu (None = bez obrysu)
            line_width: Šířka obrysu
        """
        if fill_color:
            c.setFillColor(fill_color)
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(line_width)
        
        if fill_color and stroke_color:
            c.rect(x, y, width, height, fill=1, stroke=1)
        elif fill_color:
            c.rect(x, y, width, height, fill=1, stroke=0)
        elif stroke_color:
            c.rect(x, y, width, height, fill=0, stroke=1)

