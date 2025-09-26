import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import ArgoDataGenerator
from query_processor import SmartQueryProcessor
from visualizations import ArgoVisualizer
from config import APP_TITLE, APP_SUBTITLE, SAMPLE_FLOATS
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="ARGO AI Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_system():
    data_loader = ArgoDataGenerator()
    query_processor = SmartQueryProcessor(data_loader)
    visualizer = ArgoVisualizer()
    return data_loader, query_processor, visualizer

def main():
    # Header
    st.title(APP_TITLE)
    st.markdown(f"*{APP_SUBTITLE}*")
    st.markdown("---")
    
    # Initialize system
    data_loader, query_processor, visualizer = initialize_system()
    
    # Sidebar
    with st.sidebar:
        st.header(" Demo Options")
        
        # Sample queries
        st.subheader("Try These Queries:")
        sample_queries = [
            "Show me temperature profiles near the equator",
            "Where are the ARGO floats in Arabian Sea?",
            "Compare Arabian Sea and Bay of Bengal",
            "What's the salinity profile for float 2902746?",
            "Show recent temperature data",
        ]
        
        selected_query = st.selectbox("Quick Select:", ["Type your own..."] + sample_queries)
        
        # System info
        st.markdown("---")
        st.subheader(" System Status")
        st.success(f" {len(SAMPLE_FLOATS)} ARGO floats loaded")
        st.info(" AI Query Processor: Active")
        st.info(" Visualization Engine: Ready")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(" Ask About Ocean Data")
        
        # Query input
        if selected_query != "Type your own...":
            user_query = st.text_input("Your Question:", value=selected_query, key="query_input")
        else:
            user_query = st.text_input("Your Question:", placeholder="e.g., Show me temperature profiles in Arabian Sea", key="query_input")
        
        # Process query
        if user_query:
            with st.spinner(" Processing your query..."):
                result = query_processor.process_query(user_query)
                
                # Display response
                st.markdown("###  AI Response")
                st.info(result['response'])
                
                # Display visualization
                if result.get('data') and result.get('visualization_type'):
                    st.markdown("###  Data Visualization")
                    
                    viz_type = result['visualization_type']
                    data = result['data']
                    title = result.get('title', 'Data Visualization')
                    
                    if viz_type == 'temperature_profile':
                        fig = visualizer.create_temperature_profile(data, title)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Also show salinity
                        sal_fig = visualizer.create_salinity_profile(data, title.replace('Temperature', 'Salinity'))
                        st.plotly_chart(sal_fig, use_container_width=True)
                        
                    elif viz_type == 'float_map':
                        float_map = visualizer.create_float_map(data, title)
                        st.components.v1.html(float_map._repr_html_(), height=500)
                        
                    elif viz_type == 'comparison_map':
                        # Show comparison chart
                        comp_fig = visualizer.create_comparison_chart(data, title)
                        st.plotly_chart(comp_fig, use_container_width=True)
                        
                        # Show combined map
                        all_floats = []
                        for region_floats in data.values():
                            all_floats.extend(region_floats)
                        float_map = visualizer.create_float_map(all_floats, "Combined Float Locations")
                        st.components.v1.html(float_map._repr_html_(), height=500)
    
    with col2:
        st.header(" Live Statistics")
        
        # Quick stats
        active_floats = len([f for f in SAMPLE_FLOATS if f['status'] == 'Active'])
        
        st.metric("Active Floats", active_floats, delta="Real-time")
        st.metric("Total Profiles", "2,847", delta="+12 today")
        st.metric("Data Coverage", "Indian Ocean", delta="Expanding")
        
        # Recent activity
        st.subheader(" Recent Activity")
        st.success("Float 2902750: New profile received")
        st.info("Float 2902746: Surfaced for data transmission")
        st.warning("Float 2902748: Maintenance mode")
        
        # System capabilities
        st.subheader(" Capabilities")
        capabilities = [
            " Natural language queries",
            " Real-time visualizations", 
            " Multi-parameter analysis",
            " Regional comparisons",
            " Export functionality",
            " Live data updates (coming soon)"
        ]
        
        for capability in capabilities:
            st.markdown(capability)
    
    # Footer
    st.markdown("---")
    st.markdown("###  Demo Features Showcase")
    
    demo_cols = st.columns(3)
    
    with demo_cols[0]:
        st.markdown("** Natural Language Interface**")
        st.markdown("Ask questions in plain English and get instant responses with data visualizations.")
    
    with demo_cols[1]:
        st.markdown("** Interactive Visualizations**") 
        st.markdown("Explore temperature profiles, salinity data, and float locations on interactive maps and charts.")
    
    with demo_cols[2]:
        st.markdown("**⚡ Real-time Processing**")
        st.markdown("Instant query processing and response generation without external API dependencies.")

if __name__ == "__main__":
    main()