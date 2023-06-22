import pandas as pd
import plotly.graph_objects as go


class pegando_inflacao_bc:

    def __init__(self):
        pass


    def grafico_inflacao(self):


        inflacao = pd.read_csv('inflacao.csv', index_col=[0])

        layout = go.Layout(yaxis=dict(tickformat=".2%", tickfont=dict(color="#D3D6DF"), showline = False),
                           xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

        fig_infla = go.Figure(data=[
            go.Bar(name='IPCA', x=inflacao.index, y=inflacao['ipca'], marker_color='firebrick'),
            go.Bar(name='IGPM', x=inflacao.index, y=inflacao['igp-m'], marker_color='royalblue')
        ], layout=layout)

        fig_infla.add_shape( # add a horizontal "target" line
            type="line", line_color="white", line_width=3, opacity=1,
            x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
        )
        fig_infla.update_layout(yaxis_range=[-0.012, 0.01], font = dict(color = "#D3D6DF"), margin=dict(l=24, r=45, t=31, b=23))
        
        fig_infla.layout.plot_bgcolor = '#131516'
        fig_infla.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        
        fig_infla.update_xaxes(tickcolor = '#131516')
        fig_infla.update_yaxes(tickcolor = '#131516')

        fig_infla.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False))
        
        return fig_infla
    


