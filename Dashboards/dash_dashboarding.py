#DASH
#Dashboarding with Dash - intro
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

colors = {"background":"#111111", "text":"#7FDBFF"} #store colors in same dict


app.layout = html.Div(children=[
    html.H1("Hello Dash!",style={"textAlign":"center",
                                "color":colors["text"]}), #CSS style calls
    html.Div("Dashing, dashing!"),
    dcc.Graph(id="example",
            figure={"data":[
                {"x":[1,2,3],"y":[4,1,2],"type":"bar","name":"SF"},
                {"x":[1,2,3],"y":[4,3,1],"type":"bar","name":"NYC"}
            ],
            "layout":{
                "plot_bgcolor":colors["background"],
                "paper_bgcolor":colors["background"],
                "font":{"color":colors["text"]},
                "title":"Bar plots"
            }
            })
        ], style={"backgroundColor":colors["background"]}

)

if __name__ == "__main__":
    app.run_server()
