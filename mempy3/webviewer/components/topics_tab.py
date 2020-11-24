"""LDA topics tab components"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import scipy.spatial.distance as spatial_distance
import pickle
from mempy3.config import BASE_ANALYSIS_PATH
from umap import UMAP


jumbotron_topics = dbc.Jumbotron([
    dbc.Container([
        html.H3('Topic modeling', className='display-5'),
        html.P('Visualisation des topics par documents, projection UMAP. Clic gauche pour pivoter, clic droit pour deplacer et scroll pour zoomer.', className='lead'),
        html.P('Chaque point represente un document, son ID est visible dans la fenetre', className='lead'),
    ], fluid=True)
], fluid=True, className='pt-2 pb-2')


topics_umap_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H3('Ajustements', className='bb-5', style={'text-align': 'center'}),
                html.Br(),
                dcc.Slider(min=0.1, max=1.0, step=0.1, value=1.0, id='topics-sample-slider',
                           marks={0.1: '10%', 1: '100%'}),
                html.P(['Afficher un echantillon aleatoire du corpus', html.Br(),
                        'Permet d\'ameliorer la performance et la lisibilite']),
                dcc.Markdown(id='test-p')
            ], width=2),
            dbc.Col([
                dcc.Graph(id='topics-umap', style={'height': '80vh'})
            ])
        ])
    ])
])

topics_container = dbc.Container([
    dbc.Row([
        dbc.Col([
            jumbotron_topics
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            topics_umap_card
        ]),
    ]),
    dbc.Row([
        dbc.Col([

        ]),
    ]),
], fluid=True, id='tab-topics')


def topics_callbacks(app, topics_df):
    @app.callback(
        Output(component_id='topics-umap', component_property='figure'),
        [Input(component_id='topics-sample-slider', component_property='value')]
    )
    def update_topics_plot(slider_value):
        tdf = topics_df[['x', 'y', 'z', 'main_topic']].sample(int(slider_value*len(topics_df)))
        fig = px.scatter_3d(
            tdf, x='x', y='y', z='z',
            color=tdf.main_topic, hover_name=tdf.index, labels={'color': 'Main Topic'},
            color_discrete_sequence=px.colors.qualitative.Dark24, )
        fig.update_traces(marker={'size': 5})
        return fig

    @app.callback(
        Output(component_id='test-p', component_property='children'),
        [Input(component_id='topics-umap', component_property='clickData')], prevent_initial_call=True
    )
    def update_closest_topics(data):
        doc_id = data['points'][0]['hovertext']
        wdf = topics_df.drop(['x', 'y', 'z', 'main_topic'], axis=1)
        values = wdf.loc[doc_id].sort_values(ascending=False)[:10]
        mkd = ''.join([f'* **{t}:** {p:.5f} \r\n' for t, p in values.items()])

        selected_vec = wdf.loc[doc_id]
        wdf['dist'] = wdf.apply(lambda x: spatial_distance.euclidean(x, selected_vec), axis=1)
        return f'**{doc_id}**\r\n'+mkd
