from lugares.models import Lugar
from rutas.models import Ruta, TipoTransporte

# ==============================
# LIMPIAR TABLA
# ==============================
Ruta.objects.all().delete()

# ==============================
# RUTAS DE ACCESO (trazado simplificado: punto de partida -> destino)
# ==============================
rutas = [
    {
        "nombre": "Ruta al Parque Central",
        "lugar": "Parque Central de La Maná",
        "punto_partida": "Terminal Terrestre La Maná",
        "descripcion": "Acceso directo desde el terminal por la avenida principal.",
        "tipo_transporte": TipoTransporte.A_PIE,
        "distancia_km": 0.8,
        "tiempo_estimado": "10 min",
        "trazado": [[-0.9408, -79.2295], [-0.9420, -79.2305], [-0.9431, -79.2312]],
    },
    {
        "nombre": "Ruta a Siete Cascadas (Zapanal)",
        "lugar": "Siete Cascadas (Zapanal)",
        "punto_partida": "Parque Central de La Maná",
        "descripcion": "Vía Zapanal, camino de tercer orden con parqueadero al final.",
        "tipo_transporte": TipoTransporte.VEHICULO,
        "distancia_km": 12.5,
        "tiempo_estimado": "35 min",
        "trazado": [[-0.9431, -79.2312], [-0.9250, -79.1950], [-0.9085, -79.1643]],
    },
    {
        "nombre": "Ruta al Río San Pablo",
        "lugar": "Río San Pablo",
        "punto_partida": "Puente sobre el Río San Pablo",
        "descripcion": "Acceso corto desde el puente hacia la orilla del río.",
        "tipo_transporte": TipoTransporte.A_PIE,
        "distancia_km": 1.2,
        "tiempo_estimado": "15 min",
        "trazado": [[-0.9390, -79.2260], [-0.9403, -79.2270], [-0.9415, -79.2280]],
    },
    {
        "nombre": "Ruta a Termas de Yanayacu",
        "lugar": "Termas de Yanayacu",
        "punto_partida": "Vía E30 (La Maná - Latacunga)",
        "descripcion": "Desvío desde la vía principal hacia la zona rural este.",
        "tipo_transporte": TipoTransporte.VEHICULO,
        "distancia_km": 22.0,
        "tiempo_estimado": "50 min",
        "trazado": [[-0.9320, -79.2150], [-0.9000, -79.1600], [-0.8640, -79.0980]],
    },
]

for r in rutas:
    lugar = Lugar.objects.get(nombre=r.pop("lugar"))
    Ruta.objects.create(lugar=lugar, **r)

print(f"✔️ {len(rutas)} rutas cargadas")
