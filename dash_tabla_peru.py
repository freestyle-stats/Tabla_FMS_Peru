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
import numpy as np

#Obtener dataset de votos de jurados
df=pd.read_csv("FMS_PE_VotosJurados_Temporada_2.csv",delimiter=";")
#Obtener dataset de resultados de jurados
resultados=pd.read_csv("FMS_PE_Resultados.csv",delimiter=";")

#Obtener PTB de los competidores
df_tabla=df
lista_drop=list()
for freestyler in df.Competidor.unique():
  for jornada in df.Jornada.unique():
    #Score máximo
    score_max=df_tabla[(df_tabla['Competidor']==freestyler)&
                       (df_tabla['Jornada']==jornada)].Score.max()
    index_max=df_tabla[(df_tabla['Competidor']==freestyler)&
                       (df_tabla['Jornada']==jornada)&
                       (df_tabla['Score']==score_max)].index
    index_max=index_max[0]
    lista_drop.append(index_max)
    #Score mínimo
    score_min=df_tabla[(df_tabla['Competidor']==freestyler)&
                       (df_tabla['Jornada']==jornada)].Score.min()
    index_min=df_tabla[(df_tabla['Competidor']==freestyler)&
                       (df_tabla['Jornada']==jornada)&
                       (df_tabla['Score']==score_min)].index
    index_min=index_min[0]
    lista_drop.append(index_min)
    #Drop score máximo y mínimo
df_tabla=df_tabla.drop(lista_drop)

df_tabla=df_tabla.groupby(['Competidor'],as_index=False).sum()
df_tabla=df_tabla.drop(['Jornada','Puntos'],axis=1)
df_tabla=df_tabla.sort_values(['Score'],ascending=False)

#Obtener tabla de puntajes (batallas ganadas,perdidas, replicas, etc)
conditions=[
            (resultados['Resultado']=='V'),
            (resultados['Resultado']=='VR'),
            (resultados['Resultado']=='DR'),
            (resultados['Resultado']=='D')
            ]
values=[3,2,1,0]
resultados['Puntos']=np.select(conditions,values)
resultados=resultados.groupby(['Competidor'],as_index=False).sum()
resultados=resultados.drop(['Jornada','Temporada','Cant_reps'],axis=1)

tabla_final=pd.merge(left=resultados,right=df_tabla,how='left',on='Competidor')
tabla_final=tabla_final.sort_values(['Puntos','Score'],ascending=False)

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
max_rows=10
app.layout = html.Div(children=[

    html.Div([

        #Titulo del Dashboard
        html.H4(children='TABLA DE POSICIONES - FMS Perú',style={
            'textAlign':'center',
            'color':colors['text']
        }),

        #Lista desplegable de jurados
         dcc.Dropdown(id='dropdown',options=[
             {'label': i, 'value': i} for i in df.Jurado.unique()
         ],placeholder='Elegir jurado'),

        #Display a partir de dropdown
        html.Div([
            html.Div([
                html.H4(children='|       |    Tabla personal    |       |',
                        style={'color':'#d10000'}),
                html.Div(id='tabla-jurados')],
                style={'width':'20%','display': 'inline-block'}),
            html.Div([
                html.H4(children='|       |    Tabla FMS Perú    |       |',
                        style={'color':'#d10000'}),
                html.Table(
                    # Header
                    [html.Tr([html.Th(col) for col in tabla_final.columns])] +
                    # Body
                    [html.Tr([
                        html.Td(tabla_final.iloc[i][col]) for col in tabla_final.columns
                    ]) for i in range(min(len(tabla_final), max_rows))])],
                style={'width':'20%','display': 'inline-block'})
        ])
    ])
])

#CALLBACK DE TABLA POR JURADO
@app.callback(
    dash.dependencies.Output('tabla-jurados', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):

    df_res = df[df.Jurado == dropdown_value]
    df_res = df_res.groupby(['Competidor'], as_index=False).sum()
    df_res = df_res.drop('Jornada', axis=1)
    df_res = df_res.sort_values(['Puntos', 'Score'], ascending=False)
    return generate_table(df_res)

#DISPLAY APP
if __name__ == '__main__':
    app.run_server()#debug=True)