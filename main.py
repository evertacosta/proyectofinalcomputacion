import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from datetime import date

filesdic = {'Junio': '../demcoldatos/MC-SIN-OFI-DR-Junio-2020.csv',
            'Julio': '../demcoldatos/MC-SIN-OFI-DR-Julio-2020.csv',
            'Agosto': '../demcoldatos/MC-SIN-OFI-DR-Agosto-2020.csv',
            'Septiembre': '../demcoldatos/MC-SIN-OFI-DR-Septiembre-2020.csv'}


def dataextract_demcol(csvfilepath):

    datosmes = []
    fechas = []

    file = open(csvfilepath)
    head = iter(file)
    next(head)

    for line in file:
        datos = line.replace('"', '').replace('\n', '').split(';')

        dia = datos[2]

        #print(datos)

        hora = 0

        for valor in datos[4:-1]:

            fechas.append(dia + ' ' +"%.2d" % hora)
            datosmes.append(float(valor.replace(',', '.')))

            # print(dia + ' ' +"%.2d" % hora, valor)
            hora += 1

            if hora == 24:
                hora = 0

    return fechas, datosmes


app = dash.Dash(__name__)

app.layout = html.Div(children=[

    dcc.Graph(id='graph'),

    dcc.RadioItems(
        id='mes',
        options=[
            {'label': 'Junio', 'value': 'Junio'},
            {'label': 'Julio', 'value': 'Julio'},
            {'label': 'Agosto', 'value': 'Agosto'},
            {'label': 'Septiembre', 'value': 'Septiembre'}
        ],
        value='Junio',
        labelStyle={'display': 'block'}),

    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=date(2020, 6, 1),
        max_date_allowed=date(2020, 10, 1),
        start_date=date(2020, 6, 1)
    ),
    html.Div(id='thefield')

])

@app.callback(
    Output('graph', 'figure'),
    [Input('mes', 'value'), Input('date-picker', 'start_date'), Input('date-picker', 'end_date')])
def update_figure(value2, start, end):
    fechas, datosmes = dataextract_demcol(filesdic[value2])

    dti = pd.to_datetime(fechas, format='%Y-%m-%d %H')

    # Dataframe
    df = pd.DataFrame(datosmes, index=dti, columns=['valor'])

    newdf = df[start:end]

    # fig
    fig = px.line(newdf, y='valor')

    print(value2, start, end)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=3030)
