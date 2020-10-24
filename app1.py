# -*- coding: utf-8 -*-

"""
Step 2
Import Packages (here are the packages used for SDG)
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
fig = go.Figure()
import pandas as pd
import yfinance as yf
import datetime
from datetime import date

#%%

#Get 5_yaer historical data from yahoo finance and store it in a shared folder
 
tickers=['SPY','AAPL','MSFT','FB','GOOG']
tickers.append('SPY')
min_date_allowed=date(2015,10,15)
max_date_allowed=date.today()+datetime.timedelta(days=1)
end_date = date.today()


df=yf.download(tickers,min_date_allowed,max_date_allowed)
dfff = df['Close']
df.to_csv('raw_data.csv')
df_csv = pd.read_csv('raw_data.csv')
 

#%%
 #get closing price
df['Close'].to_csv('Close.csv', header = True)
df_Close = pd.read_csv('Close.csv')
 
 #next day
next_day = datetime.date.today() + datetime.timedelta(days=1)
 #get next day closing price
next_day_closing = yf.download(tickers,end_date,next_day)
next_day_closing['Close'].to_csv('Next_day_Close.csv', header = True)
df_next_day_Close = pd.read_csv('Next_day_Close.csv')
 
 #Add it as a new row on the table
new_row = pd.concat([df_Close,df_next_day_Close])
 #recalculate index after a concatenation
#new_row.reset_index(inplace=True, drop=True) 
new_row.to_csv('updated_close.csv')
daily_close = new_row.to_csv('updated_close.csv')


dff = daily_close = pd.read_csv('updated_close.csv', index_col=1)

#%%
df_monthly_returns = df['Adj Close'].resample('M').ffill().pct_change()

#%%
# Calculate the 20 and 100 days moving averages of the closing prices
df_short_rolling = df['Adj Close'].rolling(window=20).mean()
df_long_rolling = df['Adj Close'].rolling(window=100).mean()


#%%
app = dash.Dash()
server = app.server
app.layout = html.Div([
    html.Br(),
    html.Br(),
        ##header and logo
    html.Div([
        html.H1('SDG-Index', className = 'ten columns', style = {'margin-top': 10, 'margin-left': 15}),
        html.Img(
            src='https://images.squarespace-cdn.com/content/5c036cd54eddec1d4ff1c1eb/1557908564936-YSBRPFCGYV2CE43OHI7F/GlobalAI_logo.jpg?content-type=image%2Fpng',
            style = {
                'height': '11%',
                'width': '11%',
                'float': 'right',
                'position': 'relative',
                'margin-top': 11,
                'margin-right': 0,
                'columnCount': 2
            },
            className='two columns'
        )
      
    ],className = 'row'),
    
    html.Br(),

    dbc.Row(
        [
            ##Dropdown for select company
            dbc.Col(
                html.Div([
                    html.H1('Select Company:'),
                    dcc.Dropdown(id='my_dropdown',
                    options=[
                        {'label': 'S&P 500', 'value': 'SPY'},
                        {'label': 'APPLE', 'value': 'AAPL'},
                        {'label': 'MICORESOFT', 'value': 'MSFT'},
                        {'label': 'FACEBOOK', 'value': 'FB'},
                        {'label': 'GOOGLE', 'value': 'GOOG'}
                    ],
                    value='SPY'
                    ),
                ]),
                style={'display':'inline-block','color':'lightblue'},
                width=4,
                align="start",
            ),
            
            ##Dropdown for select TimeRange
            dbc.Col(
                html.Div([
                    html.H4('Select Date Range'),
                              dcc.DatePickerRange(id='date_range',
                                                  min_date_allowed=date(2015,10,15),
                                                  max_date_allowed=date.today(),
                                                  start_date=date(2015,10,15),
                                                  end_date=date.today())
                         ],
                             style={'display':'inline-block','color':'lightblue'}
                             ),width=4,
                             align="end",
                    ),
        ]
    ),
    
    #Submitbutton
    html.Br(),
    html.Br(),
    html.Div([
        dbc.Button(children='Submit',id='button',n_clicks=0,block=True),
    ]),

    html.Br(),
    
    #Graph
    dbc.Row([
        dbc.Col(dcc.Graph(
                    id='trend',
                    figure={
                    },
                ),
                width={'size':10,'offset':1}
            ),
        
    ]),
    
    
    
    ###
    html.Br(),
    
    #Greturns
    dbc.Row([
        dbc.Col(dcc.Graph(
                    id='returns',
                    figure={
                    },
                ),
                width={'size':10,'offset':1}
            ),
        
    ]),
    
 ###
    html.Br(),
    
    html.Div([
    #rolling
    dbc.Row([
        dbc.Col(dcc.Graph(
                    id='rolling',
                    figure={
                    },
                ),
                width={'size':10,'offset':1}
            ),
        
        dbc.Col(dcc.Graph(
                    id='momentum',
                    figure={
                    },
                ),
                width={'size':10,'offset':1}
            ),
    ]),    
        ],style = {'columnCount': 2}),
    
    
    html.Br(),
    
    
    html.Div([
        #maxclosing,minclosing
    dbc.Row([
        dbc.Col(dcc.Graph(
                    id='minclosing',
                    figure={
                    },
                ),
                width={'size':5,'offset':1}
                
            ),
        
        dbc.Col(dcc.Graph(
                    id='maxclosing',
                    figure={
                    },
                ),
                width={'size':5,'offset':0}
                
            ),
        
        
    ]), 
        ],style = {'columnCount': 2}),
    
 ###
    html.Br(),
    
    #heatmap
    dbc.Row([
        dbc.Col(dcc.Graph(
                    id='heatmap',
                    figure={
                    },
                ),
                width={'size':10,'offset':1}
            ),
        
    ]),    
])   



@app.callback(
    [dash.dependencies.Output('trend', 'figure'),
     dash.dependencies.Output('returns', 'figure'),
     dash.dependencies.Output('rolling', 'figure'),
     dash.dependencies.Output('maxclosing','figure'),
     dash.dependencies.Output('minclosing','figure'),
     dash.dependencies.Output('momentum','figure'),
     dash.dependencies.Output('heatmap','figure')
     ],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('my_dropdown', 'value'),
     dash.dependencies.State("date_range", "start_date"),
     dash.dependencies.State("date_range", "end_date"),
     ]
    )


def update_graph(n_clicks,ticker,start_date,end_date):
    print(n_clicks)
    
    new_dff = dff.loc[start_date:end_date,:]
    new_df_monthly_returns = df_monthly_returns.loc[start_date:end_date,:]
    new_df_short_rolling = df_short_rolling.loc[start_date:end_date,:]
    new_df_long_rolling = df_long_rolling.loc[start_date:end_date,:]
    
###trend
    traces = [
        go.Scatter(x=new_dff.index, y=new_dff[ticker], mode="lines", name=ticker),
             ]

    trend_update = go.Figure(
      data=traces,
      layout={
            'title': {'text':f'{ticker} Price',
                      'xanchor': 'center', 'x': 0.5},
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Price'},
            'legend': {'x': 0, 'y': 1},
            'hovermode':'closest',
            #'paper_bgcolor': "Black",
            #'plot_bgcolor': 'Black',
            #'font': {'color': '#997fff'}

            },
      
      )
###returns
    traces2 = [
        go.Scatter(x=new_df_monthly_returns.index, y=new_df_monthly_returns[ticker], mode="lines", name=ticker),
             ]

    returns_update = go.Figure(
      data=traces2,
      layout={
            'title': {'text':f'{ticker} monthly returns',
                      'xanchor': 'center', 'x': 0.5},
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Percent'},
            'legend': {'x': 0, 'y': 1},
            'hovermode':'closest',
            #'paper_bgcolor': "Black",
            #'plot_bgcolor': 'Black',
            #'font': {'color': '#997fff'}

            },
      
      )
    
###rolling
    traces1 = [
        go.Scatter(x=new_df_short_rolling.index, y=new_df_short_rolling[ticker], mode="lines", name=ticker),
        go.Scatter(x=new_df_long_rolling.index, y=new_df_long_rolling[ticker], mode="lines", name=ticker)
             ]

    rolling_update = go.Figure(
      data=traces1,
      layout={
            'title': {'text':f'{ticker} 20 and 100 days moving averages of the closing prices',
                      'xanchor': 'center', 'x': 0.5},
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Percent'},
            'legend': {'x': 0, 'y': 1},
            'hovermode':'closest',
            #'paper_bgcolor': "Black",
            #'plot_bgcolor': 'Black',
            #'font': {'color': '#997fff'}

            },
      
      )
    
###maxclosing
    traces3 = [
        go.Indicator(mode='gauge+number',value=new_dff[ticker][-1]),
             ]

    maxclosing_update = go.Figure(
      data=traces3,
      layout={
          'title': {'text': f'{ticker} Max closing price',
                          'xanchor': 'center', 'x': 0.5},
                
          'paper_bgcolor': "Black",   
          'plot_bgcolor': 'Black',
          'font': {'color': 'Blue'}
          
          },
      
      ) 

###minclosing
    traces4 = [
        go.Indicator(mode='gauge+number',value=new_dff[ticker][+1]),
             ]

    minclosing_update = go.Figure(
      data=traces4,
      layout={
          'title': {'text': f'{ticker} Min closing price',
                          'xanchor': 'center', 'x': 0.5},
                
          'paper_bgcolor': "Black",   
          'plot_bgcolor': 'Black',
          'font': {'color': 'Red'}
          
          },
      
      )

###momentum
    traces5 = [
        go.Scatter(x=new_dff.index, y=new_dff[ticker]/new_dff[ticker].shift(20), mode="lines", name=ticker),
             ]

    momentum_update = go.Figure(
      data=traces5,
      layout={
          'title': {'text':f'{ticker} 20 days momentum',
                      'xanchor': 'center', 'x': 0.5},
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Percent'},
            'legend': {'x': 0, 'y': 1},
            'hovermode':'closest',
          
          },
      
      )   

###heatmap

    matrix_df = new_dff.fillna(0)
    traces6=[
        go.Heatmap(
            x=matrix_df.columns,
            y=matrix_df.columns,
            z=matrix_df.corr(),
            colorscale='viridis'
                   )
            ]
    heatmap_update = go.Figure(data=traces6,
                               layout = {'title': {'text': 'Stocks Heatmap',
                                                    'xanchor': 'center','x':0.52,
                                                    'yanchor':'top',
                                                   },
                                         'paper_bgcolor': "Black",
                                         'plot_bgcolor': 'Black',
                                         'font': {'color': 'Orange'}

                                         })
      
    return trend_update,returns_update,rolling_update,maxclosing_update,minclosing_update,momentum_update,heatmap_update


#%%
print(dff.index)

#%%
if __name__=='__main__':
    app.run_server(debug=True,port=7000)