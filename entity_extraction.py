import re
import pandas as pd
# Define your metadata lists here
LANGUAGES = ['Telugu', 'Tamil', 'Kannada', 'Malayalam']
# Sample actor and director lists
df = pd.read_csv("South_Indian_Movies_cleaned.csv")
alias_df = pd.read_csv("alias_map.csv")

#--------------ACTOR & alias maping for actors----------------------------

alias_df['alias'] = alias_df['alias'].str.lower()
alias_df['canonical'] = alias_df['canonical'].str.lower()

alias_df = alias_df.drop_duplicates()

alias_df = alias_df.reset_index(drop=True) 
alias_map = dict(zip(alias_df['alias'], alias_df['canonical']))

canonical_names = alias_df['canonical'].tolist()

#--------------------------Director---------------------------------

known_directors = df['director'].dropna().unique().tolist()
# removing brackets
def clean_director_name(name):
    return re.sub(r'\s*\(.*?\)', '', name).strip()

# Apply to the full list
cleaned_directors_list = [clean_director_name(name) for name in known_directors if isinstance(name, str)]

def extract_director_name(text):
    # This regex looks for known role keywords and removes them and what comes after
    pattern = r'(.*?)\s*(?:Story|Screenplay|Dialogues|Lyrics)\s*:?.*'
    match = re.match(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()  # If no match, return original

cleaned_directors = [extract_director_name(d) for d in cleaned_directors_list if isinstance(d, str)]
# remove the name tokens which are more than 3
cleaned_directors = [name for name in cleaned_directors if len(name.split()) <= 3 ]
# arrange names in the descending order
cleaned_directors = sorted(cleaned_directors, key=lambda x: len(x), reverse=True)
cleaned_directors = list(set(cleaned_directors))

# movie titles
known_movies = df['title'].dropna().unique().tolist()
# 1. Extract year from user input
def extract_year(text):
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return int(match.group()) if match else None

# 2. Extract decade (like '1990s', '2000s', etc.)
def extract_decade(text):
    match = re.search(r'\b(19|20)\d0s\b', text)
    if match:
        return match.group()
    match_alt = re.search(r"\b(\d{2})['’]?s\b", text)
    if match_alt:
        return '19' + match_alt.group(1) + 's'
    return None

# 3. Extract language
def extract_language(text):
    for lang in LANGUAGES:
        if lang.lower() in text.lower():
            return lang
    return None
# 4. Extract actor from known list
# def extract_actor(text, known_actors):
#     for actor in known_actors:
#         if isinstance(actor, str) and actor.lower() in text.lower():
#             return actor
#     return None

# Extract actor using fuzzy search for better entity extraction of actor
# 4. Extract actor
from rapidfuzz import fuzz

def extract_actor_fuzzy(text, actor_names, threshold=90):
    best_match = None
    highest_score = 0

    for actor in actor_names:
        if not isinstance(actor, str) or not actor.strip():
            continue
        # if len(actor) < min_name_length:  # skip short names like "Ve"
        #     continue
        score = fuzz.token_set_ratio(actor.lower(), text.lower())
        if score > highest_score:
            best_match = actor
            highest_score = score
    return best_match if highest_score >= threshold else None

def extract_actor(text, alias_map=alias_map,canonical_names=canonical_names):
    text_lower = text.lower()
    actor_names = sorted(canonical_names, key=lambda x: len(x), reverse=True)

    # First try exact matching
    # sort aliases by length (longest first)
    for alias, canonical in sorted(alias_map.items(), key=lambda x: len(x[0]), reverse=True):
        if alias.lower() in text_lower:
            return canonical
        
    for actor in actor_names:
        if isinstance(actor, str) and actor.strip():
            if actor.lower() in text_lower:
                return actor
                
    #Then try fuzzy match
    return extract_actor_fuzzy(text, actor_names, threshold=90)

#
# from rapidfuzz import fuzz, process
# import phonetics

# def extract_actor(user_input, canonical_names=canonical_names, alias_map=alias_map):
#     user_input = user_input.lower()
#     canonical_names = sorted(canonical_names, key=lambda x: len(x), reverse=True)
#     # Stage 1: Alias dictionary check
#     if user_input in alias_map:
#         return {"stage": "alias", "matched_name": alias_map[user_input], "suggestions": []}

#     # Stage 2: Exact match (case-insensitive)
#     for name in canonical_names:
#         if user_input.lower() == name.lower():
#             return {"stage": "exact", "matched_name": name, "suggestions": []}

#     # Stage 3: Fuzzy match > 90
#     best_match, score, _ = process.extractOne(user_input, canonical_names, scorer=fuzz.token_sort_ratio)
#     if score >= 90:
#         return {"stage": "fuzzy strong", "matched_name": best_match, "suggestions": []}

#     # Stage 3b: Phonetic match (Soundex/Metaphone)
#     user_phonetic = phonetics.metaphone(user_input)
#     phonetic_matches = [
#         name for name in canonical_names
#         if phonetics.metaphone(name) == user_phonetic
#     ]
#     if phonetic_matches:
#         return {"stage": "Phonetic", "matched_name": phonetic_matches[0], "suggestions": []}

#     # Stage 4: Suggest top 3 if score between 75–90
#     if score >= 75:
#         suggestions = [m[0] for m in process.extract(user_input, canonical_names, limit=3, scorer=fuzz.token_sort_ratio)]
#         return {"stage": "suggest", "matched_name": None, "suggestions": suggestions}

#     # Stage 5: Ask user to rephrase (< 75 score)
#     return {"stage": "lowfuzzy", "matched_name": None, "suggestions": []}


# 5. Extract director from known list
# def extract_director(text, known_directors):
#     for director in known_directors:
#         if isinstance(director, str) and director.lower() in text.lower():
#             return director
#     return None

# Extract director using fuzzy
from rapidfuzz import fuzz, process
def extract_director_fuzzy(query, directors_list, threshold=80):
    # Only keep strings and remove nulls
    candidates = [d for d in directors_list if isinstance(d, str)]
    
    # Use process.extractOne for best match
    match = process.extractOne(query, candidates, scorer=fuzz.token_set_ratio)
    
    if match and match[1] >= threshold:
        return match[0]  # Best matched director name
    else:
        return None  # No good match found

def extract_director(text, cleaned_directors):
    text_lower = text.lower()
    cleaned_directors = sorted(cleaned_directors, key=lambda x: len(x), reverse=True)

    # First try exact matching
    for director in cleaned_directors:
        if isinstance(director, str) and director.strip():
            if director.lower() in text_lower:
                return director
                
    # Then try fuzzy match
    return extract_director_fuzzy(text, cleaned_directors, threshold=80)

# 6. Extract movie title from known list

# def extract_title(text,known_movies):
#     for movie in known_movies:
#         if isinstance(movie, str) and movie.lower() in text.lower():
#             return movie
#     return None

def extract_title_fuzzy(query, known_movies, threshold=80):
    # Only keep strings and remove nulls
    candidates = [m for m in known_movies if isinstance(m, str)]
    
    # Use process.extractOne for best match
    match = process.extractOne(query, candidates, scorer=fuzz.token_set_ratio)

    if match and match[1] >= threshold:
        return match[0]  # Best matched title name
    else:
        return None  # No good match found

def extract_title(text, known_movies):
    text_lower = text.lower()
    known_movies = sorted(known_movies, key=lambda x: len(x), reverse=True)

    # First try exact matching
    for movie in known_movies:
        if isinstance(movie, str) and movie.strip():
            if movie.lower() in text_lower:
                return movie
                
    # Then try fuzzy match
    return extract_title_fuzzy(text, known_movies, threshold=80)

# 7. Combine all into one extractor
def extract_entities(text, known_directors=cleaned_directors):
    return {
        "year": extract_year(text),
        "decade": extract_decade(text),
        "language": extract_language(text),
        #"actor": extract_actor(text, known_actors),
        "actor": extract_actor(text),
        #"director": extract_director(text, known_directors),
        "director": extract_director(text,known_directors),
        #"title": extract_title(text,known_movies)
        "title": extract_title(text,known_movies)
    }