import requests
import json
import sys

# ČÁST 1
# stažení dat z API - vyhledání podle IČO subjektu
get_ico = input("Zadejte IČO subjektu: ").strip()
                
url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{get_ico}"

try:
    response = requests.get(url, timeout=5)
except requests.exceptions.RequestException as e:
    print("Chyba při komunikaci s API, zkontrolujte URL adresu nebo připojení k internetu.")
    sys.exit("Zkuste nové vyhledávání.")

if response.status_code == 200:
    info = response.json()
else:
    print("Zadali jste nesprávné IČO nebo subjekt neexistuje.")
    sys.exit("Zkuste nové vyhledávání.")


# uložení dat do souboru json
with open("subjekt.json", mode = "w", encoding = "utf-8") as file:
    json.dump(info, file, ensure_ascii = False, indent = 4)

# zisk info o subjektu (obchodní jméno a adresa sídla)
obchodni_jmeno = info.get("obchodniJmeno", "Neznámý subjekt")
textova_adresa = info.get("sidlo", {}).get("textovaAdresa", "Adresa nedostupná")

print(obchodni_jmeno)
print(textova_adresa)

# ČÁST 2
# vyhledání podle názvu subjektu
get_subjekt = input("Zadejte název subjektu: ")

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

data = json.dumps({"obchodniJmeno": get_subjekt})

try:
    response = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat", headers=headers, data=data, timeout=5)

except requests.exceptions.RequestException:
    print("Chyba při komunikaci s API, zkontrolujte URL adresu nebo připojení k internetu.")
    sys.exit("Zkuste nové vyhledávání.")

if response.status_code == 200:
    vysledek = response.json()
    pocetCelkem = vysledek.get("pocetCelkem", 0)
    if pocetCelkem == 0:
        print("Nebyl nalezen žádný subjekt s tímto názvem.")
        sys.exit("Zkuste nové vyhledávání.")
else:
    print("Chyba při vyhledání subjektu.")
    sys.exit("Zkuste nové vyhledávání.")

# uložení dat do souboru json
with open("nazev_subjektu.json", mode = "w", encoding = "utf-8") as file:
    json.dump(vysledek, file, ensure_ascii = False, indent = 4)

# vypiš počet nalezených subjektů a seznam nalezených subjektů
pocetCelkem = vysledek["pocetCelkem"]
print(f"Nalezeno subjektů: {pocetCelkem}")

ekonomickeSubjekty = vysledek.get("ekonomickeSubjekty", [])

for subjekt in ekonomickeSubjekty:
    obchodni_jmeno = subjekt.get("obchodniJmeno", "Neznámý subjekt")
    ico = subjekt.get("ico", "Neznámé IČO")
    print(f"{obchodni_jmeno}, {ico}")

# BONUS

# načti číselník právních forem
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data = '{"kodCiselniku": "PravniForma", "zdrojCiselniku": "res"}'

try:
    res = requests.post("https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat", headers=headers, data=data, timeout=5)
except requests.exceptions.RequestException:
    print("Chyba při komunikaci s API, zkontrolujte URL adresu nebo připojení k internetu.")
    sys.exit("Zkuste nové vyhledávání.")

if res.status_code == 200:
    vypis_ciselniky = res.json()
else:
    print("Chyba při vyhledání číselníku.")
    sys.exit("Zkuste nové vyhledávání.")

# uložení dat do souboru json
with open("ciselnik.json", mode = "w", encoding = "utf-8") as file:
    json.dump(vypis_ciselniky, file, ensure_ascii = False, indent = 4)

# Získej seznam právních forem
ciselniky = vypis_ciselniky.get("ciselniky", [])  # prvni_ciselnik = ciselniky[0]
if not ciselniky:
    print("Číselník je prázdný.")
    sys.exit("Zkuste nové vyhledávání.")
polozky = ciselniky[0].get("polozkyCiselniku", [])

# Funkce pro převod kódu na název právní formy
def find_legal_form(kod, polozky_ciselniku):
    for polozka in polozky_ciselniku:
        if polozka.get("kod") == kod:
            return polozka.get("hodnota", "Nenalezeno")
    return "Nenalezeno"

# výpis jména, IČO a právní formy
for subjekt in ekonomickeSubjekty:
    obchodni_jmeno = subjekt["obchodniJmeno"]
    ico = subjekt["ico"]
    kod_pravni_formy = subjekt.get("pravniForma")
    pravni_forma = find_legal_form(kod_pravni_formy, polozky)
    print(f"{obchodni_jmeno}, {ico}, {pravni_forma}")