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

#Función de generar tabla
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#Declarar app y definir estilo moderno
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,prevent_initial_callbacks=True)

colors = {
    'background': '#111111',
    'text': '#ED514C'
}

app.layout = html.Div(children=[
    html.Div([html.H4(children='TABLA DE POSICIONES - FMS Perú',style={
        #'textAlign':'center',
        'color':colors['text']
    }),
              dcc.Dropdown(id='dropdown',options=[
                  {'label': i, 'value': i} for i in df.Jurado.unique()
                  ],placeholder='Elegir jurado'),
              html.Div([html.H4(children='Tabla por jurado'),
                        html.Div(id='tabla-jurados',
                                 style={'width':'50%','display': 'inline-block'})
                        ])
              ])
    ])

@app.callback(
    dash.dependencies.Output('tabla-jurados', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):

    df_res = df[df.Jurado == dropdown_value]
    df_res = df_res.groupby(['Competidor'], as_index=False).sum()
    df_res = df_res.drop('Jornada', axis=1)
    df_res = df_res.sort_values(['Puntos', 'Score'], ascending=False)
    return generate_table(df_res)


if __name__ == '__main__':
    app.run_server()#debug=True)