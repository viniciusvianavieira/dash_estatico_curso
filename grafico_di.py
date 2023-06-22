import pandas as pd
import plotly.graph_objects as go

class scrap_di():

    def __init__(self):
        pass
    

    def webscraping_di(self):

        dados_di_recente_tratado = pd.read_csv("di_novo.csv")
        dados_di_antigo_tratado = pd.read_csv("di_antigo.csv")

        dados_di_antigo_tratado['data'] = pd.to_datetime(dados_di_antigo_tratado['data'])
        dados_di_recente_tratado['data'] = pd.to_datetime(dados_di_recente_tratado['data'])

        dados_di_antigo_tratado = dados_di_antigo_tratado.set_index('data')
        dados_di_recente_tratado = dados_di_recente_tratado.set_index('data')

        dados_di_antigo_tratado = dados_di_antigo_tratado.iloc[:, 0]
        dados_di_recente_tratado = dados_di_recente_tratado.iloc[:, 0]

        layout = go.Layout(yaxis=dict(tickformat=".1%", tickfont=dict(color="#D3D6DF"), showline = False),
                           xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

        fig_di = go.Figure(layout=layout)

        fig_di.add_trace(go.Scatter(x=dados_di_recente_tratado.index, y=dados_di_recente_tratado.values, name=f"Curva 14/04/2023",
                                line=dict(color='firebrick', width=4), mode='lines+markers'))
        fig_di.add_trace(go.Scatter(x=dados_di_antigo_tratado.index, y=dados_di_antigo_tratado.values, name=f"Curva 12/04/2022",
                                line=dict(color='royalblue', width=4), mode='lines+markers'))
        
        fig_di.update_layout(
            margin=dict(l=60, r=48, t=24, b=36, autoexpand = False), legend=dict(x= 0.6, y=1, bgcolor = '#131516'), font = dict(color = "#D3D6DF"))
        
        fig_di.layout.plot_bgcolor = '#131516'
        fig_di.update_layout(paper_bgcolor='rgba(0,0,0,0)') #deixamos o paper transparante pra mudar o background no CSS e fazer border

        fig_di.update_xaxes(tickcolor = '#131516')
        fig_di.update_yaxes(tickcolor = '#131516')

        fig_di.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False))

        return fig_di



if __name__ == "__main__":

    di = scrap_di()
    fig_di = di.webscraping_di()
    fig_di.show()














