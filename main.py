To create an intelligent tool like an "Eco-Commute-Planner" in Python, we need to integrate multiple functionalities, such as route optimization, cost and carbon footprint analysis, and real-time data fetching. Since real-time data and map services require external APIs, we'll use services like OpenStreetMap for routing and a hypothetical real-time data API for cost and emissions.

Below is a simplified version of the program. In a production environment, you would need to set up API credentials and ensure compliance with the terms of service of any third-party APIs you use:

```python
import requests
from geopy.distance import geodesic

# Constants for API endpoints
OSM_ROUTING_API_URL = "http://router.project-osrm.org/route/v1/driving"
REALTIME_DATA_API_URL = "http://example.com/realtimeData"  # Hypothetical endpoint

# Hypothetical emission factors for demonstration purposes
EMISSION_FACTORS = {
    'car': 0.271,  # kg CO2 per km
    'bus': 0.105,
    'bike': 0.0,
    'walk': 0.0
}

# Function to fetch a route from OpenStreetMap routing service
def fetch_route(start_coords, end_coords, mode='driving'):
    try:
        response = requests.get(
            f"{OSM_ROUTING_API_URL}/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}",
            params={"geometries": "geojson", "overview": "simplified"}
        )
        response.raise_for_status()
        data = response.json()

        if 'routes' in data and data['routes']:
            return data['routes'][0]
        else:
            raise Exception("No route found")
    except requests.RequestException as e:
        print(f"Error fetching route: {e}")
        return None

# Function to simulate fetching real-time data
def fetch_realtime_data(mode):
    # Simulate API request
    try:
        # This is hypothetical, would actually hit a real API
        response = requests.get(REALTIME_DATA_API_URL, params={"mode": mode})
        response.raise_for_status()
        # Simulate response
        data = response.json()  # This should be the result of the API call
        return data.get('cost'), data.get('emissions')
    except requests.RequestException as e:
        print(f"Error fetching real-time data: {e}")
        return None, None

# Function to calculate emissions for a route
def calculate_emissions(distance_km, mode):
    emission_factor = EMISSION_FACTORS.get(mode)
    if emission_factor is None:
        print(f"Emission factor for mode '{mode}' not found")
        return None
    return distance_km * emission_factor

def main():
    # User input for locations
    start_location = (40.712776, -74.005974)  # For example, New York City coordinates
    end_location = (34.052235, -118.243683)  # For example, Los Angeles coordinates
    mode = 'car'  # Modes can be 'car', 'bus', 'bike', 'walk'

    # Fetch the route
    route = fetch_route(start_location, end_location, mode)

    if not route:
        print("Couldn't retrieve the route.")
        return

    # Calculate distance
    distance_km = route['distance'] / 1000.0  # Convert meters to kilometers

    # Fetch real-time cost and emissions data
    real_time_cost, _ = fetch_realtime_data(mode)

    # Calculate emissions
    estimated_emissions = calculate_emissions(distance_km, mode)

    # Display results
    print(f"Route from {start_location} to {end_location} via {mode}:")
    print(f"Distance: {distance_km:.2f} km")
    if real_time_cost:
        print(f"Estimated cost: ${real_time_cost:.2f}")
    if estimated_emissions is not None:
        print(f"Estimated emissions: {estimated_emissions:.2f} kg CO2")

if __name__ == "__main__":
    main()
```

### Explanation:
1. **Data Fetching**: The program uses placeholder URLs and data for routing (`fetch_route`) and for real-time data (`fetch_realtime_data`). In a real-world situation, replace these with actual API endpoints and parse the response appropriately.

2. **Emission Calculation**: The program calculates emissions based on the distance and the type of transport using predefined emission factors.

3. **Error Handling**: The code includes basic error handling for HTTP requests using `try-except` blocks and checks for valid data in the response.

4. **Input/Outputs**: The code uses predefined start and end location coordinates; these should be derived from user input in real applications.

5. **Assumptions**: We assume a real-time data API exists and that the structure of responses is consistent. Adjustments will be needed for specific API formats.