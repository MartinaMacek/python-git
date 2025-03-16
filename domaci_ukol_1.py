import math

class Locality:
    def __init__(self, name, locality_coefficient):
        self.name = name
        self.locality_coefficient = locality_coefficient
    
    def __str__(self):
        return f"Pozemek {self.name} má místní koeficient {self.locality_coefficient}."

class Property:
    def __init__(self, locality):
        self.locality = locality

    def __str__(self):
        return f"Pozemek {self.locality.name} má místní koeficient {self.locality.locality_coefficient}"

class Estate(Property):
    Estate_type_coefficients = {"land": 0.85, "building_site": 9, "forrest": 0.35, "garden": 2}

    def __init__(self, locality, estate_type, area):
        super().__init__(locality)
        self.estate_type = estate_type
        self.area = area

    def calculate_tax(self):
        estate_coefficient = self.Estate_type_coefficients[self.estate_type]
        tax = self.area * estate_coefficient * self.locality.locality_coefficient
        return math.ceil(tax)
    
    def __str__(self):
        estate_type_cz = {"land": "Zemědělský pozemek", "building_site": "Stavební parcela", 
                          "forrest": "Lesní pozemek", "garden": "Zahrada"}
        return (f"{estate_type_cz.get(self.estate_type, 'Neznámý typ pozemku')}, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} m2, daň {self.calculate_tax()} Kč.")

class Residence(Property):
    def __init__(self, locality, area, commercial):
        super().__init__(locality)
        self.area = area
        self.commercial = commercial
    def calculate_tax(self):
        if self.commercial:
            tax = (self.area * self.locality.locality_coefficient * 15) * 2
            return math.ceil(tax)
        else:
            tax = self.area * self.locality.locality_coefficient * 15
            return math.ceil(tax)
    def __str__(self):
        if self.commercial == True:
            self.commercial = "komerční"
        else:
            self.commercial = "nekomerční"
        return (f"Rezidence ({self.commercial}), lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} m2, daň {self.calculate_tax()} Kč.")

# lokalita
manetin = Locality("Manětín", 0.8)
brno = Locality("Brno", 3)

# nemovitosti
zemedelsky_pozemek_manetin = Estate(manetin, "land", 900)
dum_manetin = Residence(manetin, 120, commercial = False)
kancelar_brno = Residence(brno, 90, commercial = True)

print(zemedelsky_pozemek_manetin.calculate_tax())
print(dum_manetin.calculate_tax())
print(kancelar_brno.calculate_tax())

print(zemedelsky_pozemek_manetin)
print(dum_manetin)
print(kancelar_brno)