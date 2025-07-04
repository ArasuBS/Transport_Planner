import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transport Planner", layout="wide")

st.title("🚌 Transport Planning Dashboard")
st.markdown("Upload your Excel sheet and view passengers route-wise.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        required_cols = ['ID', 'Name', 'Phone', 'Route', 'BoardingPoint']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Missing one or more required columns: {required_cols}")
        else:
            df['Route'] = df['Route'].astype(int)
            routes = sorted(df['Route'].unique())

            tab_labels = [f"Route {r}" for r in routes]
            tabs = st.tabs(tab_labels)

            for i, route in enumerate(routes):
                with tabs[i]:
                    st.subheader(f"Route {route} - Passengers")
                    df_route = df[df['Route'] == route].copy()
                    df_route = df_route.sort_values(by='BoardingPoint')
                    st.dataframe(df_route[['ID', 'Name', 'Phone', 'BoardingPoint']].reset_index(drop=True),
                                 use_container_width=True)
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a valid Excel (.xlsx) file.")
