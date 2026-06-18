from lugares.models import Lugar, Categoria
from django.contrib.auth.models import User


# ==============================
# 🔥 CATEGORÍAS OFICIALES (ÚNICAS)
# ==============================
CATEGORY_MAP = {
    "Canchas Deportivas": "Canchas Deportivas",
    "Deportivo": "Canchas Deportivas",

    "Área de Camping": "Área de Camping",

    "Hotel": "Centros Vacacionales",
    "Hotel / Piscinas": "Centros Vacacionales",

    "Mirador": "Miradores",

    "Parque Acuático": "Piscinas",
    "Piscinas Naturales": "Piscinas",

    "Balneario": "Balnearios",
    "Poza Natural": "Balnearios",
    "Aguas Termales": "Balnearios",

    "Río": "Ríos",

    "Cascada": "Cascadas",
    "Aventura": "Cascadas",

    "Complejo Turístico": "Complejos Turísticos",
    "Eco-turismo": "Complejos Turísticos",
    "Recreación": "Complejos Turísticos",

    "Parque Central": "Parques Recreativos",
    "Urbano": "Parques Recreativos",
    "Turismo Rural": "Parques Recreativos",
    "Geológico": "Parques Recreativos",
}


# ==============================
# 🔧 FUNCIONES
# ==============================
def get_categoria(nombre):
    nombre_normalizado = CATEGORY_MAP.get(nombre, "Parques Recreativos")
    categoria, _ = Categoria.objects.get_or_create(nombre=nombre_normalizado)
    return categoria


def get_admin_user():
    return User.objects.filter(is_superuser=True).first()


# ==============================
# 🧹 LIMPIAR TABLA
# ==============================
Lugar.objects.all().delete()


# ==============================
# 📌 LUGARES (TU DATA ORIGINAL)
# ==============================
lugares = [
    {
        "nombre": "Siete Cascadas (Zapanal)",
        "categoria": "Cascada",
        "latitud": -0.9085,
        "longitud": -79.1643,
        "direccion": "Zapanal, La Maná",
        "horario": "08:00 - 18:00",
        "costo": 2.00,
        "descripcion": "Cascadas naturales con senderos y parqueadero."
    },
    {
        "nombre": "Río San Pablo",
        "categoria": "Río",
        "latitud": -0.9415,
        "longitud": -79.2280,
        "direccion": "San Pablo, La Maná",
        "horario": "07:00 - 18:00",
        "costo": 0.00,
        "descripcion": "Balneario natural de fácil acceso."
    },
    {
        "nombre": "Río Calope",
        "categoria": "Río",
        "latitud": -0.9320,
        "longitud": -79.2150,
        "direccion": "Vía E30, La Maná",
        "horario": "08:00 - 17:00",
        "costo": 0.00,
        "descripcion": "Río junto a carretera principal."
    },
    {
        "nombre": "Río Quindigua",
        "categoria": "Río",
        "latitud": -0.8920,
        "longitud": -79.2085,
        "direccion": "Zona rural La Maná",
        "horario": "08:00 - 17:00",
        "costo": 0.00,
        "descripcion": "Río de caudal natural."
    },
    {
        "nombre": "Cueva de los Murciélagos",
        "categoria": "Cascada",
        "latitud": -0.9210,
        "longitud": -79.1915,
        "direccion": "Zona rural La Maná",
        "horario": "09:00 - 16:00",
        "costo": 1.50,
        "descripcion": "Cueva natural con recorrido guiado."
    },
    {
        "nombre": "Paraíso Escondido",
        "categoria": "Complejo Turístico",
        "latitud": -0.8755,
        "longitud": -79.1410,
        "direccion": "Sector rural La Maná",
        "horario": "08:00 - 20:00",
        "costo": 5.00,
        "descripcion": "Piscinas y áreas verdes."
    },
    {
        "nombre": "Balneario El Rinconcito",
        "categoria": "Balneario",
        "latitud": -0.9510,
        "longitud": -79.2430,
        "direccion": "La Maná",
        "horario": "08:00 - 18:00",
        "costo": 1.00,
        "descripcion": "Pozas naturales familiares."
    },
    {
        "nombre": "Balneario El Paraíso",
        "categoria": "Piscinas Naturales",
        "latitud": -0.9540,
        "longitud": -79.2195,
        "direccion": "La Maná",
        "horario": "08:00 - 18:00",
        "costo": 2.00,
        "descripcion": "Aguas cristalinas."
    },
    {
        "nombre": "Glamping El Cacahual",
        "categoria": "Eco-turismo",
        "latitud": -0.9242,
        "longitud": -79.1985,
        "direccion": "Zona rural La Maná",
        "horario": "24 horas",
        "costo": 25.00,
        "descripcion": "Experiencia de glamping."
    },
    {
        "nombre": "Minas de Mármol",
        "categoria": "Geológico",
        "latitud": -0.8850,
        "longitud": -79.1220,
        "direccion": "Zona montañosa La Maná",
        "horario": "07:00 - 17:00",
        "costo": 0.00,
        "descripcion": "Paisajes de mármol."
    },
    {
        "nombre": "Cascada del Oso",
        "categoria": "Cascada",
        "latitud": -0.9030,
        "longitud": -79.1590,
        "direccion": "Zona rural",
        "horario": "08:00 - 17:00",
        "costo": 1.50,
        "descripcion": "Sendero ecológico."
    },
    {
        "nombre": "Hostería Carlos Patricio",
        "categoria": "Hotel / Piscinas",
        "latitud": -0.9585,
        "longitud": -79.2512,
        "direccion": "La Maná",
        "horario": "08:00 - 22:00",
        "costo": 6.00,
        "descripcion": "Piscinas y hospedaje."
    },
    {
        "nombre": "Hostería Somagg",
        "categoria": "Parque Acuático",
        "latitud": -0.9235,
        "longitud": -79.2590,
        "direccion": "Vía E30",
        "horario": "08:00 - 18:00",
        "costo": 5.00,
        "descripcion": "Toboganes y piscinas."
    },
    {
        "nombre": "Piscina de Piedra",
        "categoria": "Balneario",
        "latitud": -0.9565,
        "longitud": -79.2210,
        "direccion": "La Maná",
        "horario": "08:00 - 18:00",
        "costo": 2.00,
        "descripcion": "Piscina natural."
    },
    {
        "nombre": "Quinta Aurelio Angueta",
        "categoria": "Balneario",
        "latitud": -0.9525,
        "longitud": -79.2480,
        "direccion": "La Maná",
        "horario": "08:00 - 18:00",
        "costo": 2.00,
        "descripcion": "Ambiente familiar."
    },
    {
        "nombre": "Complejo Recreativo Moreno",
        "categoria": "Recreación",
        "latitud": -0.9402,
        "longitud": -79.2395,
        "direccion": "Zona urbana La Maná",
        "horario": "08:00 - 18:00",
        "costo": 1.50,
        "descripcion": "Área recreativa."
    },
    {
        "nombre": "Cascada del Milagro",
        "categoria": "Cascada",
        "latitud": -0.8995,
        "longitud": -79.1380,
        "direccion": "Zona montañosa",
        "horario": "08:00 - 17:00",
        "costo": 2.00,
        "descripcion": "Sendero exigente."
    },
    {
        "nombre": "Balneario El Cacagual",
        "categoria": "Balneario",
        "latitud": -0.9550,
        "longitud": -79.2505,
        "direccion": "La Maná",
        "horario": "08:00 - 18:00",
        "costo": 1.00,
        "descripcion": "Poza comunitaria."
    },
    {
        "nombre": "Hostería Las Pirámides",
        "categoria": "Hotel",
        "latitud": -0.9348,
        "longitud": -79.2410,
        "direccion": "Zona urbana",
        "horario": "08:00 - 22:00",
        "costo": 6.00,
        "descripcion": "Hospedaje y piscinas."
    },
    {
        "nombre": "Parque Central de La Maná",
        "categoria": "Urbano",
        "latitud": -0.9431,
        "longitud": -79.2312,
        "direccion": "Centro de La Maná",
        "horario": "Siempre abierto",
        "costo": 0.00,
        "descripcion": "Parque central."
    },
    {
        "nombre": "Parque La Pista",
        "categoria": "Deportivo",
        "latitud": -0.9388,
        "longitud": -79.2345,
        "direccion": "Zona urbana",
        "horario": "06:00 - 22:00",
        "costo": 0.00,
        "descripcion": "Área deportiva."
    },
    {
        "nombre": "Termas de Yanayacu",
        "categoria": "Aguas Termales",
        "latitud": -0.8640,
        "longitud": -79.0980,
        "direccion": "Zona rural",
        "horario": "08:00 - 18:00",
        "costo": 3.00,
        "descripcion": "Aguas medicinales."
    },
    {
        "nombre": "Poza de Chimbilaco",
        "categoria": "Poza Natural",
        "latitud": -0.9120,
        "longitud": -79.1760,
        "direccion": "Zona rural",
        "horario": "08:00 - 17:00",
        "costo": 1.00,
        "descripcion": "Poza natural."
    },
    {
        "nombre": "Las Chozas (Estero Hondo)",
        "categoria": "Turismo Rural",
        "latitud": -0.9170,
        "longitud": -79.1830,
        "direccion": "Zona rural",
        "horario": "08:00 - 18:00",
        "costo": 2.00,
        "descripcion": "Comida típica."
    },
    {
        "nombre": "Cueva de los Tayos (La Maná)",
        "categoria": "Aventura",
        "latitud": -0.8510,
        "longitud": -79.1110,
        "direccion": "Zona montañosa",
        "horario": "09:00 - 16:00",
        "costo": 3.00,
        "descripcion": "Exploración guiada."
    },
    {
        "nombre": "Hostería Villa Valle Verde",
        "categoria": "Hotel",
        "latitud": -0.9490,
        "longitud": -79.2575,
        "direccion": "La Maná",
        "horario": "08:00 - 22:00",
        "costo": 5.00,
        "descripcion": "Piscinas y áreas verdes."
    },
    {
        "nombre": "Cascada Guadual",
        "categoria": "Cascada",
        "latitud": -0.6533,
        "longitud": -79.0692,
        "direccion": "Pucayacu",
        "horario": "08:00 - 17:00",
        "costo": 2.00,
        "descripcion": "Gran cascada."
    },
    {
        "nombre": "Mirador Pucayacu",
        "categoria": "Mirador",
        "latitud": -0.6780,
        "longitud": -79.1020,
        "direccion": "Pucayacu",
        "horario": "06:00 - 19:00",
        "costo": 0.00,
        "descripcion": "Vista panorámica."
    },
    {
        "nombre": "Cascada de Brasil",
        "categoria": "Cascada",
        "latitud": -0.6410,
        "longitud": -79.0550,
        "direccion": "Zona rural",
        "horario": "08:00 - 17:00",
        "costo": 2.00,
        "descripcion": "Sendero natural."
    },
    {
        "nombre": "Hostería D'Patrick's",
        "categoria": "Hotel",
        "latitud": -0.9465,
        "longitud": -79.2490,
        "direccion": "La Maná",
        "horario": "08:00 - 22:00",
        "costo": 6.00,
        "descripcion": "Restaurante y hospedaje."
    }
]


# ==============================
# 🚀 INSERTAR EN BD
# ==============================
for l in lugares:
    categoria = get_categoria(l["categoria"])

    Lugar.objects.create(
        nombre=l["nombre"],
        descripcion=l["descripcion"],
        direccion=l["direccion"],
        latitud=l["latitud"],
        longitud=l["longitud"],
        horario=l["horario"],
        costo_entrada=l["costo"],
        categoria=categoria,
        creado_por=get_admin_user()
    )

print("✔️ Todos los lugares cargados con SOLO 10 categorías oficiales")