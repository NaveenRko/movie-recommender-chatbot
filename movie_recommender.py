import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Load dataset
df = pd.read_csv("South_Indian_movies_cleaned.csv")

# Force all string cols to string type
df['title'] = df['title'].astype(str).fillna("")
df['director'] = df['director'].astype(str).fillna("")
df['clean_cast'] = df['clean_cast'].astype(str).fillna("")
df['language'] = df['language'].astype(str).fillna("")

# Combine safely
df['metadata'] = (
    df['title'].fillna("") + " " + 
    df['director'].fillna("") + " " + 
    df['clean_cast'].fillna("")
)

# Check for leftovers
print(df['metadata'].isna().sum())   # should print 0

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['metadata'])

# Similarity Matrix
# cosine_sim = cosine_similarity(tfidf_matrix)

# # Reset index for safe access
# df = df.reset_index(drop=True)

# def recommend(movie_title):
#     movie_title = movie_title.lower()
#     indices = df[df['title'].str.lower() == movie_title].index

#     if len(indices) == 0:
#         return []

#     idx = indices[0]
#     sim_scores = list(enumerate(cosine_sim[idx]))

#     # Get language and year to filter
#     lang = df.loc[idx, 'language']
#     year = df.loc[idx, 'year']
    
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:100]  # Exclude the movie itself

#     # Filter by same language and within +/- 10 years
#     filtered_movies = []
#     for i, score in sim_scores:
#         if df.loc[i, 'language'] == lang and abs(df.loc[i, 'year'] - year) <= 10:
#             filtered_movies.append((df.loc[i, 'title'], df.loc[i, 'year'], df.loc[i, 'language']))
#         if len(filtered_movies) == 5:
#             break
#     return filtered_movies

# due to memory error using nearestneighbors
# Use NearestNeighbors for top-k cosine similarity
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(tfidf_matrix)

# Reset index for safe access
df = df.reset_index(drop=True)

def recommend(movie_title):
    movie_title = movie_title.lower()
    indices = df[df['title'].str.lower() == movie_title].index

    if len(indices) == 0:
        return []

    idx = indices[0]
    movie_vector = tfidf_matrix[idx]

    # Find top 100 similar movies
    distances, indices = nn.kneighbors(movie_vector, n_neighbors=100)

    # Get language and year to filter
    lang = df.loc[idx, 'language']
    year = df.loc[idx, 'year']

    # Filter: same language & within ±10 years
    filtered_movies = []
    for i in indices[0][1:]:  # Skip the movie itself
        if df.loc[i, 'language'] == lang and abs(df.loc[i, 'year'] - year) <= 10:
            filtered_movies.append((df.loc[i, 'title'], df.loc[i, 'year'], df.loc[i, 'language']))
        if len(filtered_movies) == 5:
            break

    return filtered_movies

def recommend_similar(movie_title):
    if movie_title is None:
        return "I couldn’t find the movie you entered. You can try the Recommender System on the left panel — it’s built to help you discover similar movies more easily."
    sim_movies = recommend(movie_title)
    if len(sim_movies)==0:
        return f"Sorry I don't have any movies named {movie_title}."
    html_output = "<ul>\n" 
    for title, year, language in sim_movies:
        html_output += f"  <li>{title} ({year}, {language})</li>\n"
    html_output += "</ul>"
    return f"Here are the movies similar to {movie_title}: {html_output}"







