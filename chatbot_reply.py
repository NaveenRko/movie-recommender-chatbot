import random
import pandas as pd
import datetime
from entity_extraction import extract_entities,extract_actor
from intent_classifier import predict_intent
from movie_recommender import recommend, recommend_similar
from tmdb_api_helper import get_movie_info, get_person_info

# Load your metadata
df = pd.read_csv("South_Indian_movies_cleaned.csv")  # containing title, cast, director, year, decade, language

#------------------------------------------------------------------#
# -------------------Conversational Intents------------------------#

# Fallback for simple fun/joke/greeting responses
jokes = [
    "Why don’t movie stars use calendars? Because their days are already numbered! 🎬",
    "What do you call a movie about vegetables? A *romaine*-tic comedy! 🥬😂",
    "Why did the actor break up with the script? It just wasn’t his type. 🎭",
    "What’s a film director’s favorite exercise? *Cut* and run! 🎥",
    "Why did the movie go to therapy? Too many *plot* twists!",
    "Why don’t horror movies ever win awards? People are too scared to vote! 👻",
    "What do you call an action movie with only vegetables? *Fast and the Fermentous*! 🥕🍅",
    "Why was the movie theater so cold? It was full of *chillers*! 🧊",
    "Why don’t scientists trust atoms? Because they make up everything! 😄",
    "Why did the movie break up with the book? Too many plot holes!",
    "Why was the math book sad? Too many problems!"
]

def handle_joke():
    return random.choice(jokes)

# greetings
greeting_responses = [
    "Hello! 👋 How can I help you today?",
    "Hi there! Need movie recommendations?",
    "Hey! What kind of movie are you in the mood for?",
    "Namaste! Looking for something to watch?",
    "Hi! You can ask me to suggest movies by year, actor, genre, or language.",
    "Hey! I’m your movie buddy. Ask me for a movie recommendation",
    "Hello! Want a movie by actor, genre, or language?",
    "Hi! I can suggest movies — go ahead and ask."
]

def handle_greeting():
    return random.choice(greeting_responses)

# farewells
farewell_responses = [
    "Goodbye! 👋 Have a great day!",
    "See you next time! 🎬",
    "Bye! Happy movie watching!",
    "Thanks for chatting. Come back anytime!",
    "Take care! 😊",
    "Talk to you later!",
    "Hope you find a great movie. Bye!",
    "Goodbye! Have a great day 😊",
    "See you soon. Don’t forget to come back for movie tips!",
    "Take care! I’ll be here if you need more recommendations."
]

def handle_farewell():
    return random.choice(farewell_responses)

# thanks
thanks_responses = [
    "You're welcome! 😊",
    "Glad I could help!",
    "Anytime!",
    "No problem at all.",
    "Happy to help — let me know if you need anything else!",
    "You're most welcome! 🎬",
    "It was my pleasure helping you.",
    "Glad you liked it!",
    "That’s what I’m here for! 🍿",
    "Always ready to recommend a good movie!",
    "Thanks for using the movie bot — come back anytime!",
    "Anytime! 😊",
    "You're very welcome!",
    "Happy to help. Want more movie suggestions?"
]

def handle_thanks_response():
    return random.choice(thanks_responses)

# identity response
identity_responses = [
    "I'm MovieBot 🍿 — your assistant to discover and recommend South Indian movies. Built by Naveen as part of a data science project!",
    "Hey there! I'm MovieBot, designed to help you find the right movie from a collection of 23,000+ South Indian films. 🎬",
    "I'm your smart movie assistant 🤖, trained to chat with you, recommend movies, and learn from your feedback — all created by Naveen!",
    "MovieBot at your service! Built using machine learning, NLP, and a lot of movie love. Ask me anything! 😊",
    "I’m a chatbot designed for movie lovers — helping you explore Telugu, Tamil, Kannada, and Malayalam films. Created by Naveen!",
    "I was built by Naveen as part of a South Indian Movie Recommender system! 😄",
    "I'm a South Indian movie chatbot that can recommend movies, tell you about directors, actors, genres, and more!",
    "I can help you find movies by title, actor, director, year, language, and genre.",
    "Yes, I'm an AI built to help you explore South Indian cinema!",
    "Just tell me what kind of movie you're in the mood for — I’ll do my best to find a great match.",
    "You can ask me to recommend movies, find films by actor or director, or even search by language and release year.",
    "I’m an AI-powered movie assistant here to help you find great films!",
    "I’m a bot created to make movie discovery fun and easy. Ask away!",
    "I was built by Naveen as part of a AI project — powered by machine learning and a lot of cinema love.",
]

def handle_bot_identity():
    return random.choice(identity_responses)

# fallback response
fallback_response = [
    "Sorry, I didn't understand that. Could you please rephrase?",
    "I'm still learning! Try asking about South Indian movies.",
    "Oops! That didn't make sense to me. Want help finding a movie?",
    "Can you try that again with different words?",
    "I'm not sure how to respond to that. I can help with movie recommendations or info!",
    "Sorry, I didn't catch that. Can you rephrase?",
    "I'm not sure how to help with that. Try asking about movies, actors, or genres!",
    "Oops! That one’s tricky. Maybe ask me about movies or recommendations?",
    "Hmm, I didn't quite get that. Want to ask me about an actor or movie?",
    "That's a bit unclear to me. Maybe try with a movie title?",
    "I might need a little more context. Are you asking about a movie, actor, or director?",
    "Sorry, I couldn't follow. You can ask me things like 'movies of Vijay' or 'top Telugu films'.",
    "That doesn't ring a bell. Want me to suggest a movie instead?",
    "I'm still learning! Could you try asking in a simpler way?",
    "Not sure what you meant there. Want to search by actor, director, or language?",
    "I didn't catch that one. Maybe ask me for recommendations?",
    "Sorry, I'm confused. Do you want movies by year, actor, or language?",
    "That's new to me! But I can definitely help you explore movies."
]

def handle_fallback_response():
    return random.choice(fallback_response)

# crisis_intent
crisis_responses = [
    "I'm really sorry you're feeling this way. You're not alone — there are people who care about you.",
    "Please reach out to someone you trust. You're valuable and deserve support.",
    "If you're in immediate danger, contact emergency services. You can also call a mental health helpline.",
    "In India, you can call iCall at 9152987821 or AASRA at 91-9820466726 — they offer 24/7 support.",
    "I'm really sorry you're feeling this way. You're not alone — please consider reaching out to a professional or someone you trust.",
    "If you’re in crisis or need urgent help, please call a helpline or talk to someone nearby. Your safety matters.",
    "It might help to speak to a real person. Please consider contacting a mental health professional or a local support service."
]

def handle_crisis():
    return random.choice(crisis_responses)

# small talk
small_talk = [
  "I'm just a bunch of code, but I'm doing great — thanks for asking!",
  "All circuits running smoothly 😄 What about you?",
  "Every day is a movie day for me!",
  "I love movies! I’ve read about thousands of them — South Indian ones are my favorite!",
  "I don't watch movies like you do, but I know a lot about them!",
  "Age is just a number... and I’m timeless 😉",
  "I don’t sleep, I stream data 24/7!",
  "I live in the cloud — literally ☁️🎬"
]

def handle_small_talk():
    return random.choice(small_talk)

#---------------------------------------------------------------------------------#
#-------------------------Basic Search Intents------------------------------------#
# search_by_language
context_lang = {
    "last_language": None,
    "last_results": [],
    "last_index": 0
}

def search_by_language(language,top_n=5):
    if language is None or language.strip() == "":
        return "Sorry, I couldn't understand the language you mentioned. Please try again."

    filtered = df[df['language'].str.lower() == language.lower()]
    
    if filtered.empty:
        return f"Sorry, I couldn't find any {language} movies in my database."
    
    movies = filtered.sort_values("year", ascending=False)
    movies = movies[['title', 'language', 'year']].to_dict(orient='records')
    # Prepare for next batch
    context_lang["last_language"] = language
    context_lang["last_results"] = movies[:45]
    context_lang["last_index"] = 0
    return search_by_more_language(top_n)

def search_by_more_language(top_n=5):
    results = context_lang.get("last_results", [])
    start = context_lang.get("last_index", 0)
    end = start + top_n

    if start >= len(results):
        language = context_lang.get("last_language", "this language")
        return f"No more movies of {language} to show."

    # Get next batch
    batch = results[start:end]
    context_lang["last_index"] = end  # update for next round

    movie_list = "\n".join([f"<li> {m['title']} ({m['language']}, {m['year']})</li>" for m in batch])
    language = context_lang.get("last_language", "this language")
    return f"Here are some {language} movies:<ul>{movie_list}</ul>"

# search_by_actor
context_actor = {
    "last_actor": None,
    "last_results": [],
    "last_index": 0
}

def search_by_actor(actor_name,top_n=5):
    if actor_name is None:
        return "Sorry, I couldn't understand the Actor you mentioned. Please try again."
    
    matches = df[df['clean_cast'].str.lower().str.contains(actor_name.lower(), na=False)]
    if matches.empty:
        return f"Sorry, I couldn't find any actor named {actor_name}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False)
    movies = matches[['title', 'language', 'year']].to_dict(orient='records')
    
    # Prepare for next batch
    context_actor['last_actor'] = actor_name
    context_actor['last_results'] = movies[:30]
    context_actor['last_index'] = 0 # set index to 0 for next batch
    return search_more_actor_results(top_n)

# search more actor results
def search_more_actor_results(top_n = 5):
    results = context_actor.get("last_results", [])
    start = context_actor.get("last_index", 0)
    end = start + top_n

    if start >= len(results):
        actor = context_actor.get("last_actor", "this actor")
        return f"No more movies of {actor} to show."

    # Get next batch
    batch = results[start:end]
    context_actor["last_index"] = end  # update for next round
    actor = context_actor.get("last_actor", "this actor")
    movie_list = "\n".join([f"<li> {m['title']} ({m['language']}, {m['year']})</li>" for m in batch])
    return f"Here are some movies featuring {actor}:<ul>{movie_list}</ul>"


# search_by_director
context_director = {
    "last_director": None,
    "last_results": [],
    "last_index": 0
}
def search_by_director(director_name,top_n=5):
    if director_name is None:
        return "Sorry, I couldn't understand the Director you mentioned. Please try again."
    
    matches = df[df['director'].str.lower().str.contains(director_name.lower(), na=False)]
    if matches.empty:
        return f"Sorry, I couldn't find any movies directed by {director_name}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False)
    movies = matches[['title', 'language', 'year']].to_dict(orient='records')
    
    # Prepare for next batch
    context_director['last_director'] = director_name
    context_director['last_results'] = movies[:30]
    context_director['last_index'] = 0 # set index to 0 for next batch
    return search_more_director_results(top_n)

def search_more_director_results(top_n = 5):
    results = context_director.get("last_results", [])
    start = context_director.get("last_index", 0)
    end = start + top_n

    if start >= len(results):
        director_name = context_director.get("last_director")
        return f"No more movies directed by {director_name} to show."

    # Get next batch
    batch = results[start:end]
    context_director["last_index"] = end  # update for next round

    movie_list = "\n".join([f"<li> {m['title']} ({m['language']}, {m['year']})</li>" for m in batch])
    director_name = context_director.get("last_director")
    return f"Here are some movies Directed by {director_name}:<ul>{movie_list}</ul>"

# search_by_year
context_year = {
    "last_year" : None,
    "last_results" : [],
    "last_index" : 0
}

def search_by_year(year,top_n=5):
    if year is None:
        return f"Sorry, I couldn't find movies of year {year}."
    matches = df[df['year']==year]
    if matches.empty:
        return f"Sorry, I couldn't find any movies in the year {year}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False)
    movies = matches[['title', 'language', 'year']].to_dict(orient='records')
    # Prepare for next batch
    context_year['last_year'] = year
    context_year['last_results'] = movies[:30]
    context_year['last_index'] = 0 # set index to 0 for next batch
    return search_more_by_year(top_n)

def search_more_by_year(top_n=5):
    results = context_year.get("last_results", [])
    start = context_year.get("last_index", 0)
    end = start + top_n

    if start >= len(results):
        year = context_year.get("last_year", "this year")
        return f"No more movies to show in {year}."

    # Get next batch
    batch = results[start:end]
    context_year["last_index"] = end  # update for next round

    movie_list = "\n".join([f"<li> {m['title']} ({m['language']}, {m['year']})</li>" for m in batch])
    year = context_year.get("last_year", "this year")
    return f"Here are some movies from year {year}:<ul>{movie_list}</ul>"

# search_by_decade

def search_by_decade(decade):
    if decade is None:
        return f"Sorry, I couldn't find movies of {decade}, please enter valid decade"
    matches = df[df['decade']==decade]
    if matches.empty:
        return f"Sorry, I couldn't find any movies in {decade}, please enter valid decade"
    matches = matches.sort_values(by='year', ascending=True).head(5)
    # Prepare response
    movie_list = "\n".join([f"<li>{row['title']} ({row['language']}) {row['decade']}</li>" for _, row in matches.iterrows()])
    return f"Here are some movies released in {decade}:<ul>{movie_list}</ul>"

#-------------------------------------------------------------------------------------------#
#---------------------------Hybrid intents--------------------------------------------------#

## search_by_language_year
def search_by_language_year(language, year):
    if language is None or year is None:
        return "Sorry, I couldn't understand the language, I can only help with South Indian Languages. Please try again."
        
    filtered = df[(df['language'].str.lower() == language.lower()) & (df['year'] == year)]
    
    if filtered.empty:
        return f"Sorry, I couldn't find any {language} movies from {year}."
    
    movie_list = "".join([f"<li>{row['title']} ({row['language']},{row['year']})</li>" for _, row in filtered.head(5).iterrows()])
    return f"Here are some {language} movies from {year}:<ul>{movie_list} </ul>"

# filter_recent_by_language
def filter_recent_by_language(language):
    if language is None:
        return "Sorry, I couldn't understand which language you're referring to. Please try again."

    recent = df[(df['language'].str.lower() == language.lower()) & (df['year'] >= 2024)].sort_values(by='year', ascending=False).head(5)
    if recent.empty:
        return f"Sorry, I couldn't find any recent {language} movie releases."

    movie_list = "\n".join([f"<li>{row['title']} ({row['year']})</li>" for _, row in recent.iterrows()])
    return f"Here are some of the latest {language} movie releases:<ul>{movie_list}</ul>"

# search_by_decade

# recommend_similar
# recommend - imported from movie_recommender.py

# search_by_actor_language
def search_by_actor_language(language,actor_name, top_n=5):
    if language is None or actor_name is None:
        return "Sorry, I couldn't understand, I can only help with South Indian Languages and Actors. Please try again."
    matches = df[(df['language'].str.lower() == language.lower()) & df['clean_cast'].str.lower().str.contains(actor_name.lower(), na=False)]
    if matches.empty:
        return f"Sorry, I couldn't find any match of {actor_name} and {language}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False).head(top_n)

    # Prepare response
    movie_list = "\n".join([f"<li> {row['title']} ({row['language']},{row['year']}),{actor_name}</li>" for _, row in matches.iterrows()])
    return f"Here are some movies featuring {actor_name} in {language}:<ul>{movie_list}</ul>"

# search_by_director_language
def search_by_director_language(language,director_name,top_n = 5):
    if language is None or director_name is None:
        return "Sorry, I couldn't understand, I can only help with South Indian Languages and Actors. Please try again."
    matches = df[(df['language'].str.lower() == language.lower()) & df['director'].str.lower().str.contains(director_name.lower(), na=False)]
    if matches.empty:
        return f"Sorry, I couldn't find any movies directed by {director_name} in {language}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False).head(top_n)

    # Prepare response
    movie_list = "\n".join([f"<li> {row['title']} ({row['language']},{row['year']}),{director_name}</li>" for _, row in matches.iterrows()])
    return f"Here are some movies directed by {director_name} in {language}:<ul>{movie_list}</ul>"

# search_by_actor_year
def search_by_actor_year(actor_name,year):
    if actor_name is None or year is None:
        return "Sorry, I couldn't understand the Actor and year you mentioned. Please try again."
    matches = df[df['clean_cast'].str.lower().str.contains(actor_name.lower(), na=False) & (df['year'] == year)]
    if matches.empty:
        return f"Sorry, I couldn't find any movies of {actor_name} in {year}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False)

    # Prepare response
    movie_list = "\n".join([f"<li> {row['title']} ({row['language']},{row['year']})</li>" for _, row in matches.iterrows()])
    return f"Here are some movies acted by {actor_name} in {year}:<ul>{movie_list}</ul>"

# search_by_actor_director
def search_by_actor_director(actor_name,director_name):
    if actor_name is None or director_name is None:
        return "Sorry, i couldn't understand the Actor and the Director you mentioned, Please try again."
    matches = df[df['clean_cast'].str.lower().str.contains(actor_name.lower(), na=False) & (df['director'].str.lower().str.contains(director_name.lower(), na=False))]
    if matches.empty:
        return f"Sorry, I couldn't find any movies of {actor_name} directed by {director_name}."
    # Sort by year, most recent first
    matches = matches.sort_values(by='year', ascending=False)

    # Prepare response
    movie_list = "\n".join([f"<li> {row['title']} ({row['language']},{row['year']})</li>" for _, row in matches.iterrows()])
    return f"Here are some movies of {actor_name} directed by {director_name}:<ul>{movie_list}</ul>"


# 
# # Count movies by actor
# def actor_movie_count(actor_name=None):
#     if actor_name:  
#         # Filter dataset for actor
#         matches = df[df['clean_cast'].str.lower().str.contains(actor_name.lower(), na=False)]
        
#         if matches.empty:
#             return f"Sorry, I couldn't find any movies for {actor_name}."
        
#         count = len(matches)
#         return f"{actor_name} has acted in ** {count} movies ** in my database."
    
#     else:
#         # Conversation memory case
#         last_actor = context_actor.get("last_actor")
#         if last_actor:
#             matches = context_actor.get("last_results", [])
#             if matches:
#                 count = len(matches)
#                 return f"{last_actor} has acted in ** {count} movies ** (based on recent results)."
#             else:
#                 return f"Sorry, I couldn’t fetch the movie count for {last_actor}."
#         else:
#             return "Sorry, I couldn't understand the actor you mentioned. Please try again."



#-------------------------------------------------------------------------------------------------#
#---------------------------TMDB API call--------------------------------------------------#
# movie details
def handle_movie_info(user_input):
    info = get_movie_info(user_input)
    if not info:
        return f"Sorry, I couldn't find '{user_input}' in TMDb."
    return (
        f"🎬 {info['title']} ({info['release_date']})\n"
        f"Genres: {', '.join(info['genres'])}\n"
        f"Runtime: {info['runtime']} mins\n"
        f"Overview: {info['overview']}"
    )

# Actor information
def handle_actor_info(user_input):
    info = get_person_info(user_input)
    if not info:
        return f"Sorry, I couldn't find any actor named '{user_input}'. Can you rephrase or check the spelling?"
    # Validate the fields
    name = info.get("name") or user_input
    birthday = info.get("birthday")
    place_of_birth = info.get("place_of_birth")
    bio = info.get("biography")

    # Case 1: No details at all
    if not birthday and not place_of_birth and not bio:
        return f"I found {name}, but I don’t have more information about them. Could you try rephrasing (e.g., full name)?"
        
    # Case 2: Some info missing - still reply nicely
    response = f"👤 {name}\n"
    if birthday or place_of_birth:
        response += f"Born: {birthday or 'Unknown'} in {place_of_birth or 'Unknown'}\n\n"
    if bio:
        response += bio[:500] + "..."
    return response.strip()

#--------------------------------------------------------------------------------------
# Final chatbot reply function
def generate_bot_reply(user_message):
    predicted_intent = predict_intent(user_message)
    entities = extract_entities(user_message)

    # Safe entity extraction
    actor_name = extract_actor(user_message) or entities.get("actor")
    director_name = entities.get("director")
    lang = entities.get("language")
    year = entities.get("year")
    title = entities.get("title")
    decade = entities.get("decade")

    # ----------- INTENT HANDLERS ------------
    if predicted_intent == "recommend_similar":
        if title:
            return recommend_similar(title)
        return "Sorry, I couldn’t understand which movie you want similar recommendations for."

    elif predicted_intent == "search_by_actor":
        if actor_name:
            return search_by_actor(actor_name)
        return search_more_actor_results(top_n=5)  # conversation memory

    elif predicted_intent == "search_by_actor_language":
        if actor_name and lang:
            return search_by_actor_language(lang, actor_name)
        return "Please provide both actor name and language."

    elif predicted_intent == "search_by_actor_year":
        if actor_name and year:
            return search_by_actor_year(actor_name, year)
        return "Please provide both actor name and year."

    elif predicted_intent == "search_by_director":
        if director_name:
            return search_by_director(director_name)
        return search_more_director_results(top_n=5)  # conversation memory

    elif predicted_intent == "movie_info":
        if title:
            return handle_movie_info(title)
        return "Sorry, I couldn’t understand the movie title. Can you rephrase?"

    elif predicted_intent == "person_info":
        if actor_name:
            return handle_actor_info(actor_name)
        elif director_name:
            return handle_actor_info(director_name)
        return "Sorry, I couldn’t understand which person you meant. Try giving full actor/director name."

    elif predicted_intent == "actor_movie_count":
        if actor_name:
            return actor_movie_count(actor_name)
        return "Sorry, I couldn’t understand which actor you meant. Please provide a name."

    elif predicted_intent == "search_by_actor_director":
        if actor_name and director_name:
            return search_by_actor_director(actor_name, director_name)
        return "Please provide both actor and director name."

    elif predicted_intent == "search_by_director_language":
        if director_name and lang:
            return search_by_director_language(lang, director_name)
        return "Please provide both director and language."

    elif predicted_intent == "search_by_year":
        if year:
            return search_by_year(year)
        return search_more_by_year(top_n=5)  # conversation memory

    elif predicted_intent == "search_by_decade":
        if decade:
            return search_by_decade(decade)
        return "Please provide a valid decade (e.g., 1990s, 2000s)."

    elif predicted_intent == "search_by_language":
        if lang:
            return search_by_language(lang)
        return search_by_more_language(top_n=5)  # conversation memory

    elif predicted_intent == "search_by_language_year":
        if lang and year:
            return search_by_language_year(lang, year)
        return "Please provide both language and year."

    elif predicted_intent == "filter_recent_by_language":
        if lang:
            return filter_recent_by_language(lang)
        return "Please provide a valid South Indian language."

    elif predicted_intent == "filter_recent_movies":
        current_year = datetime.datetime.now().year
        recent = df[df['year'] >= current_year - 1].sort_values(by='year', ascending=False).head(5)
        if recent.empty:
            return "Sorry, I couldn’t find any recent movie releases."
        movie_list = "\n".join([f"<li>{row['title']} ({row['year']})</li>" for _, row in recent.iterrows()])
        return f"Here are some of the latest South Indian movie releases:\n<ul>{movie_list}</ul>"

    # ----------- Small talk & fallback ------------
    elif predicted_intent == "bot_identity":
        return handle_bot_identity()
    elif predicted_intent == "fallback":
        return handle_fallback_response()
    elif predicted_intent == "crisis_intent":
        return handle_crisis()
    elif predicted_intent == "small_talk":
        return handle_small_talk()
    elif predicted_intent == "greeting":
        return handle_greeting()
    elif predicted_intent == "farewell":
        return handle_farewell()
    elif predicted_intent == "tell_joke":
        return handle_joke()
    elif predicted_intent == "thanks":
        return handle_thanks_response()

    elif predicted_intent == "positive_feedback":
        return random.choice([
            "So glad you liked it! 😊 Let us know if you'd like more recommendations.",
            "Glad I could help! 😊",
            "You're welcome! Let me know if you need anything else.",
            "Happy to assist — ask me anything anytime!"
        ])

    elif predicted_intent == "negative_feedback":
        return random.choice([
            "I'm sorry it didn’t work as expected. Could you tell me what went wrong so we can improve?",
            "Sorry about that. Let me try a better answer.",
            "Thanks for the feedback — I'll try to improve.",
            "Hmm, let me give you another suggestion."
        ])

    elif predicted_intent == "neutral_feedback":
        return random.choice([
            "Thank you for your feedback! It helps us improve.",
            "Thanks for your feedback. I’ll keep trying to get better!",
            "Noted! Feel free to ask anything else.",
            "Appreciate the input. I’m learning every day!"
        ])

    elif predicted_intent == "unknown_intent":
        return "I'm not sure how to help with that. Try asking about movies, actors, or directors!"

    else:
        return "Sorry, I can’t help with that topic. I’m here to assist you with South Indian movies, actors, directors, and related information."
