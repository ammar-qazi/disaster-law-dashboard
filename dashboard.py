import streamlit as st
import pandas as pd
import glob
import pydeck as pdk

# Set page config
st.set_page_config(layout="wide")

st.title("Disaster Law Data - Geographical Dashboard")

@st.cache_data
def load_data():
    all_files = glob.glob("*.xlsx")
    df_list = []
    # Define a common set of columns based on what we've seen
    common_columns = ['State', 'Key Statutes / Codes', 'Local Authority', 'Notable Provisions', 'Vulnerable Populations Protections']

    for file in all_files:
        try:
            df = pd.read_excel(file)
            # Add missing columns with None
            for col in common_columns:
                if col not in df.columns:
                    df[col] = None
            df_list.append(df[common_columns]) # Ensure order and columns are the same
        except Exception as e:
            st.warning(f"Could not read file {file}: {e}")

    if not df_list:
        return pd.DataFrame()

    combined_df = pd.concat(df_list, ignore_index=True)

    # Clean up the 'State' column
    combined_df['State'] = combined_df['State'].str.split(', ')
    combined_df = combined_df.explode('State')
    combined_df['State'] = combined_df['State'].str.strip()
    combined_df.dropna(subset=['State'], inplace=True)

    return combined_df

# Coordinates for US States (approximations)
state_coords = {
    'Alabama': [32.361667, -86.279167],
    'Alaska': [64.200841, -149.493673],
    'Arizona': [34.048928, -111.093731],
    'Arkansas': [35.20105, -92.500481],
    'California': [36.778261, -119.417932],
    'Colorado': [39.550051, -105.782067],
    'Connecticut': [41.603221, -73.087749],
    'Delaware': [38.910832, -75.52767],
    'Florida': [27.664827, -81.515754],
    'Georgia': [32.165622, -82.900075],
    'Hawaii': [19.896766, -155.582782],
    'Idaho': [44.068202, -114.742041],
    'Illinois': [40.633125, -89.398528],
    'Indiana': [40.267194, -86.134902],
    'Iowa': [41.878003, -93.097702],
    'Kansas': [39.011902, -98.484246],
    'Kentucky': [37.839333, -84.270018],
    'Louisiana': [30.984298, -91.962333],
    'Maine': [45.253783, -69.445469],
    'Maryland': [39.045755, -76.641271],
    'Massachusetts': [42.407211, -71.382437],
    'Michigan': [44.314844, -85.602364],
    'Minnesota': [46.729553, -94.6859],
    'Mississippi': [32.354668, -89.398528],
    'Missouri': [37.964253, -91.831833],
    'Montana': [46.879682, -110.362566],
    'Nebraska': [41.492537, -99.901813],
    'Nevada': [38.80261, -116.419389],
    'New Hampshire': [43.193852, -71.572395],
    'New Jersey': [40.058324, -74.405661],
    'New Mexico': [34.51994, -105.87009],
    'New York': [43.299428, -74.217933],
    'North Carolina': [35.759573, -79.0193],
    'North Dakota': [47.551493, -101.002012],
    'Ohio': [40.417287, -82.907123],
    'Oklahoma': [35.007752, -97.092877],
    'Oregon': [43.804133, -120.554201],
    'Pennsylvania': [41.203322, -77.194525],
    'Rhode Island': [41.580095, -71.477429],
    'South Carolina': [33.836081, -81.163725],
    'South Dakota': [43.969515, -99.901813],
    'Tennessee': [35.517491, -86.580447],
    'Texas': [31.968599, -99.901813],
    'Utah': [39.32098, -111.093731],
    'Vermont': [44.558803, -72.577841],
    'Virginia': [37.431573, -78.656894],
    'Washington': [47.751074, -120.740139],
    'West Virginia': [38.597626, -80.454903],
    'Wisconsin': [43.78444, -88.787868],
    'Wyoming': [43.075968, -107.290284]
}

df = load_data()

if not df.empty:
    df['coords'] = df['State'].apply(lambda state: state_coords.get(state))
    df.dropna(subset=['coords'], inplace=True)

    # For pydeck, we need separate lat and lon columns
    df['lat'] = df['coords'].apply(lambda x: x[0])
    df['lon'] = df['coords'].apply(lambda x: x[1])

    view_state = pdk.ViewState(
        latitude=39.8283,  # Centered on the US
        longitude=-98.5795,
        zoom=3,
        pitch=50,
    )

    layer = pdk.Layer(
        'HexagonLayer',
        data=df,
        get_position='[lon, lat]',
        radius=100000,
        elevation_scale=4,
        elevation_range=[0, 1000],
        pickable=True,
        extruded=True,
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{State}"}))

    st.dataframe(df)
else:
    st.error("No data to display.")