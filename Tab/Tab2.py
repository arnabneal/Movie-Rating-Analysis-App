# -*- coding: utf-8 -*-
"""
Created on Sat May 16 16:40:44 2020

@author: Arnab Basak
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
#import datetime
from datetime import datetime 
import numpy as np
import pandas as pd

import os
#Data Folder
# get relative data folder
ROOT_DIR=os.path.abspath("datasets/rating.csv")
#  Source: Rotten Tomatos
# dataset was scrapped out through Parsehub app.
#Data
rating_df = pd.read_csv(ROOT_DIR)

#Data Part required for 
#rating_df=pd.read_csv("D:/Dash_Arnab/RottenTomatoes/Data/rotten_tomatoes_200_pgs_audience_with_rating.csv")
rating_df.date=pd.to_datetime(rating_df['date']).dt.date
rel1="2019-10-02"
rating_df["rel_date"] = datetime.strptime(rel1,'%Y-%m-%d').date()
rating_df["week_rel"]=rating_df["date"]-rating_df["rel_date"]
rating_df["week_rel"]=rating_df.week_rel/np.timedelta64(1,'W')
rating_df["week_rel"]=round(rating_df.week_rel)
rating_df['year'] =pd.to_datetime(rating_df['date']).dt.year
rating_df=rating_df.sort_values(by=['week_rel'],ascending=True)


tab_2_layout =html.Div([
            dbc.Row(
                    dbc.Col(html.B('Select Week'),width=3)
                    )
                    ,
                            
             html.Div([       
            dbc.Row(
                    dbc.Col(
                                 dcc.Dropdown(
                                         id="dropdown",
                                         options=[{'label': i, 'value': i}for i in rating_df.week_rel.unique()],
                                         value=11)
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
                                                 id='table1',
                
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

                                                          }
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
                                         dcc.Graph(id="bar1"), width=6)
                                 ]
                         ),
                dbc.Row(
                        [
                                dbc.Col(dbc.Alert("Rating Distribution - Weeks since released"), width=6),
                                dbc.Col(dbc.Alert("Number of Ratings"), width=6),
                                ]
                        ),
                    dbc.Row(
                            [
                                    dbc.Col(
                                            dcc.Graph(id="box1"), width=6),
                                    
                                    dbc.Col(
                                            dcc.Graph(id="line1"), width=6),
                            ]
                            ),
              dbc.Row(
                                  dbc.Col(
                                          dbc.Alert("Median, First and Third Quartiles Graph"),
                                          width={"size": 12,}# "offset": 3},
                                          )
                    ),
                    dbc.Row(
                                    dbc.Col(
                                            dcc.Graph(id="quart_mean1"),
                                            width={"size": 12,} #"offset": 3},
                                            )
                            ),
                 ]) 
                                               
                