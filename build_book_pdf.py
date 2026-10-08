import re
import os
import sys
import html
import subprocess

def create_koor_bell_svg():
    return '''
    <svg class="koor-bell-svg" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="bellGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#0284c7" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="bellGold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fde047"/>
          <stop offset="40%" stop-color="#eab308"/>
          <stop offset="70%" stop-color="#ca8a04"/>
          <stop offset="100%" stop-color="#854d0e"/>
        </linearGradient>
        <linearGradient id="starBlue" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="50%" stop-color="#7dd3fc"/>
          <stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>
      </defs>
      <circle cx="100" cy="100" r="90" fill="url(#bellGlow)"/>
      <circle cx="100" cy="100" r="88" stroke="#38bdf8" stroke-opacity="0.25" stroke-width="1.5" stroke-dasharray="4 4"/>
      
      <!-- Hanging Cord / Loop -->
      <path d="M 90 28 C 90 14, 110 14, 110 28 L 110 42 L 90 42 Z" fill="url(#bellGold)" stroke="#ca8a04" stroke-width="1.5"/>
      <ellipse cx="100" cy="22" rx="5" ry="7" fill="#070b14" stroke="url(#bellGold)" stroke-width="2"/>
      
      <!-- The Traditional Somali Wooden Camel Bell (Koor) -->
      <path d="M 68 46 C 78 44, 122 44, 132 46 C 144 48, 156 128, 148 144 C 142 154, 58 154, 52 144 C 44 128, 56 48, 68 46 Z" 
            fill="url(#bellGold)" stroke="#78350f" stroke-width="2.5"/>
      
      <!-- Traditional Carved Patterns -->
      <path d="M 62 82 Q 100 90 138 82" stroke="#78350f" stroke-width="2.5" fill="none"/>
      <path d="M 58 112 Q 100 120 142 112" stroke="#78350f" stroke-width="2.5" fill="none"/>
      
      <circle cx="80" cy="98" r="3" fill="#78350f"/>
      <circle cx="100" cy="101" r="3.5" fill="#78350f"/>
      <circle cx="120" cy="98" r="3" fill="#78350f"/>

      <!-- Clappers -->
      <rect x="82" y="140" width="8" height="28" rx="4" fill="url(#bellGold)" stroke="#78350f" stroke-width="1.5"/>
      <rect x="110" y="140" width="8" height="28" rx="4" fill="url(#bellGold)" stroke="#78350f" stroke-width="1.5"/>
      <circle cx="86" cy="168" r="5" fill="#ca8a04" stroke="#78350f" stroke-width="1.5"/>
      <circle cx="114" cy="168" r="5" fill="#ca8a04" stroke="#78350f" stroke-width="1.5"/>

      <!-- Somali Five-Pointed Star -->
      <polygon points="100,56 104,68 116,68 106,75 110,87 100,80 90,87 94,75 84,68 96,68" 
               fill="url(#starBlue)"/>

      <!-- Soundwave Waves -->
      <path d="M 40 85 A 70 70 0 0 0 34 115" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
      <path d="M 28 75 A 90 90 0 0 0 20 125" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
      <path d="M 160 85 A 70 70 0 0 1 166 115" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
      <path d="M 172 75 A 90 90 0 0 1 180 125" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>
    </svg>
    '''

def highlight_koor(code_text):
    lines = code_text.split('\n')
    out_lines = []

    action_phrases = [
        r"waxaad soo saartaa",
        r"waxaad soo celisaa",
        r"waxaad ku dhufataa",
        r"waxaad u qaybisaa",
        r"waxaad ku dartaa",
        r"waxaad ka jartaa",
        r"kaydi natiijada",
        r"magaceed waa",
        r"tibxuhu waa",
        r"hawshu waa",
        r"qabo hawshan",
        r"haddii kale oo ay",
        r"haddii kale oo uu",
        r"hadii kale oo ay",
        r"hadii kale oo uu",
        r"haddii kale",
        r"hadii kale",
        r"mid kasta oo",
        r"mid kastoo",
        r"mid kasta",
        r"ku celi",
        r"ku jira",
        r"ka bax",
        r"ka bood",
        r"inuu yahay",
        r"qeex",
        r"ku dhufo",
        r"u qaybi",
        r"ku dar",
        r"ka jar",
        r"haraaga",
    ]

    comp_phrases = [
        r"ay la mid tahay",
        r"uu la mid yahay",
        r"aysan la mid ahayn",
        r"uusan la mid ahayn",
        r"ka weyn tahay ama la mid tahay",
        r"ka weyn yahay ama la mid yahay",
        r"ka yar tahay ama la mid tahay",
        r"ka yar yahay ama la mid yahay",
        r"uu ka weyn yahay",
        r"ay ka weyn tahay",
        r"uu ka yar yahay",
        r"ay ka yar tahay",
    ]

    keywords = [
        r"\bwaa\b",
        r"\bhaddii\b",
        r"\bhadii\b",
        r"\bkale\b",
        r"\binta\b",
        r"\bjeer\b",
        r"\bkasta\b",
        r"\bmid\b",
        r"\bkastoo\b",
        r"\bhawl\b",
        r"\bmagaceed\b",
        r"\btibxuhu\b",
        r"\bhawshu\b",
        r"\bkaydi\b",
        r"\bnatiijada\b",
        r"\bceli\b",
        r"\bdaabac\b",
        r"\bqor\b",
        r"\bsoo saar\b",
        r"\bwaydiin\b",
        r"\bweydii\b",
    ]

    types = [
        r"\btiro\b",
        r"\bqoraal\b",
        r"\brun_been\b",
        r"\bliiska\b",
        r"\bliis\b",
        r"\bqaamuus\b",
        r"\bnooc\b",
        r"\bdherer\b",
        r"\bnasiib\b",
    ]

    literals = [
        r"\brun\b",
        r"\bbeen\b",
        r"\bwaxba\b",
    ]

    logics = [
        r"\bsidoo kale\b",
        r"\bsidoo_kale\b",
        r"\biyo\b",
        r"\bama\b",
        r"\bma aha\b",
        r"\bma\b",
    ]

    for line in lines:
        comment_part = ""
        code_part = line
        if '#' in line:
            parts = line.split('#', 1)
            q_count = parts[0].count('"') + parts[0].count("'")
            if q_count % 2 == 0:
                code_part = parts[0]
                comment_part = '#' + parts[1]

        str_tokens = []
        def str_repl(m):
            idx = len(str_tokens)
            s = html.escape(m.group(0))
            s = re.sub(r'(\{)([a-zA-Z_\'][a-zA-Z0-9_\']*)(\})', r'<span class="syn-interp">{\2}</span>', s)
            str_tokens.append(f'<span class="syn-string">{s}</span>')
            return f"__STR_{idx}__"

        code_part_sub = re.sub(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')', str_repl, code_part)
        code_part_sub = html.escape(code_part_sub)

        for phrase in action_phrases:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            code_part_sub = pattern.sub(r'<span class="syn-action">\g<0></span>', code_part_sub)

        for phrase in comp_phrases:
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            code_part_sub = pattern.sub(r'<span class="syn-comp">\g<0></span>', code_part_sub)

        for kw in keywords:
            code_part_sub = re.sub(kw, lambda m: f'<span class="syn-keyword">{m.group(0)}</span>', code_part_sub)

        for tp in types:
            code_part_sub = re.sub(tp, lambda m: f'<span class="syn-type">{m.group(0)}</span>', code_part_sub)

        for lit in literals:
            code_part_sub = re.sub(lit, lambda m: f'<span class="syn-bool">{m.group(0)}</span>', code_part_sub)

        for lg in logics:
            code_part_sub = re.sub(lg, lambda m: f'<span class="syn-logic">{m.group(0)}</span>', code_part_sub)

        code_part_sub = re.sub(r'\b(\d+(?:\.\d+)?)\b', r'<span class="syn-num">\1</span>', code_part_sub)

        for idx, s_html in enumerate(str_tokens):
            code_part_sub = code_part_sub.replace(f"__STR_{idx}__", s_html)

        if comment_part:
            c_html = html.escape(comment_part)
            final_line = code_part_sub + f'<span class="syn-comment">{c_html}</span>'
        else:
            final_line = code_part_sub

        out_lines.append(final_line)

    return '\n'.join(out_lines)

def highlight_powershell(code_text):
    escaped = html.escape(code_text)
    out = []
    for line in escaped.split('\n'):
        line = re.sub(r'(\.\\koor\.bat|\bkoor\b|\bpython\b)', r'<span class="syn-cmd">\1</span>', line)
        line = re.sub(r'\b(run|check|repl)\b', r'<span class="syn-subcmd">\1</span>', line)
        out.append(line)
    return '\n'.join(out)

def highlight_text(code_text):
    escaped = html.escape(code_text)
    out = []
    for line in escaped.split('\n'):
        out.append(line)
    return '\n'.join(out)

def format_inline(text):
    code_tokens = []
    def code_repl(m):
        idx = len(code_tokens)
        code_tokens.append(f'<code class="inline-code">{html.escape(m.group(1))}</code>')
        return f"__INLINE_CODE_{idx}__"
    
    text = re.sub(r'`([^`]+)`', code_repl, text)
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="book-link">\1</a>', text)

    for idx, c_html in enumerate(code_tokens):
        text = text.replace(f"__INLINE_CODE_{idx}__", c_html)

    return text

def parse_markdown_to_html(md_content):
    lines = md_content.split('\n')
    i = 0
    n = len(lines)
    
    output = []
    
    # 1. COVER PAGE (With only the 6 core pillars)
    output.append(f'''
    <div class="page cover-page">
      <div class="cover-bg-glow"></div>
      <div class="cover-header">
        <div class="cover-badge">OFFICIAL REFERENCE • EDITION 2026</div>
        <div class="cover-subbadge">THE NATURAL SOMALI PROGRAMMING LANGUAGE</div>
      </div>
      
      <div class="cover-center">
        {create_koor_bell_svg()}
        <h1 class="cover-title">KOOR</h1>
        <p class="cover-title-desc">The Somali Programming Language</p>
        <div class="cover-divider"></div>
        <p class="cover-tagline">"The Complete Beginner's Guide: Zero-Coding Foundations, Download &amp; Setup, Terminal Reference, the 6 Core CS Pillars, and 4 Hands-On Real-World Projects."</p>
      </div>

      <div class="cover-features">
        <div class="feat-pill"><span class="pill-dot"></span> Zero-Coding Foundations</div>
        <div class="feat-pill"><span class="pill-dot"></span> Download &amp; Setup Guide</div>
        <div class="feat-pill"><span class="pill-dot"></span> Terminal CLI Commands</div>
        <div class="feat-pill"><span class="pill-dot"></span> The 6 Core CS Pillars</div>
        <div class="feat-pill"><span class="pill-dot"></span> 4 Real-World Projects</div>
      </div>

      <div class="cover-footer">
        <div class="cover-meta-left">
          <strong>KOOR CORE ARCHITECTURE TEAM</strong>
          <span>Language Foundations &amp; Documentation</span>
        </div>
        <div class="cover-meta-right">
          <span class="version-tag">Version 1.0.0</span>
          <span>Official Handbook</span>
        </div>
      </div>
    </div>
    ''')

    # 2. FRONT MATTER & INTRO
    output.append('''
    <div class="page frontmatter-page">
      <div class="fm-header">
        <h2>FOUNDATIONS OF PROGRAMMING IN KOOR</h2>
        <div class="fm-bar"></div>
      </div>

      <div class="dedication-box">
        <p class="dedication-quote">
          "This book is dedicated to aspiring developers, students, and educators. By grounding foundational computer science concepts in authentic, natural Somali grammar, Koor empowers anyone to master computational thinking without linguistic barriers."
        </p>
        <span class="dedication-author">— Koor Core Documentation Team</span>
      </div>

      <div class="fm-meta-grid">
        <div class="fm-card">
          <div class="fm-card-title">1. WELCOME TO CODING</div>
          <div class="fm-card-val">Zero-Coding Foundations, Algorithms, &amp; The Koor Interpreter</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">2. DOWNLOAD &amp; SETUP</div>
          <div class="fm-card-val">Installation Guide, PATH Configuration, &amp; VS Code Setup</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">3. TERMINAL COMMANDS</div>
          <div class="fm-card-val">Complete CLI Reference (<code>koor run</code>, <code>repl</code>, <code>check</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">4. VARIABLES &amp; TYPES</div>
          <div class="fm-card-val">Memory Containers &amp; Primitive Data Types (<code>tiro</code>, <code>qoraal</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">5. OPERATORS &amp; LOGIC</div>
          <div class="fm-card-val">Arithmetic &amp; Natural Comparison Expressions (<code>sidoo kale</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">6. INPUT &amp; OUTPUT</div>
          <div class="fm-card-val">Screen Output (<code>waxaad soo saartaa</code>) &amp; Keyboard Input (<code>waydiin</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">7. CONTROL FLOW</div>
          <div class="fm-card-val">Decisions (<code>haddii</code>, <code>kale</code>) &amp; Automated Loops (<code>ku celi</code>, <code>inta</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">8. FUNCTIONS</div>
          <div class="fm-card-val">Reusable Modules (<code>hawl</code>) &amp; Return Values (<code>waxaad soo celisaa</code>)</div>
        </div>
        <div class="fm-card">
          <div class="fm-card-title">9. DATA STRUCTURES</div>
          <div class="fm-card-val">Lists (<code>liis</code>) &amp; Key-Value Dictionaries (<code>qaamuus</code>)</div>
        </div>
        <div class="fm-card" style="background: #f0fdf4; border-color: #86efac;">
          <div class="fm-card-title" style="color: #166534;">10. REAL-WORLD PROJECTS</div>
          <div class="fm-card-val">4 Built Projects (Retail POS, Student Grading, EVC+, Guessing Game)</div>
        </div>
      </div>

      <div class="manifesto-card">
        <h3>Mastering Computer Science Through Natural Somali</h3>
        <p>This handbook is crafted specifically for absolute beginners who have never programmed before. By working through clear analogies, step-by-step setup tutorials, interactive exercises, and real-life projects, you will develop genuine problem-solving skills that apply to any modern programming language.</p>
      </div>

      <div class="fm-footer">
        <span>© 2026 Koor Language Project. Complete Beginner &amp; Reference Edition.</span>
      </div>
    </div>
    ''')

    # 3. PARSE MARKDOWN CONTENT
    in_toc = False
    toc_cards = []
    current_card = None

    while i < n:
        line = lines[i]

        if line.startswith("# 📘 The Koor Programming Language") or line.startswith("## *The Core Foundations of Natural Somali Programming*"):
            i += 1
            continue

        if line.strip() == "# Table of Contents":
            in_toc = True
            i += 1
            continue

        if in_toc:
            if line.startswith("---") or (line.startswith("# ") and "Table of Contents" not in line):
                in_toc = False
                if current_card:
                    toc_cards.append(current_card)
                    current_card = None
                
                # Render 2-Column TOC (3 chapters on Left, 3 chapters on Right)
                output.append('''
                <div class="page toc-page">
                  <div class="chapter-header">
                    <div class="ch-badge">TABLE OF CONTENTS</div>
                    <h1 class="ch-title">Table of Contents</h1>
                    <div class="ch-accent-line"></div>
                  </div>
                  <div class="toc-columns">
                ''')
                
                for card in toc_cards:
                    num_badge = f'<span class="toc-card-num">{card["num"]}</span>'
                    sub_items_html = ""
                    if card["subs"]:
                        sub_items_html = '<div class="toc-card-subs">' + "".join([f'<div class="toc-sub-line"><span class="toc-sub-dot"></span>{s}</div>' for s in card["subs"]]) + '</div>'
                    
                    output.append(f'''
                    <div class="toc-card-box">
                      <div class="toc-card-top">
                        {num_badge}
                        <a href="{card["target"]}" class="toc-card-title">{card["title"]}</a>
                      </div>
                      {sub_items_html}
                    </div>
                    ''')

                output.append('</div></div>')

                if line.startswith("---"):
                    i += 1
                    continue
            else:
                stripped = line.strip()
                if stripped:
                    m_chap = re.match(r'^(\d+)\.\s+\*\*\[(.*?)\]\((.*?)\)\*\*', stripped)
                    m_sub = re.match(r'^-\s+(\d+\.\d+)\s+(.*)', stripped)
                    if m_chap:
                        if current_card:
                            toc_cards.append(current_card)
                        cnum = m_chap.group(1).zfill(2)
                        current_card = {"num": cnum, "title": format_inline(m_chap.group(2)), "target": m_chap.group(3), "subs": []}
                    elif m_sub and current_card:
                        current_card["subs"].append(f"<strong>{m_sub.group(1)}</strong> {format_inline(m_sub.group(2))}")
                i += 1
                continue

        if line.strip() == "---":
            i += 1
            continue

        # Headings
        if line.startswith("# "):
            title_text = line[2:].strip()
            anchor = re.sub(r'[^a-zA-Z0-9_\-]+', '', title_text.lower().replace(' ', '-'))
            
            m_cutub = re.match(r'Chapter\s+(\d+):\s+(.*)', title_text)
            if m_cutub:
                c_num = m_cutub.group(1)
                c_name = m_cutub.group(2)
                output.append(f'''
                <div class="page-break"></div>
                <div class="chapter-start" id="chapter-{c_num}">
                  <div class="ch-badge-row">
                    <span class="ch-badge">CHAPTER {c_num}</span>
                  </div>
                  <h1 class="chapter-title">{c_name}</h1>
                  <div class="ch-accent-line"></div>
                </div>
                ''')
            else:
                output.append(f'<h1 class="section-h1" id="{anchor}">{format_inline(title_text)}</h1>')
            i += 1
            continue

        if line.startswith("## "):
            h2_text = line[3:].strip()
            output.append(f'<h2 class="section-h2">{format_inline(h2_text)}</h2>')
            i += 1
            continue

        if line.startswith("### "):
            h3_text = line[4:].strip()
            m_sec = re.match(r'^(\d+\.\d+)\s+(.*)', h3_text)
            if m_sec:
                sec_num = m_sec.group(1)
                sec_title = m_sec.group(2)
                output.append(f'''
                <div class="section-header">
                  <span class="sec-num-badge">{sec_num}</span>
                  <h3 class="section-h3">{format_inline(sec_title)}</h3>
                </div>
                ''')
            else:
                output.append(f'<h3 class="section-h3">{format_inline(h3_text)}</h3>')
            i += 1
            continue

        # Code fences
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip().lower()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            
            raw_code = '\n'.join(code_lines)
            
            filename_label = ""
            if code_lines and code_lines[0].strip().startswith("# ") and ("." in code_lines[0] or "koor" in code_lines[0]):
                filename_label = code_lines[0].strip()[2:].strip()
            elif lang == "powershell":
                filename_label = "Terminal / PowerShell"
            elif lang in ("text", ""):
                filename_label = "Console Output"
            else:
                filename_label = f"Koor Source ({lang})"

            if lang in ("soomaali", "koor", "somali"):
                hl_content = highlight_koor(raw_code)
                lang_tag = "KOOR"
            elif lang in ("powershell", "bash", "sh"):
                hl_content = highlight_powershell(raw_code)
                lang_tag = "POWERSHELL"
            else:
                hl_content = highlight_text(raw_code)
                lang_tag = "OUTPUT"

            output.append(f'''
            <div class="code-card">
              <div class="code-card-header">
                <div class="window-dots">
                  <span class="dot dot-red"></span>
                  <span class="dot dot-yellow"></span>
                  <span class="dot dot-green"></span>
                </div>
                <div class="code-card-filename">{html.escape(filename_label)}</div>
                <div class="code-card-lang">{lang_tag}</div>
              </div>
              <pre class="code-body"><code>{hl_content}</code></pre>
            </div>
            ''')
            continue

        # Tables
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            if len(table_lines) >= 2:
                headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
                rows = []
                for r in table_lines[2:]:
                    cells = [c.strip() for c in r.split('|')[1:-1]]
                    rows.append(cells)
                
                table_html = ['<div class="table-container"><table class="styled-table">']
                table_html.append('<thead><tr>')
                for h in headers:
                    table_html.append(f'<th>{format_inline(h)}</th>')
                table_html.append('</tr></thead><tbody>')
                for r_idx, row in enumerate(rows):
                    row_class = "even-row" if r_idx % 2 == 0 else "odd-row"
                    table_html.append(f'<tr class="{row_class}">')
                    for cell in row:
                        table_html.append(f'<td>{format_inline(cell)}</td>')
                    table_html.append('</tr>')
                table_html.append('</tbody></table></div>')
                output.append('\n'.join(table_html))
            continue

        # Diagnostic output label
        if line.strip().startswith("**Output:**"):
            output.append(f'<div class="output-label"><strong>Output / Result:</strong></div>')
            i += 1
            continue

        # Unordered list
        if line.strip().startswith("* ") or line.strip().startswith("- "):
            list_items = []
            while i < n and (lines[i].strip().startswith("* ") or lines[i].strip().startswith("- ")):
                item_content = lines[i].strip()[2:].strip()
                list_items.append(f'<li>{format_inline(item_content)}</li>')
                i += 1
            output.append(f'<ul class="styled-list">{"".join(list_items)}</ul>')
            continue

        # Blockquote
        if line.strip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            q_text = "<br>".join([format_inline(ql) for ql in quote_lines])
            output.append(f'<blockquote class="styled-quote">{q_text}</blockquote>')
            continue

        # Paragraph
        stripped = line.strip()
        if stripped:
            output.append(f'<p class="book-para">{format_inline(stripped)}</p>')
        
        i += 1

    return '\n'.join(output)

def generate_full_html():
    with open('THE_KOOR_BOOK.md', 'r', encoding='utf-8') as f:
        md_text = f.read()

    body_html = parse_markdown_to_html(md_text)

    css = '''
    @page {
      size: A4;
      margin: 18mm 16mm 20mm 16mm;
      @bottom-left {
        content: "The Koor Programming Language — Core Foundations";
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 8pt;
        color: #94a3b8;
      }
      @bottom-right {
        content: counter(page);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 8pt;
        font-weight: 600;
        color: #0284c7;
      }
    }

    @page:first {
      margin: 0;
      @bottom-left { content: normal; }
      @bottom-right { content: normal; }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    html, body {
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Plus Jakarta Sans", "Inter", Roboto, sans-serif;
      font-size: 10pt;
      line-height: 1.65;
      color: #1e293b;
      background: #ffffff;
    }

    .page-break {
      page-break-before: always;
      break-before: page;
      margin-top: 6mm;
    }

    /* ==========================================================
       COVER PAGE
       ========================================================== */
    .cover-page {
      width: 100vw;
      height: 100vh;
      min-height: 297mm;
      background: linear-gradient(145deg, #070b14 0%, #0c1527 45%, #132038 100%);
      color: #ffffff;
      padding: 24mm 22mm 20mm 22mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      break-after: page;
    }

    .cover-bg-glow {
      position: absolute;
      top: -20%;
      right: -20%;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(2, 132, 199, 0.18) 0%, rgba(2, 132, 199, 0) 70%);
      pointer-events: none;
    }

    .cover-header {
      border-left: 3px solid #38bdf8;
      padding-left: 12px;
    }

    .cover-badge {
      font-size: 8.5pt;
      font-weight: 800;
      letter-spacing: 2px;
      color: #38bdf8;
      text-transform: uppercase;
    }

    .cover-subbadge {
      font-size: 7.5pt;
      letter-spacing: 1.5px;
      color: #94a3b8;
      margin-top: 2px;
      font-weight: 600;
    }

    .cover-center {
      text-align: center;
      margin: auto 0;
      padding: 6mm 0;
    }

    .koor-bell-svg {
      width: 130px;
      height: 130px;
      margin: 0 auto 12px auto;
      display: block;
      filter: drop-shadow(0 8px 16px rgba(0,0,0,0.5));
    }

    .cover-title {
      font-size: 54pt;
      font-weight: 900;
      letter-spacing: 8px;
      margin: 0;
      line-height: 1;
      color: #ffffff;
      text-shadow: 0 4px 20px rgba(56, 189, 248, 0.4);
    }

    .cover-title-desc {
      font-size: 14pt;
      font-weight: 600;
      color: #f1f5f9;
      margin: 12px 0 0 0;
      letter-spacing: 0.5px;
    }

    .cover-divider {
      width: 80px;
      height: 3px;
      background: linear-gradient(90deg, #38bdf8, #f59e0b);
      margin: 16px auto;
      border-radius: 2px;
    }

    .cover-tagline {
      font-size: 9pt;
      color: #cbd5e1;
      max-width: 480px;
      margin: 0 auto;
      line-height: 1.6;
      font-style: italic;
    }

    .cover-features {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-bottom: 8mm;
      max-width: 580px;
      margin-left: auto;
      margin-right: auto;
    }

    .feat-pill {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 20px;
      padding: 6px 14px;
      font-size: 8pt;
      font-weight: 600;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .pill-dot {
      width: 6px;
      height: 6px;
      background: #38bdf8;
      border-radius: 50%;
    }

    .cover-footer {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      padding-top: 5mm;
    }

    .cover-meta-left strong {
      display: block;
      font-size: 9pt;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: 0.5px;
    }

    .cover-meta-left span {
      font-size: 8pt;
      color: #94a3b8;
    }

    .cover-meta-right {
      text-align: right;
    }

    .version-tag {
      display: inline-block;
      background: #0284c7;
      color: #ffffff;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 8pt;
      font-weight: 700;
      margin-bottom: 3px;
    }

    .cover-meta-right span:last-child {
      display: block;
      font-size: 8pt;
      color: #94a3b8;
    }

    /* ==========================================================
       FRONT MATTER & DEDICATION
       ========================================================== */
    .frontmatter-page {
      padding: 10mm 4mm;
      page-break-after: always;
      break-after: page;
    }

    .fm-header h2 {
      font-size: 13pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: 1.5px;
      margin: 0;
      text-transform: uppercase;
    }

    .fm-bar {
      width: 40px;
      height: 3px;
      background: #0284c7;
      margin: 8px 0 20px 0;
    }

    .dedication-box {
      background: #f8fafc;
      border-left: 4px solid #0284c7;
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin: 16px 0 24px 0;
    }

    .dedication-quote {
      font-size: 9.8pt;
      font-style: italic;
      color: #334155;
      line-height: 1.7;
      margin: 0 0 8px 0;
    }

    .dedication-author {
      font-size: 8.5pt;
      font-weight: 700;
      color: #0284c7;
      text-align: right;
      display: block;
    }

    .fm-meta-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px 10px;
      margin-bottom: 16px;
    }

    .fm-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 6px 10px;
    }

    .fm-card-title {
      font-size: 7.2pt;
      font-weight: 800;
      color: #0284c7;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 2px;
    }

    .fm-card-val {
      font-size: 8pt;
      font-weight: 500;
      color: #0f172a;
      line-height: 1.35;
    }

    .manifesto-card {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
      padding: 16px 18px;
      margin-bottom: 24px;
    }

    .manifesto-card h3 {
      margin: 0 0 8px 0;
      font-size: 10.5pt;
      font-weight: 800;
      color: #166534;
    }

    .manifesto-card p {
      font-size: 9pt;
      color: #1e293b;
      line-height: 1.6;
      margin: 0 0 8px 0;
    }

    .manifesto-card p:last-child {
      margin-bottom: 0;
    }

    .fm-footer {
      border-top: 1px solid #e2e8f0;
      padding-top: 14px;
      font-size: 7.8pt;
      color: #94a3b8;
      text-align: center;
    }

    /* ==========================================================
       TABLE OF CONTENTS (2-COLUMN CARDS)
       ========================================================== */
    .toc-page {
      padding: 4mm 0;
      page-break-after: always;
      break-after: page;
    }

    .ch-badge {
      background: #0284c7;
      color: #ffffff;
      font-size: 7.5pt;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 4px;
      letter-spacing: 1px;
      display: inline-block;
    }

    .ch-title {
      font-size: 20pt;
      font-weight: 800;
      color: #0f172a;
      margin: 8px 0 0 0;
    }

    .toc-columns {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px 10px;
      margin-top: 8px;
    }

    .toc-card-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      padding: 6px 10px;
      page-break-inside: avoid;
    }

    .toc-card-box:nth-child(10) {
      background: #f0fdf4;
      border-color: #86efac;
    }

    .toc-card-box:nth-child(10) .toc-card-num {
      background: #16a34a;
    }

    .toc-card-top {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .toc-card-num {
      background: #0284c7;
      color: #ffffff;
      font-size: 7pt;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 3px;
      min-width: 22px;
      text-align: center;
    }

    .toc-card-title {
      font-size: 8.6pt;
      font-weight: 700;
      color: #0f172a;
      text-decoration: none;
      line-height: 1.2;
    }

    .toc-card-subs {
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px dashed #cbd5e1;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .toc-sub-line {
      font-size: 7.2pt;
      color: #475569;
      display: flex;
      align-items: center;
      gap: 4px;
      line-height: 1.25;
    }

    .toc-sub-dot {
      width: 4px;
      height: 4px;
      background: #0284c7;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* ==========================================================
       CHAPTER HEADERS
       ========================================================== */
    .chapter-start {
      margin-top: 4mm;
      margin-bottom: 7mm;
      page-break-inside: avoid;
    }

    .ch-badge-row {
      display: flex;
      gap: 8px;
      margin-bottom: 6px;
    }

    .ch-badge-eng {
      background: #e0f2fe;
      color: #0369a1;
      font-size: 7.5pt;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }

    .chapter-title {
      font-size: 20pt;
      font-weight: 800;
      color: #0f172a;
      margin: 0;
      line-height: 1.25;
      letter-spacing: -0.3px;
    }

    .ch-accent-line {
      width: 100%;
      height: 2px;
      background: linear-gradient(90deg, #0284c7 0%, #38bdf8 30%, #e2e8f0 100%);
      margin-top: 8px;
      margin-bottom: 14px;
    }

    /* ==========================================================
       SECTION HEADERS
       ========================================================== */
    .section-header {
      display: flex;
      align-items: center;
      gap: 9px;
      margin-top: 16px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }

    .sec-num-badge {
      background: #f1f5f9;
      color: #0284c7;
      border: 1px solid #cbd5e1;
      font-weight: 800;
      font-size: 7.5pt;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .section-h3 {
      font-size: 11pt;
      font-weight: 700;
      color: #0f172a;
      margin: 0;
    }

    .section-h1 {
      font-size: 14pt;
      font-weight: 800;
      color: #0f172a;
      margin: 18px 0 8px 0;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 4px;
      page-break-after: avoid;
    }

    .section-h2 {
      font-size: 12pt;
      font-weight: 700;
      color: #1e293b;
      margin: 14px 0 6px 0;
      page-break-after: avoid;
    }

    .book-para {
      margin: 0 0 10px 0;
      text-align: justify;
      hyphens: auto;
    }

    .inline-code {
      font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, monospace;
      font-size: 8.5pt;
      background: #f1f5f9;
      color: #0369a1;
      padding: 1.5px 5px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
    }

    /* ==========================================================
       CODE CARDS
       ========================================================== */
    .code-card {
      background: #0b1120;
      border: 1px solid #1e293b;
      border-radius: 6px;
      margin: 11px 0 15px 0;
      overflow: hidden;
      page-break-inside: avoid;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
    }

    .code-card-header {
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
      padding: 5px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .window-dots {
      display: flex;
      gap: 5px;
    }

    .dot {
      width: 7.5px;
      height: 7.5px;
      border-radius: 50%;
      display: inline-block;
    }

    .dot-red { background: #ef4444; }
    .dot-yellow { background: #f59e0b; }
    .dot-green { background: #10b981; }

    .code-card-filename {
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 7.5pt;
      color: #94a3b8;
      font-weight: 500;
    }

    .code-card-lang {
      font-family: -apple-system, sans-serif;
      font-size: 6.5pt;
      font-weight: 800;
      background: #1e293b;
      color: #38bdf8;
      padding: 2px 6px;
      border-radius: 3px;
      letter-spacing: 0.5px;
    }

    .code-body {
      margin: 0;
      padding: 10px 14px;
      font-family: "JetBrains Mono", "Cascadia Code", "Fira Code", Consolas, monospace;
      font-size: 8.5pt;
      line-height: 1.5;
      color: #f1f5f9;
      background: #0b1120;
      overflow-x: auto;
      white-space: pre-wrap;
      word-break: break-all;
    }

    /* SYNTAX HIGHLIGHTING CLASSES */
    .syn-keyword { color: #818cf8; font-weight: 700; }
    .syn-action { color: #34d399; font-weight: 700; }
    .syn-comp { color: #f472b6; font-weight: 600; }
    .syn-type { color: #38bdf8; font-weight: 600; }
    .syn-string { color: #fde047; }
    .syn-interp { color: #67e8f9; font-weight: 700; }
    .syn-num { color: #fb923c; font-weight: 600; }
    .syn-bool { color: #a78bfa; font-weight: 700; }
    .syn-logic { color: #e879f9; font-weight: 700; }
    .syn-comment { color: #64748b; font-style: italic; }
    .syn-cmd { color: #38bdf8; font-weight: 700; }
    .syn-subcmd { color: #fbbf24; font-weight: 600; }
    .repl-prompt { color: #34d399; font-weight: 800; }
    .diag-err { color: #f87171; font-weight: 700; }
    .diag-tip { color: #fbbf24; font-weight: 700; }
    .diag-trace { color: #94a3b8; }

    /* ==========================================================
       TABLES
       ========================================================== */
    .table-container {
      margin: 12px 0 16px 0;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      overflow: hidden;
      page-break-inside: avoid;
    }

    .styled-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8.5pt;
      text-align: left;
    }

    .styled-table thead tr {
      background: #0f172a;
      color: #ffffff;
    }

    .styled-table th {
      padding: 8px 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      font-size: 8pt;
      border: none;
    }

    .styled-table td {
      padding: 7px 12px;
      border-top: 1px solid #e2e8f0;
      color: #1e293b;
      vertical-align: middle;
    }

    .even-row { background: #ffffff; }
    .odd-row { background: #f8fafc; }

    /* ==========================================================
       LISTS & QUOTES
       ========================================================== */
    .styled-list {
      margin: 5px 0 11px 0;
      padding-left: 18px;
    }

    .styled-list li {
      margin-bottom: 3.5px;
      line-height: 1.5;
    }

    .styled-quote {
      border-left: 3px solid #0284c7;
      background: #f0f9ff;
      margin: 10px 0;
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      font-style: italic;
      color: #0369a1;
    }

    .output-label {
      font-size: 8.5pt;
      font-weight: 700;
      color: #475569;
      margin-top: 5px;
      margin-bottom: -5px;
    }
    '''

    full_html = f'''<!DOCTYPE html>
<html lang="so">
<head>
  <meta charset="utf-8">
  <title>The Koor Programming Language - Core Foundations</title>
  <style>{css}</style>
</head>
<body>
  {body_html}
</body>
</html>'''

    html_path = os.path.abspath('THE_KOOR_BOOK.html')
    pdf_path = os.path.abspath('THE_KOOR_BOOK.pdf')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("THE_KOOR_BOOK.html generated.")

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    chrome_bin = next((c for c in chrome_candidates if os.path.exists(c)), None)
    if chrome_bin:
        print(f"Building PDF using {chrome_bin}...")
        cmd = [
            chrome_bin,
            "--headless=new",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}",
            html_path,
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and os.path.exists(pdf_path):
            print(f"THE_KOOR_BOOK.pdf successfully generated ({os.path.getsize(pdf_path):,} bytes).")
        else:
            print("Warning: Chrome exited with non-zero code:", res.stderr.decode('utf-8', errors='ignore'))
    else:
        print("Note: Chrome/Edge not found for automated PDF rendering.")

if __name__ == '__main__':
    generate_full_html()

