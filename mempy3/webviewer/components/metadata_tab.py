"""Metadata tab components"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


card_word_counts = dbc.Card([
    dbc.CardHeader('Repartition des documents selon la longueur des textes ou des abstracts', className='card-header'),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
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
                    dbc.Label('Separer les categories doctypes', html_for='bags-select-2')
                ], className='pt-2'),
            ], width=3),

            dbc.Col([
                dcc.Graph(
                    id='token_counts_fig', style={'width': '180%'}
                )
            ], width=5)
        ])
    ])
])


card_metadata_by_words = dbc.Card([
    dbc.CardHeader('Taille des documents et Metadonnnees (10 plus nombreux)', className='card-header'),
    dbc.CardBody([
        # html.Br(),
        dbc.Row([
           # dbc.Col([
            #    html.P('Choisir la metadonnee:', className='pt-3', style={'text-align': 'right'})
            #]),
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupAddon('Choisir la metadonnee', addon_type='prepend'),
                    dbc.Select(id='metadata-table-select', value='source',
                               options=[{'label': 'Revues', 'value': 'source'},
                                        {'label': 'Doctypes', 'value': 'doctype'},
                                        {'label': 'Categories Doctypes', 'value': 'doctype_cat'},
                                        {'label': 'Annee de Publication', 'value': 'year'}]
                    ),

                ]),
            ])
        ], justify='center', align='center'),
        html.Br(),
        dcc.RangeSlider(id='metadata-slider', min=0, max=5000, step=500, value=[0, 5000],
                        marks={i*500: {'label': str(i*500) if i < 10 else '5000+'} for i in range(11)}),
        html.P(id='metadata-slider-para', style={'text-align': 'center'}),
        html.Div(id='metadata-table'),
    ])
])

jumbotron_corpus = dbc.Jumbotron([
    dbc.Container([
        html.H3('Corpus BioMed', className='display-5'),
        html.P('Le Corpus est composé de près de 120 000 documents issus de 299 revues appartenant au groupe BioMed Central.', className='lead'),
        html.P('Les graphiques et tableaux ci-dessous permettent de l\'explorer à partir de diverses métadonnées.', className='lead'),
    ], fluid=True)
], fluid=True, className='pt-2 pb-2')



tab_metadata = dbc.Container([

    dbc.Row([
        dbc.Col([
            jumbotron_corpus
        ])
    ]),

    dbc.Row([
        dbc.Col([
            card_word_counts
        ]),

        dbc.Col([
            card_metadata_by_words
        ], width=3),
    ]),

    dbc.Row([])

], fluid=True, id='tab-metadata')

