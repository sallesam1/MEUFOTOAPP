import os
tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# ===== LOGIN standalone dark premium =====
login = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login — MeuFotoApp</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif}
.login-bg{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%)}
.login-card{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:40px;width:380px;box-shadow:0 20px 50px rgba(0,0,0,0.6)}
.login-card h1{color:#fff;font-size:26px;font-weight:700;text-align:center;margin-bottom:4px}
.login-card .sub{color:#8b949e;font-size:13px;text-align:center;margin-bottom:28px}
.login-card label{color:#8b949e;font-size:12px;display:block;margin-bottom:6px}
.login-card input{width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;margin-bottom:14px}
.login-card input:focus{border-color:#4a90d9}
.login-card .btn{width:100%;padding:12px;background:#4a90d9;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-bottom:16px}
.login-card .btn-google{display:block;text-align:center;padding:12px;background:#0d1117;border:1px solid #30363d;border-radius:8px;text-decoration:none;color:#fff;font-size:14px}
.login-card .divider{text-align:center;margin:16px 0;position:relative}
.login-card .divider hr{border:none;border-top:1px solid #30363d}
.login-card .divider span{position:absolute;top:-8px;left:50%;transform:translateX(-50%);background:#161b22;color:#8b949e;font-size:11px;padding:0 12px}
.login-card .footer{text-align:center;margin-top:20px;font-size:13px;color:#8b949e}
.login-card .footer a{color:#4a90d9;text-decoration:none}
</style>
</head>
<body>
<div class="login-bg">
<div class="login-card">
<h1>MeuFotoApp</h1>
<p class="sub">Acesse sua conta</p>
<form method="POST">
<label>E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required>
<label>SENHA</label>
<input type="password" name="password" placeholder="********" required>
<button type="submit" class="btn">ENTRAR</button>
</form>
<div class="divider"><hr><span>OU</span></div>
<a href="/login-google" class="btn-google">Entrar com Google</a>
<p class="footer">Nao tem conta? <a href="/registro">Criar agora</a></p>
</div>
</div>
</body>
</html>"""

with open(os.path.join(tpl, 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login.strip() + '\n')
print('OK: login.html (standalone dark)')

# ===== REGISTRO standalone dark premium =====
registro = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Criar conta — MeuFotoApp</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,sans-serif}
.login-bg{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);padding:20px}
.login-card{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:40px;width:380px;box-shadow:0 20px 50px rgba(0,0,0,0.6)}
.login-card h1{color:#fff;font-size:26px;font-weight:700;text-align:center;margin-bottom:4px}
.login-card .sub{color:#8b949e;font-size:13px;text-align:center;margin-bottom:28px}
.login-card label{color:#8b949e;font-size:12px;display:block;margin-bottom:6px}
.login-card input{width:100%;padding:12px 14px;background:#0d1117;border:1px solid #30363d;border-radius:8px;color:#fff;font-size:14px;outline:none;margin-bottom:14px}
.login-card input:focus{border-color:#4a90d9}
.login-card .btn{width:100%;padding:12px;background:#4a90d9;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}
.login-card .footer{text-align:center;margin-top:20px;font-size:13px;color:#8b949e}
.login-card .footer a{color:#4a90d9;text-decoration:none}
</style>
</head>
<body>
<div class="login-bg">
<div class="login-card">
<h1>Criar Conta</h1>
<p class="sub">Comece agora</p>
<form method="POST">
<label>NOME DO ESTUDIO</label>
<input type="text" name="studio_name" placeholder="Seu estudio">
<label>SEU NOME</label>
<input type="text" name="name" placeholder="Como te chamam">
<label>E-MAIL</label>
<input type="email" name="email" placeholder="seu@email.com" required>
<label>SENHA</label>
<input type="password" name="password" placeholder="********" required>
<button type="submit" class="btn">CRIAR CONTA</button>
</form>
<p class="footer">Ja tem conta? <a href="/login">Entrar</a></p>
</div>
</div>
</body>
</html>"""

with open(os.path.join(tpl, 'registro.html'), 'w', encoding='utf-8') as f:
    f.write(registro.strip() + '\n')
print('OK: registro.html (standalone dark)')

print('\n=== LOGIN DARK STANDALONE! ===')