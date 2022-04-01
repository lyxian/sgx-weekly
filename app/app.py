from dash_bootstrap_components import Row, Col, themes
from dash import Dash, html, dash_table, dcc
from plotly import graph_objects, express

import weekly
import postWeekly

from utils import getFileNameAndData, getMinMaxDf

# app = Dash(__name__)

external_stylesheets = [themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
FILENAME, data = getFileNameAndData()

styleTable = {
    'marginTop': '40px',
    'marginBottom': '40px',
    'marginLeft': '100px',
    'marginRight': '100px'
}

styleZeroMargin = {
    'margin': '0px'
}

TABLE_DATA = getMinMaxDf().T.reset_index()
TABLE_DATA.columns = ['ticker', 'min', 'max']

if 0:
    ASSETS = [
        dash_table.DataTable(
            id='table',
            style_cell={'textAlign': 'center'},
            # style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': '50px'},
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
            data=data.to_dict('records'),
            columns=[{"name": i, "id": i} for i in data.columns],
            page_size=4000 # default = 250
        )
    ]
else:
    # Insert custom ranges here
    RANGES = {
        'X': [1, 3],
        'Y': [3.5, 5.5],
        'A': [0, 5],
        'B': [5, 15],
        'C': [15, 100],
    }
    if 0:
        figure = graph_objects.Figure()
        figure.update_traces(express.line(
            data, x='date', y='close', color='ticker'
        ))
    else:
        if 0:
            figure = express.line(
                data, x='date', y='close', color='ticker'
            )
            graphs = [
                dcc.Graph(id='graph', figure=figure)
            ]
        else:
            graphs = [
                dcc.Graph(id=f'graph-{k}', figure=express.line(
                    data.loc[(v[0] < data.close) & (data.close < v[1])], x='date', y='close', color='ticker', title=f'Group {k}: ${v[0]} - ${v[1]}'
                ), style={'height': 1000})  for k, v in RANGES.items()
            ]
    ASSETS = [
        *graphs,
        # dcc.Graph(id='graph', figure=figure) # style={'height':550}
    ]

if 1:
    app.layout = html.Div(children = [
        html.Div(children = [
            html.Div(children = [
                html.H1(children=FILENAME),
                Row([
                    Col([
                        *ASSETS
                    ], width={'size': 10, 'offset': 0, 'order': 1}),
                    Col([
                        dash_table.DataTable(
                            id='table',
                            style_cell={'textAlign': 'center'},
                            # style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': '50px'},
                            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                            data=TABLE_DATA.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in TABLE_DATA.columns],
                            page_size=4000 # default = 250
                        ),
                    ], width={'size': 2, 'offset': 0, 'order': 2},)
                ])
            ], style=styleTable)
        ])
    ])
else:
    app.layout = html.Div(children = [
        html.Div(children = [
            html.Div(children = [
                html.H1(children=FILENAME),
                *ASSETS
            ], style=styleTable)
        ])
    ])

app.run_server(debug=True, host='0.0.0.0', port=8008)



    
    # dash_bootstrap_components.Row([  # start of second row
    # dash_bootstrap_components.Col([  # first column on second row
    #             ], width={'size': 8, 'offset': 0, 'order': 1}),  # width first column on second row