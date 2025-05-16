import random

# Tabla de efectividad de tipos
type_chart = {
    'Normal': {'Lucha': 2.0, 'Fantasma': 0.0, 'Acero': 0.5, 'Roca': 0.5},
    'Dragón': {'Dragón': 2.0, 'Acero': 0.5, 'Hada': 0.0},
    'Tierra': {'Eléctrico': 2.0, 'Fuego': 2.0, 'Roca': 2.0, 'Acero': 2.0, 'Planta': 0.5, 'Veneno': 2.0, 'Bicho': 0.5, 'Volador': 0.0},
    'Roca': {'Fuego': 2.0, 'Hielo': 2.0, 'Bicho': 2.0, 'Volador': 2.0, 'Acero': 0.5, 'Lucha': 0.5, 'Siniestro': 0.5},
    'Siniestro': {'Psíquico': 2.0, 'Fantasma': 2.0, 'Hada': 0.5, 'Lucha': 0.5, 'Siniestro': 0.5},
    'Fantasma': {'Fantasma': 2.0, 'Psíquico': 2.0, 'Normal': 0.0, 'Lucha': 0.0, 'Siniestro': 0.5},
    'Acero': {'Roca': 2.0, 'Hielo': 2.0, 'Hada': 2.0, 'Veneno': 0.0, 'Acero': 0.5, 'Agua': 0.5, 'Electrico': 0.5, 'Fuego': 0.5},
    'Hielo': {'Dragón': 2.0, 'Volador': 2.0, 'Planta': 2.0, 'Agua': 0.5, 'Acero': 0.5, 'Fuego': 0.5, 'Hielo': 0.5, 'Tierra': 2.0,},
    'Fuego': {'Planta': 2.0, 'Hielo': 2.0, 'Acero': 2.0, 'Agua': 0.5, 'Dragón': 0.5, 'Fuego': 0.5, 'Roca': 0.5, 'Bicho': 2.0,},
    'Lucha': {'Normal': 2.0, 'Hielo': 2.0, 'Roca': 2.0, 'Siniestro': 2.0, 'Acero': 2.0, 'Fantasma': 0.0, 'Bicho': 0.5, 'Hada': 0.5, 'Psiquico': 0.5, 'Veneno': 0.5, 'Volador': 0.5},
    'Agua': {'Fuego': 2.0, 'Roca': 2.0, 'Tierra': 2.0, 'Agua': 0.5, 'Dragón': 0.5, 'Planta': 0.5},
    'Psíquico': {'Lucha': 2.0, 'Veneno': 2.0, 'Acero': 0.5, 'Psíquico': 0.5, 'Siniestro': 0.0},
    'Volador': {'Lucha': 2.0, 'Planta': 2.0, 'Bicho': 2.0, 'Acero': 0.5, 'Eléctrico': 0.5, 'Roca': 0.5},
    'Eléctrico': {'Agua': 2.0, 'Volador': 2.0, 'Tierra': 0.0, 'Planta': 0.5, 'Dragón': 0.5},
    'Veneno': {'Planta': 2.0, 'Hada': 2.0, 'Fantasma': 0.5, 'Roca': 0.5, 'Tierra': 0.5, 'Veneno': 0.5},
    'Bicho': {'Psíquico': 2.0, 'Siniestro': 2.0, 'Planta': 2.0, 'Acero': 0.5, 'Fantasma': 0.5, 'Fuego': 0.5, 'Hada': 0.5, 'Lucha': 0.5, 'Veneno': 0.5, 'Volador': 0.5},
    'Hada': {'Dragón': 2.0, 'Lucha': 2.0, 'Siniestro': 2.0, 'Acero': 0.5, 'Fuego': 0.5, 'Veneno': 0.5},
    'Planta': {'Agua': 2.0, 'Roca': 2.0, 'Tierra': 2.0, 'Acero': 0.5, 'Bicho': 0.5, 'Dragón': 0.5, 'Fuego': 0.5, 'Planta': 0.5, 'Veneno': 0.5, 'Volador': 0.5},
}

def get_type_multiplier(move_type, defender_types):
    multiplier = 1.0
    for dtype in defender_types:
        if move_type in type_chart and dtype in type_chart[move_type]:
            multiplier *= type_chart[move_type][dtype]
    return multiplier

class Movimiento:
    def __init__(self, nombre, tipo, poder, categoria):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder
        self.categoria = categoria  # 'Físico' o 'Especial'

class Pokemon:
    def __init__(self, nombre, tipos, nivel, stats, movimientos):
        self.nombre = nombre
        self.tipos = tipos
        self.nivel = nivel
        self.stats = stats
        self.movimientos = movimientos
        self.ps_actual = stats['PS']

    def esta_vivo(self):
        return self.ps_actual > 0

    def elegir_movimiento(self):
        print(f"\nMovimientos de {self.nombre}:")
        for i, mov in enumerate(self.movimientos, 1):
            print(f"{i}. {mov.nombre} ({mov.tipo}, Poder: {mov.poder}, {mov.categoria})")
        while True:
            try:
                opcion = int(input("Elige un movimiento (1-4): "))
                if 1 <= opcion <= 4:
                    return self.movimientos[opcion - 1]
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Entrada inválida.")

    def usar_movimiento(self, movimiento, objetivo):
        print(f"\n{self.nombre} usa {movimiento.nombre}!")

        if movimiento.categoria == 'Físico':
            ataque = self.stats['Ataque']
            defensa = objetivo.stats['Defensa']
        else:
            ataque = self.stats['AtqEsp']
            defensa = objetivo.stats['DefEsp']

        stab = 1.5 if movimiento.tipo in self.tipos else 1.0
        efectividad = get_type_multiplier(movimiento.tipo, objetivo.tipos)
        daño = (((2 * self.nivel / 5 + 2) * movimiento.poder * (ataque / defensa)) / 50 + 2) * stab * efectividad
        daño = int(daño)
        objetivo.ps_actual -= daño
        print(f"¡Causó {daño} puntos de daño!")
        if efectividad > 1:
            print("¡Es muy efectivo!")
        elif efectividad < 1 and efectividad > 0:
            print("No es muy efectivo...")
        elif efectividad == 0:
            print("No tiene efecto...")
        if objetivo.ps_actual < 0:
            objetivo.ps_actual = 0
        print(f"{objetivo.nombre} tiene {objetivo.ps_actual}/{objetivo.stats['PS']} PS restantes.")

# Espacio para los Pokémon no borrar, aqui los pongo despues para que no sea largo el codigo en
garchomp = Pokemon(
    "Garchomp", ["Dragón", "Tierra"], 50,
    {'PS': 215, 'Ataque': 200, 'Defensa': 161, 'AtqEsp': 145, 'DefEsp': 150, 'Velocidad': 169},
    [Movimiento("Terremoto", "Tierra", 100, "Especial"),
     Movimiento("Garra Dragón", "Dragón", 80, "Físico"),
     Movimiento("Colmillo Ígneo", "Fuego", 65, "Físico"),
     Movimiento("Triturar", "Siniestro", 80, "Físico")]
)

tyranitar = Pokemon(
    "Tyranitar", ["Roca", "Siniestro"], 50,
    {'PS': 207, 'Ataque': 204, 'Defensa': 178, 'AtqEsp': 161, 'DefEsp': 167, 'Velocidad': 124},
    [Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Puño Fuego", "Fuego", 75, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico")]
)

salamence = Pokemon(
    "Salamence", ["Dragón", "Volador"], 50,
    {'PS': 202, 'Ataque': 205, 'Defensa': 145, 'AtqEsp': 178, 'DefEsp': 145, 'Velocidad': 167},
    [Movimiento("Garra Dragón", "Dragón", 80, "Físico"),
     Movimiento("Vuelo", "Volador", 90, "Físico"),
     Movimiento("Llamarada", "Fuego", 110, "Especial"),
     Movimiento("Colmillo Trueno", "Eléctrico", 65, "Físico")]
)

metagross = Pokemon(
    "Metagross", ["Acero", "Psíquico"], 50,
    {'PS': 187, 'Ataque': 205, 'Defensa': 200, 'AtqEsp': 161, 'DefEsp': 156, 'Velocidad': 134},
    [Movimiento("Puño Meteoro", "Acero", 90, "Físico"),
     Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Puño Hielo", "Hielo", 75, "Físico")]
)

# Nuevos Pokémon rivales
charizard = Pokemon(
    "Charizard", ["Fuego", "Volador"], 50,
    {'PS': 185, 'Ataque': 149, 'Defensa': 143, 'AtqEsp': 177, 'DefEsp': 150, 'Velocidad': 160},
    [Movimiento("Llamarada", "Fuego", 110, "Especial"),
     Movimiento("Rayo Solar", "Planta", 120, "Especial"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]
)

blastoise = Pokemon(
    "Blastoise", ["Agua"], 50,
    {'PS': 186, 'Ataque': 148, 'Defensa': 167, 'AtqEsp': 150, 'DefEsp': 172, 'Velocidad': 143},
    [Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Hidrocañón", "Agua", 120, "Especial"),
     Movimiento("Esfera Aural", "Lucha", 80, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial")]
)

alakazam = Pokemon(
    "Alakazam", ["Psíquico"], 50,
    {'PS': 162, 'Ataque': 112, 'Defensa': 106, 'AtqEsp': 205, 'DefEsp': 161, 'Velocidad': 180},
    [Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial"),
     Movimiento("Psicocarga", "Psiquico", 80, "Especial"),
     Movimiento("Bola sombra", "Fantasma", 80, "Especial")]
)

gengar = Pokemon(
    "Gengar", ["Fantasma", "Veneno"], 50,
    {'PS': 167, 'Ataque': 128, 'Defensa': 123, 'AtqEsp': 200, 'DefEsp': 139, 'Velocidad': 178},
    [Movimiento("Bola sombra", "Fantasma", 80, "Especial"),
     Movimiento("Onda Tóxica", "Veneno", 95, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial"),
     Movimiento("Rayo", "Electrico", 90, "Especial")]
)

snorlax = Pokemon(
    "Snorlax", ["Normal"], 50,
    {'PS': 267, 'Ataque': 178, 'Defensa': 128, 'AtqEsp': 128, 'DefEsp': 178, 'Velocidad': 90},
    [Movimiento("Fuerza Esquina", "Tierra", 95, "Físico"),
     Movimiento("Triturar", "Siniestro", 80, "Físico"),
     Movimiento("Puño fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño hielo", "Hielo", 75, "Físico")]
)
excadrill = Pokemon(
    "Excadrill", ["Tierra", "Acero"], 50,
    {'PS': 217, 'Ataque': 205, 'Defensa': 123, 'AtqEsp': 112, 'DefEsp': 128, 'Velocidad': 154},
    [Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Cabeza de Hierro", "Acero", 80, "Físico"),
     Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("Corte X", "Bicho", 80, "Físico")]
)

hydreigon = Pokemon(
    "Hydreigon", ["Siniestro", "Dragón"], 50,
    {'PS': 199, 'Ataque': 172, 'Defensa': 156, 'AtqEsp': 194, 'DefEsp': 156, 'Velocidad': 159},
    [Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Llama Final", "Fuego", 130, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial")]
)

scizor = Pokemon(
    "Scizor", ["Bicho", "Acero"], 50,
    {'PS': 177, 'Ataque': 200, 'Defensa': 167, 'AtqEsp': 117, 'DefEsp': 145, 'Velocidad': 128},
    [Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico"),
     Movimiento("Ala de Acero", "Acero", 70, "Físico"),
     Movimiento("Fuerza Bruta", "Lucha", 120, "Físico"),
     Movimiento("Tijera X", "Bicho", 80, "Físico")]
)
togekiss = Pokemon(
    "Togekiss", ["Hada", "Volador"], 50,
    {'PS': 192, 'Ataque': 112, 'Defensa': 161, 'AtqEsp': 189, 'DefEsp': 183, 'Velocidad': 145},
    [Movimiento("Llama Mágica", "Hada", 95, "Especial"),
     Movimiento("Esfera Aural", "Lucha", 80, "Especial"),
     Movimiento("LanzaLlamas", "Fuego", 90, "Especial"),
     Movimiento("Tajo Aéreo", "Volador", 75, "Especial")]
)

weavile = Pokemon(
    "Weavile", ["Siniestro", "Hielo"], 50,
    {'PS': 177, 'Ataque': 189, 'Defensa': 128, 'AtqEsp': 106, 'DefEsp': 150, 'Velocidad': 180},
    [Movimiento("Demolición", "Lucha", 75, "Físico"),
     Movimiento("Puño Hielo", "Hielo", 75, "Físico"),
     Movimiento("Golpe Bajo", "Siniestro", 70, "Físico"),
     Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico")]
)
infernape = Pokemon(
    "Infernape", ["Fuego", "Lucha"], 50,
    {'PS': 183, 'Ataque': 171, 'Defensa': 135, 'AtqEsp': 171, 'DefEsp': 135, 'Velocidad': 170},
    [Movimiento("Envite Ígneo", "Fuego", 120, "Físico"),
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),
     Movimiento("Velocidad Extrema", "Normal", 100, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico")]
)

gliscor = Pokemon(
    "Gliscor", ["Tierra", "Volador"], 50,
    {'PS': 182, 'Ataque': 161, 'Defensa': 194, 'AtqEsp': 106, 'DefEsp': 139, 'Velocidad': 160},
    [Movimiento("Tajo Aéreo", "Volador", 75, "Especial"),
     Movimiento("Colmillo Hielo", "Hielo", 65, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Acróbata", "Volador", 55, "Físico")]
)

magnezone = Pokemon(
    "Magnezone", ["Eléctrico", "Acero"], 50,
    {'PS': 177, 'Ataque': 134, 'Defensa': 183, 'AtqEsp': 200, 'DefEsp': 156, 'Velocidad': 123},
    [Movimiento("Rayo", "Eléctrico", 90, "Especial"),
     Movimiento("Bomba Imán", "Acero", 60, "Físico"),
     Movimiento("Chispazo", "Eléctrico", 80, "Especial"),
     Movimiento("Doble Filo", "Normal", 100, "Fisico")]
)
chandelure = Pokemon(
    "Chandelure", ["Fantasma", "Fuego"], 50,
    {'PS': 167, 'Ataque': 117, 'Defensa': 156, 'AtqEsp': 216, 'DefEsp': 156, 'Velocidad': 145},
    [Movimiento("Llamarada", "Fuego", 110, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Poder Oculto", "Hielo", 60, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial")]
)

krookodile = Pokemon(
    "Krookodile", ["Tierra", "Siniestro"], 50,
    {'PS': 202, 'Ataque': 185, 'Defensa': 145, 'AtqEsp': 128, 'DefEsp': 134, 'Velocidad': 150},
    [Movimiento("Tierra Viva", "Tierra", 90, "Especial"),
     Movimiento("Triturar", "Siniestro", 80, "Físico"),
     Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico")]
)

volcarona = Pokemon(
    "Volcarona", ["Bicho", "Fuego"], 50,
    {'PS': 192, 'Ataque': 123, 'Defensa': 128, 'AtqEsp': 205, 'DefEsp': 172, 'Velocidad': 160},
    [Movimiento("Picadura", "Bicho", 75, "físico"),
     Movimiento("Giga Drenado", "Planta", 75, "Especial"),
     Movimiento("Lanzallamas", "Fuego", 90, "Especial"),
     Movimiento("Psíquico", "Psíquico", 90, "Especial")]
)

conkeldurr = Pokemon(
    "Conkeldurr", ["Lucha"], 50,
    {'PS': 212, 'Ataque': 211, 'Defensa': 161, 'AtqEsp': 117, 'DefEsp': 128, 'Velocidad': 106},
    [Movimiento("Puño Drenaje", "Lucha", 75, "Físico"),
     Movimiento("Golpe Kárate", "Lucha", 50, "Físico"),
     Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico")]
)

galvantula = Pokemon(
    "Galvantula", ["Bicho", "Eléctrico"], 50,
    {'PS': 177, 'Ataque': 141, 'Defensa': 123, 'AtqEsp': 163, 'DefEsp': 123, 'Velocidad': 158},
    [Movimiento("Electrotela", "Eléctrico", 55, "Especial"),
     Movimiento("Zumbido", "Bicho", 90, "Especial"),
     Movimiento("Energibola", "Planta", 90, "Especial"),
     Movimiento("Rayo", "Electrico", 90, "Especial")]
)
serperior = Pokemon(
    "Serperior", ["Planta"], 50,
    {'PS': 182, 'Ataque': 139, 'Defensa': 161, 'AtqEsp': 139, 'DefEsp': 161, 'Velocidad': 181},
    [Movimiento("Hoja Aguda", "Planta", 90, "Físico"),
     Movimiento("Golpe Aéreo", "Volador", 60, "Físico"),
     Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Planta Feroz", "Planta", 150, "Especial")]
)

zoroark = Pokemon(
    "Zoroark", ["Siniestro"], 50,
    {'PS': 167, 'Ataque': 172, 'Defensa': 123, 'AtqEsp': 189, 'DefEsp': 123, 'Velocidad': 172},
    [Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Alarido", "Siniestro", 55, "Especial"),
     Movimiento("Llamarada", "Fuego", 110, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial")]
)
meowscarada = Pokemon(
    "Meowscarada", ["Planta", "Siniestro"], 50,
    {'PS': 183, 'Ataque': 178, 'Defensa': 134, 'AtqEsp': 146, 'DefEsp': 134, 'Velocidad': 192},
    [Movimiento("Ida y Vuelta", "Bicho", 70, "Físico"),
     Movimiento("Tajo Umbrío", "Fantasma", 70, "Físico"),
     Movimiento("Truco Floral", "Planta", 111, "Físico"),
     Movimiento("Carantoña", "Hada", 90, "Físico")
]

)
spiritomb = Pokemon(
    "Spiritomb", ["Fantasma", "Siniestro"], 50,
    {'PS': 157, 'Ataque': 158, 'Defensa': 176, 'AtqEsp': 158, 'DefEsp': 176, 'Velocidad': 95},
    [Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Puño Sombra", "Fantasma", 60, "Físico")]
)

roserade = Pokemon(
    "Roserade", ["Planta", "Veneno"], 50,
    {'PS': 167, 'Ataque': 134, 'Defensa': 128, 'AtqEsp': 194, 'DefEsp': 172, 'Velocidad': 156},
    [Movimiento("Brillo Mágico", "Hada", 95, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Bomba Lodo", "Veneno", 90, "Especial"),
     Movimiento("Bola Energía", "Planta", 90, "Especial")]
)

gastrodon = Pokemon(
    "Gastrodon", ["Agua", "Tierra"], 50,
    {'PS': 218, 'Ataque': 148, 'Defensa': 132, 'AtqEsp': 158, 'DefEsp': 147, 'Velocidad': 100},
    [Movimiento("Escaldar", "Agua", 80, "Especial"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Bomba Lodo", "Veneno", 90, "Especial"),
     Movimiento("Avalancha", "Roca", 75, "Físico")]
)

lucario = Pokemon(
    "Lucario", ["Lucha", "Acero"], 50,
    {'PS': 177, 'Ataque': 178, 'Defensa': 134, 'AtqEsp': 183, 'DefEsp': 134, 'Velocidad': 156},
    [Movimiento("Esfera Aural", "Lucha", 80, "Especial"),
     Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Cañón de Flash", "Acero", 100, "Especial"),
     Movimiento("Psiquico", "Psíquico", 90, "Especial")]
)

milotic = Pokemon(
    "Milotic", ["Agua"], 50,
    {'PS': 202, 'Ataque': 123, 'Defensa': 144, 'AtqEsp': 167, 'DefEsp': 194, 'Velocidad': 146},
    [Movimiento("Pulso Dragón", "Dragón", 80, "Especial"),
     Movimiento("Brillo Magico", "Hada", 90, "Especial"),
     Movimiento("Rayo Hielo", "Hielo", 95, "Especial"),
     Movimiento("Escaldar", "Agua", 80, "Especial")]
)

garchomp2 = Pokemon(
    "Garchomp", ["Dragón", "Tierra"], 50,
    {'PS': 215, 'Ataque': 200, 'Defensa': 161, 'AtqEsp': 145, 'DefEsp': 150, 'Velocidad': 169},
    [Movimiento("Garra Dragón", "Dragón", 75, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Cometa Dragón", "Dragón", 120, "Físico"),
     Movimiento("Pulso Dragón", "Dragón", 70, "Especial")]
)
aggron = Pokemon(
    "Aggron", ["Acero", "Roca"], 50,
    {'PS': 177, 'Ataque': 178, 'Defensa': 255, 'AtqEsp': 123, 'DefEsp': 123, 'Velocidad': 112},
    [Movimiento("Doble filo", "Normal", 120, "Físico"),
     Movimiento("Puño fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Puño hielo", "Hielo", 75, "Físico")]
)

drapion = Pokemon(
    "Drapion", ["Veneno", "Siniestro"], 57,
    {'PS': 177, 'Ataque': 156, 'Defensa': 178, 'AtqEsp': 123, 'DefEsp': 139, 'Velocidad': 144},
    [Movimiento("Tijera X", "Bicho", 80, "Físico"),
     Movimiento("Puño fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Puño hielo", "Hielo", 75, "Físico")]
)

ninjask = Pokemon(
    "Ninjask", ["Bicho", "Volador"], 50,
    {'PS': 168, 'Ataque': 156, 'Defensa': 106, 'AtqEsp': 112, 'DefEsp': 112, 'Velocidad': 233},
    [Movimiento("Excavar", "Tierra", 100, "Físico"),
     Movimiento("Puño fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Puño hielo", "Hielo", 75, "Físico")]
)

electivire = Pokemon(
    "Electivire", ["Eléctrico"], 50,
    {'PS': 182, 'Ataque': 192, 'Defensa': 130, 'AtqEsp': 161, 'DefEsp': 150, 'Velocidad': 144},
    [Movimiento("Puño trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Puño fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño hielo", "Hielo", 75, "Físico"),
     Movimiento("Tajo Cruzado", "Lucha", 75, "Físico")]
)

froslass = Pokemon(
    "Froslass", ["Hielo", "Fantasma"], 58,
    {'PS': 177, 'Ataque': 145, 'Defensa': 134, 'AtqEsp': 145, 'DefEsp': 134, 'Velocidad': 178},
    [Movimiento("Pulso Umbrio", "Siniestro", 80, "Especial"),
     Movimiento("Ventisca", "Hielo", 120, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial")]
)
smeargle = Pokemon(
    "Smeargle", ["Normal"], 80,
    {'PS': 200, 'Ataque': 152, 'Defensa': 185, 'AtqEsp': 152, 'DefEsp': 207, 'Velocidad': 273},
    [Movimiento("Hidrocañón", "Agua", 100, "Especial"),
     Movimiento("Anillo Ígneo", "Fuego", 100, "Especial"),
     Movimiento("Planta Feroz", "Planta", 100, "Especial"),
     Movimiento("Rayo Fusión", "Electrico", 100, "Especial")]
)
gyarados = Pokemon(
    "Gyarados", ["Agua", "Volador"], 50,
    {'PS': 202, 'Ataque': 194, 'Defensa': 144, 'AtqEsp': 123, 'DefEsp': 167, 'Velocidad': 146},
    [Movimiento("Triturar", "Siniestro", 80, "Físico"),
     Movimiento("Cascada", "Agua", 80, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Bote", "Volador", 80, "Físico")]
)
toxapex = Pokemon(
    "Toxapex", ["Agua", "Veneno"], 50,
    {'PS': 157, 'Ataque': 126, 'Defensa': 224, 'AtqEsp': 115, 'DefEsp': 213, 'Velocidad': 146},
    [Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Hidroariete", "Agua", 85, "Físico"),
     Movimiento("Puya Nociva", "Veneno", 80, "Físico"),
     Movimiento("Pin Misil", "Bicho", 80, "Físico")]
)
zeraora = Pokemon(
    "Zeraora", ["Eléctrico"], 50,
    {'PS': 195, 'Ataque': 180, 'Defensa': 139, 'AtqEsp': 169, 'DefEsp': 145, 'Velocidad': 214},
    [Movimiento("Bote", "Volador", 85, "Físico"),
     Movimiento("Puño Fuego", "Fuego", 75, "Físico"),
     Movimiento("Puños Plasma", "Eléctrico", 100, "Físico"),
     Movimiento("A Bocajarro", "Lucha", 120, "Físico")]
)
probopass = Pokemon(
    "Probopass", ["Roca"], 50,
    {'PS': 167, 'Ataque': 117, 'Defensa': 216, 'AtqEsp': 139, 'DefEsp': 222, 'Velocidad': 101},
    [Movimiento("Brillo Mágico", "Hada", 85, "Especial"),
     Movimiento("Trueno", "Fuego", 110, "Especial"),
     Movimiento("Foco Resplandor", "Acero", 80, "Especial"),
     Movimiento("Joya de Luz", "Roca", 80, "Especial")]
)
florges = Pokemon(
    "Florges", ["Hada"], 50,
    {'PS': 185, 'Ataque': 128, 'Defensa': 132, 'AtqEsp': 180, 'DefEsp': 226, 'Velocidad': 140},
    [Movimiento("Rayo solar", "Planta", 120, "Especial"),
     Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Fuerza Lunar", "Hada", 90, "Especial"),
     Movimiento("Tormenta Floral", "Planta", 90, "Especial")]
)
darkrai = Pokemon(
    "Darkrai", ["Siniestro"], 50,
    {'PS': 177, 'Ataque': 156, 'Defensa': 156, 'AtqEsp': 205, 'DefEsp': 156, 'Velocidad': 194},
    [Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Bomba Lodo", "Veneno", 90, "Especial"),
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]
)
gardevoir = Pokemon(
    "Gardevoir", ["Psíquico", "Hada"], 50,
    {'PS': 155, 'Ataque': 85, 'Defensa': 85, 'AtqEsp': 182, 'DefEsp': 135, 'Velocidad': 100},
    [Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Fuerza Lunar", "Hada", 95, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]
)
naganadel = Pokemon(
    "Naganadel", ["Veneno", "Dragón"], 50,
    {'PS': 146, 'Ataque': 105, 'Defensa': 105, 'AtqEsp': 182, 'DefEsp': 105, 'Velocidad': 194},
    [Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Bomba Lodo", "Veneno", 90, "Especial"),
     Movimiento("Lanzallamas", "Fuego", 90, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]
)
buzzwole = Pokemon(
    "Buzzwole", ["Bicho", "Lucha"], 50,
    {'PS': 187, 'Ataque': 194, 'Defensa': 194, 'AtqEsp': 85, 'DefEsp': 85, 'Velocidad': 119},
    [Movimiento("Chupavidas", "Bicho", 80, "Físico"),
     Movimiento("Puño Incremento", "Lucha", 40, "Físico"),
     Movimiento("Puño Hielo", "Hielo", 75, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico")]
)
tapu_koko = Pokemon(
    "Tapu Koko", ["Eléctrico", "Hada"], 50,
    {'PS': 155, 'Ataque': 182, 'Defensa': 135, 'AtqEsp': 105, 'DefEsp': 115, 'Velocidad': 194},
    [Movimiento("Chispa", "Eléctrico", 65, "Físico"),
     Movimiento("Brillo Mágico", "Hada", 80, "Especial"),
     Movimiento("Voltiocambio", "Eléctrico", 70, "Especial"),
     Movimiento("Acrobata", "Volador", 55, "Físico")]
)
incineroar = Pokemon(
    "Incineroar", ["Fuego", "Siniestro"], 50,
    {'PS': 177, 'Ataque': 182, 'Defensa': 135, 'AtqEsp': 105, 'DefEsp': 135, 'Velocidad': 100},
    [Movimiento("Alarido", "Siniestro", 55, "Especial"),
     Movimiento("Envite Ígneo", "Fuego", 120, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico")]
)

decidueye = Pokemon(
    "Decidueye", ["Planta", "Fantasma"], 50,
    {'PS': 165, 'Ataque': 167, 'Defensa': 125, 'AtqEsp': 115, 'DefEsp': 125, 'Velocidad': 115},
    [Movimiento("Pájaro Osado", "Volador", 120, "Físico"),
     Movimiento("Follaje", "Planta", 40, "Físico"),
     Movimiento("Sombra Vil", "Fantasma", 40, "Físico"),
     Movimiento("Sombras Traidoras", "Fantasma", 90, "Físico")]
)

hoopa = Pokemon(
    "Hoopa", ["Psíquico", "Fantasma"], 50,
    {'PS': 165, 'Ataque': 115, 'Defensa': 115, 'AtqEsp': 205, 'DefEsp': 175, 'Velocidad': 85},
    [Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Foco Resplandor", "Acero", 80, "Especial"),
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]
)

noivern = Pokemon(
    "Noivern", ["Volador", "Dragón"], 50,
    {'PS': 167, 'Ataque': 115, 'Defensa': 105, 'AtqEsp': 162, 'DefEsp': 115, 'Velocidad': 183},
    [Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Ala de Acero", "Acero", 70, "Físico"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Lanzallamas", "Fuego", 90, "Especial")]
)

hawlucha = Pokemon(
    "Hawlucha", ["Lucha", "Volador"], 50,
    {'PS': 157, 'Ataque': 167, 'Defensa': 125, 'AtqEsp': 85, 'DefEsp': 105, 'Velocidad': 183},
    [Movimiento("Acróbata", "Volador", 55, "Físico"),
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Tajo Cruzado", "Lucha", 100, "Físico")]
)

pangoro = Pokemon(
    "Pangoro", ["Lucha", "Siniestro"], 50,
    {'PS': 187, 'Ataque': 194, 'Defensa': 125, 'AtqEsp': 95, 'DefEsp': 105, 'Velocidad': 95},
    [Movimiento("Puño Incremento", "Lucha", 40, "Físico"),
     Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Demolición", "Lucha", 75, "Físico")]
)

greninja = Pokemon(
    "Greninja", ["Agua", "Siniestro"], 50,
    {'PS': 157, 'Ataque': 135, 'Defensa': 105, 'AtqEsp': 162, 'DefEsp': 105, 'Velocidad': 183},
    [Movimiento("Surf", "Agua", 90, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial"),
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Tajo Aéreo", "Volador", 75, "Especial")]
)

druddigon = Pokemon(
    "Druddigon", ["Dragón"], 50,
    {'PS': 177, 'Ataque': 194, 'Defensa': 135, 'AtqEsp': 95, 'DefEsp': 115, 'Velocidad': 85},
    [Movimiento("Garra Dragón", "Dragón", 80, "Físico"),
     Movimiento("Puño Fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Cabeza Hierro", "Acero", 80, "Físico")]
)
mienshao = Pokemon(
    "Mienshao", ["Lucha"], 50,
    {'PS': 157, 'Ataque': 194, 'Defensa': 105, 'AtqEsp': 125, 'DefEsp': 105, 'Velocidad': 183},
    [Movimiento("A Bocajarro", "Lucha", 120, "Físico"),
     Movimiento("Giro Bola", "Acero", 60, "Físico"),
     Movimiento("Puño Drenaje", "Lucha", 75, "Físico"),
     Movimiento("Tajo Aéreo", "Volador", 75, "Especial")]
)

haxorus = Pokemon(
    "Haxorus", ["Dragón"], 50,
    {'PS': 177, 'Ataque': 222, 'Defensa': 125, 'AtqEsp': 95, 'DefEsp': 105, 'Velocidad': 135},
    [Movimiento("Garra Dragón", "Dragón", 80, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Tajo Aéreo", "Volador", 75, "Especial"),
     Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico")]
)

gothitelle = Pokemon(
    "Gothitelle", ["Psíquico"], 50,
    {'PS': 177, 'Ataque': 95, 'Defensa': 135, 'AtqEsp': 125, 'DefEsp': 155, 'Velocidad': 95},
    [Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Foco Resplandor", "Acero", 80, "Especial"),
     Movimiento("Rayo", "Eléctrico", 90, "Especial")]
)

crustle = Pokemon(
    "Crustle", ["Bicho", "Roca"], 50,
    {'PS': 167, 'Ataque': 172, 'Defensa': 205, 'AtqEsp': 75, 'DefEsp': 115, 'Velocidad': 75},
    [Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("X-Scissor", "Bicho", 80, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Garra Metal", "Acero", 50, "Físico")]
)

darmanitan = Pokemon(
    "Darmanitan", ["Fuego"], 50,
    {'PS': 185, 'Ataque': 222, 'Defensa': 115, 'AtqEsp': 95, 'DefEsp': 105, 'Velocidad': 145},
    [Movimiento("Envite Ígneo", "Fuego", 120, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico")]
)

zebstrika = Pokemon(
    "Zebstrika", ["Eléctrico"], 50,
    {'PS': 167, 'Ataque': 167, 'Defensa': 105, 'AtqEsp': 125, 'DefEsp': 105, 'Velocidad': 175},
    [Movimiento("Chispazo", "Eléctrico", 80, "Especial"),
     Movimiento("Nitrocarga", "Fuego", 50, "Físico"),
     Movimiento("Golpe Cuerpo", "Normal", 85, "Físico"),
     Movimiento("Carantoña", "Hada", 90, "Físico")]
)
stoutland = Pokemon(
    "Stoutland", ["Normal"], 50,
    {'PS': 185, 'Ataque': 172, 'Defensa': 135, 'AtqEsp': 95, 'DefEsp': 115, 'Velocidad': 115},
    [Movimiento("Golpe Cuerpo", "Normal", 85, "Físico"),
     Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),
     Movimiento("Carantoña", "Hada", 90, "Físico")]
)

rotom = Pokemon(
    "Rotom", ["Eléctrico", "Fantasma"], 50,
    {'PS': 157, 'Ataque': 95, 'Defensa': 135, 'AtqEsp': 157, 'DefEsp': 145, 'Velocidad': 135},
    [Movimiento("Rayo", "Eléctrico", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Voltiocambio", "Eléctrico", 70, "Especial"),
     Movimiento("Pulso Umbrío", "Siniestro", 80, "Especial")]
)

gallade = Pokemon(
    "Gallade", ["Psíquico", "Lucha"], 50,
    {'PS': 165, 'Ataque': 194, 'Defensa': 125, 'AtqEsp': 105, 'DefEsp': 135, 'Velocidad': 125},
    [Movimiento("Psico Corte", "Psíquico", 70, "Físico"),
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),
     Movimiento("Hoja Aguda", "Planta", 70, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico")]
)

leafeon = Pokemon(
    "Leafeon", ["Planta"], 50,
    {'PS': 167, 'Ataque': 194, 'Defensa': 175, 'AtqEsp': 85, 'DefEsp': 115, 'Velocidad': 125},
    [Movimiento("Hoja Aguda", "Planta", 70, "Físico"),
     Movimiento("Doble Filo", "Normal", 120, "Físico"),
     Movimiento("Tajo Aéreo", "Volador", 75, "Especial"),
     Movimiento("Golpe Cabeza", "Normal", 70, "Físico")]
)

glaceon = Pokemon(
    "Glaceon", ["Hielo"], 50,
    {'PS': 167, 'Ataque': 105, 'Defensa': 135, 'AtqEsp': 182, 'DefEsp': 145, 'Velocidad': 95},
    [Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Foco Resplandor", "Acero", 80, "Especial"),
     Movimiento("Poder Oculto", "Dragón", 60, "Especial")]
)

empoleon = Pokemon(
    "Empoleon", ["Agua", "Acero"], 50,
    {'PS': 177, 'Ataque': 125, 'Defensa': 135, 'AtqEsp': 157, 'DefEsp': 145, 'Velocidad': 95},
    [Movimiento("Surf", "Agua", 90, "Especial"),
     Movimiento("Garra Metal", "Acero", 50, "Físico"),
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Tierra Viva", "Tierra", 90, "Especial")]
)

emboar = Pokemon(
    "Emboar", ["Fuego", "Lucha"], 50,
    {'PS': 227, 'Ataque': 174, 'Defensa': 100, 'AtqEsp': 146, 'DefEsp': 100, 'Velocidad': 100},
    [Movimiento("Lanzallamas", "Fuego", 90, "Especial"),    # MT/BMO
     Movimiento("Giro Fuego", "Fuego", 120, "Físico"),      # Nivel 59
     Movimiento("Terremoto", "Tierra", 100, "Físico"),      # MT/BMO
     Movimiento("A Bocajarro", "Lucha", 120, "Físico")]     # Nivel 66
)

samurott = Pokemon(
    "Samurott", ["Agua"], 50,
    {'PS': 157, 'Ataque': 134, 'Defensa': 116, 'AtqEsp': 142, 'DefEsp': 104, 'Velocidad': 104},
    [Movimiento("Hidrocañón", "Agua", 120, "Especial"),    # Nivel 58
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),     # Nivel 67
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),     # MT/BMO
     Movimiento("Acua Jet", "Agua", 40, "Físico")]          # Nivel 49
)

archeops = Pokemon(
    "Archeops", ["Roca", "Volador"], 50,
    {'PS': 157, 'Ataque': 188, 'Defensa': 106, 'AtqEsp': 150, 'DefEsp': 106, 'Velocidad': 166},
    [Movimiento("Ala de Acero", "Acero", 70, "Físico"),     # Nivel 62
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),     # MT/BMO
     Movimiento("Golpe Cabeza", "Normal", 70, "Físico"),    # Nivel 54
     Movimiento("Pico Taladro", "Volador", 80, "Físico")]   # Nivel 68
)

eelektross = Pokemon(
    "Eelektross", ["Eléctrico"], 50,
    {'PS': 167, 'Ataque': 161, 'Defensa': 107, 'AtqEsp': 141, 'DefEsp': 107, 'Velocidad': 86},
    [Movimiento("Rayo", "Eléctrico", 90, "Especial"),       # MT/BMO
     Movimiento("Voltio Cruel", "Eléctrico", 120, "Físico"),# Nivel 50
     Movimiento("Terremoto", "Tierra", 100, "Físico"),      # MT/BMO
     Movimiento("Cabezazo Ígneo", "Fuego", 120, "Físico")]  # Nivel 75
)

genesect = Pokemon(
    "Genesect", ["Bicho", "Acero"], 50,
    {'PS': 157, 'Ataque': 176, 'Defensa': 141, 'AtqEsp': 166, 'DefEsp': 141, 'Velocidad': 142},
    [Movimiento("Estallido Tecno", "Bicho", 120, "Especial"), # Nivel 50
     Movimiento("Rayo", "Eléctrico", 90, "Especial"),        # MT/BMO
     Movimiento("Cabeza de Hierro", "Acero", 80, "Físico"),   # Nivel 62
     Movimiento("Puño Fuego", "Fuego", 75, "Físico")]         # MT/BMO
)
seismitoad = Pokemon(
    "Seismitoad", ["Agua", "Tierra"], 50,
    {'PS': 212, 'Ataque': 150, 'Defensa': 127, 'AtqEsp': 137, 'DefEsp': 127, 'Velocidad': 126},
    [Movimiento("Cabezazo Ígneo", "Fuego", 120, "Físico"),     # Nivel 75
     Movimiento("Terremoto", "Tierra", 100, "Físico"),         # MT
     Movimiento("Hiperrayo", "Normal", 150, "Especial"),       # MT
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial")]        # MT
)

sigilyph = Pokemon(
    "Sigilyph", ["Psíquico", "Volador"], 50,
    {'PS': 179, 'Ataque': 69, 'Defensa': 132, 'AtqEsp': 170, 'DefEsp': 132, 'Velocidad': 149},
    [Movimiento("Psíquico", "Psíquico", 90, "Especial"),       # MT
     Movimiento("Sombra Vil", "Fantasma", 80, "Especial"),     # MT
     Movimiento("Pájaro Osado", "Volador", 120, "Físico"),     # Nivel 62
     Movimiento("Onda Certera", "Lucha", 120, "Especial")]     # MT
)

vanilluxe = Pokemon(
    "Vanilluxe", ["Hielo"], 50,
    {'PS': 178, 'Ataque': 147, 'Defensa': 137, 'AtqEsp': 167, 'DefEsp': 157, 'Velocidad': 131},
    [Movimiento("Ventisca", "Hielo", 120, "Especial"),         # MT
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),        # Nivel 55
     Movimiento("Lanzallamas", "Fuego", 90, "Especial"),       # MT
     Movimiento("Terremoto", "Tierra", 100, "Físico")]         # MT
)

sawsbuck = Pokemon(
    "Sawsbuck", ["Planta", "Normal"], 50,
    {'PS': 187, 'Ataque': 167, 'Defensa': 122, 'AtqEsp': 112, 'DefEsp': 122, 'Velocidad': 147},
    [Movimiento("Cuerno Férreo", "Normal", 85, "Físico"),      # Nivel 60
     Movimiento("A Bocajarro", "Lucha", 120, "Físico"),        # MT
     Movimiento("Superpoder", "Lucha", 120, "Físico"),         # MT
     Movimiento("Doble Filo", "Normal", 120, "Físico")]        # Nivel 68
)

klinklang = Pokemon(
    "Klinklang", ["Acero"], 50,
    {'PS': 167, 'Ataque': 200, 'Defensa': 147, 'AtqEsp': 182, 'DefEsp': 147, 'Velocidad': 122},
    [Movimiento("Cabeza de Hierro", "Acero", 80, "Físico"),    # Nivel 62
     Movimiento("Chispazo", "Eléctrico", 80, "Especial"),      # MT
     Movimiento("Terratemblor", "Tierra", 100, "Físico"),      # MT
     Movimiento("Rayo Carga", "Eléctrico", 90, "Físico")]      # MT
)
delphox = Pokemon(
    "Delphox", ["Fuego", "Psíquico"], 50,
    {'PS': 146, 'Ataque': 65, 'Defensa': 65, 'AtqEsp': 171, 'DefEsp': 125, 'Velocidad': 150},
    [Movimiento("Llamarada",      "Fuego",    110, "Especial"),  # TM35
     Movimiento("Psíquico",       "Psíquico", 90,  "Especial"),  # TM29
     Movimiento("Psyshock",       "Psiquico", 80,  "Especial"),  # Nivel 46
     Movimiento("Puño Fuego",     "Fuego",    75,  "Físico")]   # TM39
)

chesnaught = Pokemon(
    "Chesnaught", ["Planta", "Lucha"], 50,
    {'PS': 170, 'Ataque': 189, 'Defensa': 135, 'AtqEsp': 85,  'DefEsp': 115, 'Velocidad': 100},
    [Movimiento("Golpe Germen",   "Planta",   80,  "Físico"),   # Nivel 59
     Movimiento("Puño Certero",   "Lucha",    50,  "Físico"),   # TM01
     Movimiento("Martillo Escudo","Lucha",   100,  "Físico"),   # Nivel 54
     Movimiento("Doble Filo",     "Normal",  120,  "Físico")]   # Nivel 68
)

goodra = Pokemon(
    "Goodra", ["Dragón"], 50,
    {'PS': 163, 'Ataque': 100, 'Defensa': 100, 'AtqEsp': 175, 'DefEsp': 150, 'Velocidad':  80},
    [Movimiento("Pulso Dragón",   "Dragón",   85,  "Especial"), # Nivel 44
     Movimiento("Draco Meteor",   "Dragón",  130,  "Especial"), # TM02
     Movimiento("Rayo Hielo",     "Hielo",    90,  "Especial"), # TM13
     Movimiento("Llama Final",    "Fuego",   130,  "Especial")] # TM38
)

aegislash = Pokemon(
    "Aegislash", ["Acero", "Fantasma"], 50,
    {'PS': 163, 'Ataque': 150, 'Defensa': 120, 'AtqEsp': 150, 'DefEsp': 120, 'Velocidad':  60},
    [Movimiento("Espada Sagrada", "Acero",    90,  "Físico"),   # Nivel 50
     Movimiento("Hoja Afilada",   "Acero",    70,  "Físico"),   # TM76
     Movimiento("Sombra Vil",     "Fantasma", 80,  "Especial"), # TM30
     Movimiento("Onda Certera",   "Lucha",   120,  "Especial")] # TM52
)

aurorus = Pokemon(
    "Aurorus", ["Roca", "Hielo"], 50,
    {'PS': 147, 'Ataque': 110, 'Defensa': 100, 'AtqEsp': 155, 'DefEsp': 115, 'Velocidad':  52},
    [Movimiento("Poder Pasado",   "Roca",     60,  "Especial"), # Nivel 45
     Movimiento("Ventisca",       "Hielo",   120,  "Especial"), # TM14
     Movimiento("Vozarrón",       "Normal",   90,  "Especial"), # TM43
     Movimiento("Roca Afilada",   "Roca",     75,  "Físico")]   # TM80
)
tyranntrum = Pokemon(
    "Tyrantrum", ["Roca", "Dragón"], 50,
    {'PS': 166, 'Ataque': 180, 'Defensa': 131, 'AtqEsp': 112, 'DefEsp': 100, 'Velocidad': 91},
    [Movimiento("Cabeza de Hierro", "Acero",    80, "Físico"),  # TM
     Movimiento("Colmillo Dragón",  "Dragón",  100, "Físico"),  # Nivel
     Movimiento("Terremoto",         "Tierra",  100, "Físico"),  # TM
     Movimiento("Enfado",            "Dragón",  120, "Físico")]  # Nivel
)

dragalge = Pokemon(
    "Dragalge", ["Veneno", "Dragón"], 50,
    {'PS': 131, 'Ataque': 86, 'Defensa': 97, 'AtqEsp': 146, 'DefEsp': 119, 'Velocidad': 54},
    [Movimiento("Punta Dragón",     "Dragón",  70,  "Especial"),  # Nivel
     Movimiento("Pulso Draco",       "Dragón",  90,  "Especial"),  # TM
     Movimiento("Bomba Lodo",        "Veneno",  90,  "Especial"),  # TM
     Movimiento("Rayo Hielo",        "Hielo",  90,   "Especial")]  # TM
)

sylveon = Pokemon(
    "Sylveon", ["Hada"], 50,
    {'PS': 146, 'Ataque': 94, 'Defensa': 95, 'AtqEsp': 167, 'DefEsp': 136, 'Velocidad': 90},
    [Movimiento("Brillo Mágico",    "Hada",    90,  "Especial"),  # Nivel
     Movimiento("Psíquico",          "Psíquico", 90,  "Especial"), # TM
     Movimiento("Rayo",              "Eléctrico",90,  "Especial"), # TM
     Movimiento("Hiperrayo",         "Normal",  150,  "Especial")] # TM
)

talonflame = Pokemon(
    "Talonflame", ["Fuego", "Volador"], 50,
    {'PS': 138, 'Ataque': 140, 'Defensa': 94, 'AtqEsp': 109, 'DefEsp': 90, 'Velocidad': 161},
    [Movimiento("Pájaro Osado",     "Volador",  80,  "Físico"),  # Nivel
     Movimiento("Llama Final",      "Fuego",    130, "Físico"),  # MT
     Movimiento("Golpe Aéreo",      "Volador",  75,  "Físico"),  # TM
     Movimiento("Doble Filo",       "Normal",  120,  "Físico")]  # MT
)

heliolisk = Pokemon(
    "Heliolisk", ["Eléctrico", "Normal"], 50,
    {'PS': 131, 'Ataque': 94, 'Defensa': 72, 'AtqEsp': 140, 'DefEsp': 90, 'Velocidad': 132},
    [Movimiento("Rayo",             "Eléctrico", 90,  "Especial"),  # TM
     Movimiento("Bola Sombra",      "Fantasma",  80,  "Especial"),  # TM
     Movimiento("Rayo Solar",       "Planta",    120, "Especial"),  # TM
     Movimiento("Golpe Bajo",       "Lucha",     70,  "Físico")]    # TM
)
dragapult = Pokemon(
    "Dragapult", ["Dragón", "Fantasma"], 50,
    {'PS': 164, 'Ataque': 173, 'Defensa': 106, 'AtqEsp': 173, 'DefEsp': 106, 'Velocidad': 213},
    [Movimiento("Cabeza de Hierro",  "Acero",    80,  "Físico"),  # Nivel
     Movimiento("Pulso Dragón",      "Dragón",  85,  "Especial"), # TM
     Movimiento("Bola Sombra",       "Fantasma", 80,  "Especial"), # TM
     Movimiento("Enfado",            "Dragón", 120,  "Físico")]   # Nivel
)


corviknight = Pokemon(
    "Corviknight", ["Volador", "Acero"], 50,
    {'PS': 177, 'Ataque': 130, 'Defensa': 182, 'AtqEsp': 75, 'DefEsp': 150, 'Velocidad': 88},
    [Movimiento("Pico Taladro", "Volador", 80, "Físico"),        # Nivel
     Movimiento("Cabeza de Hierro", "Acero", 80, "Físico"),      # TM
     Movimiento("Golpe Aéreo", "Volador", 75, "Físico"),         # TM
     Movimiento("Ataque Ala",   "Volador", 60, "Físico")]        # Nivel
)

coalossal = Pokemon(
    "Coalossal", ["Roca", "Fuego"], 50,
    {'PS': 155, 'Ataque': 145, 'Defensa': 147, 'AtqEsp': 75, 'DefEsp': 80, 'Velocidad': 41},
    [Movimiento("Lanzallamas",     "Fuego", 90, "Especial"),   # TM
     Movimiento("Avalancha",       "Roca", 75, "Físico"),      # TM
     Movimiento("Terremoto",       "Tierra", 100, "Físico"),   # TM
     Movimiento("Roca Afilada",    "Roca", 75, "Físico")]      # TM
)

grimmsnarl = Pokemon(
    "Grimmsnarl", ["Siniestro", "Hada"], 50,
    {'PS': 148, 'Ataque': 139, 'Defensa': 86, 'AtqEsp': 93, 'DefEsp': 81, 'Velocidad': 80},
    [Movimiento("Beso Drenaje",    "Hada", 60, "Físico"),      # Nivel
     Movimiento("Golpe Bajo",      "Siniestro", 70, "Físico"), # TM
     Movimiento("Pulso Umbrío",    "Siniestro", 80, "Especial"),# TM
     Movimiento("Carantoña",       "Hada", 40, "Físico")]      # Nivel
)

urshifu = Pokemon(
    "Urshifu", ["Lucha", "Siniestro"], 50,
    {'PS': 177, 'Ataque': 224, 'Defensa': 106, 'AtqEsp': 94, 'DefEsp': 106, 'Velocidad': 144},
    [Movimiento("Puño Incremento",   "Lucha",   15,  "Físico"),  # Movimiento característico (daño, aunque bajo)
     Movimiento("A Bocajarro",       "Lucha",  120,  "Físico"),  # Movimiento característico
     Movimiento("Pulso Umbrío",      "Siniestro",  80,  "Especial"), # TM
     Movimiento("Cuchillada",        "Siniestro",  70,  "Físico")]  # Nivel
)


dracovish = Pokemon(
    "Dracovish", ["Dragón", "Agua"], 50,
    {'PS': 146, 'Ataque': 176, 'Defensa': 90, 'AtqEsp': 80, 'DefEsp': 70, 'Velocidad': 87},
    [Movimiento("Mandíbula Dragón", "Dragón", 100, "Físico"),  # Movimiento característico
     Movimiento("Colmillo Ígneo", "Fuego", 65, "Físico"),      # Movimiento característico
     Movimiento("Hidro Bomba",    "Agua", 110, "Especial"),    # TM
     Movimiento("Rayo Hielo",     "Hielo", 90, "Especial")]    # TM
)

toxtricity = Pokemon(
    "Toxtricity", ["Eléctrico", "Veneno"], 50,
    {'PS': 138, 'Ataque': 152, 'Defensa': 86, 'AtqEsp': 105, 'DefEsp': 95, 'Velocidad': 106},
    [Movimiento("Chispa",       "Eléctrico", 65,  "Especial"),  # Nivel
     Movimiento("Bomba Lodo",   "Veneno",    65,  "Especial"),  # TM
     Movimiento("Rayo",         "Eléctrico", 90,  "Especial"),  # TM
     Movimiento("Voltio Cruel", "Eléctrico", 120, "Especial")]  # Movimiento característico
)

centriskorch = Pokemon(
    "Centriskorch", ["Bicho", "Fuego"], 50,
    {'PS': 137, 'Ataque': 154, 'Defensa': 83, 'AtqEsp': 135, 'DefEsp': 87, 'Velocidad': 94},
    [Movimiento("Lanzallamas",  "Fuego", 90,  "Especial"),  # TM
     Movimiento("Cabezazo",     "Normal", 70,  "Físico"),   # Nivel
     Movimiento("Bomba Germen", "Bicho",  80,  "Especial"), # TM
     Movimiento("Ataque Rápido","Normal", 40,  "Físico")]   # Nivel
)

obstagoon = Pokemon(
    "Obstagoon", ["Siniestro", "Normal"], 50,
    {'PS': 159, 'Ataque': 165, 'Defensa': 110, 'AtqEsp': 60, 'DefEsp': 80, 'Velocidad': 69},
    [Movimiento("Puño Incremento", "Lucha", 40, "Físico"),     # TM
     Movimiento("Cabezazo",        "Normal", 70, "Físico"),    # Nivel
     Movimiento("Corte Furia",     "Siniestro", 80, "Físico"), # TM
     Movimiento("Tajo Cruzado",    "Siniestro", 70, "Físico")] # TM
)

rillaboom = Pokemon(
    "Rillaboom", ["Planta"], 50,
    {'PS': 160, 'Ataque': 163, 'Defensa': 111, 'AtqEsp': 80, 'DefEsp': 90, 'Velocidad': 75},
    [Movimiento("Golpe Cuerpo", "Normal", 75, "Físico"),     # Nivel
     Movimiento("Triturador",   "Siniestro", 80, "Físico"),  # TM
     Movimiento("Fuerza Bruta", "Lucha", 120, "Físico"),    # TM
     Movimiento("Roca Afilada", "Roca", 75, "Físico")]      # TM
)
skeledirge = Pokemon(
    "Skeledirge", ["Fuego", "Fantasma"], 50,
    {'PS': 186, 'Ataque': 105, 'Defensa': 105, 'AtqEsp': 130, 'DefEsp': 115, 'Velocidad': 85},
    [Movimiento("Lanzallamas", "Fuego", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Tajo Umbrío", "Fantasma", 70, "Físico"),
     Movimiento("Rayo Solar", "Planta", 120, "Especial")]
)

annihilape = Pokemon(
    "Annihilape", ["Lucha", "Fantasma"], 50,
    {'PS': 190, 'Ataque': 145, 'Defensa': 105, 'AtqEsp': 80, 'DefEsp': 100, 'Velocidad': 110},
    [Movimiento("Puño Drenaje", "Lucha", 75, "Físico"),
     Movimiento("Puño Sombra", "Fantasma", 60, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico"),
     Movimiento("Avalancha", "Roca", 75, "Físico")]
)

miraidon = Pokemon(
    "Miraidon", ["Eléctrico", "Dragón"], 50,
    {'PS': 175, 'Ataque': 85, 'Defensa': 105, 'AtqEsp': 182, 'DefEsp': 115, 'Velocidad': 120},
    [Movimiento("Electrocañón", "Eléctrico", 120, "Especial"),
     Movimiento("Pulso Dragón", "Dragón", 85, "Especial"),
     Movimiento("Rayo", "Eléctrico", 90, "Especial"),
     Movimiento("Llama Final", "Fuego", 140, "Especial")]
)

chien_pao = Pokemon(
    "Chien-Pao", ["Siniestro", "Hielo"], 50,
    {'PS': 140, 'Ataque': 182, 'Defensa': 95, 'AtqEsp': 80, 'DefEsp': 100, 'Velocidad': 135},
    [Movimiento("Alarido", "Siniestro", 55, "Especial"),
     Movimiento("Carámbano", "Hielo", 85, "Físico"),
     Movimiento("Colmillo Hielo", "Hielo", 65, "Físico"),
     Movimiento("Cuchillada", "Normal", 70, "Físico")]
)

iron_valiant = Pokemon(
    "Iron Valiant", ["Lucha", "Hada"], 50,
    {'PS': 150, 'Ataque': 160, 'Defensa': 95, 'AtqEsp': 115, 'DefEsp': 95, 'Velocidad': 130},
    [Movimiento("Fuerza Bruta", "Lucha", 120, "Físico"),
     Movimiento("Carantoña", "Hada", 90, "Físico"),
     Movimiento("Cabezazo Zen", "Psíquico", 80, "Físico"),
     Movimiento("Sombra Vil", "Fantasma", 40, "Físico")]
)

tinkaton = Pokemon(
    "Tinkaton", ["Hada", "Acero"], 50,
    {'PS': 160, 'Ataque': 110, 'Defensa': 105, 'AtqEsp': 75, 'DefEsp': 95, 'Velocidad': 100},
    [Movimiento("Carantoña", "Hada", 90, "Físico"),
     Movimiento("Cabeza de Hierro", "Acero", 80, "Físico"),
     Movimiento("Puño Fuego", "Fuego", 75, "Físico"),
     Movimiento("Puño Trueno", "Eléctrico", 75, "Físico")]
)

ceruledge = Pokemon(
    "Ceruledge", ["Fuego", "Fantasma"], 50,
    {'PS': 160, 'Ataque': 155, 'Defensa': 100, 'AtqEsp': 80, 'DefEsp': 90, 'Velocidad': 115},
    [Movimiento("Envite Ígneo", "Fuego", 120, "Físico"),
     Movimiento("Sombra Vil", "Fantasma", 40, "Físico"),
     Movimiento("Colmillo Ígneo", "Fuego", 65, "Físico"),
     Movimiento("Cuchillada", "Normal", 70, "Físico")]
)

clodsire = Pokemon(
    "Clodsire", ["Veneno", "Tierra"], 50,
    {'PS': 200, 'Ataque': 100, 'Defensa': 100, 'AtqEsp': 80, 'DefEsp': 120, 'Velocidad': 55},
    [Movimiento("Terremoto", "Tierra", 100, "Físico"),
     Movimiento("Bomba Lodo", "Veneno", 90, "Especial"),
     Movimiento("Rayo Hielo", "Hielo", 90, "Especial"),
     Movimiento("Golpe Cuerpo", "Normal", 85, "Físico")]
)

armarouge = Pokemon(
    "Armarouge", ["Fuego", "Psíquico"], 50,
    {'PS': 160, 'Ataque': 85, 'Defensa': 100, 'AtqEsp': 170, 'DefEsp': 105, 'Velocidad': 100},
    [Movimiento("Llamarada", "Fuego", 110, "Especial"),
     Movimiento("Psíquico", "Psíquico", 90, "Especial"),
     Movimiento("Bola Sombra", "Fantasma", 80, "Especial"),
     Movimiento("Foco Resplandor", "Acero", 80, "Especial")]
)

roaring_moon = Pokemon(
    "Roaring Moon", ["Dragón", "Siniestro"], 50,
    {'PS': 175, 'Ataque': 165, 'Defensa': 105, 'AtqEsp': 90, 'DefEsp': 95, 'Velocidad': 115},
    [Movimiento("Garra Dragón", "Dragón", 80, "Físico"),
     Movimiento("Tajo Umbrío", "Siniestro", 70, "Físico"),
     Movimiento("Avalancha", "Roca", 75, "Físico"),
     Movimiento("Cabeza de Hierro", "Acero", 80, "Físico")]
)


# Lista de enemigos
enemigos_posibles = [tyranitar, skeledirge, annihilape, miraidon, chien_pao, iron_valiant, tinkaton, ceruledge, clodsire, armarouge, roaring_moon, dragapult, corviknight, coalossal, grimmsnarl, urshifu, dracovish, toxtricity, centriskorch, obstagoon, rillaboom, tyranntrum, dragalge, sylveon, talonflame, heliolisk, emboar, delphox, chesnaught, goodra, aegislash, aurorus, seismitoad, sigilyph, vanilluxe, sawsbuck, klinklang, samurott, archeops, eelektross, genesect, stoutland, rotom, gallade, leafeon, glaceon, empoleon, mienshao, haxorus, gothitelle, crustle, darmanitan, zebstrika, incineroar, decidueye, hoopa, noivern, hawlucha, pangoro, greninja, druddigon, darkrai, gardevoir, naganadel, buzzwole, tapu_koko, florges, zeraora, toxapex, smeargle, garchomp, garchomp2, drapion, gastrodon, aggron, froslass, electivire, lucario, milotic, salamence, metagross, charizard, blastoise, alakazam, gengar, snorlax, excadrill, hydreigon, scizor, togekiss, weavile, infernape, gliscor, magnezone, chandelure, krookodile, volcarona, conkeldurr, galvantula, zoroark, serperior]

# Definición de los Pokémon de Cynthia
cintia_sinho = [
    spiritomb,
    roserade,
    gastrodon,
    lucario,
    milotic,
    garchomp2
]

# Definición de los Pokémon de Paul
paul_sinho = [
    aggron,
    drapion,
    ninjask,
    electivire,
    gastrodon,
    froslass
]
equipo_pokemon = [
    serperior, 
    garchomp, 
    meowscarada, 
    metagross,
    milotic,
    lucario]

# Función para seleccionar un personaje
def seleccionar_Reto():
    while True:
        print("\nElige un personaje de batalla:")
        print("1. FronteraBatalla")
        print("2. Cintia Sinho")
        print("3. Paul Sinho")
        print("4. Volver al menú principal")
        opcion = input("Elige una opción (1-4): ")
        if opcion == '1':
            print("Seleccionaste a FronteraBatalla")
            enemigo_random = random.choice(enemigos_posibles)  # Selección de un Pokémon aleatorio
            return enemigo_random  # Aquí devuelves el Pokémon aleatorio de FronteraBatalla
        elif opcion == '2':
            print("Seleccionaste a Cintia Sinho")
            return cintia_sinho  # Aquí se seleccionan los Pokémon de Cynthia
        elif opcion == '3':
            print("Seleccionaste a Paul Sinho")
            return paul_sinho  # Aquí se seleccionan los Pokémon de Paul
        elif opcion == '4':
            return None
        else:
            print("Opción inválida.")

# Función para iniciar la batalla
def iniciar_batalla(jugador, modo):
    print(f"\n¡Modo {modo} activado!")
    puntaje = 0 if modo == "FronteraBatalla" else None

    jugador.ps_actual = jugador.stats['PS']

    while jugador.esta_vivo():
        enemigo = random.choice(enemigos_posibles)
        enemigo.ps_actual = enemigo.stats['PS']
        tipos = ", ".join(enemigo.tipos)
        print(f"\n¡Un nuevo enemigo aparece: {enemigo.nombre} ({tipos})!")

        while jugador.esta_vivo() and enemigo.esta_vivo():
            mov_j = jugador.elegir_movimiento()
            jugador.usar_movimiento(mov_j, enemigo)
            if not enemigo.esta_vivo():
                print(f"\n{enemigo.nombre} ha sido derrotado.")
                if modo == "FronteraBatalla":
                    puntaje += 1
                    jugador.ps_actual = jugador.stats['PS']
                    print(f"{jugador.nombre} se ha curado completamente.")
                break

            mov_e = random.choice(enemigo.movimientos)
            enemigo.usar_movimiento(mov_e, jugador)
            if not jugador.esta_vivo():
                print(f"\n{jugador.nombre} ha sido derrotado...")

    print("\nTu Pokémon ha caído. Fin de FronteraBatalla.")
    if modo == "FronteraBatalla":
        print(f"\nTu puntaje final es: {puntaje}")





def iniciar_batalla_vs_equipo(equipo_jugador, equipo_enemigo, nombre_entrenador, modo):
    print(f"\n¡Modo {nombre_entrenador} activado!")

    puntaje = 0 if modo == "FronteraBatalla" else None

    for jugador in equipo_jugador:
        jugador.ps_actual = jugador.stats['PS']

    jugador_idx = 0

    for enemigo in equipo_enemigo:
        enemigo.ps_actual = enemigo.stats['PS']
        tipos = ", ".join(enemigo.tipos)
        print(f"\n{nombre_entrenador} envía a {enemigo.nombre} ({tipos}) a combatir.")

        while enemigo.esta_vivo():
            if jugador_idx >= len(equipo_jugador):
                print("\nYa no tienes Pokémon disponibles. Has perdido la batalla.")
                return

            jugador = equipo_jugador[jugador_idx]
            if not jugador.esta_vivo():
                jugador_idx += 1
                continue

            print(f"\n¡{jugador.nombre}, te elijo a ti!")

            mov_jugador = jugador.elegir_movimiento()
            jugador.usar_movimiento(mov_jugador, enemigo)
            if not enemigo.esta_vivo():
                print(f"\n{enemigo.nombre} ha sido derrotado.")
                if modo == "FronteraBatalla":
                    puntaje += 1
                break

            mov_enemigo = random.choice(enemigo.movimientos)
            enemigo.usar_movimiento(mov_enemigo, jugador)
            if not jugador.esta_vivo():
                print(f"\n{jugador.nombre} ha sido derrotado...")

    print(f"\n¡Has derrotado a todo el equipo de {nombre_entrenador}! ¡Victoria!")

    if modo == "FronteraBatalla":
        print(f"\nTu puntaje final es: {puntaje}")





# Menú principal
def menu_principal():
    while True:
        print("\n--- Menú ---")
        print("1. Batalla")
        print("2. Salir")
        opcion = input("Elige una opción (1-2): ")
        if opcion == '1':
            modo = None
            # Primero elige el modo de batalla
            print("\nElige un modo de batalla:")
            print("1. FronteraBatalla")
            print("2. Cintia Sinho")
            print("3. Paul Sinho")
            sub = input("Opción (1-3): ")
            if sub == '1':
                modo = "FronteraBatalla"
                jugador = random.choice(enemigos_posibles)
                iniciar_batalla(jugador, modo)

            elif sub == '2':
                modo = "Cintia"
                iniciar_batalla_vs_equipo(equipo_pokemon, cintia_sinho, modo, modo)

            elif sub == '3':
                modo = "Paul"
                iniciar_batalla_vs_equipo(equipo_pokemon, paul_sinho, modo, modo)

            else:
                print("Sub‑opción inválida.")
        elif opcion == '2':
            print("Gracias por jugar. ¡Hasta la próxima!")
            break
        else:
            print("Opción inválida.")



# Llamar a la función principal para comenzar el juego
if __name__ == "__main__":
    menu_principal()