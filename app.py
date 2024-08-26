import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback,  dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# 1 
dirpath = os.getcwd()
datapath = os.path.join(dirpath, "data")

trial_dict = [{'label': c, 'value': c} for c in os.listdir(datapath)]


def blank_fig():
    fig = go.Figure(go.Scatter3d(x=[], y = [], z=[]))
    fig.update_layout(paper_bgcolor="black")
    fig.update_layout(legend_font_color="white")
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig
    
def plot_teat(trial_name, cow, ti):
    if cow != None:
        filename = f"tmp{ti}.csv"
        filepath = os.path.join(datapath, trial_name, cow, filename)
        teat_df = pd.read_csv(filepath, header=None).to_numpy()
    
        # udder = teat_df[np.where((teat_df[:, 4]==1) & (teat_df[:, 3]=="u"))[0], :]
        teat = teat_df[:, 2]
        udder1 = teat_df[:,[ 0,1,3]]
        udder2 = udder1.copy()
        udder2[:, 2] = udder1[:, 2] - teat
        rows = np.where(teat_df[:, 2] == 0)[]
        teat2 = udder2[rows, :]
        
        points = udder1
        fig =  go.Figure(data=[go.Scatter3d(x = points[:, 0], y = points[:, 1], z=points[:, 2],mode='markers',
             marker=dict(size=1, color="red", opacity=0.8), name = "gp")])
        
        points = teat2
        fig.add_trace(go.Scatter3d(x= points[:, 0], y = points[:, 1], z=points[:, 2], mode='markers', marker=dict(color="skyblue", size = 1, opacity = 0.8), name = "gp + teat"))
        fig.update_layout(paper_bgcolor="black", font_color = "white", plot_bgcolor = "black")
        fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    else: 
        fig = blank_fig()
    return fig

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

MENU_STYLE = {
    'backgroundColor': 'black',
    'color': 'white',
}

sidebar = html.Div(
    [
        html.H2("GP", className="display-4"),
        html.Hr(),
        html.P(
            "choose a preprocessing option, and a cow", className="lead"
        ),
        html.Label("Trial mane:"),
        dcc.Dropdown(id='tn-dpdn',options= trial_dict, value = 'vol', style = MENU_STYLE),
        
        html.Label("Cow ID:"),
        dcc.Dropdown(id='cows-dpdn',options= [], style = MENU_STYLE),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
[html.Div(
             [dbc.Row(
                [dbc.Col([dcc.Graph(id='graph2', figure = blank_fig())], md = 6),
                 dbc.Col([dcc.Graph(id='graph1', figure = blank_fig())], md = 6),]),
              dbc.Row(
                [dbc.Col([dcc.Graph(id='graph4', figure = blank_fig())], md = 6),
                 dbc.Col([dcc.Graph(id='graph3', figure = blank_fig())], md = 6),]), 
             ])
], id="page-content", style=CONTENT_STYLE)


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output('cows-dpdn', 'options'),
    Input('tn-dpdn', 'value'))
def get_frames(trial_name):
    global datapath
    cow_list = os.listdir(os.path.join(datapath, trial_name))
    return [{'label': c, 'value': c} for c in cow_list]

@app.callback(
    Output("graph1", "figure"), 
    Input('tn-dpdn', 'value'),
    Input('cows-dpdn', 'value'))
def update_bar_chart(trial_name, cow):
    fig = plot_teat(trial_name, cow, 1)
    return fig

@app.callback(
    Output("graph2", "figure"), 
    Input('tn-dpdn', 'value'),
    Input('cows-dpdn', 'value'))
def update_bar_chart(trial_name, cow):
    fig = plot_teat(trial_name, cow, 2)
    return fig

@app.callback(
    Output("graph3", "figure"), 
    Input('tn-dpdn', 'value'),
    Input('cows-dpdn', 'value'))
def update_bar_chart(trial_name, cow):
    fig = plot_teat(trial_name, cow, 3)
    return fig

@app.callback(
    Output("graph4", "figure"), 
    Input('tn-dpdn', 'value'),
    Input('cows-dpdn', 'value'))
def update_bar_chart(trial_name, cow):
    fig = plot_teat(trial_name, cow, 4)
    return fig

if __name__ == '__main__':
    app.run()