# Diiwaanka Naxwaha iyo Eraybixinta Luuqadda Koor

Dukumeentigani waxa uu si qotodheer u faahfaahinayaa qawaaniinta naxwaha iyo eraybixinta sayniska kombuyuutarka ee Af-Soomaaliga ee loo adeegsado luuqadda madaxa-bannaan ee **Koor**.

Luuqadda Koor waxay ku dhisan tahay oo keliya **lixda konsob ee aasaasiga ah**:
1. **Doorsoomayaasha & Noocyada Xogta (Variables & Data Types)**
2. **Xakameynta Socodka (Control Flow)**
3. **Hawlaha (Functions)**
4. **Qaababka Xogta (Data Structures)**
5. **Xisaabiyayaasha & Weedhaha (Operators & Expressions)**
6. **Gelinta & Soo Saarista (Input and Output)**

---

## 1. Mabaadi'da Eraybixinta ee Koor

1. **Doorsoome (Variable)**: Weel lagu kaydiyo xogta oo ku dhisan weedha dabiiciga ah ee `waa` (tusaale: `x waa 10.`).
2. **Wax Ka Beddel (Mutation)**: Falalka dabiiciga ah sida `waxaad ku dartaa`, `waxaad ka jartaa`, `waxaad ku dhufataa`, `waxaad u qaybisaa`.
3. **Shardi (Condition)**: Go'aan qaadashada naxwaha dabiiciga ah sida `haddi ... waxaad soo saartaa ...` ama `haddii ... haddii kale ... kale`.
4. **Wareeg (Loop)**: Ku celcelin ku dhisan `ku celi N jeer:`, `inta shardi:`, ama `mid kastoo ku jira taxane ( xubin ):`.
5. **Hawl (Function)**: Cutub shaqo oo la waco karo, leh naxwe toosan (`hawshu waa ("magac") (expr)`) ama baloog rasmi ah (`hawl magac(): ... waxaad soo celisaa ...`).
6. **Qaababka Xogta (Data Structures)**: Liisaska (`[1, 2, 3]`), Qoraalka (`"..."`), iyo Qaamuusyada furaha iyo qiimaha leh (`{"furaha": qiimaha}`).
7. **Xisaabiye & Caqli (Operator & Logic)**: Calaamadaha xisaabta (`+`, `-`, `*`, `/`, `%`), weedhaha isbarbardhigga ee Af-Soomaaliga (`ay la mid tahay`, `uu ka weyn yahay`, `ka yar yahay ama la mid yahay`), iyo xiriiriyayaasha caqliga (`sidoo kale` / `iyo` oo ah AND, `ama` oo ah OR, iyo `ma` oo ah NOT).
8. **Gelinta & Soo Saarista (Input & Output)**: Bixinta xogta (`waxaad soo saartaa`) iyo qaadashada xogta dadweynaha (`waydiin(...)`).

---

## 2. Naxwaha Luuqadda (Grammar Rules)

### A. Xaaladaha (Conditionals)
```soomaali
# Weedha toosan:
haddi x ay la mid tahay 12 waxaad soo saartaa "waad guulaysatay".

# Baloogga rasmiga ah:
haddii dhibco >= 90:
    waxaad soo saartaa "Darajo: A (Heer Sare)".
hadii kale oo ay dhibco >= 80:
    waxaad soo saartaa "Darajo: B (Aad u Wanaagsan)".
kale:
    waxaad soo saartaa "Darajo: C (Dadaal Dheeraad ah)".
```

### B. Wareegyada (Loops)
```soomaali
# Ku celcelin tiro xaddidan:
ku celi 3 jeer:
    waxaad soo saartaa "Salaan!".

# Wareegga 'inta' (while loop):
tirsade waa 1.
inta tirsade <= 5:
    waxaad soo saartaa tirsade.
    waxaad ku dartaa 1 tirsade.

# Wareegga 'mid kastoo' (for-each loop):
ardayda waa ["Cali", "Aamina", "Warsame"].
mid kastoo ku jira ardayda ( qof ):
    waxaad soo saartaa "Soo dhawoow {qof}!".
```

### C. Hawlaha (Functions)
```soomaali
# Qaabka 1: Naxwaha Qaabeysan (Structured Declarative)
hawl
magaceed waa : isku dhufasho
tibxuhu waa : x , y
hawshu waa : x ku dhufo y
kaydi natiijada

# Wicitaanka hawsha leh qiimayaasha:
natiijo waa qabo hawshan (isku dhufasho) (12, 3)

# Wicitaanka hawl bilaa dood ah:
qabo hawshan (salaan)

# Qaabka 2: Baloogga Rasmiga ah
hawl labanlaab(n):
    waxaad soo celisaa n * 2.

jawaab waa labanlaab(15).
```

### D. Qaababka Xogta (Data Structures)
```soomaali
# Liisaska
liis waa [10, 20, 30].
liis.ku_dar(40).
liis[0] = 99.

# Qaamuusyada
arday waa {
    "magac": "Faadumo",
    "da'": 21,
    "magaalo": "Boorama"
}.
waxaad soo saartaa arday["magac"].

# Qoraalka
hadal waa "  Soomaaliya  ".
waxaad soo saartaa hadal.jar().weyneey().
```

---

## 3. Shaxda Buuxda ee Noocyada Khaladaadka Koor

| Magaca Khaladka | Macnaha |
|---|---|
| `KhaladNaxwo` | Khalad naxwaha qoraalka koodka ah |
| `KhaladMagac` | Magac doorsoome ama hawl aan la aqoon (wata talo sixitaan) |
| `KhaladNooc` | Hawlgal aan ku habboonayn nooca xogta |
| `KhaladQiimo` | Qiime khaldan baa la bixiyey |
| `KhaladTusmo` | Tusmada liiska ama qoraalka ayaa xadkeeda dhaaftay |
| `KhaladFure` | Furaha lagama helin qaamuuska |
| `KhaladEberLooQaybiyay` | Tiro laguma qaybin karo eber (0) |
