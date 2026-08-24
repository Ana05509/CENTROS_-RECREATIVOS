import requests
from django.core.management.base import BaseCommand

from rutas.models import Ruta, TipoTransporte

# Servidores públicos de ruteo OSRM (sin API key). El proyecto OSRM solo
# aloja el perfil "driving"; a pie/bicicleta usan el demo de openstreetmap.de.
URL_POR_PERFIL = {
    TipoTransporte.VEHICULO: "https://router.project-osrm.org/route/v1/driving/{}",
    TipoTransporte.BUS: "https://router.project-osrm.org/route/v1/driving/{}",
    TipoTransporte.A_PIE: "https://routing.openstreetmap.de/routed-foot/route/v1/foot/{}",
    TipoTransporte.BICICLETA: "https://routing.openstreetmap.de/routed-bike/route/v1/bike/{}",
}


class Command(BaseCommand):
    help = (
        "Recalcula el trazado de cada Ruta para que siga calles reales "
        "(en vez de la línea recta entre 2-3 puntos), usando el mismo "
        "estilo de ruteo que el botón 'Cómo llegar' del mapa."
    )

    def handle(self, *args, **options):
        actualizadas = 0
        fallidas = 0

        for ruta in Ruta.objects.select_related("lugar").all():
            if not ruta.trazado:
                self.stdout.write(self.style.WARNING(f"⏭️  {ruta.nombre}: sin trazado inicial, se omite"))
                continue

            origen = ruta.trazado[0]  # [lat, lng]
            destino = [ruta.lugar.latitud, ruta.lugar.longitud]
            coords = f"{origen[1]},{origen[0]};{destino[1]},{destino[0]}"

            url_tpl = URL_POR_PERFIL.get(ruta.tipo_transporte, URL_POR_PERFIL[TipoTransporte.VEHICULO])
            url = url_tpl.format(coords)

            try:
                resp = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                if data.get("code") != "Ok" or not data.get("routes"):
                    raise ValueError(data.get("message", "el servicio no devolvió rutas"))

                geometria = data["routes"][0]["geometry"]["coordinates"]  # [[lng, lat], ...]
                ruta.trazado = [[lat, lng] for lng, lat in geometria]
                ruta.distancia_km = round(data["routes"][0]["distance"] / 1000, 2)
                ruta.tiempo_estimado = f"{round(data['routes'][0]['duration'] / 60)} min"
                ruta.save(update_fields=["trazado", "distancia_km", "tiempo_estimado"])

                actualizadas += 1
                self.stdout.write(self.style.SUCCESS(
                    f"✔️  {ruta.nombre}: {len(ruta.trazado)} puntos, "
                    f"{ruta.distancia_km} km, {ruta.tiempo_estimado}"
                ))
            except Exception as exc:
                fallidas += 1
                self.stdout.write(self.style.ERROR(f"✗ {ruta.nombre}: {exc}"))

        self.stdout.write(f"\nListo: {actualizadas} actualizadas, {fallidas} fallidas.")
