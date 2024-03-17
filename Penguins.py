#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv("penguins.csv")
df=df.dropna()
df


# In[2]:


# 颜色映射
color_discrete_map = {
    'Adelie': '#27005D',
    'Gentoo': '#9400FF',
    'Chinstrap': '#8594E7'
}

# 创建初始图表
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

# 初始化轨迹可见性列表
initial_visibility = [True] * len(fig.data)  # 初始所有物种可见

# 添加性别区分的轨迹
all_traces_len = len(fig.data)  # 记录初始轨迹数量
for sex in df['sex'].dropna().unique():  # 排除缺失性别的数据
    for species in df['species'].unique():
        df_filtered = df[(df['sex'] == sex) & (df['species'] == species)]
        fig.add_trace(go.Scatter(
            x=df_filtered['bill_length_mm'],
            y=df_filtered['body_mass_g'],
            mode='markers',
            name=f"{species} ({sex})",
            marker=dict(color=color_discrete_map[species]),
            visible=False  # 初始不显示
        ))

# 定义按钮逻辑
buttons = [
    dict(label="All",
         method="update",
         args=[{"visible": initial_visibility + [False] * (len(fig.data) - all_traces_len)},  # 只显示初始物种轨迹
               {"title": "Bill Length & Body Mass by Species"}]),
]

# 分别为男性和女性添加按钮
for sex in df['sex'].dropna().unique():
    visibility = [False] * all_traces_len  # 初始轨迹隐藏
    visibility += [(t.name.endswith(f"({sex})")) for t in fig.data[all_traces_len:]]  # 根据性别显示轨迹
    buttons.append(dict(label=sex,
                        method="update",
                        args=[{"visible": visibility},
                              {"title": f"Bill Length & Body Mass by Species: {sex}"}]))

# 更新图表布局以添加按钮
fig.update_layout(updatemenus=[dict(type="buttons", direction="down", x=1.115, y=0.8, buttons=buttons)])

fig.update_xaxes(title_text='Bill Length (mm)',gridcolor='#EEEEEE')
fig.update_yaxes(title_text='Body Mass (g)',gridcolor='#EEEEEE')

fig.update_traces(marker=dict(size=10))

fig.show()


# In[ ]:




