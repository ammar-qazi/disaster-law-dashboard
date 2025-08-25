import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import numpy as np
from collections import defaultdict

# Page configuration
st.set_page_config(
    page_title="Disaster Law Dashboard",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme matching reference dashboard
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .main-header {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
        padding: 20px 0;
    }
    
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 15px;
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 5px;
    }
    
    .metric-card {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4a90e2;
    }
    
    .state-detail {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .filter-section {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .protection-score {
        font-size: 24px;
        font-weight: bold;
        color: #4a90e2;
    }
    
    div[data-testid="metric-container"] {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        padding: 10px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    """Load and process all Excel files into a normalized dataset"""
    
    # Get all Excel files
    excel_files = glob.glob("*.xlsx")
    
    # Dictionary to store combined state data
    state_data = defaultdict(lambda: {
        'state': '',
        'key_statutes': '',
        'local_authority': '',
        'notable_provisions': '',
        'vulnerable_protections': '',
        'civil_rights': '',
        'disability_needs': '',
        'language_access': '',
        'equity_initiatives': '',
        'emergency_declaration': '',
        'mitigation_planning': '',
        'mutual_aid': '',
        'data_availability': 0.0,  # Default no data
        'region': 'Unknown'
    })
    
    # State name mapping for consistency
    state_mapping = {
        'Iowa, etc.': 'Iowa',
        'Others': 'Wisconsin',  # Assuming from context
        'Guam, USVI, American Samoa, Northern Mariana I...': 'Guam'
    }
    
    # Process each Excel file
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            
            # Skip files without state column
            state_col = None
            for col in df.columns:
                if 'state' in col.lower() or 'territory' in col.lower() or 'jurisdiction' in col.lower():
                    state_col = col
                    break
            
            if state_col is None:
                continue
                
            for _, row in df.iterrows():
                state_name = str(row[state_col]).strip()
                
                # Apply state name mapping
                if state_name in state_mapping:
                    state_name = state_mapping[state_name]
                
                # Skip non-state entries
                if not state_name or state_name in ['nan', 'Approach', 'Aspect', 'Impact Area', 'Protection Area', 'Region']:
                    continue
                
                # Update state data with available information
                state_entry = state_data[state_name]
                state_entry['state'] = state_name
                
                # Map columns to standardized fields
                for col in df.columns:
                    col_lower = col.lower()
                    value = str(row[col]) if pd.notna(row[col]) else ''
                    
                    if 'statute' in col_lower or 'code' in col_lower:
                        if value and value != 'nan':
                            state_entry['key_statutes'] = value
                    elif 'local authority' in col_lower:
                        if value and value != 'nan':
                            state_entry['local_authority'] = value
                    elif 'notable provision' in col_lower:
                        if value and value != 'nan':
                            state_entry['notable_provisions'] = value
                    elif 'vulnerable' in col_lower and 'protection' in col_lower:
                        if value and value != 'nan':
                            state_entry['vulnerable_protections'] = value
                    elif 'civil rights' in col_lower or 'discrimination' in col_lower:
                        if value and value != 'nan':
                            state_entry['civil_rights'] = value
                    elif 'disability' in col_lower or 'functional' in col_lower:
                        if value and value != 'nan':
                            state_entry['disability_needs'] = value
                    elif 'language access' in col_lower:
                        if value and value != 'nan':
                            state_entry['language_access'] = value
                    elif 'equity' in col_lower:
                        if value and value != 'nan':
                            state_entry['equity_initiatives'] = value
                    elif 'emergency declaration' in col_lower:
                        if value and value != 'nan':
                            state_entry['emergency_declaration'] = value
                    elif 'mitigation' in col_lower:
                        if value and value != 'nan':
                            state_entry['mitigation_planning'] = value
                    elif 'mutual aid' in col_lower:
                        if value and value != 'nan':
                            state_entry['mutual_aid'] = value
                
                # Calculate data availability score (0-1) based on how many fields have data
                data_fields = [
                    'key_statutes', 'local_authority', 'notable_provisions', 
                    'vulnerable_protections', 'civil_rights', 'disability_needs',
                    'language_access', 'equity_initiatives', 'emergency_declaration',
                    'mitigation_planning', 'mutual_aid'
                ]
                
                filled_fields = sum(1 for field in data_fields if state_entry[field] and state_entry[field].strip() and state_entry[field] != 'nan')
                state_entry['data_availability'] = filled_fields / len(data_fields)
                
                # Determine region
                if file.startswith('CA-WA-OR'):
                    state_entry['region'] = 'West Coast'
                elif 'Southwest' in file or file.startswith('SW-'):
                    state_entry['region'] = 'Southwest'
                elif 'Midwest' in file:
                    state_entry['region'] = 'Midwest'
                elif 'Northeast' in file:
                    state_entry['region'] = 'Northeast'
                elif 'Appalachia' in file:
                    state_entry['region'] = 'Appalachia'
                elif 'MTN' in file:
                    state_entry['region'] = 'Mountain West'
                elif 'AK-HI' in file:
                    state_entry['region'] = 'Alaska & Hawaii'
                
        except Exception as e:
            st.error(f"Error processing file {file}: {e}")
            continue
    
    # Convert to DataFrame
    df_final = pd.DataFrame(list(state_data.values()))
    
    # Add state abbreviations for map
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
        'District of Columbia': 'DC', 'Puerto Rico': 'PR'
    }
    
    df_final['state_code'] = df_final['state'].map(state_abbrev)
    
    return df_final

def get_data_availability_level(score):
    """Convert data availability score to categorical level"""
    if score >= 0.7:
        return "Rich Data"
    elif score >= 0.4:
        return "Moderate Data"
    else:
        return "Limited Data"

def has_specific_data_type(state_data, data_type):
    """Check if state has specific type of data available"""
    field_mapping = {
        'vulnerable_protections': 'vulnerable_protections',
        'equity_initiatives': 'equity_initiatives', 
        'civil_rights': 'civil_rights',
        'language_access': 'language_access',
        'disability_provisions': 'disability_needs',
        'emergency_powers': 'emergency_declaration'
    }
    
    field = field_mapping.get(data_type)
    if field and field in state_data:
        return bool(state_data[field] and str(state_data[field]).strip() and str(state_data[field]) != 'nan')
    return False

# Initialize session state
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = None

if 'filter_data_type' not in st.session_state:
    st.session_state.filter_data_type = "All"

if 'filter_region' not in st.session_state:
    st.session_state.filter_region = "All"

# Load data
df = load_and_process_data()

# Main header
st.markdown('<div class="main-header">🗺️ Disaster Law Data Discovery Dashboard</div>', unsafe_allow_html=True)
st.markdown("*Explore available disaster law data across states - discover what information exists rather than making assumptions about protection levels*")

# Apply filters
filtered_df = df.copy()

if st.session_state.filter_data_type != "All":
    if st.session_state.filter_data_type == "Vulnerable Protections":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'vulnerable_protections'), axis=1)]
    elif st.session_state.filter_data_type == "Equity Initiatives":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'equity_initiatives'), axis=1)]
    elif st.session_state.filter_data_type == "Civil Rights":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'civil_rights'), axis=1)]
    elif st.session_state.filter_data_type == "Language Access":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'language_access'), axis=1)]
    elif st.session_state.filter_data_type == "Disability Provisions":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'disability_provisions'), axis=1)]
    elif st.session_state.filter_data_type == "Emergency Powers":
        filtered_df = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'emergency_powers'), axis=1)]

if st.session_state.filter_region != "All":
    filtered_df = filtered_df[filtered_df['region'] == st.session_state.filter_region]

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">🗺️ State Disaster Law Data Availability</div>', unsafe_allow_html=True)
    
    # Create choropleth map showing data availability
    if not filtered_df.empty:
        fig = px.choropleth(
            filtered_df,
            locations='state_code',
            color='data_availability',
            locationmode='USA-states',
            scope='usa',
            color_continuous_scale=['#64748b', '#3b82f6', '#06b6d4'],  # Gray to Blue gradient
            range_color=[0, 1],
            hover_name='state',
            hover_data={
                'state_code': False,
                'data_availability': ':.1%',
                'region': True
            },
            labels={
                'data_availability': 'Data Coverage',
                'region': 'Region'
            }
        )
        
        fig.update_layout(
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#1a1a1a'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            coloraxis_colorbar=dict(
                title="Data Coverage",
                tickformat='.0%',
                bgcolor='rgba(0,0,0,0.5)'
            ),
            height=500
        )
        
        # Handle map clicks
        event = st.plotly_chart(fig, key="disaster_map", on_select="rerun", use_container_width=True)
        
        if event and hasattr(event, 'selection') and event.selection.points:
            clicked_state_code = event.selection.points[0]['location']
            clicked_state = df[df['state_code'] == clicked_state_code]['state'].iloc[0]
            st.session_state.selected_state = clicked_state
    else:
        st.info("No states match the current filter criteria.")

with col2:
    st.markdown('<div class="section-header">📋 State Details</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_state:
        state_info = df[df['state'] == st.session_state.selected_state].iloc[0]
        
        st.markdown(f'<div class="state-detail">', unsafe_allow_html=True)
        st.subheader(f"📍 {state_info['state']}")
        
        # Data availability metric
        data_coverage = state_info['data_availability']
        coverage_level = get_data_availability_level(data_coverage)
        
        col_coverage, col_region = st.columns(2)
        with col_coverage:
            st.metric("Data Coverage", f"{data_coverage:.1%}", delta=f"{coverage_level}")
        with col_region:
            st.metric("Region", state_info['region'])
        
        # Detailed information
        if state_info['vulnerable_protections']:
            st.subheader("🛡️ Vulnerable Population Protections")
            st.write(state_info['vulnerable_protections'][:300] + "..." if len(state_info['vulnerable_protections']) > 300 else state_info['vulnerable_protections'])
        
        if state_info['key_statutes']:
            st.subheader("📜 Key Statutes")
            st.write(state_info['key_statutes'][:200] + "..." if len(state_info['key_statutes']) > 200 else state_info['key_statutes'])
        
        if state_info['equity_initiatives']:
            st.subheader("⚖️ Equity Initiatives")
            st.write(state_info['equity_initiatives'])
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="state-detail">', unsafe_allow_html=True)
        st.info("👆 Click a state on the map to view detailed disaster law information")
        st.markdown('</div>', unsafe_allow_html=True)

# Filter controls
st.markdown('<div class="section-header">🔍 Filter States</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    data_type_options = ["All", "Vulnerable Protections", "Equity Initiatives", "Civil Rights", "Language Access", "Disability Provisions", "Emergency Powers"]
    data_type_filter = st.selectbox(
        "Data Type",
        data_type_options,
        index=data_type_options.index(st.session_state.filter_data_type) if st.session_state.filter_data_type in data_type_options else 0,
        key="data_type_selectbox"
    )
    if data_type_filter != st.session_state.filter_data_type:
        st.session_state.filter_data_type = data_type_filter
        st.rerun()

with col2:
    region_options = ["All"] + sorted(df['region'].unique().tolist())
    region_filter = st.selectbox(
        "Region",
        region_options,
        index=region_options.index(st.session_state.filter_region) if st.session_state.filter_region in region_options else 0,
        key="region_selectbox"
    )
    if region_filter != st.session_state.filter_region:
        st.session_state.filter_region = region_filter
        st.rerun()

with col3:
    # Count only actual US states (exclude territories)
    us_states_only = filtered_df[~filtered_df['state'].isin(['District of Columbia', 'Puerto Rico', 'Guam', 'U.S. Virgin Islands', 'American Samoa', 'Northern Mariana Islands'])]
    total_states = len(us_states_only)
    total_jurisdictions = len(filtered_df)
    st.metric("US States", total_states)
    if total_jurisdictions > total_states:
        st.caption(f"({total_jurisdictions} total jurisdictions)")

with col4:
    avg_coverage = filtered_df['data_availability'].mean() if not filtered_df.empty else 0
    st.metric("Avg Data Coverage", f"{avg_coverage:.1%}")

# Summary statistics  
if not filtered_df.empty:
    st.markdown('<div class="section-header">📊 Data Discovery Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Count states with different types of data
    with col1:
        st.subheader("🛡️ Vulnerable Protections")
        vuln_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'vulnerable_protections'), axis=1)].shape[0]
        st.metric("States with Data", vuln_count)
        
    with col2:
        st.subheader("⚖️ Equity Initiatives") 
        equity_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'equity_initiatives'), axis=1)].shape[0]
        st.metric("States with Data", equity_count)
        
    with col3:
        st.subheader("🏛️ Civil Rights")
        civil_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'civil_rights'), axis=1)].shape[0]
        st.metric("States with Data", civil_count)
    
    # Additional data categories
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.subheader("🌐 Language Access")
        lang_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'language_access'), axis=1)].shape[0]
        st.metric("States with Data", lang_count)
    
    with col5:
        st.subheader("♿ Disability Provisions")
        disability_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'disability_provisions'), axis=1)].shape[0]
        st.metric("States with Data", disability_count)
        
    with col6:
        st.subheader("🚨 Emergency Powers")
        emergency_count = filtered_df[filtered_df.apply(lambda x: has_specific_data_type(x, 'emergency_powers'), axis=1)].shape[0]
        st.metric("States with Data", emergency_count)

st.markdown("---")
st.markdown("*Data discovery dashboard showing available information about disaster laws across US states and territories. Use filters to explore specific data types and click states to view detailed information.*")