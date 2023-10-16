# NexTrip - Smart location recommender

<strong>NexTrip &#9992;</strong> helps you find your next destination.
     
<br>
NexTrip uses Non-negatve Matrix Factoring (<strong>NMF</strong>) to predict destination ratings based on your preferences from the experience of similar users (calculated with <strong>Euclidian Distances</strong>).
<br>
Find out more about the statistics in the background, which are frequently used in recommender systems <a href="https://en.wikipedia.org/wiki/Non-negative_matrix_factorization">here</a>.

## Development

**Nextrip** is a the final project of a 12 week data science bootcamp I participated in during 2022.
The app was written over the course of 10 days. 
It uses several concepts that I learned and/or improved on during the bootcamp, ranging from:

- `bash` scripting
- `python` scripting and software development
- ETL concepts (including `SQL`, `docker compose` for hosting `PostgreSQL` on AWS)
- data visualization with `matplotlib`, `seaborn` and dashboarding tools like `metabase`
- machine learning concepts (supervised/unsupervised classification, regression approaches, image processing, deep learning, using `pipelines`)
- web development with `flask` and `bootstrap`

## Approach and Data

The underlying observations are derived from a TripAdvisor data set developed by Alexandra Roshchinain October 2015; it is licensed  under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/). See the readme included in [_etl/tripadvisor/TripAdvisor_dataset_2015.rar](_etl/tripadvisor/TripAdvisor_dataset_2015.rar) for details. 

The data is cleaned and transformed in [_etl/02_read_transform.py](_etl/02_read_transform.py):
- Missing age classes are replaced with the median age class.
- Missing travel styles are replaced with random sampling from all existing classing using their respective weights
- Age classes and travel styles are one hot encoded and combined with personality scores
- Individual ratings for a given user are summarized across all categories (e.g., restaurants, hotelts) for each city/location
- An attempt is made to geolocate each city/location by name through the `OpenStreetMap Overpass API` in [_etl/03_geolocation.py](_etl/03_geolocation.py)


NexTrip aims to identify suitable cities and locations as future travel destinations that are likely enjoyable to the user.
It does this by 1) identifying similar travellers, and 2) identiying suitable destinations based on the reviews of these similar travellers:  

1. NexTrip identifies the 500 closest travellers based on age, travel style and personality scores from the TripAdvisor data set based on user input. For this, `euclidian_distances()` from `sklearn.metrics` is used ([see scripts/stats/distances.py](scripts/stats/distances.py)).  
2. Non-negatve Matrix Factoring is implemented to identify potential destinations based on previous travellers' ratings. Predictions can be improved by providing information on destination likes and dislikes. For this, `NFM` from `sklearn.decomposition` is applied ([see scripts/stats/nmf.py](scripts/stats/nmf.py)).

## Licensing

MIT License

Copyright (c) 2023 Alexander Hurley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.