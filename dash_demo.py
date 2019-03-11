# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 12:35:50 2018

@author: YIPINL
"""

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        username='9ae93ac4-8752-4d42-8773-ac9200eedce5',
        password='ci3M6CFZfCxG',
        url='https://gateway.watsonplatform.net/tone-analyzer/api'
    )
app = dash.Dash()

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='I like you'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])

def update_output(n_clicks,input1):
    tone_analysis = tone_analyzer.tone(
    {'text': input1},
    'application/json'
    ).get_result()
    score = tone_analysis['document_tone']['tones'][0]['score']
    tone_name = tone_analysis['document_tone']['tones'][0]['tone_name']
    
    return u'''
        The button has been pressed for "{}" times,
        The input is "{}",
        Tone name is "{}",
        Score is "{}"
    '''.format(n_clicks,input1, tone_name,score)

if __name__ == '__main__':
    app.run_server(debug=True)

















