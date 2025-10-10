"""PDF šablony pro generování faktur."""

from .classic import ClassicTemplate
from .modern import ModernTemplate
from .minimal import MinimalTemplate

__all__ = ['ClassicTemplate', 'ModernTemplate', 'MinimalTemplate']


def get_template(template_name: str):
    """
    Vrací třídu šablony podle názvu.
    
    Args:
        template_name: Název šablony (classic, modern, minimal)
        
    Returns:
        Třída šablony
        
    Raises:
        ValueError: Pokud šablona neexistuje
    """
    templates = {
        'classic': ClassicTemplate,
        'modern': ModernTemplate,
        'minimal': MinimalTemplate
    }
    
    if template_name not in templates:
        raise ValueError(f"Neznámá šablona: {template_name}. Dostupné: {', '.join(templates.keys())}")
    
    return templates[template_name]

