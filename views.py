from django.shortcuts import render
import dash 
import dash_core_components as dcc
import dash_html_components as html

def graph(request):
    views = dash.Dash()
    views.layout = html.Div(
        html.H1(children="Charted Data hai ye!!")
    )
    return render(request,'chartedData/graph.html')