# Pair B - etape 2 : cas DEMO-SQL-C11 + DEMO-VOTE, sur data/boutique.sqlite
# Usage (depuis la racine du repo) : python3 td2_pairB/03_c11_demo.py
import sqlite3
import csv
from datetime import date

def lire_sql(nom):
    return open("td2_pairB/sql/" + nom, encoding="utf-8").read()

# base ouverte en lecture seule
con = sqlite3.connect("file:data/boutique.sqlite?mode=ro", uri=True)

# ---------- 1. DEMO-VOTE : table jouet ----------
print("=== DEMO-VOTE (table jouet) ===")
jouet = sqlite3.connect(":memory:")
jouet.execute("CREATE TABLE sales (sale_date TEXT, amount_cents INTEGER)")
jouet.execute("INSERT INTO sales VALUES ('2026-01-01', 100)")
q1 = "SELECT COALESCE(SUM(amount_cents), 0) FROM sales WHERE sale_date > '2026-01-01' AND sale_date < '2026-01-02'"
q2 = "SELECT COALESCE(SUM(amount_cents), 0) FROM sales WHERE sale_date >= '2026-01-01' AND sale_date < '2026-01-02'"
v1 = jouet.execute(q1).fetchone()[0]
v2 = jouet.execute(q2).fetchone()[0]
print("variante > (2 propositions) :", v1)
print("variante >= (1 proposition) :", v2)
propositions = [v1, v1, v2]
print("propositions :", propositions, "| reference : 100")
print("-> 2-sur-3 : la valeur", v1, "a", propositions.count(v1), "voix, donc elle gagne = wrong consensus")

# ---------- 2. C11 : M1, M2, reference ----------
print()
print("=== C11 sur data/boutique.sqlite ===")
m1 = con.execute(lire_sql("c11_M1_gpt-oss-20b.sql")).fetchone()[0]
m2 = con.execute(lire_sql("c11_M2_north-mini-code.sql")).fetchone()[0]
ref = con.execute(lire_sql("c11_reference.sql")).fetchone()[0]
print("M1 (gpt-oss-20b)   :", m1)
print("M2 (north-mini)    :", m2)
print("reference C11      :", ref)
print("ecart ref - M      :", ref - m1)

# Qu'est-ce que chaque WHERE teste vraiment ?
print()
print("clients nes exactement le 2001-12-01 (WHERE de M1) :",
      con.execute("SELECT COUNT(*) FROM customers WHERE birth_date = '2001-12-01'").fetchone()[0])
print("clients dans la fenetre de M2 (<= 2026-12-01 ET >= 2027-12-01) :",
      con.execute("SELECT COUNT(*) FROM customers WHERE '2026-12-01' >= birth_date AND '2027-12-01' <= birth_date").fetchone()[0])
fenetre = con.execute("SELECT date('2026-12-01','-26 years'), date('2026-12-01','-25 years')").fetchone()
print("fenetre correcte : ]", fenetre[0], ";", fenetre[1], "]")
print("clients dans la fenetre correcte :",
      con.execute("SELECT COUNT(*) FROM customers WHERE birth_date > ? AND birth_date <= ?", fenetre).fetchone()[0])

# ---------- 3. Requete delta ----------
print()
print("=== Requete delta (detail des lignes) ===")
lignes = con.execute(lire_sql("c11_delta_detail.sql")).fetchall()
print("customer_id | birth_date | order_id | produit | ligne_cents | M1 | M2")
total = 0
for l in lignes:
    print(l)
    total += l[4]
print("nombre de lignes :", len(lignes), "| somme des lignes :", total)

print()
print("=== Requete delta (total par client) ===")
somme = 0
for l in con.execute(lire_sql("c11_delta_total.sql")).fetchall():
    print(l)
    somme += l[3]
print("TOTAL manquant :", somme, "| reference :", ref, "| ok :", somme == ref)

# ---------- 4. Verification independante, sans SQL ----------
# On relit les 3 CSV de data/ et on calcule l'age en Python avec des dates.
print()
print("=== Verification independante (Python + CSV, sans SQL) ===")
prix = {}
for r in csv.DictReader(open("data/product.csv", encoding="utf-8")):
    prix[r["product_id"]] = int(r["price"])

def age_au(naissance, jour):
    a, m, j = naissance.split("-")
    a, m, j = int(a), int(m), int(j)
    age = jour.year - a
    if (jour.month, jour.day) < (m, j):
        age = age - 1
    return age

jour_ref = date(2026, 12, 1)
clients_25 = set()
for r in csv.DictReader(open("data/customers.csv", encoding="utf-8")):
    if age_au(r["birth_date"], jour_ref) == 25:
        clients_25.add(r["customer_id"])
print("clients de 25 ans au 2026-12-01 :", len(clients_25))

ca = 0
for r in csv.DictReader(open("data/orders.csv", encoding="utf-8")):
    if r["customer_id"] in clients_25:
        ca = ca + int(r["quantity_product"]) * prix[r["product_id"]]
print("CA calcule en Python :", ca, "| ok :", ca == ref)
