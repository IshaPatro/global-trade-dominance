import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

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
            'US': [float('nan')],  # No trade with itself
            'China': [0],
            'Dominance': ['US'],
            'Year': [2000],
            'iso_alpha': ['USA']
        })
        df_2000 = pd.concat([df_2000, us_row_2000], ignore_index=True)
    else:
        # Ensure US is marked as US dominance
        df_2000.loc[df_2000['Country'] == 'United States', 'Dominance'] = 'US'
        df_2000.loc[df_2000['Country'] == 'United States', 'iso_alpha'] = 'USA'
    
    if 'United States' not in df_2024['Country'].values:
        us_row_2024 = pd.DataFrame({
            'Country': ['United States'],
            'US': [float('nan')],  # No trade with itself
            'China': [0],
            'Dominance': ['US'],
            'Year': [2024],
            'iso_alpha': ['USA']
        })
        df_2024 = pd.concat([df_2024, us_row_2024], ignore_index=True)
    else:
        # Ensure US is marked as US dominance
        df_2024.loc[df_2024['Country'] == 'United States', 'Dominance'] = 'US'
        df_2024.loc[df_2024['Country'] == 'United States', 'iso_alpha'] = 'USA'
    
    # Add China to the dataframes with explicit coloring
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
        # Ensure China is marked as China dominance
        df_2024.loc[df_2024['Country'] == 'China', 'Dominance'] = 'China'
        df_2024.loc[df_2024['Country'] == 'China', 'iso_alpha'] = 'CHN'

    
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
            projection_type='natural earth'
        )
        fig_2000.update_layout(height=600)
        st.plotly_chart(fig_2000, use_container_width=True)

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
            projection_type='natural earth'
        )
        fig_2024.update_layout(height=600)
        st.plotly_chart(fig_2024, use_container_width=True)

    st.markdown("### Data Summary")
    total_us_trade_2000 = df_2000["US"].sum()/1000
    total_china_trade_2000 = df_2000["China"].sum()/1000
    total_us_trade_2024 = df_2024["US"].sum()/1000
    total_china_trade_2024 = df_2024["China"].sum()/1000
    
    # Calculate dominance counts for both years
    total_countries = len(df_2000)
    us_dominant_countries_2000 = len(df_2000[df_2000["Dominance"] == "US"])
    china_dominant_countries_2000 = len(df_2000[df_2000["Dominance"] == "China"])
    us_dominant_countries_2024 = len(df_2024[df_2024["Dominance"] == "US"])
    china_dominant_countries_2024 = len(df_2024[df_2024["Dominance"] == "China"])
    
    st.write("""In 2000, the United States was the undisputed global trade leader, with a total trade volume of \$1.88 trillion, more than five times China's \$362 billion. At that time, the U.S. was the dominant trade partner for the vast majority of countries.
    However, over the next 24 years, China’s trade grew exponentially—by nearly 1,380%, reaching \$5.35 trillion in 2024. In contrast, the U.S. trade volume grew by around 152%, reaching \$4.75 trillion.""")
    
    # Display metrics
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
    
    # Calculate percentages for both years
    total_countries_2000 = len(df_2000)
    total_countries_2024 = len(df_2024)
    us_pct_2000 = (us_dominant_countries_2000 / total_countries_2000) * 100
    china_pct_2000 = (china_dominant_countries_2000 / total_countries_2000) * 100
    us_pct_2024 = (us_dominant_countries_2024 / total_countries_2024) * 100
    china_pct_2024 = (china_dominant_countries_2024 / total_countries_2024) * 100
    
    st.markdown("#### Trade Dominance Comparison (2000 vs 2024)")
    pie_col1, pie_col2 = st.columns(2)
    
    with pie_col1:
        # 2000 Pie Chart
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
        # 2024 Pie Chart
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
    
    st.markdown("### Trade Data by Country - Side-by-Side Comparison")
    
    # Create a better structured comparison dataframe with multi-level headers
    # First, get unique countries from both dataframes
    countries_2000 = [str(c) for c in df_2000['Country'].tolist() if pd.notna(c)]
    countries_2024 = [str(c) for c in df_2024['Country'].tolist() if pd.notna(c)]
    all_countries = sorted(set(countries_2000 + countries_2024))
    
    # Create a base dataframe with just countries
    comparison_df = pd.DataFrame({'Country': all_countries})
    
    # Create separate dataframes for each year with proper column names
    df_2000_subset = df_2000[['Country', 'US', 'China', 'Dominance']].copy()
    df_2024_subset = df_2024[['Country', 'US', 'China', 'Dominance']].copy()
    
    # Merge the data from both years
    comparison_df = comparison_df.merge(df_2000_subset, on='Country', how='left')
    comparison_df = comparison_df.merge(df_2024_subset, on='Country', how='left', suffixes=('_2000', '_2024'))
    
    for col in ['US', 'China', 'US_2000', 'China_2000','US_2024', 'China_2024']:
        if col in comparison_df.columns:
            comparison_df[col] = comparison_df[col].apply(lambda x: f"${x:,.1f}" if pd.notna(x) else "")
    
    # Create a multi-level column DataFrame
    # First, create the multi-level columns structure
    columns = pd.MultiIndex.from_tuples([('Country', ''), ('2000', 'US'), ('2000', 'China'), ('2000', 'Dominance'), ('2024', 'US'), ('2024', 'China'), ('2024', 'Dominance')])
    multi_df = pd.DataFrame(columns=columns)
    
    print(comparison_df)
    multi_df[('Country', '')] = comparison_df['Country']
    multi_df[('2000', 'US')] = comparison_df['US_2000']
    multi_df[('2000', 'China')] = comparison_df['China_2000']
    multi_df[('2000', 'Dominance')] = comparison_df['Dominance_2000']
    multi_df[('2024', 'US')] = comparison_df['US_2024']
    multi_df[('2024', 'China')] = comparison_df['China_2024']
    multi_df[('2024', 'Dominance')] = comparison_df['Dominance_2024']
    
    # Define a styling function that works with multi-level columns
    def highlight_dominance(val, props=''):
        # This function is applied to each cell individually
        if pd.isna(val):
            return ''
        if val == 'US':
            return 'background-color: blue'
        elif val == 'China':
            return 'background-color: red'
        return ''
    
    # Apply styling only to the Dominance columns
    styled_df = multi_df.style.applymap(
        highlight_dominance,
        subset=pd.IndexSlice[:, [('2000', 'Dominance'), ('2024', 'Dominance')]]
    )
    
    st.caption("Trade values are in millions of dollars. The table shows trade volumes with US and China for each country.")
    st.dataframe(styled_df, use_container_width=True)
else:
    st.error("Failed to load data. Please check your CSV file.")