# Run with `python -m streamlit run gapminder-dash.py `

import plotly.express as px
import streamlit as st


@st.cache_data
def get_data():
    return px.data.gapminder()


# Load data (only once, is cached).
data = get_data()


def build_figure(log_x_axis):
    """Build figure depending on what kind of x_axis to use."""
    fig = px.scatter(
        data,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        size_max=60,
        log_x=log_x_axis,
        height=600,
        width=1000,
        template="simple_white",
        color_discrete_sequence=px.colors.qualitative.G10,
        title=f"Health vs Wealth",
        labels={
            "continent": "Continent",
            "year": "Year",
            "pop": "Population",
            "gdpPercap": "GDP per Capita (US$ PPP)",
            "lifeExp": "Life Expectancy (years)",
        },
        # Use plotly rather than streamlit slider because it's faster.
        animation_frame="year",
        animation_group="country",
    )

    fig.update_layout(
        font_family="Rockwell",
        legend={
            "orientation": "h",
            "title": "",
            "y": 1.1,
            "x": 1,
            "xanchor": "right",
            "yanchor": "bottom",
        },
    )
    if log_x_axis:
        fig.update_xaxes(tickprefix="$", range=(2, 5), dtick=1)
    else:
        fig.update_xaxes(tickprefix="$", range=(0, 50_000), dtick=10000)
    fig.update_yaxes(range=[30, 90])

    return fig


### BUILD THE APP ##################

# Build sidebar.
with st.sidebar:
    st.title("Gapminder Data Dashboard")
    st.markdown("""
        Plotly example data, originally from https://www.gapminder.org/data/.

        Each row represents a country on a given year.
    """)
    st.divider()
    st.subheader("Options")
    # Use Streamlit toggle to change x-axis.
    use_log_x_axis = st.toggle("Use log GDP axis", value=True)

# Build the chart.
st.plotly_chart(build_figure(log_x_axis=use_log_x_axis))
st.caption('Life expectancy and GDP per capita are closely correlated and grow together over time.')


# Show the data.
st.divider()
st.markdown("**Full Source Data**")
st.dataframe(data, hide_index=True)
