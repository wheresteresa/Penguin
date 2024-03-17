#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv("penguins.csv")
df=df.dropna()


# Color definition
color_discrete_map = {
    'Adelie': '#27005D',
    'Gentoo': '#9400FF',
    'Chinstrap': '#8594E7'
}

# Create the basic chart
fig = px.scatter(df, x="bill_length_mm", y="body_mass_g",
                 color="species",
              
                 color_discrete_map=color_discrete_map,
                 hover_name="species",
                 hover_data={"bill_length_mm": True, "body_mass_g": True})



fig.update_layout(
    width=990,
    height=850,
    title="Bill Length & Body Mass by Species",
    title_x=0.48,
    title_y=0.99,
    plot_bgcolor='#FCFBF9',
    paper_bgcolor='#FCFBF9',
    title_font=dict(size=24))

# Initialize the track visibility list
initial_visibility = [True] * len(fig.data)  # all species are visible initially 

# Add gender-specific trajectories
all_traces_len = len(fig.data)
for sex in df['sex'].dropna().unique():
    for species in df['species'].unique():
        df_filtered = df[(df['sex'] == sex) & (df['species'] == species)]
        fig.add_trace(go.Scatter(
            x=df_filtered['bill_length_mm'],
            y=df_filtered['body_mass_g'],
            mode='markers',
            name=f"{species} ({sex})",
            marker=dict(color=color_discrete_map[species]),
            visible=False 
        ))

# Define the function of button
buttons = [
    dict(label="All",
         method="update",
         args=[{"visible": initial_visibility + [False] * (len(fig.data) - all_traces_len)},
               {"title": "Bill Length & Body Mass by Species"}]),
]

# Add buttons
for sex in df['sex'].dropna().unique():
    visibility = [False] * all_traces_len 
    visibility += [(t.name.endswith(f"({sex})")) for t in fig.data[all_traces_len:]] 
    buttons.append(dict(label=sex,
                        method="update",
                        args=[{"visible": visibility},
                              {"title": f"Bill Length & Body Mass by Species: {sex}"}]))

# Update the layout of the chart
fig.update_layout(updatemenus=[dict(type="buttons", direction="down", x=1.115, y=0.8, buttons=buttons)])

fig.update_xaxes(title_text='Bill Length (mm)',gridcolor='#EEEEEE')
fig.update_yaxes(title_text='Body Mass (g)',gridcolor='#EEEEEE')

fig.update_traces(marker=dict(size=10))

fig.show()






