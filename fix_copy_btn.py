import os

# Procurar o template do admin
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Tentar admin.html primeiro
admin_path = os.path.join(templates_dir, 'admin.html')

with open(admin_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Adicionar botao Copiar Prompt antes do botao Salvar Prompt
if 'copiarPrompt' not in code:
    # Adicionar botao apos cada area de prompt
    old_btn = '<button type="submit">Salvar Prompt</button>'
    new_btn = '<button type="button" onclick="copiarPrompt(this)" style="background:#10b981;color:#fff;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-weight:600;margin-right:8px;">📋 Copiar Prompt</button>\n                <button type="submit">Salvar Prompt</button>'
    code = code.replace(old_btn, new_btn)
    print('OK: botao Copiar Prompt adicionado')
else:
    print('SKIP: botao Copiar Prompt ja existe')

# 2. Adicionar funcao JavaScript copiarPrompt
if 'function copiarPrompt' not in code:
    js = """
<script>
function copiarPrompt(btn) {
    var form = btn.closest('form');
    var textarea = form.querySelector('textarea[name="prompt"]');
    if (!textarea) {
        textarea = form.querySelector('textarea');
    }
    if (textarea) {
        textarea.select();
        document.execCommand('copy');
        var original = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        btn.style.background = '#059669';
        setTimeout(function() {
            btn.innerHTML = original;
            btn.style.background = '#10b981';
        }, 2000);
    }
}
</script>
"""
    code = code + '\n' + js
    print('OK: JavaScript copiarPrompt adicionado')

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('PRONTO! Rode: python app.py')