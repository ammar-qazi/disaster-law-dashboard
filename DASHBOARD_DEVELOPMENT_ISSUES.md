# Dashboard Development Issues & Takeaways

## Project Goal
Create an interactive disaster law dashboard similar to the minimum wage reference dashboard with:
- Interactive choropleth map showing state-level data with click functionality
- State detail panel showing comprehensive law information
- Filter controls for different law categories
- Dark theme with professional styling

## Critical Issues Encountered

### 🔴 **Map Interaction Problems**
1. **Non-clickable Map**: Despite implementing `on_select="rerun"` and click handlers, the Plotly choropleth map was not clickable in the browser
2. **No Color Display**: The map showed state outlines but no color fill, indicating data mapping issues between state names and Plotly's location expectations
3. **Session State Issues**: Map click events were not properly captured or stored in session state

### 🔴 **Data Processing Issues**
1. **State Name Mismatches**: 
   - Excel data contains entries like "Iowa, etc." and "Guam, USVI, American Samoa, Northern Mariana Islands"
   - Multi-state entries need proper expansion and normalization
   - Territory names may not match Plotly's expected location codes

2. **Empty Protection Scores**: 
   - Many states showed protection scores of 0 or very low values
   - Scoring algorithm may not be properly weighing available data
   - Data columns may contain mostly NaN or empty values

3. **Column Mapping Problems**:
   - Different Excel files have varying column structures
   - Column normalization may be losing data during processing
   - Need better handling of inconsistent schemas

### 🔴 **Technical Implementation Issues**
1. **Plotly Configuration**: 
   - Colorbar properties used deprecated syntax (`titlefont` vs `title.font`)
   - Map styling may not be compatible with current Plotly version
   
2. **Streamlit Limitations**:
   - Map click events are unreliable in Streamlit
   - Session state management for map interactions is complex
   - Plotly chart interactions have known limitations in Streamlit

3. **State Selector Issues**:
   - Dropdown functionality works but doesn't trigger proper re-renders
   - State detail updates are not consistent
   - Need better integration between map and dropdown selection

## Root Cause Analysis

### **Primary Issue: Data-Map Integration**
The core problem appears to be that our processed state data doesn't properly align with Plotly's choropleth expectations:

1. **Location Mapping**: Plotly choropleth requires exact state name matches (e.g., "California", not "CA" or "California, Oregon")
2. **Data Aggregation**: Multiple rows per state aren't being properly aggregated for visualization
3. **Score Calculation**: Protection scores may be calculated incorrectly due to missing or malformed data

### **Secondary Issue: Streamlit-Plotly Integration**
Streamlit's handling of Plotly interactions is limited:
1. Click events don't reliably trigger reruns
2. Map state selection requires complex session state management  
3. Alternative approaches (like using st.plotly_chart with selection) have compatibility issues

## Lessons Learned

### ✅ **What Worked**
1. **Data Loading**: Successfully loaded and parsed 25+ Excel files with varying schemas
2. **UI Styling**: CSS styling and dark theme implementation worked well
3. **Layout Design**: Two-column layout with metrics and filters was effective
4. **State Selection Dropdown**: Basic dropdown functionality worked for state selection

### ❌ **What Didn't Work**
1. **Map Interactivity**: Could not achieve reliable map click functionality
2. **Color Visualization**: States did not display proper color coding
3. **Data Integration**: Failed to properly connect processed data to map visualization
4. **Real-time Updates**: Map and detail panel synchronization was inconsistent

## Recommendations for Next Attempt

### 🎯 **Core Strategy Changes**
1. **Start with Streamlit Documentation**: Read official docs for plotly_chart, session_state, and map interactions
2. **Simpler Data Structure**: Begin with a single Excel file to establish working baseline
3. **Alternative Visualization**: Consider using st.map() or other Streamlit-native components instead of Plotly
4. **Incremental Development**: Build basic functionality first, then add complexity

### 🛠️ **Technical Approach**
1. **Data Validation First**: 
   - Ensure state names exactly match Plotly requirements
   - Validate protection scores are calculated correctly
   - Test with minimal dataset before scaling

2. **Map Implementation Options**:
   - **Option A**: Use Folium with st.folium for better interactivity
   - **Option B**: Use st.plotly_chart with simpler scatter plots on map
   - **Option C**: Use st.map with custom markers and popups

3. **Interaction Strategy**:
   - Rely primarily on dropdown selection rather than map clicks
   - Use map hover information to guide user selection
   - Implement clear visual feedback for selected states

### 📋 **Development Checklist for Next Session**
1. ✅ Read Streamlit documentation on maps and plotly integration
2. ✅ Create minimal working example with 3-5 states and simple data
3. ✅ Verify color mapping works before adding complexity
4. ✅ Test click interactions with simple callback functions
5. ✅ Gradually add data complexity only after basic functionality works
6. ✅ Consider alternative visualization libraries if Plotly continues to have issues

## Data Quality Issues to Address

### 🔍 **State Data Normalization**
- **Multi-state entries**: "Iowa, etc." needs to be properly expanded
- **Territory handling**: Territories need separate handling from states
- **Consistency**: Ensure all state names use full names (not abbreviations)

### 📊 **Protection Score Algorithm**
- **Weight validation**: Verify scoring weights make sense for the data
- **Data completeness**: Handle cases where most fields are empty
- **Score distribution**: Ensure scores have meaningful variation across states

### 📁 **File Processing**  
- **Schema mapping**: Create robust column mapping that handles all file variations
- **Error handling**: Better handling of corrupted or incomplete files
- **Data validation**: Validate data integrity during processing

## Tools and Libraries Assessment

### ✅ **Successful Components**
- **Streamlit**: Core app framework worked well
- **Pandas**: Data processing was effective
- **CSS Styling**: Custom styling achieved desired appearance

### ❌ **Problematic Components**  
- **Plotly Choropleth**: Interaction issues, data mapping problems
- **Session State**: Complex state management for map interactions
- **PyDeck**: Previous attempts also had interaction issues

### 🤔 **Alternative Approaches to Consider**
- **Folium**: Better interactivity for maps
- **Altair**: Streamlit-native visualization
- **Simple HTML/JS**: Custom map implementation
- **Multiple visualization types**: Combine map with other chart types

---

**Bottom Line**: The interactive map functionality requires a more thorough understanding of Streamlit's capabilities and limitations. The next attempt should focus on documentation-first approach and incremental development rather than complex feature implementation from the start.