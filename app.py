import streamlit as st
import altair as alt
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_csv("./sv_unpiv.csv")

def format_data(stock_data):
    # stock_data = stock_data[stock_data["Code"].isin(["AFG", "FRA"])]
    stock_data["value"] = stock_data["value"] / 1000000
    return stock_data
stock_data = get_data()
stock_data_formatted = format_data(stock_data)




hover = alt.selection_single(
    nearest=True,
    on="mouseover",
    empty="none",
)
# hover = alt.selection_point(name="highlight", on="pointerover", empty=False, nearest=True)


lines = (
    alt.Chart(stock_data_formatted, title=["Evolution des émissions de CO2 par pays (1990-2022)", "Source : Climate Watch (2025) – with major processing by Our World in Data"])
    .mark_line(interpolate="monotone")
    .encode(
        x=alt.X("Year:O", title="Année"),
        y=alt.Y("value", title="Emissions en Mégatonnes de CO2"),
        color=alt.Color('variable').legend(title="Secteur d'activité", labelFontSize=10),
    )
)
points = lines.transform_filter(hover).mark_circle(size=65)


# A dropdown filter
country_dropdown = alt.binding_select(options=list(stock_data_formatted["Entity"].unique()), name='Pays ')
# country_select = alt.param(fields=['Entity'], value="France", bind=country_dropdown, name="toto")
country_select = alt.selection_point(fields=['Entity'], bind=country_dropdown, value="France")
# filter_country = points.add_params(
#     country_select
# ) 

tooltips = (
    alt.Chart(stock_data_formatted)
    .mark_line()
    .encode(
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("Year", title="Année"),
            alt.Tooltip("variable", title="Secteur"),
            alt.Tooltip("value", title="Emissions CO2 (Mégatonnes)"),
        ],
    )
    .add_params(hover)

)
data_layer = lines + points + tooltips
data_layer = data_layer.add_params(country_select).interactive().transform_filter(country_select)


# ANNOTATIONS = [
#     ("Sep 01, 2007", 450, "🙂", "Something's going well for GOOG & AAPL."),
#     ("Nov 01, 2008", 220, "🙂", "The market is recovering."),
#     ("Dec 01, 2007", 750, "😱", "Something's going wrong for GOOG & AAPL."),
#     ("Dec 01, 2009", 680, "😱", "A hiccup for GOOG."),
# ]
# annotations_df = pd.DataFrame(
#     ANNOTATIONS, columns=["Year", "value", "variable"]
# )xdfs
# annotations_df.date = pd.to_datetime(annotations_df.Year)

# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=20, dx=-10, dy=0, align="left")
#     .encode(x="Year:T", y=alt.Y("value:Q"), text="marker")
# )

combined_chart = data_layer 


base = st.altair_chart(combined_chart, use_container_width=True)
