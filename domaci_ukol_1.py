import math
from abc import ABC, abstractmethod
from enum import Enum

class Locality:
    def __init__(self, name, locality_coefficient):
        self.name = name
        self.locality_coefficient = locality_coefficient
    
    def __str__(self):
        return f"Pozemek {self.name} má místní koeficient {self.locality_coefficient}."

class Property(ABC):
    def __init__(self, locality):
        self.locality = locality
    
    @abstractmethod
    def calculate_tax(self):
        pass

    def __str__(self):
        return f"Pozemek {self.locality.name} má místní koeficient {self.locality.locality_coefficient}"

class Estate(Property):

    class EstateType(Enum):
        land = 0.85 
        building_site = 9
        forrest = 0.35 
        garden = 2

    def __init__(self, locality, estate_type, area):
        super().__init__(locality)
        self.estate_type = self.EstateType[estate_type]
        self.area = area

    def calculate_tax(self):
        estate_coefficient = self.estate_type.value
        tax = self.area * estate_coefficient * self.locality.locality_coefficient
        return math.ceil(tax)
    
    def __str__(self):
        estate_type_cz = {"land": "Zemědělský pozemek", "building_site": "Stavební parcela", 
                          "forrest": "Lesní pozemek", "garden": "Zahrada"}
        return (f"{estate_type_cz[self.estate_type.name]}, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} m2, daň {self.calculate_tax()} Kč.")

class Residence(Property):
    def __init__(self, locality, area, commercial):
        super().__init__(locality)
        self.area = area
        self.commercial = commercial

    def calculate_tax(self):
        tax_multiplier = 15
        tax = self.area * self.locality.locality_coefficient * tax_multiplier
        if self.commercial:
            tax = tax * 2
        return math.ceil(tax)
    
    def __str__(self):
        if self.commercial:
            commercial_status = "komerční" 
        else:
            commercial_status = "nekomerční"
        return (f"Rezidence ({commercial_status}), lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} m2, daň {self.calculate_tax()} Kč")

class TaxReport:
    def __init__(self, name):
        self.name = name
        self.property_list = []

    def add_property(self, property):
        self.property_list.append(property)

    def calculate_tax(self):
        total_tax = sum(property.calculate_tax() for property in self.property_list)
        return total_tax
    
    def __str__(self):
        return (f"Daňové přiznání pro {self.name}: {'\n'.join(str(property) for property in self.property_list)}, celková daň: {self.calculate_tax()} Kč.")

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

report = TaxReport("Jan Novák")
report.add_property(zemedelsky_pozemek_manetin)
report.add_property(dum_manetin)
report.add_property(kancelar_brno)
print(report)
