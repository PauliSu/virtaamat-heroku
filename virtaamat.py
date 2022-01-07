import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

"""
todo

- kuva aukeaa hitaasti kun lataa niin paljon kirjastoja ja dataa
- koodi githubiin
- kts. miten dash deployataan Herokuun

"""
virtaamat = pd.read_csv('testidata.csv', sep=';', decimal=',')
virtaamat.Aika = pd.to_datetime(virtaamat.Aika, format='%d.%m.%Y %H:%M')

# Lisätään puutuvat päivämäärät. Aineistossa ei välttämättä ole riviä jokaiselle päivälle.
for p in virtaamat.Paikka.unique():
    # valitaan paikkaan liittyvä pienin ja suurin pvm
    df_aika = pd.DataFrame(pd.date_range(min(virtaamat[virtaamat.Paikka == p]['Aika']), max(virtaamat[virtaamat.Paikka == p]['Aika'])), columns=['Aika'])
    # lisätään p eli paikka sarake ja siihen vakio arvo
    df_aika['Paikka'] = p
    # tehdään outer merge dataframeen
    virtaamat = pd.merge(virtaamat, df_aika, how="outer", on=["Aika", "Paikka"]).sort_values(by=['Paikka', 'Aika'])
    
virtaamat = virtaamat.sort_values(by=['Paikka', 'Aika'])

paikka_options = [{'label': i, 'value': i} for i in virtaamat[
    'Paikka'].unique()]

app = dash.Dash()

server = app.server

app.layout = html.Div([
    html.H1('Virtaamat'),
    html.P(['Tämä dashboard näyttää virtaamat.',
            html.Br(),
    dcc.Dropdown(id='paikka-dropdown',
                 options=paikka_options,
                 value='894'),
    dcc.Graph(id='virtaamat-graph', figure={})])
])

@app.callback(
    Output(component_id='virtaamat-graph', component_property='figure'),
    Input(component_id='paikka-dropdown', component_property='value'))
def update_graph(selected_paikka):
    filtered_virtaamat = virtaamat[virtaamat['Paikka'] == selected_paikka]
    line_fig = px.line(filtered_virtaamat,
                       x='Aika', y='Arvo',
                       title=f'Virtaama paikassa {selected_paikka}')
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)
