import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import plotly.graph_objects as go
import numpy as np
import json
from streamlit.components.v1 import html

st.set_page_config(layout="wide", page_title="US vs China Trade Dominance")

st.title("Global Trade Dominance: U.S. vs. China (2024)")

@st.cache_data
def load_data():
    df = pd.read_csv('GlobalTrade Dominance-U.S. vs. China (2000 & 2024).csv')

    cleaned_df_2000 = pd.DataFrame()
    cleaned_df_2024 = pd.DataFrame()
    cleaned_df_2000['Country'] = df['Country2000']
    cleaned_df_2024['Country'] = df['Country2024']
    cleaned_df_2000['US'] = df['US2000']
    cleaned_df_2000['China'] = df['China2000']
    cleaned_df_2024['US'] = df['US2024']
    cleaned_df_2024['China'] = df['China2024']
    cleaned_df_2000['Year'] = 2000
    cleaned_df_2024['Year'] = 2024

    for cleaned_df in [cleaned_df_2000, cleaned_df_2024]:
        for col in ['US', 'China']:
            cleaned_df[col] = cleaned_df[col].astype(str)
            cleaned_df[col] = cleaned_df[col].replace('-', float('nan')).replace('', float('nan')).replace(' ', float('nan'))
            cleaned_df[col] = cleaned_df[col].str.replace('"', '', regex=False).str.replace(',', '', regex=False).str.strip()
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
            cleaned_df[col] = cleaned_df[col] 

        cleaned_df['Dominance'] = 'US'
        cleaned_df.loc[cleaned_df['China'].fillna(0) > cleaned_df['US'].fillna(0), 'Dominance'] = 'China'

    return cleaned_df_2000, cleaned_df_2024

def get_iso3(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_3
        
        special_cases = {
            "Russia": "RUS", "Burma": "MMR", "Vietnam": "VNM", "Brunei Darussalam": "BRN",
            "Congo (Kinshasa)": "COD", "Congo (Brazzaville)": "COG", "South Korea": "KOR",
            "North Korea": "PRK", "Taiwan": "TWN", "Côte d'Ivoire": "CIV", "Myanmar": "MMR",
            "Palestine": "PSE", "Bolivia": "BOL", "Venezuela": "VEN", "Tanzania": "TZA",
            "Eswatini": "SWZ", "Kosovo": "XKX", "United States": "USA", "The Bahamas": "BHS",
            "Laos": "LAO", "Syria": "SYR", "Iran": "IRN"
        }
        return special_cases.get(country_name, None)
    except:
        return None

df_2000, df_2024 = load_data()

if df_2000 is not None and df_2024 is not None:
    df_2000['iso_alpha'] = df_2000['Country'].apply(get_iso3)
    df_2024['iso_alpha'] = df_2024['Country'].apply(get_iso3)
    
    if 'United States' not in df_2000['Country'].values:
        us_row_2000 = pd.DataFrame({
            'Country': ['United States'],
            'US': [float('nan')],
            'China': [0],
            'Dominance': ['US'],
            'Year': [2000],
            'iso_alpha': ['USA']
        })
        df_2000 = pd.concat([df_2000, us_row_2000], ignore_index=True)
    else:
        df_2000.loc[df_2000['Country'] == 'United States', 'Dominance'] = 'US'
        df_2000.loc[df_2000['Country'] == 'United States', 'iso_alpha'] = 'USA'
    
    if 'United States' not in df_2024['Country'].values:
        us_row_2024 = pd.DataFrame({
            'Country': ['United States'],
            'US': [float('nan')],
            'China': [0],
            'Dominance': ['US'],
            'Year': [2024],
            'iso_alpha': ['USA']
        })
        df_2024 = pd.concat([df_2024, us_row_2024], ignore_index=True)
    else:
        df_2024.loc[df_2024['Country'] == 'United States', 'Dominance'] = 'US'
        df_2024.loc[df_2024['Country'] == 'United States', 'iso_alpha'] = 'USA'
    
    if 'China' not in df_2000['Country'].values:
        china_row_2000 = pd.DataFrame({
            'Country': ['China'],
            'US': [0],
            'China': [float('nan')], 
            'Dominance': ['China'],
            'Year': [2000],
            'iso_alpha': ['CHN']
        })
        df_2000 = pd.concat([df_2000, china_row_2000], ignore_index=True)
    else:
        df_2000.loc[df_2000['Country'] == 'China', 'Dominance'] = 'China'
        df_2000.loc[df_2000['Country'] == 'China', 'iso_alpha'] = 'CHN'
    
    if 'China' not in df_2024['Country'].values:
        china_row_2024 = pd.DataFrame({
            'Country': ['China'],
            'US': [0],
            'China': [float('nan')], 
            'Dominance': ['China'],
            'Year': [2024],
            'iso_alpha': ['CHN']
        })
        df_2024 = pd.concat([df_2024, china_row_2024], ignore_index=True)
    else:
        df_2024.loc[df_2024['Country'] == 'China', 'Dominance'] = 'China'
        df_2024.loc[df_2024['Country'] == 'China', 'iso_alpha'] = 'CHN'
        
    def convert_to_json_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        return obj

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### 2000 Trade Dominance')
        
        fig_2000 = px.choropleth(
            df_2000,
            locations='iso_alpha',
            color='Dominance',
            hover_name='Country',
            color_discrete_map={'US': 'blue', 'China': 'red'},
            title='US vs China Trade Dominance (2000)',
            hover_data=['US', 'China']
        )
        
        fig_2000.update_geos(
            showcoastlines=True,
            coastlinecolor='Black',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='aliceblue',
            projection_type='orthographic'
        )
        
        fig_dict = fig_2000.to_dict()
        def convert_dict_values(d):
            if isinstance(d, dict):
                return {k: convert_dict_values(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [convert_dict_values(i) for i in d]
            else:
                return convert_to_json_serializable(d)
        
        fig_dict = convert_dict_values(fig_dict)
        fig_json = json.dumps(fig_dict)
        
        html_2000 = f"""
        <div id="chart_2000" style="height:600px;"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            var fig = {fig_json};
            Plotly.newPlot('chart_2000', fig.data, fig.layout);
            
            function rotateGlobe() {{
                var degrees = 0;
                setInterval(function() {{
                    degrees += 2;
                    if (degrees > 360) degrees = 0;
                    
                    Plotly.relayout('chart_2000', {{
                        'geo.projection.rotation.lon': degrees
                    }});
                }}, 100);
            }}
            
            Plotly.newPlot('chart_2000', fig.data, fig.layout).then(rotateGlobe);
        </script>
        """
        
        html(html_2000, height=600, scrolling=False)

    with col2:
        st.markdown('#### 2024 Trade Dominance')
        
        fig_2024 = px.choropleth(
            df_2024,
            locations='iso_alpha',
            color='Dominance',
            hover_name='Country',
            color_discrete_map={'US': 'blue', 'China': 'red'},
            title='US vs China Trade Dominance (2024)',
            hover_data=['US', 'China']
        )
        
        fig_2024.update_geos(
            showcoastlines=True,
            coastlinecolor='Black',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='aliceblue',
            projection_type='orthographic'
        )
        
        fig_dict = fig_2024.to_dict()
        fig_dict = convert_dict_values(fig_dict)
        fig_json = json.dumps(fig_dict)
        
        html_2024 = f"""
        <div id="chart_2024" style="height:600px;"></div>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script>
            var fig = {fig_json};
            Plotly.newPlot('chart_2024', fig.data, fig.layout);
            
            function rotateGlobe() {{
                var degrees = 0;
                setInterval(function() {{
                    degrees += 2;
                    if (degrees > 360) degrees = 0;
                    
                    Plotly.relayout('chart_2024', {{
                        'geo.projection.rotation.lon': degrees
                    }});
                }}, 100);
            }}
            
            Plotly.newPlot('chart_2024', fig.data, fig.layout).then(rotateGlobe);
        </script>
        """
        
        html(html_2024, height=600, scrolling=False)
    
    
    st.markdown("### Data Summary")
    total_us_trade_2000 = df_2000["US"].sum()/1000
    total_china_trade_2000 = df_2000["China"].sum()/1000
    total_us_trade_2024 = df_2024["US"].sum()/1000
    total_china_trade_2024 = df_2024["China"].sum()/1000
    
    total_countries = len(df_2000)
    us_dominant_countries_2000 = len(df_2000[df_2000["Dominance"] == "US"])
    china_dominant_countries_2000 = len(df_2000[df_2000["Dominance"] == "China"])
    us_dominant_countries_2024 = len(df_2024[df_2024["Dominance"] == "US"])
    china_dominant_countries_2024 = len(df_2024[df_2024["Dominance"] == "China"])
    
    st.write("""In 2000, the United States was the undisputed global trade leader, with a total trade volume of $1.88 trillion, more than five times China's $362 billion. At that time, the U.S. was the dominant trade partner for the vast majority of countries.
    However, over the next 24 years, China's trade grew exponentially—by nearly 1,380%, reaching $5.35 trillion in 2024. In contrast, the U.S. trade volume grew by around 152%, reaching $4.75 trillion.""")
    
    col1, col2= st.columns(2)
    with col1:
        st.metric("Total US Trade 2000 ($ billions)", f"${total_us_trade_2000:,.1f}")
        st.metric("Total US Trade 2024 ($ billions)", f"${total_us_trade_2024:,.1f}")
        st.metric("US Dominant Countries 2000", us_dominant_countries_2000)
        st.metric("US Dominant Countries 2024", us_dominant_countries_2024)
    with col2:
        st.metric("Total China Trade 2000 ($ billions)", f"${total_china_trade_2000:,.1f}")
        st.metric("Total China Trade 2024 ($ billions)", f"${total_china_trade_2024:,.1f}")
        st.metric("China Dominant Countries 2000", china_dominant_countries_2000)
        st.metric("China Dominant Countries 2024", china_dominant_countries_2024)
    
    total_countries_2000 = len(df_2000)
    total_countries_2024 = len(df_2024)
    us_pct_2000 = (us_dominant_countries_2000 / total_countries_2000) * 100
    china_pct_2000 = (china_dominant_countries_2000 / total_countries_2000) * 100
    us_pct_2024 = (us_dominant_countries_2024 / total_countries_2024) * 100
    china_pct_2024 = (china_dominant_countries_2024 / total_countries_2024) * 100
    
    st.markdown("#### Trade Dominance Comparison (2000 vs 2024)")
    pie_col1, pie_col2 = st.columns(2)
    
    with pie_col1:
        pie_data_2000 = pd.DataFrame({
            'Country': ['US', 'China'],
            'Dominance': [us_dominant_countries_2000, china_dominant_countries_2000],
            'Percentage': [us_pct_2000, china_pct_2000]
        })
        fig_pie_2000 = px.pie(
            pie_data_2000, 
            values='Dominance', 
            names='Country',
            title='Trade Dominance Distribution (2000)',
            color='Country',
            color_discrete_map={'US': 'blue', 'China': 'red'},
            hover_data=['Percentage'],
            labels={'Dominance': 'Number of Countries', 'Percentage': 'Percentage (%)'}
        )
        fig_pie_2000.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie_2000, use_container_width=True)
    
    with pie_col2:
        pie_data_2024 = pd.DataFrame({
            'Country': ['US', 'China'],
            'Dominance': [us_dominant_countries_2024, china_dominant_countries_2024],
            'Percentage': [us_pct_2024, china_pct_2024]
        })
        fig_pie_2024 = px.pie(
            pie_data_2024, 
            values='Dominance', 
            names='Country',
            title='Trade Dominance Distribution (2024)',
            color='Country',
            color_discrete_map={'US': 'blue', 'China': 'red'},
            hover_data=['Percentage'],
            labels={'Dominance': 'Number of Countries', 'Percentage': 'Percentage (%)'}
        )
        fig_pie_2024.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie_2024, use_container_width=True)
    
    st.markdown("### Trade Data")

    countries_2000 = [str(c) for c in df_2000['Country'].tolist() if pd.notna(c)]
    countries_2024 = [str(c) for c in df_2024['Country'].tolist() if pd.notna(c)]
    all_countries = sorted(set(countries_2000 + countries_2024))
    comparison_df = pd.DataFrame({'Country': all_countries})
    
    df_2000_subset = df_2000[['Country', 'US', 'China', 'Dominance']].copy()
    df_2024_subset = df_2024[['Country', 'US', 'China', 'Dominance']].copy()
    comparison_df = comparison_df.merge(df_2000_subset, on='Country', how='left')
    comparison_df = comparison_df.merge(df_2024_subset, on='Country', how='left', suffixes=('_2000', '_2024'))
    
    for col in ['US', 'China', 'US_2000', 'China_2000','US_2024', 'China_2024']:
        if col in comparison_df.columns:
            comparison_df[col] = comparison_df[col].apply(lambda x: f"${x:,.1f}" if pd.notna(x) else "")
    
    columns = pd.MultiIndex.from_tuples([('Country', ''), ('2000', 'US'), ('2000', 'China'), ('2000', 'Dominance'), ('2024', 'US'), ('2024', 'China'), ('2024', 'Dominance')])
    multi_df = pd.DataFrame(columns=columns)
    
    multi_df[('Country', '')] = comparison_df['Country']
    multi_df[('2000', 'US')] = comparison_df['US_2000']
    multi_df[('2000', 'China')] = comparison_df['China_2000']
    multi_df[('2000', 'Dominance')] = comparison_df['Dominance_2000']
    multi_df[('2024', 'US')] = comparison_df['US_2024']
    multi_df[('2024', 'China')] = comparison_df['China_2024']
    multi_df[('2024', 'Dominance')] = comparison_df['Dominance_2024']
    
    def highlight_dominance(val, props=''):
        if pd.isna(val):
            return ''
        if val == 'US':
            return 'background-color: blue'
        elif val == 'China':
            return 'background-color: red'
        return ''
    
    styled_df = multi_df.style.applymap(
        highlight_dominance,
        subset=pd.IndexSlice[:, [('2000', 'Dominance'), ('2024', 'Dominance')]]
    )
    
    st.caption("Trade values are in millions of dollars. The table shows trade volumes with US and China for each country.")
    st.dataframe(styled_df, use_container_width=True)