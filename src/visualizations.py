
import plotly.graph_objects as go
import plotly.express as px
import folium
import pandas as pd
from config import REGIONS

class ArgoVisualizer:
    def __init__(self):
        self.colors = {
            'temperature': '#FF6B6B',
            'salinity': '#4ECDC4',
            'depth': '#45B7D1',
            'float': '#96CEB4'
        }
    
    def create_temperature_profile(self, profile_data, title="Temperature Profile"):
        """Create temperature vs depth plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=profile_data['temperatures'],
            y=[-d for d in profile_data['depths']],  # Negative for depth
            mode='lines+markers',
            name='Temperature',
            line=dict(color=self.colors['temperature'], width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18)),
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_salinity_profile(self, profile_data, title="Salinity Profile"):
        """Create salinity vs depth plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=profile_data['salinities'],
            y=[-d for d in profile_data['depths']],
            mode='lines+markers',
            name='Salinity',
            line=dict(color=self.colors['salinity'], width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18)),
            xaxis_title="Salinity (PSU)",
            yaxis_title="Depth (m)",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_float_map(self, floats_data, title="ARGO Float Locations"):
        """Create map showing float locations"""
        # Calculate center
        if floats_data:
            center_lat = sum(f['lat'] for f in floats_data) / len(floats_data)
            center_lon = sum(f['lon'] for f in floats_data) / len(floats_data)
        else:
            center_lat, center_lon = 15, 70  # Indian Ocean center
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add float markers
        for float_data in floats_data:
            color = 'green' if float_data['status'] == 'Active' else 'red'
            
            folium.Marker(
                location=[float_data['lat'], float_data['lon']],
                popup=folium.Popup(
                    f"""
                    <b>Float ID:</b> {float_data['id']}<br>
                    <b>Status:</b> {float_data['status']}<br>
                    <b>Deployment:</b> {float_data['deployment']}<br>
                    <b>Cycles:</b> {float_data['cycles']}
                    """,
                    max_width=300
                ),
                tooltip=f"Float {float_data['id']} ({float_data['status']})",
                icon=folium.Icon(color=color, icon='tint')
            ).add_to(m)
        
        return m
    
    def create_comparison_chart(self, comparison_data, title="Regional Comparison"):
        """Create comparison visualization"""
        regions = list(comparison_data.keys())
        counts = [len(comparison_data[region]) for region in regions]
        
        fig = go.Figure(data=[
            go.Bar(
                x=[REGIONS[region]['name'] for region in regions],
                y=counts,
                marker_color=[self.colors['float'], self.colors['temperature']]
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Region",
            yaxis_title="Number of ARGO Floats",
            template="plotly_white",
            height=400
        )
        
        return fig
    
    def create_time_series(self, profiles_data, parameter='temperature'):
        """Create time series plot"""
        if not profiles_data:
            return None
            
        # Extract surface values
        dates = [p['date'] for p in profiles_data]
        values = [p[f'{parameter}s'][0] for p in profiles_data]  # Surface values
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=parameter.title(),
            line=dict(color=self.colors[parameter])
        ))
        
        fig.update_layout(
            title=f"Surface {parameter.title()} Time Series",
            xaxis_title="Date",
            yaxis_title=f"{parameter.title()} ({'°C' if parameter == 'temperature' else 'PSU'})",
            template="plotly_white",
            height=400
        )
        
        return fig