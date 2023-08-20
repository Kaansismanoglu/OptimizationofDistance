import googlemaps
from datetime import datetime
import itertools


# Google Maps API anahtarınızı buraya girin
API_KEY = 'AIzaSyBFsVou9cjdp6q_m2mLKqKk0Eo_6z-8Mp8'

# Hedef konumları ve başlangıç konumu
locations = [
    "Kızılay, Ankara, Turkey",
    "Taksim Square, Istanbul, Turkey",
    "Alsancak, Izmir, Turkey",
    "Konyaalti Beach, Antalya, Turkey"
]
starting_location = "Ankara, Turkey"

def get_all_routes(api_key, locations, starting_location):
    gmaps = googlemaps.Client(key=api_key)

    all_routes = []

    for permutation in itertools.permutations(locations):
        waypoints = list(permutation)
        waypoints.insert(0, starting_location)

        directions_result = gmaps.directions(
            origin=starting_location,
            destination=starting_location,
            waypoints=waypoints,
            optimize_waypoints=False,
            mode="driving",
            departure_time=datetime.now()
        )

        total_duration = sum(leg['duration']['value'] for leg in directions_result[0]['legs'])
        all_routes.append((directions_result[0]['legs'], total_duration))

    return all_routes

if __name__ == "__main__":
    all_routes = get_all_routes(API_KEY, locations, starting_location)

    print("Tüm rotalar:")
    for route_num, (legs, total_duration) in enumerate(all_routes):
        print(f"Rota {route_num + 1}:")
        for i, leg in enumerate(legs):
            print(f"  {i+1}. Adım: {leg['start_address']} --> {leg['end_address']}, Mesafe: {leg['distance']['text']}, Süre: {leg['duration']['text']}")
        print(f"  Toplam Süre: {total_duration // 60} dakika {total_duration % 60} saniye")

    # En kısa rota
    shortest_route_index = min(range(len(all_routes)), key=lambda i: all_routes[i][1])
    print("\nEn kısa rota:")
    for i, leg in enumerate(all_routes[shortest_route_index][0]):
        print(f"{i+1}. Adım: {leg['start_address']} --> {leg['end_address']}, Mesafe: {leg['distance']['text']}, Süre: {leg['duration']['text']}")
    print(f"Toplam Süre: {all_routes[shortest_route_index][1] // 60} dakika {all_routes[shortest_route_index][1] % 60} saniye")