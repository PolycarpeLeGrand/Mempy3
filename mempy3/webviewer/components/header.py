"""Banner component"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


mempy_banner = dbc.Navbar([
    dbc.Row([
        dbc.Col([
            dbc.NavbarBrand('Mempy 3 Dashboard', className='ml-2', style={'font-size': '200%'}),
            # html.Hr(),
            dbc.NavbarBrand('Outil de visualisation dynamique', className='ml-2', style={'font-size': '100%'}),
        ]),
    ])
], color='primary', dark=True)

