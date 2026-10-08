# 🇸🇴 How Koor Works — Complete Architectural & Internal Guide

This document explains **how the Koor programming language works under the hood**, from raw source code to execution. It details the internal pipeline and breaks down how all **6 core concepts** are tokenized, parsed, and executed by Koor's virtual runtime.

---

## 🏗️ 1. The High-Level Architecture Pipeline

When you execute code in Koor, it goes through a 3-stage compiler/interpreter pipeline:

```mermaid
graph TD
    A["Raw Source Code (.koor)"] -->|1. Character Stream| B["Lexer (Scanner / Tokenizer)"]
    B -->|2. Token Stream| C["Parser (Recursive Descent)"]
    C -->|3. Abstract Syntax Tree (AST)| D["Interpreter / Runtime Engine"]
    D -->|4. Environment & Scopes (Deegaan)| E["Memory / Heap Storage"]
    D -->|5. Execution Output| F["Terminal / Standard Output"]
    B -.->|Syntax Error| G["Somali Error Diagnostics (errors.py)"]
    C -.->|Syntax Error| G
    D -.->|Runtime Error| G
```

### Stage 1: Lexical Analysis (`koor/lexer.py`)
Converts raw string characters into structured **Tokens**. 
* Unlike English languages that look for single words (e.g. `if`, `while`), Koor recognizes **multi-word Somali natural phrases** (e.g. `ay la mid tahay`, `waxaad soo saartaa`, `ku celi`, `ka weyn yahay ama la mid yahay`).
* It tracks indentation (`INDENT` / `DEDENT`) when outside brackets, and suppresses indentation inside brackets (`()`, `[]`, `{}`) using `bracket_depth`.

### Stage 2: Parsing & AST Construction (`koor/parser.py`)
Consumes tokens using **Recursive Descent Parsing** to build an **Abstract Syntax Tree (AST)**.
* Understands both **single-line natural sentences** terminated with a period (`.`) and **multi-line indented code blocks** (`:` + indent).
* Enforces mathematical operator precedence (multiplication before addition, etc.).

### Stage 3: AST Interpretation & Environment (`koor/interpreter.py`)
Walks the AST tree and evaluates nodes:
* Manages **Lexical Environments (`Deegaan`)** for variable scoping and parent lookups.
* Handles control-flow interruptions using Python exceptions as signals (`CeliException` for return, `KaBaxException` for break, `KaBoodException` for continue).
* Dispatches data structure operations (list methods, dictionary lookups, string functions).

---

## 🔍 2. Step-by-Step Execution of a Natural Sentence

Let's trace how an idiomatic Somali sentence is executed from characters to output:

```soomaali
x waa 12.
haddi x ay la mid tahay 12 waxaad soo saartaa " waad guulaysatay ".
```

### Step 1: What the Lexer Produces
The Lexer reads the text character-by-character and outputs these tokens:
```python
Token(MAGAC, 'x')
Token(WAA, 'waa')
Token(TIRO, 12)
Token(DOT, '.')
Token(NEWLINE, '\n')
Token(HADDII, 'haddi')
Token(MAGAC, 'x')
Token(LA_MID_YAHAY, 'ay la mid tahay')   # Greedy match of 4 Somali words into 1 equality token!
Token(TIRO, 12)
Token(DAABAC, 'waxaad soo saartaa')     # Greedy match of 3 Somali words into 1 output token!
Token(QORAAL, ' waad guulaysatay ')
Token(DOT, '.')
Token(EOF, '')
```

### Step 2: What the Parser Produces (The AST)
The parser organizes the tokens into hierarchical Python data structures:
```python
Barnaamij(hadallo=[
    # 1. Variable Assignment
    GeliStmt(magac='x', qiimo=TiroExpr(qiimo=12)),
    
    # 2. Natural Condition
    HaddiiStmt(
        shardi=HawlgalLabaaleExpr(
            bidix=MagacExpr(magac='x'),
            calaanad='==',
            midig=TiroExpr(qiimo=12)
        ),
        haddii_run_tahay=[
            QorStmt(qoraallo=[QoraalExpr(qiimo=' waad guulaysatay ')])
        ]
    )
])
```

### Step 3: What the Interpreter Does
1. `GeliStmt`: Stores `x = 12` in the current `Deegaan` (environment memory dictionary).
2. `HaddiiStmt`:
   - Evaluates `shardi` (`x == 12`):
     - Looks up `x` in `Deegaan` ➔ returns `12`.
     - Compares `12 == 12` ➔ returns `True`.
   - Since condition is `True`, it executes `haddii_run_tahay`:
     - Calls `QorStmt`: evaluates `" waad guulaysatay "` and prints it to standard output.

---

## 🧩 3. How the 6 Core Concepts Work Internally

---

### 1. Variables & Data Types (Doorsoomayaasha & Noocyada Xogta)
* **Code:** `x waa 10.`, `waxaad ku dartaa 5 x.`, `nooc(x)`
* **How it works:**
  * Variables are parsed into `GeliStmt(magac, qiimo)` and stored in `Deegaan.qeex(magac, qiimo)`.
  * Increments/decrements parse into `BeddelStmt(hawlgal, qaddar, magac)`.
  * The interpreter looks up the current value of `x`, computes `current + 5`, and updates `Deegaan.beddel('x', new_value)`.
  * If a variable is read before declaration, `Deegaan.hel()` catches it and uses `difflib.get_close_matches` to suggest the nearest variable name in Somali: `💡 TALO: Miyaad u jeedday 'magac'?`
  * Native runtime types:
    * Numbers ➔ Python `int` or `float`
    * Strings ➔ Python `str`
    * Booleans ➔ `run` (`True`), `been` (`False`)
    * Null ➔ `waxba` (`None`)
    * Lists ➔ Python `list`
    * Dictionaries ➔ Python `dict`
  * The built-in `nooc()` inspects the underlying object and returns authentic Somali type names (`tiro`, `qoraal`, `run_been`, `waxba`, `liis`, `qaamuus`).

---

### 2. Control Flow (Xakameynta Socodka)
* **Code:** `haddii ... hadii kale oo ay / uu ... kale`, `ku celi N jeer:`, `inta ... :`, `mid kastoo ku jira liis ( x ):`
* **How it works:**
  * **Conditionals:** `HaddiiStmt` evaluates branches in sequence; as soon as a condition evaluates to `True`, that block executes and remaining branches are skipped.
  * **Repeat Loop:** `KuCeliStmt(jeer, jir)` evaluates the count expression `N` and loops from `0` to `int(N)`.
  * **While Loop:** `IntaStmt(shardi, jir)` re-evaluates the condition expression at the top of each iteration.
  * **For-Each Loop:** `KastaStmt(doorsoome, taxane, jir)` evaluates the iterable and sets the trailing loop variable for each element.
  * **Jump Statements:** `ka bax.` raises `KaBaxException`, caught by loop handlers. `ka bood.` raises `KaBoodException`, terminating the current iteration.

---

### 3. Functions (Hawlaha)
* **Code:**
  * Style A (Structured Declarative): `hawl ... magaceed waa : magac ... tibxuhu waa : x, y ... hawshu waa : x ku dhufo y ... kaydi natiijada` & `qabo hawshan (magac) (args)`
  * Style B (Block Syntax): `hawl magac(args): ... waxaad soo celisaa ...`
* **How it works:**
  * In Style A: The parser captures the declarative fields (`magaceed waa`, `tibxuhu waa`, `hawshu waa`, `kaydi natiijada`). The interpreter stores a callable `KoorHawl` in the environment.
  * In Style B: `HawlQeexidStmt` encapsulates parameters and body statements into a `KoorHawl` instance preserving the closure environment.
  * In `qabo hawshan (magac) (args)`: The parser identifies the function name token inside the first parentheses (without requiring strings/quotes) and any arguments in the optional second parentheses.
  * Function calls create an isolated child `Deegaan(waalid=xirid)` environment, bind arguments to parameter names, and execute the body.
  * `waxaad soo celisaa` or `kaydi natiijada` preserves execution results, returning the value to the caller.

---

### 4. Data Structures (Qaababka Xogta)
* **Code:** `[10, 20, 30]`, `{"magac": "Cali"}`, `"salaan".weyneey()`
* **How it works:**
  * **Lists:** Evaluated into Python `list`. Bracket indexing `liis[0]` is parsed into `TusmoHelExpr`. Method calls `liis.ku_dar(item)`, `liis.ka_saar()`, `liis.kala_sooc()`, `liis.rog()` execute native list modifications.
  * **Dictionaries:** Key-value pairs `{furaha: qiimaha}` form Python `dict`. Subscript assignments `d[k] = v` and `waxaad ku dartaa 100 d[k]` update map entries directly.
  * **Strings:** Built-in methods (`.jar()`, `.weyneey()`, `.yaree()`, `.kala_bax()`, `.beddel()`) execute string transformations and support method chaining.

---

### 5. Operators & Expressions (Hawlgalayaasha & Weedhaha)
* **Code:** `a + b`, `a uu ka weyn yahay b`, `x sidoo kale y`
* **How it works:**
  * Arithmetic: `+`, `-`, `*`, `/`, `%` create `HawlgalLabaaleExpr` nodes.
  * Division by zero (`x / 0`) is intercepted before the host crashes and raises a formatted `KhaladEberLooQaybiyay("Tiro laguma qaybin karo eber.")`.
  * Multi-word phrases like `uu ka weyn yahay` are mapped directly to `TokenType.KA_WEYN` (`>`) by the lexer's regex table.
  * Logical operators `sidoo kale` / `iyo` (and), `ama` (or), `ma` (not) follow short-circuit evaluation in `_qiimee()`.

---

### 6. Input & Output (Gelinta & Soo Saarista)
* **Code:** `waxaad soo saartaa "Salaan {magac}."`, `waydiin("Geli magacaaga: ")`
* **How it works:**
  * `waxaad soo saartaa` and `daabac` parse into `QorStmt`.
  * Expressions inside curly braces `{magac}` in string literals are dynamically interpolated at runtime.
  * `waydiin(fariin)` parses into `WacExpr` calling the built-in function `waydiin`, which prompts via host standard input.

---

## 🔬 4. Visual Diagnostics

Koor features rich diagnostics that locate errors accurately:
```
❌ [KhaladNaxwo] Sadarka 12, Tiirka 5: Kood aan la fahmin: '...'
    │
    │  waxaad ku dartaa
    │      ^
💡 TALO: Hubi qoraalka koodka meeshan ku yaalla.
```

---

## 🏃 5. Verifying the Implementation

Run the automated test suite covering all 6 core pillars:
```powershell
python -m unittest discover tests_koor
```
