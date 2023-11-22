from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_draggable

df = pd.read_csv('https://raw.githubusercontent.com/yupest/nti/master/%D0%9D%D0%A2%D0%98-2021/movies_emotions.csv')

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children='Application with movies', style={'textAlign': 'center'}),
    html.Div(children='emotion:', style={'font-size': 18, 'padding': 5}),
    dcc.Dropdown(
        df.emotion.unique(),
        value='Атмосферный',
        id='dropdown-emotion',
        persistence='local',
        multi=False),
    html.Div(children='genre:', style={'font-size': 18, 'padding': 5}),
    dcc.Dropdown(
        df.genres.unique(),
        value='Детектив',
        id='dropdown-genres',
        persistence='local',
        multi=False),
    dash_draggable.ResponsiveGridLayout([
        dcc.Graph(id='top-10'),
        dcc.Graph(id='pie'),
        dcc.Graph(id='linear'),
        dcc.Graph(id='scatter', figure=px.scatter(df, x='rating_emotion', y='rating'
                                                  , title='Зависимость рейтинга и рейтинга эмоций'))
    ]),

])


@callback(
    Output('top-10', 'figure'),
    Input('dropdown-emotion', 'value'),
    Input('dropdown-genres', 'value')
)
def update(emotion, genres):
    dff = df[(df.emotion == emotion) & (df.genres == genres)].sort_values('rating', ascending=False).head(10)
    return px.bar(dff, x='title', y='rating', title='Топ-10 фильмов')


@callback(
    Output('pie', 'figure'),
    Input('dropdown-emotion', 'value'),
    Input('dropdown-genres', 'value')
)
def update(emotion, genres):
    dff = df[(df.emotion == emotion) & (df.genres == genres)].sort_values('rating', ascending=False)
    len_choose = len(dff.title.unique())
    len_full = len(df.title.unique())
    return px.pie(values=[len_choose, len_full - len_choose], names=['Подходящие', 'Остальные']
                  , title='Результат отбора')


@callback(
    Output('linear', 'figure'),
    Input('dropdown-genres', 'value')
)
def update(genres):
    dff = df[(df.genres == genres)]
    ans = pd.DataFrame(dff.value_counts('emotion'))

    return px.line(ans, x=ans.index, y='count', title='Количество эмоций по выбранному жанру')


if __name__ == '__main__':
    app.run(debug=True)
