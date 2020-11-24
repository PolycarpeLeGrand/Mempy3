import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dtc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import pickle
from mempy3.config import CORPUSFRAMES_PATH, LEXCATS_BASE, LEXCATS_FULL, BASE_ANALYSIS_PATH
from mempy3.utils.dftools import classify_lexical_occurences
from mempy3.webviewer.components.header import mempy_banner
from mempy3.webviewer.components.metadata_tab import tab_metadata
from mempy3.webviewer.components.topics_tab import topics_container, topics_callbacks
# import mempy3.webviewer.components.topics_tab as tt
from umap import UMAP


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX], suppress_callback_exceptions=True)
DF = pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb'))
DF2 = pickle.load(open(CORPUSFRAMES_PATH / 'lexicon_corpusframe.p', 'rb'))
DF_DOC_TOPICS = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / 'old' /'topics_20_5_5' / 'doc_topics_df.p', 'rb'))

reducer = UMAP(n_components=3)
DF_WORDS_TOPICS = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / 'old' / 'topics_128_1_01_10_3_raw' / 'topic_words_df.p', 'rb'))
DF_WORDS_TOPICS['main_topic'] = DF_WORDS_TOPICS.idxmax(axis=1)
DF_WORDS_TOPICS[['x', 'y', 'z']] = reducer.fit_transform(DF_WORDS_TOPICS.drop('main_topic', axis=1))

# DF2 = pd.DataFrame({'a': [1,2,3]})
# DF3 = pickle.load(open(CORPUSFRAMES_PATH / 'lexicon_paras_corpusframe.p', 'rb'))


# tabs pour differentes analyses
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
                    dbc.Row([dbc.Col([
                        dcc.Graph(id='lexicon-heatmap', style={'height': '160vh'})  # 'width': '140vh',
                    ])])
                ])
            ])
        ], width=10)
    ]),
], fluid=True)


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
        dbc.Tab(label="Metadonnees", label_style={'cursor': 'pointer'}),
        dbc.Tab(label="Lexique", label_style={'cursor': 'pointer'}),
        dbc.Tab(label="Topic Modeling", label_style={'cursor': 'pointer'}),
        dbc.Tab(label="Tables", label_style={'cursor': 'pointer'}),
    ], id='tabs', active_tab='tab-0', style={'padding-left': '10px', }
)


# html.Div donne full largeur, dbc.Container une row au centre. Ou utiliser fluid=True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    mempy_banner,
    html.Div([
        tabs,
    ], className='pt-2 bg-dark text-light'),
    dbc.Container([], id='tab-container', fluid=True, className='bt-2 pt-3'),

])


topics_callbacks(app, DF_WORDS_TOPICS)


@app.callback(Output(component_id='url', component_property='pathname'),
              [Input(component_id='tabs', component_property='active_tab')])
def update_pathname(selected_tab):
    tab_mapping = {'tab-0': '/metadata',
                   'tab-1': '/lexicon',
                   'tab-2': '/topics',
                   'tab-3': '/tables'}
    print(1)
    return tab_mapping[selected_tab]


@app.callback(
    [Output(component_id='tab-container', component_property='children'),
     Output(component_id='tabs', component_property='active_tab')],
    [Input(component_id='url', component_property='pathname')],
    State(component_id='tabs', component_property='active_tab')
)
def update_tab(curr_tab, active_tab_state):
    tab_mapping = {'/metadata': (tab_metadata, 'tab-0'),
                   '/lexicon': (tab_lexicon, 'tab-1'),
                   '/topics': (topics_container, 'tab-2'),
                   '/tables': (tab_result_table, 'tab-3')}
    return tab_mapping[curr_tab][0], tab_mapping[curr_tab][1]


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
            html.Tr([html.Th(value), html.Th('Documents'), html.Th('')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(i), html.Td(v), html.Td(f'{v/s*100:.2f}%')
            ]) for i, v in tdf.items()
        ])
    ], style={'width': '100%'})
    text = ['Ajuster le slider pour filtrer par nombre de tokens.', html.Br(),
            f'Min tokens: {min_tokens} | Max tokens: {max_tokens if max_tokens < 10000 else "5000+"} | Total docs: {s}']
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
    public = True  # 24.212.252.134:33
    if public:
        ip = '192.168.0.129'  #essayer 0.0.0.0 c'est peut-etre un wildcard
        port = 33
        app.run_server(debug=False, host=ip, port=port)
    else:
        app.run_server(debug=True)

