#importar librerías

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
import pandas as pd
import xlsxwriter

#Obtener dataset de votos de jurados
df=pd.read_csv("FMS_PE_VotosJurados_Temporada_2.csv",delimiter=";")

#Declarar app y definir estilo moderno
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,prevent_initial_callbacks=True)

app.layout = html.Div([

])