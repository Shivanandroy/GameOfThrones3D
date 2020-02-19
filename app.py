# importing packages
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly_express as px
import sd_material_ui as sd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,"https://codepen.io/chriddyp/pen/brPBPO.css"])
app.title="Game of Thrones"
# Loading screen CSS
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

data = pd.read_csv("got_embeddings.csv")

#fig = px.scatter_3d(df[:10000], x='Dimension 1', y="Dimension 2", z="Dimension 3", height=600, size='frequency', color='frequency', hover_name='words')

app.layout = html.Div([

	html.Div(html.H4("Visualizing Game of Thrones with BERT"), style={'textAlign':'center','backgroundColor':'#ff8533','color':'white','font-size':5,'padding':'1px'}),
	
	dbc.Row([
		dbc.Col([

			html.Br(),
			html.Div("Choose a Book", style={'font-weight':'bold'}),
			sd.DropDownMenu(id='book',
                                    value='Book 1',
                                    options=[
                                        dict(value='Book 1', primaryText='Game of Thrones 1',
                                             label='Game of Thrones 1'),
                                        dict(value='Book 2', primaryText='Game of Thrones 2'),
                                        dict(value='Book 3', primaryText='Game of Thrones 3'),
										dict(value='Book 4', primaryText='Game of Thrones 4'),
                                        dict(value='Book 5', primaryText='Game of Thrones 5'),
                                    ],
                                    menuStyle=dict(width=300),  # controls style of the open menu
                                    listStyle=dict(height=35),
                                    selectedMenuItemStyle=dict(height=30),
                                    anchorOrigin=dict(vertical='bottom', horizontal='right')),
			

			html.Hr(),

			html.Div("Number of words:", style={'font-weight':'bold'}),
			dcc.Slider(id='num_words', min=0, tooltip={'always_visible':False}, value=5000, max=10000, step=100),

			html.Hr(),

			html.Div("Projection", style={'font-weight':'bold'}),
			dbc.RadioItems( options=[{"label": "Truncated SVD", "value": "tSVD"},
									 {"label": "PCA", "value": "PCA"}],
									 value="tSVD", id="projection"),
			
			html.Hr(),

			html.Div("Options", style={'font-weight':'bold'}),
			dbc.Checklist(options=[{"label": "Show Noun Phrases", "value": 'noun'}],
			            	id="noun_toggle",switch=True, value=[]),
			dbc.Checklist(options=[{"label": "Show Unique Words", "value": 'unique'}],
			            	id="unique_toggle",switch=True, value=['unique']),
			dbc.Checklist(options=[{"label": "Remove Stopwords", "value": 'stopword'}],
			            	id="stopword_toggle",switch=True, value=['stopword']),
			
			html.Hr(),

		], width=2),

		dbc.Col(dcc.Graph(id='visualization'), width=10)




	], no_gutters=True)
	
	])



@app.callback(Output("visualization", "figure"),
    [
        Input("book", "value"),
        Input("num_words", "value"),
        Input("projection", "value"),
		Input("noun_toggle", "value"),
		Input("unique_toggle", "value"),
		Input("stopword_toggle", "value")
    ],
)
def on_form_change(book_num, num_words, projection, is_noun, is_unique, is_stopwords):
	
	df = data[(data.book == book_num) & (data.type == projection) & (data.length != 1)]
	df['word_usage'] = pd.qcut(df.frequency,5, labels=['Rare','Less Frequent','Moderate', 'Frequent','Most Frequent'])
	if "noun" in is_noun:
		df = df[df.pos == "NN"]
	if "unique" in is_unique:
		df = df.loc[df.words.drop_duplicates().index]
	
	if "stopword" in is_stopwords:
		df = df[df.stopwords == False]
	df = df.sort_values(by='frequency', ascending=False)[:num_words]
	n_words = df.shape[0]
	fig = px.scatter_3d(df, x='Dimension 1', y="Dimension 2", z="Dimension 3", height=600, size='frequency', color='frequency', size_max=40,hover_name='words')
	
	fig.update_layout(	
			scene = dict(
                    xaxis = dict(
                         backgroundcolor="white",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
						 ticks='',
						showticklabels=False),
                    yaxis = dict(
                        backgroundcolor="white",
                        gridcolor="white",
                        showbackground=True,
                        zerolinecolor="white",
						ticks='',
						showticklabels=False),
                    zaxis = dict(
                        backgroundcolor="white",
                        gridcolor="white",
                        showbackground=True,
                        zerolinecolor="white",
						ticks='',
						showticklabels=False),
					xaxis_title='.',
                    yaxis_title='.',
                    zaxis_title='.'
						
						),
						
                    
                  )
	return fig



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)