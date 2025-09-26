# Configuration - No API keys needed!
APP_TITLE = "AI-Powered ARGO Ocean Data Explorer"
APP_SUBTITLE = "Natural Language Interface for Oceanographic Data (Prototype)"

# Sample float data for Indian Ocean
SAMPLE_FLOATS = [
    {"id": "2902746", "lat": 15.2, "lon": 68.5, "status": "Active", "deployment": "2023-01-15", "cycles": 45},
    {"id": "2902747", "lat": 12.8, "lon": 75.3, "status": "Active", "deployment": "2023-02-20", "cycles": 38},
    {"id": "2902748", "lat": 8.1, "lon": 73.2, "status": "Inactive", "deployment": "2022-11-10", "cycles": 67},
    {"id": "2902749", "lat": 20.5, "lon": 70.1, "status": "Active", "deployment": "2023-03-05", "cycles": 32},
    {"id": "2902750", "lat": 6.3, "lon": 79.8, "status": "Active", "deployment": "2023-01-28", "cycles": 41},
    {"id": "2902751", "lat": 18.7, "lon": 63.2, "status": "Active", "deployment": "2023-04-12", "cycles": 28},
    {"id": "2902752", "lat": 10.4, "lon": 77.6, "status": "Active", "deployment": "2023-02-08", "cycles": 35}
]

# Predefined regions
REGIONS = {
    "arabian_sea": {"lat_range": [10, 25], "lon_range": [55, 80], "name": "Arabian Sea"},
    "bay_of_bengal": {"lat_range": [5, 22], "lon_range": [80, 100], "name": "Bay of Bengal"},
    "indian_ocean": {"lat_range": [-10, 30], "lon_range": [40, 100], "name": "Indian Ocean"},
    "equator": {"lat_range": [-5, 5], "lon_range": [40, 100], "name": "Near Equator"}
}