import os

base = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(base, 'static', 'css', 'style.css')

fix = """
/* FIX BOTOES - APPEND */
.btn-primary, .btn-danger, .btn-secondary {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    border: 1px solid transparent !important;
    transition: 0.2s !important;
    gap: 8px !important;
    width: auto !important;
    text-decoration: none !important;
}
"""

with open(css_path, 'a', encoding='utf-8') as f:
    f.write(fix)

print("Fix adicionado no final do style.css!")