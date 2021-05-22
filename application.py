# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:30:07 2020

@author: Arnab Basak
"""
import dash_html_components as html
import dash_bootstrap_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import datetime
import numpy as np
from datetime import datetime
import sort_dataframeby_monthorweek
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

# import pathlib
import socket

from app import app,application
from Tab import Tab1, Tab2

import os

# FA = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width","initial-scale":1.0}], external_stylesheets=[dbc.themes.MINTY])
# app.config.suppress_callback_exceptions = True
# app.scripts.config.serve_locally=True
# app.css.config.serve_locally=True
#D:\PythonProject\Rating_app\datasets
# Data Folder
# get relative data folder
#path = os.path.dirname(os.path.realpath('__file__'))
ROOT_DIR=os.path.abspath("datasets/rating.csv")
#ROOT_DIR=cwd

#DATA_PATH = ROOT_DIR + "\Data"
#  Source: Rotten Tomatos
# dataset was scrapped out through Parsehub app.
#Data=DATA_PATH + " \ rotten_tomatoes_200_pgs_audience_with_rating.csv"
#rating_df = pd.read_csv(DATA_PATH + " \ rotten_tomatoes_200_pgs_audience_with_rating.csv")
rating_df=pd.read_csv(ROOT_DIR)

# Data
# rating_df=pd.read_csv("D:/appfordplmnt/Data/rotten_tomatoes_200_pgs_audience_with_rating.csv")
# rating_df.date=rating_df["date"].astype('datetime64[ns]')
# rel_date = datetime.datetime.strptime("2019-10-02","%Y-%d-%m").strftime("%Y-%m-%d")
rating_df.date = pd.to_datetime(rating_df['date']).dt.date
rel1 = "2019-10-02"
rating_df["rel_date"] = datetime.strptime(rel1, '%Y-%m-%d').date()
rating_df["week_rel"] = rating_df["date"] - rating_df["rel_date"]
rating_df["week_rel"] = rating_df.week_rel / np.timedelta64(1, 'W')
rating_df["week_rel"] = round(rating_df.week_rel)
rating_df['year'] = pd.to_datetime(rating_df['date']).dt.year
rating_df = rating_df.sort_values(by=['week_rel'], ascending=True)

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                dbc.Alert(html.H1("Rating Analysis App For Movie Theaters", style={"text-align": "center"},
                                  className="alert-heading"), color="info"),
                width=12),

        ]
    ),

    dbc.FormGroup(
        [
            dbc.Label("Choose one"),
            dbc.RadioItems(
                options=[
                    {'label': 'Date Range', 'value': 'first'},
                    {'label': 'Weekly', 'value': 'second'},
                ],
                value='first',
                id="radio-items",
                inline=True,
                switch=True,
            ),
        ]
    ),
    
            
    dbc.Spinner(    
            html.Div([ html.Div(id="div", children=[])]),
            size="lg",
                color="primary",
                type="grow"),
                    
        
    #html.Div(id="div", children=[]),
    html.Footer("© 2021 Arnab Basak. All Rights Reserved.")
], style={'padding': '2px'})


# Radio Button Callback for layout
@app.callback(Output('div', 'children'),
              [Input('radio-items', 'value')])
def render_charts(value):
    if value == 'first':

        return Tab1.tab_1_layout
    elif value == 'second':

        return Tab2.tab_2_layout


# Date Range Callback
@app.callback([Output('table', 'data'),
               Output('table', 'columns'),
               Output('bar', 'figure'),
               Output('quart_mean', 'figure')],

              [Input('date_range_picker', 'start_date'),
               Input('date_range_picker', 'end_date')
               ])
# Output('dm_box','figure'),

def update_data1(start, end):
    # start_date =datetime.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
    print(start, end)
    # start = datetime.strptime(start,'%Y-%m-%d').date()
    # end = datetime.strptime(end,'%Y-%m-%d').date()
    print("after", start, end)

    sd = datetime.strptime(start, '%Y-%m-%d').date()
    # sd = datetime.strptime(sd,'%Y-%m-%d').datetime.normalize()
    print("start-date", sd)

    ed = datetime.strptime(end, '%Y-%m-%d').date()
    print("end-date", ed)
    # end_date =datetime.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')

    mask = (rating_df['date'] >= sd) & (rating_df['date'] <= ed)

    rating_req = rating_df.loc[mask]

    date_range = sd.strftime("%Y-%m-%d") + " " + "-" + " " + ed.strftime("%Y-%m-%d")
    no_rating = len(rating_req)
    avg_rating = round(rating_req.rating.mean(skipna=True), 2)
    med_rating = rating_req.rating.median(skipna=True)
    q1_rat = rating_req.rating.quantile(0.25)
    q3_rat = rating_req.rating.quantile(0.75)
    # mad_rat = rating_req.rating.mad( skipna = True)
    mad_rat = (abs(rating_req.rating - rating_req.rating.median())).median()
    columns = [{'name': "Summary Measures", 'id': 0},
               {'name': "Values", 'id': 1},
               ]

    col = ("Date Range", "No of Ratings", "Average Rating", "Median Rating", "First Quartile", "Third Quartile",
           "Median Absolute Deviation")
    req_cols = pd.Series(col).reset_index()
    values = [date_range, no_rating, avg_rating, med_rating, q1_rat, q3_rat, mad_rat, col]
    req_vals = pd.Series(values).reset_index()
    data = req_cols.merge(req_vals, on='index')
    data = data.drop('index', axis=1)

    # boxplot
    box_df = rating_req[["rating"]]
    box_df1 = pd.crosstab(index=box_df["rating"], columns="count").reset_index()

    box_df1["per"] = (box_df1[["count"]] / box_df1[["count"]].sum()) * 100
    box_df1 = box_df1.sort_values(by=['rating'], ascending=False)

    fig = px.bar(box_df1, x=box_df1["per"], y=box_df1["rating"], orientation='h')
    fig.update_layout(xaxis_title="<b>Relative Frequency(%)</b>", yaxis_title="<b>Rating</b>")

    rating_add = rating_req.filter(['rating', 'week_rel'])
    rating_add = rating_add.groupby("week_rel").count().reset_index()
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # fig1 = px.box(rating_req,y='rating',color=rating_req.week_rel)
    # fig1.update_traces(quartilemethod="exclusive",alignmentgroup=True)
    fig1.add_trace(go.Box(x=rating_req.week_rel, y=rating_req.rating, marker_color='#3D9970'), secondary_y=False, )
    fig1.update_traces(quartilemethod="exclusive", alignmentgroup=True)
    fig1.add_trace(go.Scatter(x=rating_add.week_rel, y=rating_add.rating), secondary_y=True, )
    fig1.update_layout(xaxis_title="<b>Weeks since release</b>", yaxis_title="<b>Rating</b>", showlegend=False)
    fig1.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)

    date_ratings = rating_req.groupby("date").count().reset_index()
    date_ratings = date_ratings.filter(['date', 'rating'])

    fig2 = px.line(date_ratings, x='date', y='rating')
    fig2.update_layout(xaxis_title="<b>Date</b>", yaxis_title="<b>No of Rating</b>")

    quartile_bind = rating_req.groupby("date").describe()
    quartile_bind = quartile_bind.filter([('rating', '25%'), ('rating', '50%'), ('rating', '75%')]).reset_index()
    fig3 = px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['25%'])
    fig3.update_traces(name='1st Quartile', showlegend=True)

    fig3.add_trace(go.Scatter(x=quartile_bind['date'], y=quartile_bind['rating']['50%'],
                              mode='lines+markers',
                              name='Median',
                              line=dict(color='rgb(189,189,189)', width=8)))
    fig3.add_trace(go.Scatter(x=quartile_bind['date'], y=quartile_bind['rating']['75%'],
                              mode='lines+markers',
                              name='3rd Quartile'))
    # fig3.add_trace(px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['50%']))
    # fig3.update_traces(name='Median')

    # fig3.add_trace(px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['75%']))
    # fig3.update_traces(name='3rd Quartile')

    fig3.update_layout(xaxis_title="<b>Date</b>", yaxis_title="<b>No of Rating</b>")

    return data.values, columns, fig, fig3


# fig1,


# Week Callback
@app.callback([Output('table1', 'data'), Output('table1', 'columns'),
               Output('bar1', 'figure'), Output('box1', 'figure'), Output('line1', 'figure'),
               Output('quart_mean1', 'figure')],
              [Input('dropdown', 'value')])
def week_update(sel_week):
    rating_req1 = rating_df[rating_df.week_rel == sel_week]

    week_selected_since_release = sel_week
    no_rating = len(rating_req1)
    avg_rating = round(rating_req1.rating.mean(skipna=True), 2)
    med_rating = rating_req1.rating.median(skipna=True)
    q1_rat = rating_req1.rating.quantile(0.25)
    q3_rat = rating_req1.rating.quantile(0.75)
    # mad_rat = rating_req.rating.mad( skipna = True)
    mad_rat = (abs(rating_req1.rating - rating_req1.rating.median())).median()
    columns = [{'name': "Summary Measures", 'id': 0},
               {'name': "Values", 'id': 1},
               ]

    col = ("week_selected_since_release", "No of Ratings", "Average Rating", "Median Rating", "First Quartile",
           "Third Quartile", "Median Absolute Deviation")
    req_cols = pd.Series(col).reset_index()
    values = [week_selected_since_release, no_rating, avg_rating, med_rating, q1_rat, q3_rat, mad_rat, col]
    req_vals = pd.Series(values).reset_index()
    data = req_cols.merge(req_vals, on='index')
    data = data.drop('index', axis=1)

    # boxplot
    box_df = rating_req1[["rating"]]
    box_df1 = pd.crosstab(index=box_df["rating"], columns="count").reset_index()

    box_df1["per"] = (box_df1[["count"]] / box_df1[["count"]].sum()) * 100
    box_df1 = box_df1.sort_values(by=['rating'], ascending=False)

    fig = px.bar(box_df1, x=box_df1["per"], y=box_df1["rating"], orientation='h')
    fig.update_layout(xaxis_title="Relative Frequency(%)", yaxis_title="Rating")

    # rating_add=rating_req.filter(['rating','week_rel'])
    # rating_add=rating_add.groupby("week_rel").count().reset_index()
    # fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1 = px.box(rating_req1, y='rating', color=rating_req1.week_rel)
    fig1.update_traces(quartilemethod="exclusive", alignmentgroup=True)
    # fig1.add_trace(go.Box(x=rating_req.week_rel,y=rating_req.rating,marker_color = '#3D9970'),secondary_y=False,)
    # fig1.update_traces(quartilemethod="exclusive",alignmentgroup=True)
    # fig1.add_trace(go.Scatter(x=rating_add.week_rel, y=rating_add.rating),secondary_y=True,)
    fig1.update_layout(xaxis_title="Weeks since release", yaxis_title="<b>Rating</b>", showlegend=False)
    # fig1.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)

    date_ratings = rating_req1.groupby("date").count().reset_index()
    date_ratings = date_ratings.filter(['date', 'rating'])

    fig2 = px.line(date_ratings, x='date', y='rating')
    fig2.update_layout(xaxis_title="Date", yaxis_title="No of Rating")

    quartile_bind = rating_req1.groupby("date").describe()
    quartile_bind = quartile_bind.filter([('rating', '25%'), ('rating', '50%'), ('rating', '75%')]).reset_index()
    fig3 = px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['25%'])
    fig3.update_traces(name='1st Quartile', showlegend=True)

    fig3.add_trace(go.Scatter(x=quartile_bind['date'], y=quartile_bind['rating']['50%'],
                              mode='lines+markers',
                              name='Median',
                              line=dict(color='rgb(189,189,189)', width=8)))
    fig3.add_trace(go.Scatter(x=quartile_bind['date'], y=quartile_bind['rating']['75%'],
                              mode='lines+markers',
                              name='3rd Quartile'))
    # fig3.add_trace(px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['50%']))
    # fig3.update_traces(name='Median')

    # fig3.add_trace(px.line(quartile_bind, x=quartile_bind['date'], y=quartile_bind['rating']['75%']))
    # fig3.update_traces(name='3rd Quartile')

    fig3.update_layout(xaxis_title="<b>Date</b>", yaxis_title="<b>No of Rating</b>")

    return data.values, columns, fig, fig1, fig2, fig3


# Radio Button Callback for 3 radio button-Rating Distribution
@app.callback(Output('dm_box', 'figure'),
              [
                  Input('date_range_picker', 'start_date'),
                  Input('date_range_picker', 'end_date'),
                  Input('ri', 'value')])
def render_charts1(start_date1, end_date1, value1):
    start_date1 = datetime.strptime(start_date1, '%Y-%m-%d').date()
    print("2nd :", start_date1)

    end_date1 = datetime.strptime(end_date1, '%Y-%m-%d').date()

    print(end_date1)

    mask2 = (rating_df['date'] >= start_date1) & (rating_df['date'] <= end_date1)

    rating_req2 = rating_df.loc[mask2]

    # weekly Data
    rating_add2 = rating_req2.filter(['rating', 'week_rel'])
    rating_add2 = rating_add2.groupby("week_rel").count().reset_index()

    # Day data
    rating_add3 = rating_req2.filter(['rating', 'date'])
    rating_add3 = rating_add3.groupby("date").count().reset_index()

    # Month Data
    rating_req2["monthly"] = pd.to_datetime(rating_req2['date']).dt.month_name()
    rating_add4 = rating_req2.filter(['rating', 'monthly', 'year'])
    rating_add4 = rating_add4.groupby(["monthly", "year"]).count().reset_index()
    rating_add4 = sort_dataframeby_monthorweek.Sort_Dataframeby_Month(df=rating_add4, monthcolumnname='monthly')
    rating_add4 = rating_add4.sort_values(by="year")

    # Secondary Y axis Activation
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1.add_trace(go.Box(x=rating_req2.week_rel, y=rating_req2.rating, marker_color='#3D9970'), secondary_y=False, )
    fig1.update_traces(quartilemethod="exclusive", alignmentgroup=True)
    fig1.add_trace(go.Scatter(x=rating_add2.week_rel, y=rating_add2.rating), secondary_y=True, )
    fig1.update_layout(xaxis_title="<b>Weeks since release</b>", yaxis_title="<b>Rating</b>", showlegend=False)
    fig1.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)

    fig2.add_trace(go.Box(x=rating_req2.date, y=rating_req2.rating, marker_color='#3D9970'), secondary_y=False, )
    fig2.update_traces(quartilemethod="exclusive", alignmentgroup=True)
    fig2.add_trace(go.Scatter(x=rating_add3.date, y=rating_add3.rating), secondary_y=True, )
    fig2.update_layout(xaxis_title="<b>Day Wise</b>", yaxis_title="<b>Rating</b>", showlegend=False)
    fig2.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)

    # to_period('M')
    # rating_req2["monthly"]=pd.to_datetime(rating_req2['date']).strftime("%d %B, %Y")
    # rating_req2["monthly"]=pd.to_datetime(rating_req2['date']).dt.to_period('M')

    # fig3 =px.box(rating_req2,y='rating',color=rating_req2.monthly)
    # fig3.update_traces(quartilemethod="exclusive",alignmentgroup=True)
    # figg=px.box(rating_req2,x=rating_req2.monthly,color=rating_req2.rating)
    # fig3.add_trace(figg,secondary_y=False)

    # fig3.add_trace(px.line(rating_add4,x=rating_add4.monthly, y=rating_add4.rating),secondary_y=True,)

    fig3.add_trace(go.Box(x=rating_req2.monthly, y=rating_req2.rating, marker_color='#1a9bdb'), secondary_y=False, )
    fig3.update_traces(quartilemethod="exclusive", alignmentgroup=True)
    fig3.add_trace(go.Scatter(x=rating_add4.monthly, y=rating_add4.rating,
                              hovertemplate='<i>Months</i>: %{x}' +
                                            '<br><b>Total Reviews</b>:%{y}<br>'), secondary_y=True, )
    fig3.update_layout(xaxis_title="<b>Monthly</b>", yaxis_title="<b>Rating</b>", showlegend=False)
    fig3.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)

    if value1 == 1:

        return fig1

    elif value1 == 2:

        return fig2
    elif value1 == 3:

        return fig3


if __name__ == '__main__':
    host = socket.gethostbyname(socket.gethostname())
    application.run(debug=False, host=host, port=8080)


# =============================================================================
# Test Purpose
# =============================================================================
# app.run_server(debug=False, port=8080,host='0.0.0.0')


# start_date =datetime.strptime(re.split('T| ', rel1)[0], '%Y-%m-%d')
# end_date=datetime.strptime(rel1,'%Y-%m-%d').date()
# start_date_string = start_date.strftime('%B %d, %Y')

# mad_rat = stats.median_absolute_deviation(rating_df.rating,axis=0)
# from astropy.stats import median_absolute_deviation
# mad = median_absolute_deviation(rating_df.rating)
# mad1=(abs(rating_df.rating-rating_df.rating.median())).median()

# import plotly.offline as pyo
# fig=px.box(rating_req2,x=rating_req2.monthly,color=rating_req2.rating)
# fig.add_trace({'x':rating_add4["monthly"],'y':rating_add4["rating"],'type':'scatter','name':'Dist Avg'},1,1)
# pyo.plot(fig)
# fig3 = make_subplots(cols=1,rows=1,specs=[[{"secondary_y": True}]])
# fig.add_trace(go.Box(y=rating_req2.rating),row=1,col=1,secondary_y=False,)
##fig3.add_trace(go.Box(y=rating_req2.rating),secondary_y=False,)
# fig3.update_traces(quartilemethod="exclusive",alignmentgroup=True)
# fig3.add_trace(go.Scatter(x=rating_add4.monthly, y=rating_add4.rating),row=1,col=1,secondary_y=True,)
# fig3.update_layout(xaxis_title="<b>Monthly</b>",yaxis_title="<b>Rating</b>",showlegend=False)
# fig3.update_yaxes(title_text="<b>Reviewers</b> ", secondary_y=True)
# pyo.plot(fig3)

# fig1 =px.box(rating_req2,y='rating',color=rating_req2.monthly)
# fig1.update_traces(quartilemethod="exclusive",alignmentgroup=True)
# pyo.plot(fig1)
# rating_req2["monthly"]=pd.to_datetime(rating_req2['date']).dt.to_period('M')
# import calendar
# df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
# rating_req2["monthly"]=pd.to_datetime(rating_req2['date']).dt.month.apply(lambda x: calendar.month_abbr[x])
# rating_req2["monthly"]=pd.to_datetime(rating_req2['date']).apply(lambda x: x.strftime('%B-%Y'))
