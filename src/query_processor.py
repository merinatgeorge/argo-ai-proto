import re
from datetime import datetime
from config import REGIONS

class SmartQueryProcessor:
    """Rule-based query processor - No API needed!"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        
        # Query patterns and responses
        self.patterns = {
            'temperature_profile': {
                'keywords': ['temperature', 'temp', 'profile', 'depth'],
                'response_template': "Here's the temperature profile for {location}. The data shows temperatures ranging from {max_temp:.1f}°C at the surface to {min_temp:.1f}°C at depth."
            },
            'salinity_profile': {
                'keywords': ['salinity', 'salt', 'profile'],
                'response_template': "Salinity profile for {location} shows values between {min_sal:.1f} and {max_sal:.1f} PSU (Practical Salinity Units)."
            },
            'float_locations': {
                'keywords': ['float', 'location', 'where', 'position'],
                'response_template': "Found {count} active ARGO floats in the {region}. The floats are collecting oceanographic data including temperature and salinity profiles."
            },
            'comparison': {
                'keywords': ['compare', 'comparison', 'between', 'vs', 'versus'],
                'response_template': "Comparing oceanographic data between regions shows distinct patterns in temperature and salinity distributions."
            },
            'recent_data': {
                'keywords': ['recent', 'latest', 'current', 'now', 'today'],
                'response_template': "Latest data from ARGO floats shows {count} active profiles. The most recent measurements were taken within the last 30 days."
            }
        }
    
    def extract_region(self, query):
        """Extract region from query"""
        query_lower = query.lower()
        
        # Check for specific regions
        if any(word in query_lower for word in ['arabian sea', 'arabian']):
            return 'arabian_sea'
        elif any(word in query_lower for word in ['bay of bengal', 'bengal', 'bay']):
            return 'bay_of_bengal'
        elif any(word in query_lower for word in ['equator', 'equatorial']):
            return 'equator'
        else:
            return 'indian_ocean'
    
    def extract_float_id(self, query):
        """Extract float ID from query"""
        float_pattern = r'(\d{7})'
        matches = re.findall(float_pattern, query)
        return matches[0] if matches else None
    
    def classify_query(self, query):
        """Classify the type of query"""
        query_lower = query.lower()
        
        for query_type, pattern_info in self.patterns.items():
            if any(keyword in query_lower for keyword in pattern_info['keywords']):
                return query_type
                
        return 'general'
    
    def process_query(self, query):
        """Process natural language query and return response + data"""
        query_type = self.classify_query(query)
        region = self.extract_region(query)
        float_id = self.extract_float_id(query)
        
        # Generate appropriate response and data
        if query_type == 'temperature_profile':
            return self.handle_temperature_query(region, float_id)
        elif query_type == 'salinity_profile':
            return self.handle_salinity_query(region, float_id)
        elif query_type == 'float_locations':
            return self.handle_location_query(region)
        elif query_type == 'comparison':
            return self.handle_comparison_query(query)
        else:
            return self.handle_general_query(region)
    
    def handle_temperature_query(self, region, float_id=None):
        """Handle temperature-related queries"""
        if float_id:
            profiles = self.data_loader.get_profile_data(float_id, 1)
            if profiles:
                profile = profiles[0]
                return {
                    'response': f"Temperature profile for ARGO float {float_id}: Surface temperature is {profile['temperatures'][0]:.1f}°C, decreasing to {profile['temperatures'][-1]:.1f}°C at {profile['depths'][-1]}m depth.",
                    'data': profile,
                    'visualization_type': 'temperature_profile',
                    'title': f"Temperature Profile - Float {float_id}"
                }
        
        # Regional temperature data
        floats = self.data_loader.get_floats_by_region(region)
        if floats:
            sample_float = floats[0]
            profiles = self.data_loader.get_profile_data(sample_float['id'], 1)
            if profiles:
                return {
                    'response': f"Temperature profiles in {REGIONS[region]['name']} show typical tropical ocean patterns with warm surface waters (~{profiles[0]['temperatures'][0]:.1f}°C) and cooler deep waters.",
                    'data': profiles[0],
                    'visualization_type': 'temperature_profile',
                    'title': f"Temperature Profile - {REGIONS[region]['name']}"
                }
        
        return {'response': "No temperature data available for the specified criteria.", 'data': None}
    
    def handle_location_query(self, region):
        """Handle float location queries"""
        floats = self.data_loader.get_floats_by_region(region)
        active_floats = [f for f in floats if f['status'] == 'Active']
        
        return {
            'response': f"Found {len(active_floats)} active ARGO floats in the {REGIONS[region]['name']}. These floats are continuously collecting temperature and salinity data from the ocean surface to 2000m depth.",
            'data': floats,
            'visualization_type': 'float_map',
            'title': f"ARGO Float Locations - {REGIONS[region]['name']}"
        }
    
    def handle_comparison_query(self, query):
        """Handle comparison queries"""
        arabian_floats = self.data_loader.get_floats_by_region('arabian_sea')
        bengal_floats = self.data_loader.get_floats_by_region('bay_of_bengal')
        
        return {
            'response': f"Regional comparison: Arabian Sea has {len(arabian_floats)} floats while Bay of Bengal has {len(bengal_floats)} floats. The Arabian Sea typically shows higher salinity due to increased evaporation rates.",
            'data': {'arabian_sea': arabian_floats, 'bay_of_bengal': bengal_floats},
            'visualization_type': 'comparison_map',
            'title': "Regional Comparison - Arabian Sea vs Bay of Bengal"
        }
    
    def handle_general_query(self, region):
        """Handle general queries"""
        floats = self.data_loader.get_floats_by_region(region)
        return {
            'response': f"The {REGIONS[region]['name']} has {len(floats)} ARGO floats providing valuable oceanographic data. These autonomous instruments measure temperature, salinity, and pressure profiles from surface to 2000m depth every 10 days.",
            'data': floats,
            'visualization_type': 'float_map',
            'title': f"ARGO Network - {REGIONS[region]['name']}"
        }