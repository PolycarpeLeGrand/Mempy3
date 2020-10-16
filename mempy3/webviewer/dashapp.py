import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dtc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from mempy3.config import CORPUSFRAMES_PATH, LEXCATS_BASE, LEXCATS_FULL
from mempy3.utils.dftools import classify_lexical_occurences
import pickle

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
DF = pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb'))
DF2 = pickle.load(open(CORPUSFRAMES_PATH / 'lexicon_corpusframe.p', 'rb'))

# header alert
head_card = dbc.Card(
    [
        dbc.CardBody([
            html.H1("Mempy3 Dashboard", className="alert-heading"),
            html.P(
                "On veut utiliser cette app pour permettre une visualisation "
                "et tester la technologie. On fait des tests, c'est la raison pour laquelle ce paragraphe "
                "est aussi long et ne dit pas grand chose."
            ),
            html.Hr(),
            html.P(
                "Utiliser les onglets ci-dessous pour naviguer.",
                className="mb-0",
            ),
        ]),
    ], color="primary", inverse=True
)

foot_alert = dbc.Alert()

# tabs pour differentes analyses
tab_metadata = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4('Longueur des documents', className="card-title"),
                html.P('Le graphique a la droite montre la repartition des documents en fonction du nombre de mots. '
                       'Le menu permet de choisir entre les textes et les abstracts. '
                       'Chaque barre correspond a un interval, par exemple la premiere bar du graphique representant '
                       'les textes complets representes les textes ayant de 0 a 499 mots.', className='card-text'),
                dbc.Select(id='bags-select', value='texts',
                           options=[{'label': 'Textes (tranches de 500)', 'value': 'texts'},
                                    {'label': 'Abstracts (tranches de 50)', 'value': 'abstracts'}]),
                dbc.FormGroup([
                    dbc.Checkbox(id='bags-select-2'),
                    dbc.Label('Couleurs par cat doctype', html_for='bags-select-2')
                ]),
            ]),
        ]), width=2),
        dbc.Col(dbc.Card(
            dcc.Graph(
                id='token_counts_fig',
                # figure=bags_fig
                ), body=True
        ), width=6),
        dbc.Col(dbc.Card([
            dbc.CardHeader('Taille des documents et Metadonnnees (10 plus nombreux)'),
            dbc.CardBody([
                html.Div(id='metadata-table'),
                html.Br(),
                dbc.Select(id='metadata-table-select', value='source',
                           options=[{'label': 'Revues', 'value': 'source'},
                                    {'label': 'Doctypes', 'value': 'doctype'},
                                    {'label': 'Categories Doctypes', 'value': 'doctype_cat'}]),
                html.Br(),
                dcc.RangeSlider(id='metadata-slider', min=0, max=5000, step=500, value=[0, 5000],
                                marks={i*500: {'label': str(i*500) if i < 10 else '5000+'} for i in range(11)}),
                dcc.Markdown(id='metadata-slider-para')
            ])
        ]), width=4),
    ]),

], fluid=True)


tab_lexicon = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4('Champs lexicaux et filtres')),
                dbc.CardBody([
                    dbc.Select(id='lexicon-cat-select', value='full',
                               options=[{'label': 'Base', 'value': 'base'},
                                        {'label': 'Full', 'value': 'full'}]),
                    html.P('Lister les mots ici')
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3('Correlations entre les champs')),
                dbc.CardBody([
                    dcc.Graph(id='lexicon-heatmap', style={'width': '150vh', 'height': '150vh'})
                ])
            ])
        ], width=10)
    ]),

], fluid=True)


tab_lexicon_test = html.Div(dcc.Graph(id='lexicon-heatmap2', style={'width': '180vh', 'height': '180vh'}))




tab_result_topics = dbc.Container(
    dbc.CardBody(
        [
            html.P("Apercu du topic modeling", className="card-text"),
        ]
    ),
    className="mt-3",
)

tab_result_table = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 3!", className="card-text"),

        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_metadata, label="Metadonnees", label_style={"color": "primary"}),
        dbc.Tab(tab_lexicon, label='Lexique'),
        dbc.Tab(tab_lexicon_test, label='lextest'),
        dbc.Tab(tab_result_topics, label="Topic Modeling"),
        dbc.Tab(tab_result_table, label="Tables", disabled=False),
    ]
)

# html.Div donne full largeur, dbc.Container une row au centre. Ou utiliser fluid=True
app.layout = dbc.Container([
    #dbc.Alert("Hello Dash!", color='primary'),
    head_card,
    tabs,
], fluid=True)


@app.callback(
    Output('token_counts_fig', 'figure'),
    [Input('bags-select', 'value'), Input('bags-select-2', 'checked')])
def update_bags_fig(selected_part, color_checked):
    params = {'texts':
                  {'df_col': 'text_tokens',
                   'bag_size': 500,
                   'title': 'Text bags'},
              'abstracts':
                  {'df_col': 'abs_tokens',
                   'bag_size': 50,
                   'title': 'Abstract bags'}
              }
    col = params[selected_part]['df_col']
    size = params[selected_part]['bag_size']
    grouping = [DF[col].apply(lambda x: int(x / size) * size if x < 10*size else 10*size)]
    if color_checked:
        grouping.append('doctype_cat')
    cdf = DF.groupby(grouping).size().reset_index(name='counts')
    return px.bar(cdf, x=col, y='counts', text='counts', color='doctype_cat' if color_checked else None, title=params[selected_part]['title'])


@app.callback(
    [Output(component_id='metadata-table', component_property='children'),
     Output(component_id='metadata-slider-para', component_property='children')],
    [Input(component_id='metadata-table-select', component_property='value'),
     Input(component_id='metadata-slider', component_property='value')]
)
def update_metadata_table(value, slider_values):
    #tdf = DF[['source', 'text_tokens']].sort_values('text_tokens', ascending=False).head(10)
    min_tokens = slider_values[0]
    max_tokens = slider_values[1] if slider_values[1] < 5000 else 1000000
    tdf = DF[(DF['text_tokens'] >= min_tokens) & (DF['text_tokens'] <= max_tokens)]
    s = len(tdf)
    tdf = tdf[value].value_counts().head(10)
    t = html.Table([
        html.Thead(
            html.Tr([html.Th('Source'), html.Th('Documents'), html.Th('')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(i), html.Td(v), html.Td(f'{v/s*100:.2f}%')
            ]) for i, v in tdf.items()
        ])
    ])
    text = f'''
Ajuster le slider pour filtrer par nombre de tokens.

Min tokens: {min_tokens} | Max tokens: {max_tokens if max_tokens < 10000 else "5000+"} | Total docs: {s}
'''
    return t, text


@app.callback(
    Output(component_id='lexicon-heatmap', component_property='figure'),
    [Input(component_id='lexicon-cat-select', component_property='value')]
)
def update_lexical_heatmap(lexcat):
    lexcat_d = {'base': LEXCATS_BASE, 'full': LEXCATS_FULL}
    #return go.Figure(data=px.imshow(classify_lexical_occurences(DF2, lexcat_d[lexcat]).corr()), layout=go.Layout(title='allo', height=1700))
    return px.imshow(classify_lexical_occurences(DF2, lexcat_d[lexcat]).corr().applymap(lambda x: 0 if x==1 else x))


if __name__ == '__main__':
    app.run_server(debug=True)

