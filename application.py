from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
from grafico_media_movel import graph_moving_average
from grafico_di import scrap_di
import pandas as pd
from grafico_inflacao import pegando_inflacao_bc
from waitress import serve

opcoes_empresas = ['RRRP3', 'ALSO3', 'ALPA4', 'ABEV3', 'ARZZ3', 'ASAI3', 'AZUL4', 'B3SA3', 'BPAN4', 'BBSE3', 'BBDC3', 'BBDC4', 'BRAP4', 
                    'BBAS3', 'BRKM5', 'BRFS3', 'BPAC11', 'CRFB3', 'CCRO3', 'CMIG4', 'CIEL3', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 
                    'CVCB3', 'CYRE3', 'DXCO3', 'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'EQTL3', 'EZTC3', 
                    'FLRY3', 'GGBR4', 'GOAU4', 'GOLL4', 'NTCO3', 'SOMA3', 'HAPV3', 'HYPE3', 'IGTI11', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 
                    'RENT3', 'LWSA3', 'LREN3', 'MGLU3', 'MRFG3', 'CASH3', 'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'PRIO3', 'PETZ3', 
                    'QUAL3', 'RADL3', 'RAIZ4', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 
                    'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VIIA3', 'VBBR3', 'WEGE3', 'YDUQ3']

opcoes_empresas.append("IBOV")

grafico_media_m = graph_moving_average()


inflacao = pegando_inflacao_bc()
fig_infla = inflacao.grafico_inflacao()

tabela_maior = pd.read_csv("tabela_maior.csv")
tabela_maior = tabela_maior.drop("a", axis = 1)

tabela_maior.iloc[1, 1] = tabela_maior.iloc[1, 1]/100

maiores_altas = pd.read_csv("maiores_altas.csv")
maiores_altas = maiores_altas.drop("a", axis = 1)

maiores_baixas = pd.read_csv("maiores_baixas.csv")
maiores_baixas = maiores_baixas.drop("a", axis = 1)

di = scrap_di()
fig_di = di.webscraping_di()

print("DI Ok")

application = Dash(__name__)
application_server = application.server


colunas_padrao = [{'name': 'Ticker', 'id': 'Ticker'},
                    {'name': 'Preço', 'id': 'Preço', 'type': 'numeric'},
                    {'name': 'Retorno', 'id': 'Retorno', 'type': 'numeric'}]


# App layout
application.layout = html.Main(children=[
    
                        html.Div(children=[html.H1(children = "Mercado", className= 'categorias-dash'),
                                           
                                           html.Div(children=[
    
                                                dcc.Interval(
                                                            id='interval-component',
                                                            interval=1*1000, # in milliseconds
                                                            n_intervals=0),

                                                html.Div(children = [
                                                    
                                                    html.H2(children="Ao vivo", className='subtitulos-dash'),
                                                    html.Div([
                                                                dash_table.DataTable(
                                                                    tabela_maior.to_dict("records"),
                                                                    colunas_padrao,
                                                                    id = 'cotacoes-tempo-real',
                                                                    style_header={
                                                                                'backgroundColor': '#333E66',
                                                                                'fontWeight': 'bold',
                                                                                'border': '0px',
                                                                                'font-size': "12px",
                                                                                'color': '#D3D6DF',
                                                                                "borderRadius": "8px"},
                                                                                
                                                                    style_cell={'textAlign': 'center',
                                                                                'padding': '12px 8px',
                                                                                'backgroundColor': '#212946',
                                                                                "borderRadius": "8px",
                                                                                'color': '#D3D6DF'
                                                                                
                                                                                },

                                                                    style_data={ 'border': '0px',
                                                                                'font-size': "12px",
                                                                                  },

                                                                    style_table={
                                                                                
                                                                                'borderRadius': '8px',
                                                                                'overflow': 'hidden'
                                                                            },

                                                                    style_data_conditional=[
                                                                                    {
                                                                                    'if': {
                                                                                            'filter_query': '{Retorno} > 0',
                                                                                            'column_id': 'Retorno'
                                                                                        }, 
                                                                                        'color': '#19C819',
                                                                                        
                                                                                    },
                                                                                    {
                                                                                    'if': {
                                                                                            'filter_query': '{Retorno} < 0',
                                                                                            'column_id': 'Retorno'
                                                                                        }, 
                                                                                        'color': '#E50000'
                                                                                    }
                                                                            ]),

                        
                                                                        ], style= {'margin-top': "13px"})
                                                    
                                                ], style= {'max-width': "300px", 
                                                           'grid-column': "1", 'grid-row': "1 / span 2"}), 
                                                
                                                html.Div(children = [
                                                    
                                                    html.H2(children="Maiores altas Ibovespa", className='subtitulos-dash'),
                                                    html.Div([
                                                                dash_table.DataTable(maiores_altas.to_dict("records"),
                                                                    colunas_padrao,
                                                                    id = 'maiores_altas',
                                                                    style_header={
                                                                                'backgroundColor': '#333E66',
                                                                                'fontWeight': 'bold',
                                                                                'border': '0px',
                                                                                'font-size': "12px",
                                                                                'color': '#D3D6DF'},
                                                                                
                                                                    style_cell={'textAlign': 'center',
                                                                                'padding': '12px 8px',
                                                                                'backgroundColor': '#212946',
                                                                                'color': '#D3D6DF'
                                                                                },

                                                                    style_data={ 'border': '0px',
                                                                                'font-size': "12px" },

                                                                                style_table={
                                                                                
                                                                                'borderRadius': '8px',
                                                                                'overflow': 'hidden'
                                                                            },

                                                                    style_data_conditional=[
                                                                            {
                                                                            'if': {
                                                                                    'filter_query': '{Retorno} > 0',
                                                                                    'column_id': 'Retorno'
                                                                                }, 
                                                                                'color': '#19C819',
                                                                                
                                                                            },
                                                                            {
                                                                            'if': {
                                                                                    'filter_query': '{Retorno} < 0',
                                                                                    'column_id': 'Retorno'
                                                                                }, 
                                                                                'color': '#E50000'
                                                                            }
                                                                    ]
                                                                  

                                                                                )
                                                            ], style= {'margin-top': "13px"})
                                                    
                                                ], style= {'max-width': "300px",
                                                           'grid-column': "2", 'grid-row': "1"}),

                                                html.Div(children = [
                                                    
                                                    html.H2(children="Maiores baixas Ibovespa", className='subtitulos-dash'),
                                                    html.Div([
                                                                dash_table.DataTable(maiores_baixas.to_dict("records"),
                                                                    colunas_padrao,
                                                                    id = 'maiores_quedas',
                                                                    style_header={
                                                                                'backgroundColor': '#333E66',
                                                                                'fontWeight': 'bold',
                                                                                'border': '0px',
                                                                                'font-size': "12px",
                                                                                'color': '#D3D6DF'},
                                                                                
                                                                    style_cell={'textAlign': 'center',
                                                                                'padding': '12px 8px',
                                                                                'backgroundColor': '#212946',
                                                                                'color': '#D3D6DF'
                                                                                },

                                                                    style_data={ 'border': '0px',
                                                                                'font-size': "12px" },

                                                                    style_table={
                                                                    
                                                                    'borderRadius': '8px',
                                                                    'overflow': 'hidden'
                                                                },

                                                                    style_data_conditional=[
                                                                                    {
                                                                                    'if': {
                                                                                            'filter_query': '{Retorno} > 0',
                                                                                            'column_id': 'Retorno'
                                                                                        }, 
                                                                                        'color': '#19C819',
                                                                                        
                                                                                    },
                                                                                    {
                                                                                    'if': {
                                                                                            'filter_query': '{Retorno} < 0',
                                                                                            'column_id': 'Retorno'
                                                                                        }, 
                                                                                        'color': '#E50000'
                                                                                    }
                                                                            ]
                                                                  
                                                                                
                                                                                
                                                                                )
                                                            ], style= {'margin-top': "13px"})
                                                    
                                            ], style= {'max-width': "300px", 'align-self': "end",
                                                       'grid-column': "2", 'grid-row': "2"})


                                           ], style = {'display': 'grid', 'grid-template-rows': 'auto 1fr', 'gap': '0px 25px', 'margin-top': '32px'}),

                                           dcc.Dropdown(opcoes_empresas, value = 'IBOV', id = 'escolher-grafico-aovivo',
                                                        style = {"background-color": 'black', 'color': 'white'}),
                                                        
                                           dcc.Graph( style={"width": "100%", 'height': "302px", 'margin-top': '16px', 
                                                             'border-radius':'8px', 
                                                             'background-color': '#131516', 'border': "2px solid #212946"}, id ='grafico_candle')
                                                             
                                           
                                           ],
                                 
                                 style= {"width": "100%", "max-width": "600px"}),
                        
                        html.Div(children=[html.H1(children = "Economia", className= 'categorias-dash'),
                                           
                                            html.Div(children=[
    
                                                html.Div(className= 'graficos-economia', children=[
    
                                                    html.H2(children="Evolução da Curva de Juros", className='subtitulos-dash'),
                                                    dcc.Graph(id = "grafico_juros", figure=fig_di,
                                                              style={"width": "100%", 'height': "302px", 
                                                                     'border-radius':'8px', 'background-color': '#131516',
                                                                     'border': "2px solid #212946"})
                                                ]), 
                                                
                                                html.Div(className= 'graficos-economia', children=[
                                                    
                                                    html.H2(children="Inflação últimos 6 meses", className='subtitulos-dash'),
                                                    dcc.Graph(id = "grafico_inflacao", figure=fig_infla,
                                                              style={"width": "100%", 'height': "302px",
                                                                     'border-radius':'8px', 'background-color': '#131516',
                                                                     'border': "2px solid #212946"})    

                                                ])],
                                                
                                                style = {"display": "flex", "gap": "90px", 'margin-top': "32px"}),


                                            html.Div(children=[

                                            ], style = {"margin-top": "25px"})
                                           
                                           
                                           ],
                                 
                                 style= {"width": "100%", "max-width": "999px"})

                    ],
    
    style = {'display': "flex", 'width': '100%', 'background-color': '#131516', 'align-itens': 'center',
                                  'justify-content': 'space-around', 'gap': "90px", 'padding': "25px 25px 0px 25px", 'height': '100vh'})
    
@application.callback(
    Output('grafico_candle', 'figure'),
    Input('escolher-grafico-aovivo', 'value')
)
def update_options(value):

    if value == "IBOV":

        fig_ma = grafico_media_m.criando_grafico_acao("^BVSP")

    else:

        ticker = value + ".SA"

        fig_ma = grafico_media_m.criando_grafico_acao(ticker)

    return fig_ma                          


# Run the app
if __name__ == '__main__':
    
    serve(app=application,port=80)
 