from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT,
            event         TEXT    NOT NULL,
            registered_at TEXT    NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ── Registration form page ─────────────────────────────────────────────────────
@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Event Registration</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg:       #0a0a0f;
      --surface:  #12121a;
      --border:   #1e1e2e;
      --border2:  #2a2a3e;
      --accent:   #6c63ff;
      --accent2:  #a78bfa;
      --success:  #10b981;
      --error:    #f43f5e;
      --text:     #e2e8f0;
      --muted:    #64748b;
      --mono:     'JetBrains Mono', monospace;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Outfit', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
      overflow-x: hidden;
      position: relative;
    }

    /* Particle canvas */
    #canvas {
      position: fixed;
      inset: 0;
      z-index: 0;
      pointer-events: none;
    }

    /* Glowing orbs in background */
    .orb {
      position: fixed;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.12;
      pointer-events: none;
      z-index: 0;
      animation: drift 12s ease-in-out infinite alternate;
    }
    .orb1 { width: 400px; height: 400px; background: var(--accent); top: -100px; left: -100px; animation-delay: 0s; }
    .orb2 { width: 300px; height: 300px; background: #ec4899; bottom: -80px; right: -80px; animation-delay: -4s; }
    .orb3 { width: 250px; height: 250px; background: var(--success); top: 50%; left: 60%; animation-delay: -8s; }

    @keyframes drift {
      from { transform: translate(0, 0) scale(1); }
      to   { transform: translate(30px, 20px) scale(1.08); }
    }

    /* Main card */
    .card {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 460px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 2.5rem;
      backdrop-filter: blur(20px);
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
      box-shadow: 0 0 0 1px rgba(108,99,255,0.08), 0 40px 80px rgba(0,0,0,0.6);
    }

    @keyframes slideUp {
      from { opacity: 0; transform: translateY(30px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* Header */
    .header {
      margin-bottom: 2rem;
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
    }

    .tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent2);
      background: rgba(108,99,255,0.12);
      border: 1px solid rgba(108,99,255,0.2);
      border-radius: 20px;
      padding: 4px 12px;
      margin-bottom: 1rem;
    }

    .tag::before {
      content: '';
      width: 5px; height: 5px;
      border-radius: 50%;
      background: var(--accent2);
      animation: blink 2s ease-in-out infinite;
    }

    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    h1 {
      font-size: 28px;
      font-weight: 700;
      line-height: 1.2;
      background: linear-gradient(135deg, #fff 0%, var(--accent2) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .subtitle {
      font-size: 14px;
      color: var(--muted);
      margin-top: 6px;
    }

    /* Fields */
    .field {
      margin-bottom: 1.1rem;
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    .field:nth-child(1) { animation-delay: 0.15s; }
    .field:nth-child(2) { animation-delay: 0.2s;  }
    .field:nth-child(3) { animation-delay: 0.25s; }

    label {
      display: block;
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 8px;
      transition: color 0.2s;
    }

    .field:focus-within label { color: var(--accent2); }

    .input-wrap {
      position: relative;
    }

    input {
      width: 100%;
      padding: 12px 16px;
      font-size: 15px;
      font-family: 'Outfit', sans-serif;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border2);
      border-radius: 10px;
      color: var(--text);
      outline: none;
      transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
    }

    input::placeholder { color: #334155; }

    input:focus {
      border-color: var(--accent);
      background: rgba(108,99,255,0.06);
      box-shadow: 0 0 0 3px rgba(108,99,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    /* Animated underline on focus */
    .input-line {
      position: absolute;
      bottom: 0; left: 50%;
      width: 0; height: 2px;
      background: linear-gradient(90deg, var(--accent), var(--accent2));
      border-radius: 2px;
      transform: translateX(-50%);
      transition: width 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }

    input:focus + .input-line { width: calc(100% - 4px); }

    /* Message */
    .msg {
      display: none;
      font-size: 13px;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 1rem;
      border: 1px solid transparent;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn { from{opacity:0;transform:translateY(-4px)} to{opacity:1;transform:none} }

    .msg.success {
      background: rgba(16,185,129,0.1);
      border-color: rgba(16,185,129,0.3);
      color: #34d399;
    }
    .msg.error {
      background: rgba(244,63,94,0.1);
      border-color: rgba(244,63,94,0.3);
      color: #fb7185;
    }

    /* Buttons */
    .btn-register {
      width: 100%;
      padding: 13px;
      font-size: 15px;
      font-weight: 600;
      font-family: 'Outfit', sans-serif;
      background: linear-gradient(135deg, var(--accent) 0%, #8b5cf6 100%);
      color: #fff;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: transform 0.15s, box-shadow 0.2s, opacity 0.2s;
      margin-top: 0.5rem;
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
    }

    .btn-register::before {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
      opacity: 0;
      transition: opacity 0.2s;
    }

    .btn-register:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(108,99,255,0.4); }
    .btn-register:hover::before { opacity: 1; }
    .btn-register:active { transform: scale(0.98); }
    .btn-register:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }

    /* Ripple effect */
    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(255,255,255,0.25);
      transform: scale(0);
      animation: ripple 0.5s linear;
      pointer-events: none;
    }
    @keyframes ripple { to { transform: scale(4); opacity: 0; } }

    .divider {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 1.25rem 0;
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both;
    }
    .divider::before, .divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }
    .divider span {
      font-size: 11px;
      color: var(--muted);
      font-family: var(--mono);
    }

    .btn-view {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 12px;
      font-size: 14px;
      font-weight: 500;
      font-family: 'Outfit', sans-serif;
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border2);
      border-radius: 10px;
      cursor: pointer;
      text-decoration: none;
      transition: border-color 0.2s, background 0.2s, color 0.2s;
      animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.4s both;
    }

    .btn-view:hover {
      border-color: var(--accent);
      background: rgba(108,99,255,0.08);
      color: var(--accent2);
    }

    .btn-view svg { transition: transform 0.2s; }
    .btn-view:hover svg { transform: translateX(3px); }
  </style>
</head>
<body>

<canvas id="canvas"></canvas>
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>

<div class="card">
  <div class="header">
    <div class="tag">Registration Open</div>
    <h1>Join the Event</h1>
    <p class="subtitle">Fill in your details to secure your spot.</p>
  </div>

  <div class="field">
    <label for="name">Full Name</label>
    <div class="input-wrap">
      <input type="text" id="name" placeholder="Priya Sharma" autocomplete="off"/>
      <div class="input-line"></div>
    </div>
  </div>

  <div class="field">
    <label for="email">Email Address</label>
    <div class="input-wrap">
      <input type="email" id="email" placeholder="priya@example.com" autocomplete="off"/>
      <div class="input-line"></div>
    </div>
  </div>

  <div class="field">
    <label for="event">Event Name</label>
    <div class="input-wrap">
      <input type="text" id="event" placeholder="Cloud Computing Workshop" autocomplete="off"/>
      <div class="input-line"></div>
    </div>
  </div>

  <div id="msg" class="msg"></div>

  <button class="btn-register" id="submitBtn">Register Now</button>

  <div class="divider"><span>or</span></div>

  <a href="/registrations" class="btn-view">
    View All Registrations
    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
      <path d="M5 12h14M12 5l7 7-7 7"/>
    </svg>
  </a>
</div>

<script>
  /* ── Particle canvas ── */
  const canvas = document.getElementById('canvas');
  const ctx    = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      r: Math.random() * 1.5 + 0.3,
      dx: (Math.random() - 0.5) * 0.3,
      dy: (Math.random() - 0.5) * 0.3,
      o: Math.random() * 0.4 + 0.1
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(108,99,255,${p.o})`;
      ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if (p.x < 0 || p.x > W) p.dx *= -1;
      if (p.y < 0 || p.y > H) p.dy *= -1;
    });
    requestAnimationFrame(drawParticles);
  }
  drawParticles();

  /* ── Ripple on button ── */
  document.getElementById('submitBtn').addEventListener('click', function(e) {
    const btn  = this;
    const rect = btn.getBoundingClientRect();
    const r    = document.createElement('span');
    r.className = 'ripple';
    r.style.cssText = `width:${btn.offsetWidth}px;height:${btn.offsetWidth}px;left:${e.clientX - rect.left - btn.offsetWidth/2}px;top:${e.clientY - rect.top - btn.offsetWidth/2}px`;
    btn.appendChild(r);
    setTimeout(() => r.remove(), 600);
    handleRegister();
  });

  /* ── Register ── */
  function showMsg(text, type) {
    const el = document.getElementById('msg');
    el.textContent = text;
    el.className   = 'msg ' + type;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 5000);
  }

  async function handleRegister() {
    const name  = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const event = document.getElementById('event').value.trim();
    const btn   = document.getElementById('submitBtn');

    if (!name || !event) { showMsg('Name and Event are required.', 'error'); return; }

    btn.disabled    = true;
    btn.textContent = 'Registering...';

    try {
      const res  = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, event })
      });
      const data = await res.json();
      if (res.ok) {
        showMsg(data.message, 'success');
        document.getElementById('name').value  = '';
        document.getElementById('email').value = '';
        document.getElementById('event').value = '';
      } else {
        showMsg(data.error || 'Something went wrong.', 'error');
      }
    } catch(e) {
      showMsg('Cannot reach backend.', 'error');
    }

    btn.disabled    = false;
    btn.textContent = 'Register Now';
  }
</script>
</body>
</html>'''


# ── Registrations table page ───────────────────────────────────────────────────
@app.route('/registrations')
def registrations():
    conn   = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, event, registered_at FROM registrations ORDER BY id DESC")
    rows   = cursor.fetchall()
    conn.close()

    rows_html = ""
    for i, row in enumerate(rows):
        email_cell = row[2] if row[2] else "—"
        initials   = ''.join(w[0].upper() for w in row[1].split()[:2])
        delay      = i * 0.04
        rows_html += f"""
        <tr style="animation-delay:{delay}s">
          <td><span class="id-pill">#{row[0]}</span></td>
          <td>
            <div class="name-cell">
              <div class="avatar">{initials}</div>
              <span>{row[1]}</span>
            </div>
          </td>
          <td class="muted">{email_cell}</td>
          <td><span class="event-pill">{row[3]}</span></td>
          <td class="mono muted">{row[4]}</td>
        </tr>"""

    if not rows:
        rows_html = '<tr><td colspan="5" class="empty">No registrations yet.</td></tr>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Registrations</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    :root {{
      --bg:      #0a0a0f;
      --surface: #12121a;
      --border:  #1e1e2e;
      --border2: #2a2a3e;
      --accent:  #6c63ff;
      --accent2: #a78bfa;
      --text:    #e2e8f0;
      --muted:   #64748b;
      --mono:    'JetBrains Mono', monospace;
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Outfit', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 2.5rem 1.5rem 4rem;
    }}

    .orb {{
      position: fixed; border-radius: 50%; filter: blur(80px); opacity: 0.08;
      pointer-events: none; z-index: 0;
    }}
    .orb1 {{ width:500px;height:500px;background:var(--accent);top:-150px;left:-150px; }}
    .orb2 {{ width:350px;height:350px;background:#ec4899;bottom:-100px;right:-100px; }}

    .container {{
      position: relative;
      z-index: 1;
      max-width: 900px;
      margin: 0 auto;
      animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
    }}

    @keyframes slideUp {{
      from {{ opacity:0; transform:translateY(20px); }}
      to   {{ opacity:1; transform:none; }}
    }}

    .topbar {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }}

    h1 {{
      font-size: 26px;
      font-weight: 700;
      background: linear-gradient(135deg, #fff 0%, var(--accent2) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}

    .count-badge {{
      display: inline-block;
      font-family: var(--mono);
      font-size: 11px;
      background: rgba(108,99,255,0.15);
      color: var(--accent2);
      border: 1px solid rgba(108,99,255,0.25);
      border-radius: 20px;
      padding: 3px 12px;
      margin-top: 6px;
    }}

    .back {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 500;
      color: var(--muted);
      text-decoration: none;
      border: 1px solid var(--border2);
      padding: 8px 16px;
      border-radius: 8px;
      background: var(--surface);
      transition: border-color 0.2s, color 0.2s;
    }}
    .back:hover {{ border-color: var(--accent); color: var(--accent2); }}

    .table-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}

    table {{ width: 100%; border-collapse: collapse; }}

    thead tr {{
      background: rgba(255,255,255,0.02);
      border-bottom: 1px solid var(--border);
    }}

    thead th {{
      text-align: left;
      padding: 14px 20px;
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    tbody tr {{
      border-bottom: 1px solid rgba(255,255,255,0.04);
      transition: background 0.15s;
      animation: rowIn 0.4s cubic-bezier(0.16,1,0.3,1) both;
    }}

    @keyframes rowIn {{
      from {{ opacity:0; transform:translateX(-8px); }}
      to   {{ opacity:1; transform:none; }}
    }}

    tbody tr:last-child {{ border-bottom: none; }}
    tbody tr:hover       {{ background: rgba(108,99,255,0.06); }}

    tbody td {{
      padding: 14px 20px;
      font-size: 14px;
      vertical-align: middle;
    }}

    .id-pill {{
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border2);
      border-radius: 6px;
      padding: 2px 8px;
    }}

    .name-cell {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .avatar {{
      width: 32px; height: 32px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--accent), #8b5cf6);
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; font-weight: 600; color: #fff;
      flex-shrink: 0;
    }}

    .event-pill {{
      display: inline-block;
      font-size: 12px;
      background: rgba(108,99,255,0.12);
      color: var(--accent2);
      border: 1px solid rgba(108,99,255,0.2);
      border-radius: 20px;
      padding: 3px 12px;
    }}

    .muted {{ color: var(--muted); }}
    .mono  {{ font-family: var(--mono); font-size: 12px; }}

    .empty {{
      text-align: center;
      padding: 3rem;
      color: var(--muted);
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>

  <div class="container">
    <div class="topbar">
      <div>
        <h1>Registrations</h1>
        <div class="count-badge">{len(rows)} total entries</div>
      </div>
      <a href="/" class="back">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Back to form
      </a>
    </div>

    <div class="table-card">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Event</th>
            <th>Registered At</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>'''


# ── API routes ─────────────────────────────────────────────────────────────────
@app.route('/register', methods=['POST'])
def register():
    data  = request.json
    name  = data.get('name', '').strip()
    event = data.get('event', '').strip()
    email = data.get('email', '').strip()

    if not name or not event:
        return jsonify({"error": "Name and Event are required."}), 400

    registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn   = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO registrations (name, email, event, registered_at) VALUES (?, ?, ?, ?)",
        (name, email, event, registered_at)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"You're in! Welcome, {name}."})


@app.route('/data', methods=['GET'])
def get_data():
    conn   = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, event, registered_at FROM registrations ORDER BY id DESC")
    rows   = cursor.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "name": r[1], "email": r[2], "event": r[3], "registered_at": r[4]}
        for r in rows
    ])


if __name__ == '__main__':
    app.run(debug=True)
