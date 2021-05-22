# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:48:37 2020

@author: Arnab Basak
"""


import dash_core_components as dcc
import dash_html_components as html
import dash_table
#from datetime import datetime
from datetime import date
import dash_bootstrap_components as dbc


tab_1_layout =html.Div([
            dbc.Row(
                    dbc.Col(html.B('Select Date Range'),width=3)
                    )
                    ,
            html.Div([
                    
            dbc.Row(
                    dbc.Col(
                                 dcc.DatePickerRange(id='date_range_picker',
                                                     min_date_allowed=date(2019,10,2),
                                                     max_date_allowed=date.today(),
                                                     start_date=date(2019,10,2),
                                                     end_date=date.today())
                              ,width=3)
                                ),
                                 ],style={'padding':'3px'}),
                dbc.Row(
                        [
                                dbc.Col(dbc.Alert("Rating Summary",color="warning"), width=6),
                
                                dbc.Col(dbc.Alert("Relative Frequency For Movie Rating",color="warning"), width=6),
                        ]
                        ),
                 dbc.Row(
                         [
                                 
                                 dbc.Col(
                                         
                                         dash_table.DataTable(
                                                 id='table',
                
                                                 data=[],
                                                 style_table={
                                                'height': '300px',
                                                'overflowY': 'scroll',
                                            },
                                            style_cell={'textAlign': 'center',
                                                        'font_family': 'cursive',
                                                        'font_size': '18px',
                                                        },
                                            style_header={'fontWeight': 'bold',
                                                          'font_size': '20px',
                                                          'color': 'white',
                                                          'backgroundColor': 'black'

                                                          },
                                        
#                                            style_data_conditional=[
#                                                {
#                                                'if': {'row_index': 'odd'},
#                                                      'backgroundColor': 'rgb(248, 248, 248)'
#                                                }
#                                                 style_header={'backgroundColor': 'rgb(30, 30, 30)'},
#                                                 style_cell={
#                                                         'backgroundColor': 'rgb(50, 50, 50)',
#                                                         'color': 'white'
#                                                         
#                                                         },
#                                                 

                                       #  style_data_conditional=[
                                              #   {
                                              #           'if': {'row_index': 'odd'},
                                               #          'backgroundColor': 'rgb(248, 248, 248)'
                                               #   }
                                                # ],
                                        # style_header={
                                        #         'backgroundColor': 'rgb(230, 230, 230)',
                                        #         'fontWeight': 'bold'
                                        #         },

                                        ), width=6),
                                 dbc.Col(
                                         dcc.Graph(id="bar"), width=6)
                                 ]
                         ),
                dbc.Row(
                        [
                                dbc.Col(dbc.Alert("Rating Distribution - Weeks since released"), width=12),
                              #  dbc.Col(dbc.Alert("Number of Ratings"), width=6),
                                ]
                        ),
                
                
                        dbc.FormGroup(
                                            [
                                                    dbc.Label("Choose one"),
                                                    dbc.RadioItems(
                                                            options=[
                                                                    {'label':'Weekly','value':1},
                                                                    {'label': 'Daily', 'value': 2},
                                                                    {'label': 'Monthly', 'value': 3},
                                                                    ],  
                                                                    value=1,
                                                                    id="ri",
                                                                    inline=True,
                                                                    switch=True,
                                                                    ),
                                    
                                            ]
                                             ),
                    dbc.Row(
                            [
                                    dbc.Col(
                                            dcc.Graph(id="dm_box"), width=12),
                                    
#                                    dbc.Col(
#                                            dcc.Graph(id="line"), width=6),
                            ]
                            ),
              dbc.Row(
                      [
                                  
                                   
                                   
                                    dbc.Col(
                                          dbc.Alert("Median, First and Third Quartiles Graph"),
                                          width={"size": 12}# "offset": 3},
                                          ),
                                     ]
                                    ),
                     
                dbc.Row([
                                    
                                    
                                    dbc.Col(
                                            dcc.Graph(id="quart_mean"),
                                            width={"size": 12,} #"offset": 3},
                                            )
                            
                 ]),
                                    ])
                                               
                