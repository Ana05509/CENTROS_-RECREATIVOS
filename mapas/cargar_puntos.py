from mapas.models import PuntoInteres, TipoPunto

# ==============================
# LIMPIAR TABLA
# ==============================
PuntoInteres.objects.all().delete()

# ==============================
# PUNTOS DE INTERÉS (recursos naturales e infraestructura)
# ==============================
puntos = [
    {
        "nombre": "Hospital Básico La Maná",
        "tipo": TipoPunto.INFRAESTRUCTURA,
        "subtipo": "Hospital",
        "latitud": -0.9445,
        "longitud": -79.2288,
        "descripcion": "Centro de salud público del cantón.",
    },
    {
        "nombre": "Terminal Terrestre La Maná",
        "tipo": TipoPunto.INFRAESTRUCTURA,
        "subtipo": "Terminal",
        "latitud": -0.9408,
        "longitud": -79.2295,
        "descripcion": "Terminal de transporte interprovincial.",
    },
    {
        "nombre": "Puente sobre el Río San Pablo",
        "tipo": TipoPunto.INFRAESTRUCTURA,
        "subtipo": "Puente",
        "latitud": -0.9390,
        "longitud": -79.2260,
        "descripcion": "Acceso principal hacia la zona rural sur.",
    },
    {
        "nombre": "Vía E30 (La Maná - Latacunga)",
        "tipo": TipoPunto.INFRAESTRUCTURA,
        "subtipo": "Vía principal",
        "latitud": -0.9320,
        "longitud": -79.2150,
        "descripcion": "Carretera principal de acceso al cantón.",
    },
    {
        "nombre": "Bosque protector Zapanal",
        "tipo": TipoPunto.RECURSO_NATURAL,
        "subtipo": "Bosque",
        "latitud": -0.9070,
        "longitud": -79.1620,
        "descripcion": "Área de bosque que rodea las Siete Cascadas.",
    },
    {
        "nombre": "Cuenca del Río Calope",
        "tipo": TipoPunto.RECURSO_NATURAL,
        "subtipo": "Cuenca hidrográfica",
        "latitud": -0.9300,
        "longitud": -79.2130,
        "descripcion": "Cuenca que abastece a varios balnearios de la zona.",
    },
    {
        "nombre": "Zona montañosa de Pucayacu",
        "tipo": TipoPunto.RECURSO_NATURAL,
        "subtipo": "Montaña",
        "latitud": -0.6650,
        "longitud": -79.0850,
        "descripcion": "Relieve montañoso donde nacen varias cascadas.",
    },
]

for p in puntos:
    PuntoInteres.objects.create(**p)

print(f"✔️ {len(puntos)} puntos de interés cargados")
