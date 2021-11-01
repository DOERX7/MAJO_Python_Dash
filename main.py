# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import callback_context
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_table

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = dash.Dash(__name__)


ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)




# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig2 = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 450,
    mode = "gauge+number+delta",
    title = {'text': "Speed"},
    delta = {'reference': 380},
    gauge = {'axis': {'range': [None, 500]},
             'steps' : [
                 {'range': [0, 250], 'color': "lightgray"},
                 {'range': [250, 400], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))


dataFile = pd.read_csv('data.csv')
dataDict = dataFile.to_dict('records')

layout = html.Div(id="global",children=[
    html.H1(children='Datos tabla'),

    html.Div(children='''
        Por favor ingresar lo siguientes datos y a continuación presionar el botón "Ingresar".
    '''),

    dcc.Input(id="sensor1_x", type="number", placeholder="sensor1_x"),
    dcc.Input(id="sensor1_y", type="number", placeholder="sensor1_y"),
    dcc.Input(id="sensor2", type="number", placeholder="sensor2"),
    dcc.RadioItems(
        id="alarma",
        options=[
            {'label': 'Con alarma', 'value': 'true'},
            {'label': 'Sin alarma', 'value': 'false'},
        ],
        value='true',
        labelStyle={'display': 'inline-block'}

    ),
    html.Button('Ingresar', id='btnIngresar'),
    html.Button('Limpiar data', id='btnLimpiar'),
    html.Hr(),
    html.Div(id="number-out"),

    html.Div(id='hidden-div', style={'display': 'none'}),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dataFile.columns],
        data=dataDict
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),



])
app.layout = layout

@app.callback(
    Output("table", "data"),
    [dash.dependencies.State("sensor1_x", "value")],
    [dash.dependencies.State("sensor1_y", "value")],
    [dash.dependencies.State("sensor2", "value")],
    [dash.dependencies.State("alarma", "value")],
    [dash.dependencies.State("table", "data")],
    Input('btnIngresar', 'n_clicks'),
    Input('btnLimpiar', 'n_clicks')

)
def update_table(sensor1_x, sensor1_y, sensor2,alarma,data,n_clicks,btnLimpiar):
    print(data)
    print(n_clicks)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btnLimpiar' in changed_id:
        file_object = open('data.csv', 'w')
        file_object.write('sensor1_x,sensor1_y,sensor2,alarma')
        file_object.close()
        dataFile = pd.read_csv('data.csv')
        dataDict = dataFile.to_dict('records')
        return dataDict
    if n_clicks is None:
        return data
    nuevaFila = {
        'sensor1_x':sensor1_x,
        'sensor1_y':sensor1_y,
        'sensor2':sensor2,
        'alarma': alarma
    }
    data.append(nuevaFila)
    #Agregamos al archivo de texto
    nuevaFilaTexto = '\n'+str(sensor1_x)+','+str(sensor1_y)+','+str(sensor2)+','+str(alarma)
    file_object = open('data.csv', 'a')
    file_object.write(nuevaFilaTexto)
    file_object.close()
    return data




if __name__ == '__main__':
    app.run_server(debug=True)