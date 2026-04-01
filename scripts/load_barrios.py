import json
import math
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR / 'mi_proyecto'

sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

import django  # noqa: E402

django.setup()

from Proyecto_Soderia.models import Barrio  # noqa: E402


def iter_points(coords):
    # coords for MultiPolygon: [ [ [ [lon,lat], ... ] , ... ] , ... ]
    for polygon in coords:
        for ring in polygon:
            for point in ring:
                if len(point) >= 2:
                    yield point[0], point[1]


def centroid_of_coords(coords):
    count = 0
    sum_lon = 0.0
    sum_lat = 0.0
    for lon, lat in iter_points(coords):
        sum_lon += lon
        sum_lat += lat
        count += 1
    if count == 0:
        return None
    return (sum_lon / count, sum_lat / count)


def main():
    data_path = BASE_DIR / 'barrios.txt'
    with data_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    features = data.get('features') or []
    feature_centroids = []
    for feat in features:
        coords = ((feat.get('geometry') or {}).get('coordinates')) or []
        c = centroid_of_coords(coords)
        if c is not None:
            feature_centroids.append(c)

    if not feature_centroids:
        print('No centroids found. Aborting.')
        return

    center_lon = sum(c[0] for c in feature_centroids) / len(feature_centroids)
    center_lat = sum(c[1] for c in feature_centroids) / len(feature_centroids)

    # max distance for thresholds
    max_dist = 0.0
    for lon, lat in feature_centroids:
        d = math.hypot(lon - center_lon, lat - center_lat)
        if d > max_dist:
            max_dist = d

    if max_dist == 0:
        print('All centroids identical. Aborting.')
        return

    centro_thresh = 0.2 * max_dist
    interior_thresh = 0.8 * max_dist

    created = 0
    skipped = 0
    no_coords = 0

    for feat in features:
        props = feat.get('properties') or {}
        nombre = (props.get('barrio') or '').strip()
        if not nombre:
            skipped += 1
            continue

        if Barrio.objects.filter(nombre=nombre).exists():
            # Option A: keep first, skip duplicates
            skipped += 1
            continue

        coords = ((feat.get('geometry') or {}).get('coordinates')) or []
        c = centroid_of_coords(coords)
        if c is None:
            no_coords += 1
            continue

        lon, lat = c
        d = math.hypot(lon - center_lon, lat - center_lat)

        if d <= centro_thresh:
            zona = 'Centro'
        elif d >= interior_thresh:
            zona = 'Interior'
        else:
            dlat = lat - center_lat
            dlon = lon - center_lon
            if abs(dlat) >= abs(dlon):
                zona = 'Norte' if dlat >= 0 else 'Sur'
            else:
                zona = 'Este' if dlon >= 0 else 'Oeste'

        Barrio.objects.create(nombre=nombre, zona=zona, active=True)
        created += 1

    print(f'Centroide dataset: ({center_lon:.6f}, {center_lat:.6f})')
    print(f'Created: {created}')
    print(f'Skipped (duplicates/empty): {skipped}')
    print(f'Skipped (no coords): {no_coords}')


if __name__ == '__main__':
    main()
