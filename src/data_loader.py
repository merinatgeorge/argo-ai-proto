import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from config import SAMPLE_FLOATS, REGIONS

class ArgoDataGenerator:
    def __init__(self):
        self.floats = SAMPLE_FLOATS
        random.seed(42)  # Consistent data for demo
        
    def generate_temperature_profile(self, surface_temp=28):
        """Generate realistic temperature profile"""
        depths = np.arange(0, 2000, 50)
        temperatures = []
        
        for depth in depths:
            if depth <= 50:  # Mixed layer
                temp = surface_temp + random.uniform(-1, 1)
            elif depth <= 200:  # Thermocline
                temp = surface_temp - (depth - 50) * 0.1 + random.uniform(-2, 2)
            else:  # Deep water
                temp = max(2, surface_temp - 20 - (depth - 200) * 0.002) + random.uniform(-1, 1)
            temperatures.append(max(2, temp))  # Ocean temp never below 2°C
            
        return depths, temperatures
    
    def generate_salinity_profile(self, surface_salinity=35):
        """Generate realistic salinity profile"""
        depths = np.arange(0, 2000, 50)
        salinities = []
        
        for depth in depths:
            if depth <= 100:
                sal = surface_salinity + random.uniform(-0.5, 0.5)
            else:
                sal = surface_salinity + random.uniform(-1, 1)
            salinities.append(max(30, min(38, sal)))  # Realistic salinity bounds
            
        return depths, salinities
    
    def get_profile_data(self, float_id, months_back=6):
        """Generate profile data for a specific float"""
        float_info = next((f for f in self.floats if f['id'] == float_id), None)
        if not float_info:
            return None
            
        profiles = []
        for i in range(months_back):
            date = datetime.now() - timedelta(days=30*i + random.randint(0, 10))
            
            # Vary temperature by season and location
            seasonal_factor = np.sin(2 * np.pi * date.timetuple().tm_yday / 365.25) * 3
            base_temp = 26 + seasonal_factor + (float_info['lat'] - 10) * 0.2
            
            depths, temps = self.generate_temperature_profile(base_temp)
            _, salinities = self.generate_salinity_profile()
            
            profiles.append({
                'date': date.strftime('%Y-%m-%d'),
                'float_id': float_id,
                'latitude': float_info['lat'] + random.uniform(-0.5, 0.5),
                'longitude': float_info['lon'] + random.uniform(-0.5, 0.5),
                'depths': depths,
                'temperatures': temps,
                'salinities': salinities
            })
            
        return sorted(profiles, key=lambda x: x['date'], reverse=True)
    
    def get_floats_by_region(self, region_name):
        """Get floats in specific region"""
        if region_name.lower() not in REGIONS:
            return self.floats
            
        region = REGIONS[region_name.lower()]
        lat_range, lon_range = region['lat_range'], region['lon_range']
        
        return [f for f in self.floats 
                if lat_range[0] <= f['lat'] <= lat_range[1] 
                and lon_range[0] <= f['lon'] <= lon_range[1]]
    
    def generate_sample_csv(self):
        """Generate CSV file for demo"""
        all_data = []
        for float_data in self.floats:
            profiles = self.get_profile_data(float_data['id'], 3)
            for profile in profiles:
                for i, depth in enumerate(profile['depths']):
                    all_data.append({
                        'float_id': profile['float_id'],
                        'date': profile['date'],
                        'latitude': profile['latitude'],
                        'longitude': profile['longitude'],
                        'depth': depth,
                        'temperature': profile['temperatures'][i],
                        'salinity': profile['salinities'][i]
                    })
        
        df = pd.DataFrame(all_data)
        df.to_csv('data/sample_argo_data.csv', index=False)
        return df