# Run with `python -m streamlit run gapminder-dash.py `

import plotly.express as px
import streamlit as st


data = px.data.gapminder()


def build_figure(year):
    df = data.query(f'year == {year}')

    fig = px.scatter(
        df, 
        x='gdpPercap', 
        y='lifeExp', 
        hover_name='country',
        color='continent',
        size='pop',
        size_max=60,
        log_x=True,
        height=600,
        width=1000,
        template='simple_white',
        color_discrete_sequence=px.colors.qualitative.G10,
        title=f"Health vs Wealth {year}",
        labels={
            'continent': 'Continent',
            'pop': 'Population',
            'gdpPercap': 'GDP per Capita (US$ PPP)',
            'lifeExp': 'Life Expectancy (years)',
        },
    )

    fig.update_layout(
        font_family='Rockwell',
        legend={
            'orientation': 'h',
            'title': '',
            'y': 1.1,
            'x': 1,
            'xanchor': 'right',
            'yanchor': 'bottom',
        }
    )
    fig.update_xaxes(tickprefix='$', range=[2, 5], dtick=1)
    fig.update_yaxes(range=[30, 90])
    # Linien zeigen gewichtete Durchschnitte.
    fig.add_hline((df['lifeExp']*df['pop']).sum() / df['pop'].sum(), line_width=1, line_dash='dot')
    fig.add_vline((df['gdpPercap']*df['pop']).sum() / df['pop'].sum(), line_width=1, line_dash='dot')
    
    return fig


st.title('Dashboard Gapminder Data')

# Use Streamlit slider widget to select one year from all years in data set.
year = st.select_slider('Select year', sorted(set(data['year'])))

# Rebuild chart every time slider selection changes.
st.plotly_chart(build_figure(year))