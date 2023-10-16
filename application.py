from flask import Flask, render_template, request, session, redirect, url_for
import config.VARS as VARS
from requests import Session
from scripts.controllers.forms import BigFiveForm, TravelStyles, CityRater
import scripts.stats.nmf as nmf
import scripts.stats.distances as ds
import scripts.viz.viz as viz


from functools import reduce
from operator import add

import pandas as pd


locations = pd.read_csv('./data/city_geolocation.csv', index_col=0)


new_user = VARS.USER_CHARS.iloc[-1:,:]
new_user = new_user.copy()
new_user.iloc[0,:] = 0
new_user['username'] = "_flaskuser"


# sess = Session()

app = Flask(__name__)

user_char_input = {}
user_style_input = {}
user_city_input = {}

@app.route('/', methods = ['GET', 'POST'])
def index():

    render = render_template('index.html')

    return render




@app.route('/bigfive/', methods = ['GET', 'POST'])
def bigfive():

    form_bigfive = BigFiveForm()

    if form_bigfive.validate_on_submit():

        age_value = reduce(add, form_bigfive.age.data)
        
        
        # age_choices = dict(form_bigfive.age.choices)
        # age_label = age_choices[age_value]

        user_char_input['open'] = form_bigfive.open.data
        user_char_input['cons']  = form_bigfive.cons.data
        user_char_input['extra'] = form_bigfive.extra.data
        user_char_input['agree'] = form_bigfive.agree.data
        user_char_input['neuro'] = form_bigfive.neuro.data
        user_char_input[age_value] = 1

        # [print(v, k) for v, k in user_char_input.items()]



        return redirect(url_for('travelstyle'))

    return render_template('bigfive.html', form = form_bigfive)





@app.route('/travelstyle/', methods = ['GET', 'POST'])
def travelstyle():

    form_style = TravelStyles()


    if form_style.validate_on_submit():

        for input in form_style.style.data:
            user_style_input[input] = 1

        # [print(v, k) for v, k in user_style_input.items()]


        return redirect(url_for('rater'))


    return render_template('travelstyle.html', form = form_style)



@app.route('/rater/', methods = ['GET', 'POST'])
def rater():
    
    form_city = CityRater()

    if form_city.validate_on_submit():

        user_city_input['good'] = form_city.goodcity.data 
        user_city_input['bad'] = form_city.badcity.data if form_city.badcity.data is not None else None

        


        return redirect(url_for('recommender'))

    return render_template('rater.html', form = form_city)




@app.route('/recommender/', methods = ['GET', 'POST'])
def recommender():

    # [print(k,v) for k,v in user_char_input.items()]
    # [print(k,v) for k,v in user_style_input.items()]

    for k, v in user_char_input.items():
        new_user.loc[:, k] = v

    for k, v in user_style_input.items():
        new_user.loc[:, k] = v


    # # calculate distances between new user and user characteristics data


    dists = ds.Distancer(user_matrix=VARS.USER_CHARS)


    dtest = dists.calculate(new_user=new_user)
    top_n = dists.top_n_closest(n = 500)

    # Subset ratings matrix with users
    # Note that ratings matrix only contains cities with more than 5 reviews
    REVIEWS = nmf.subset_reviews(top_n.index, VARS.CITY_REVIEWS)

    nmfrec = nmf.nmfer(reviews = REVIEWS, n_components=20)
    nmfrec.set_model()


    recs = nmfrec.get_best_cities(
        X = nmfrec.new_review(
                top_cities = user_city_input['good'],
                bottom_cities= user_city_input['bad'],
                other_ratings=0.2
            ),
        n = 10)


    loc_rec = locations.loc[recs.index, :]
    recs['na'] = locations.lon.isna()

    
    
    
    plot = viz.plot_locations(lat = loc_rec.lat, lon = loc_rec.lon, locations=recs.index)

    recs = recs.reset_index().values.tolist()
  

    return render_template('recommender.html', recs = recs, plot = plot)




@app.route('/travelexplore/', methods = ['GET', 'POST'])
def travelex():

    render = render_template('db_explore.html')
      
    return render

@app.route('/about/travellers/', methods = ['GET', 'POST'])
def about_travellers():

    render = render_template('about_travellers.html')
      
    return render


@app.route('/about/locations/', methods = ['GET', 'POST'])
def about_locations():

    render = render_template('about_cities.html')
      
    return render


# @app.route('/api/data/')
# def data():

#     data_dict = {'data' : [r.to_dict() for i,r in rc.movies.reset_index().iterrows()]}
#     print(data_dict['data'][0])

#     return data_dict

# @app.route('/dbmovies/')
# def dbmovies():

#     return render_template("db_movies.html")

# @app.route('/dbusers/')
# def dbusers():

#     plot = viz.plot_users()

#     return render_template("db_users.html", plot = plot)



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'


    # sess.init_app(app)
    app.run(debug=True)
    
