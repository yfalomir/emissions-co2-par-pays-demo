import altair as alt
import pandas as pd
import streamlit as st
  
data = {
    'Score': [0.85, 0.9, 0.95],
    'Gene': ['Gene1', 'Gene2', 'Gene3'],
    'Species': ['Human', 'Mouse', 'Rat'],
    'Region': ['Exon', 'Intron', 'Promoter'],
    'Position A': [100, 200, 300],
    'Position B': [50, -100, 150]
}
df = pd.DataFrame(data)
  
source = df.copy()
source['Gene_Region'] = source['Gene'] + " " + source['Species'] + " " + source['Region']
  
score_range = source['Score'].astype(float)
ystart = score_range.min() - 0.02
ystop = score_range.max() + 0.02
scale = alt.Scale(scheme='category10')
color_scale = alt.Color("Gene_Region:N", scale=scale)
gene_region_selection = alt.selection_point(fields=['Gene_Region'], on='click', bind='legend')
  
# X Axis dropdown selection
dropdown = alt.binding_select(
    options=["Position A", "Position B"],
    name='(X-axis) Position: '
)
xcol_param = alt.param(value='Position A', bind=dropdown, name="x_axis_param")
  
chart = alt.Chart(source).mark_circle().encode(
    x=alt.X('x:Q', title='Position (bp)'),
    y=alt.Y('Score:Q', axis=alt.Axis(title='Relative Score'),
            scale=alt.Scale(domain=[source['Score'].astype(float).min() - 0.02, source['Score'].astype(float).max() + 0.02])),
    color=alt.condition(gene_region_selection, color_scale, alt.value('lightgray')),
    tooltip=['Score', 'Gene', 'Species', 'Region', 'Position A', 'Position B'],
    opacity=alt.condition(gene_region_selection, alt.value(0.8), alt.value(0.2))
).transform_calculate(
    x=f"datum[{xcol_param.name}]"
).properties(width=600, height=400
             ).interactive().add_params(gene_region_selection, xcol_param)
  
st.altair_chart(chart, theme=None, use_container_width=True)