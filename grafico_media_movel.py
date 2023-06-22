import pandas as pd
import plotly.graph_objects as go
import datetime


class graph_moving_average():

    def __init__(self):

        self.tickers = None

    def criando_grafico_acao(self, acao, teste = False):

        dadosopen = pd.read_csv("abertura.csv", index_col=[0])
        dados_max = pd.read_csv("max.csv", index_col=[0])
        dados_min = pd.read_csv("min.csv", index_col=[0])
        dados_close = pd.read_csv("close.csv", index_col=[0])


        dadosopen = dadosopen[acao]
        dados_max = dados_max[acao]
        dados_min = dados_min[acao]
        dados_close = dados_close[acao]

        acao_grafico = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close'], index=dadosopen.index)

        acao_grafico['Open'] = dadosopen.values
        acao_grafico['High'] = dados_max.values
        acao_grafico['Close'] = dados_close.values
        acao_grafico['Low'] = dados_min.values

        acao_grafico.index = pd.to_datetime(acao_grafico.index)

        acao_grafico = acao_grafico.dropna()

        acao_grafico['media_movel_200d'] = acao_grafico['Close'].rolling(200).mean()

        acao_grafico = acao_grafico.dropna()

        acao_grafico = acao_grafico[acao_grafico.index > datetime.datetime.now() - datetime.timedelta(days = 504)]

        acao_grafico = acao_grafico[acao_grafico.index < datetime.datetime.now() - datetime.timedelta(days = 2)]

        layout = go.Layout(yaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False),
                           xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

        fig_ma = go.Figure(data=[go.Candlestick(x=acao_grafico.index,
                                            open=acao_grafico['Open'], 
                                            high=acao_grafico['High'],
                                            low=acao_grafico['Low'],
                                            close=acao_grafico['Close']), 
                            go.Scatter(x=acao_grafico.index, y=acao_grafico['media_movel_200d'], line=dict(color='white', width=1)),
                            ], layout=layout)

        fig_ma.update_layout(
            margin=dict(l=24, r=45, t=31, b=23), showlegend = False, font = dict(color = "#D3D6DF"))
        
        fig_ma.layout.plot_bgcolor = '#131516'
        fig_ma.update_layout(paper_bgcolor='rgba(0,0,0,0)')

        fig_ma.update_xaxes(tickcolor = '#131516')
        fig_ma.update_yaxes(tickcolor = '#131516')
        
        fig_ma.update_layout(xaxis_rangeslider_visible=False)

        fig_ma.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False))

        return fig_ma


if __name__ == '__main__':

    grafico_media_m = graph_moving_average()

    fig_ma = grafico_media_m.criando_grafico_acao("WEGE3.SA")
    fig_ma.show()
















