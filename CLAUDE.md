# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a disaster law data analysis project that processes Excel files containing state-by-state information about emergency management laws, vulnerable population protections, and civil rights provisions. 

**CURRENT GOAL**: Create an interactive disaster law dashboard similar to the minimum wage reference dashboard (see reference image: `2025-08-26_00-38.png`) with:
- Interactive choropleth map showing state-level disaster law data with clickable states
- Detailed state information panel on the right showing law specifics  
- Filter controls at the bottom for different law categories
- Professional dark theme design
- Working map-to-detail panel integration

## Previous Attempt - Issues Encountered

**CRITICAL**: Previous dashboard development attempts failed due to:
1. **Non-functional map clicks** - Plotly choropleth maps were not clickable despite implementation attempts
2. **No color display** - States showed outlines but no color fill indicating data mapping issues
3. **Data integration problems** - State names in Excel don't match Plotly's location expectations
4. **Complex Streamlit-Plotly interactions** - Map click events unreliable in Streamlit

See `DASHBOARD_DEVELOPMENT_ISSUES.md` for detailed analysis of problems encountered.

## Required Next Steps

### 🎯 **MANDATORY FIRST STEP**
**Before writing any code, Claude must read and understand Streamlit documentation for:**
- `st.plotly_chart()` and map interactions  
- Session state management (`st.session_state`)
- Map visualization best practices
- Alternative map libraries (Folium, Altair) if Plotly has limitations

### 📋 **Development Strategy**
1. **Documentation First**: Read Streamlit docs thoroughly before coding
2. **Start Simple**: Begin with 3-5 states and minimal data to establish working baseline
3. **Validate Data-Map Integration**: Ensure state names match visualization requirements
4. **Test Incrementally**: Verify each feature works before adding complexity
5. **Alternative Approaches**: Consider Folium, st.map(), or other solutions if Plotly fails

### 🛠️ **Technical Requirements**
- **Interactive Map**: States must be clickable to select for detailed view
- **State Detail Panel**: Show comprehensive law information for selected states
- **Visual Color Coding**: States colored by protection level (red=limited, green=comprehensive)
- **Filter Controls**: Category and protection level filters that update the map
- **Responsive Design**: Professional styling matching reference dashboard

## Data Structure

### Excel Files
- 25+ Excel files with disaster law information organized by regions
- Common columns: State, Key Statutes/Codes, Local Authority, Notable Provisions, Vulnerable Populations Protections
- **DATA ISSUES**: Multi-state entries ("Iowa, etc."), territory names, inconsistent schemas

### Key Data Categories  
- **Emergency Declaration Powers**: State and local emergency authority
- **Vulnerable Population Protections**: Specific protections for at-risk groups
- **Civil Rights Provisions**: Non-discrimination and accessibility requirements
- **Equity Initiatives**: Programs targeting underserved communities
- **Language Access**: Multilingual emergency communications
- **Disability Provisions**: Functional needs accommodations

## Development Commands

### Running the Application
```bash
# Activate virtual environment
source venv/bin/activate

# Run the Streamlit dashboard (when created)
streamlit run disaster_dashboard.py

# Inspect Excel file structures  
python inspect_files.py
```

### Dependencies
Current environment includes:
- streamlit: Web application framework
- pandas: Data processing and Excel file handling  
- plotly: Visualization library (had interaction issues)
- openpyxl: Excel file reading
- playwright: Testing framework

## Implementation Notes

### ✅ **Proven Working Components**
- Data loading and Excel file processing
- CSS styling and dark theme implementation
- Basic Streamlit layout and UI elements
- State dropdown selection functionality

### ❌ **Known Problem Areas**  
- Plotly choropleth map click interactions
- State name normalization for map visualization
- Session state management for map-detail panel sync
- Data aggregation for meaningful protection scores

### 🤔 **Alternative Approaches to Consider**
- **Folium maps** with `st_folium` for better interactivity
- **Altair** for Streamlit-native visualizations  
- **st.map()** with custom markers
- **Multiple visualization types** combining maps with other charts

## Success Criteria

The final dashboard must demonstrate:
1. ✅ **Functional map clicks** that select states and update detail panel
2. ✅ **Proper color coding** showing state-by-state protection levels  
3. ✅ **Working filters** that update map visualization in real-time
4. ✅ **Professional design** matching the reference minimum wage dashboard
5. ✅ **Reliable data integration** with accurate state information display

**REMEMBER**: Read Streamlit documentation first, start with simple implementation, and test each component thoroughly before adding complexity.