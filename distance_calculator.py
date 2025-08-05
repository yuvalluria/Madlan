from geopy.distance import geodesic

def sort_by_distance(properties, target_location):
    results = []
    for prop in properties:
        if prop.latitude is not None and prop.longitude is not None:
            prop_coords = (prop.latitude, prop.longitude)
            distance = geodesic(prop_coords, target_location).meters
            prop.distance = distance
            results.append(prop)

    results.sort(key=lambda x: x.distance)
    return results[:3]