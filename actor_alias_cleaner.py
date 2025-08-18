import pandas as pd
import json
from rapidfuzz import fuzz, process
from collections import defaultdict

# Get all unique names
def get_unique_names(df, col):
    names = set()
    for val in df[col]:
        if isinstance(val, list):
            names.update(val)
        elif isinstance(val, str):
            names.update([a.strip() for a in val.split(",")])
    return sorted(names)

# Build alias map (no manual approval)
def build_alias_map(names, threshold=93):
    alias_map = {}
    visited = set()
    
    for name in names:
        if name in visited:
            continue
        matches = process.extract(name, names, scorer=fuzz.token_set_ratio, limit=None)
        cluster = {m for m, score, _ in matches if score >= threshold}
        visited.update(cluster)
        
        # Pick canonical (longest name in cluster)
        canonical = max(cluster, key=len)
        for alias in cluster:
            alias_map[alias] = canonical
    return alias_map

# Apply alias mapping to dataframe
def apply_alias_mapping(df, col, alias_map):
    def replace_names(val):
        if isinstance(val, list):
            return [alias_map.get(name, name) for name in val]
        elif isinstance(val, str):
            return [alias_map.get(a.strip(), a.strip()) for a in val.split(",")]
        return val
    df[col] = df[col].apply(replace_names)
    return df

if __name__ == "__main__":
    # Load your dataset
    df = pd.read_csv("movies.csv")
    
    # Optional: Convert stringified lists to real lists
    import ast
    try:
        df['clean_cast'] = df['clean_cast'].apply(ast.literal_eval)
    except:
        pass
    
    # Get all unique names (actor & director)
    actors = get_unique_names(df, "clean_cast")
    directors = get_unique_names(df, "clean_director")

    print(f"Actors: {len(actors)}, Directors: {len(directors)}")

    # Build alias maps
    actor_alias_map = build_alias_map(actors, threshold=93)
    director_alias_map = build_alias_map(directors, threshold=93)

    # Save alias maps
    with open("actor_aliases.json", "w", encoding="utf-8") as f:
        json.dump(actor_alias_map, f, ensure_ascii=False, indent=2)
    with open("director_aliases.json", "w", encoding="utf-8") as f:
        json.dump(director_alias_map, f, ensure_ascii=False, indent=2)

    print("✅ Alias mapping saved!")

    # Apply mapping to dataframe
    df = apply_alias_mapping(df, "clean_cast", actor_alias_map)
    df = apply_alias_mapping(df, "clean_director", director_alias_map)

    # Save updated dataset
    df.to_csv("movies_clean.csv", index=False)
    print("✅ Clean dataset saved!")

# import pandas as pd
# # Load movie dataset
# df = pd.read_csv("South_Indian_movies.csv")
# # preprocess the actors list
# known_actors = df['clean_cast'].dropna().unique()
# # Split, strip, and flatten the list
# flat_actor_list = []
# for line in known_actors:
#     # skip unknown
#     if line.lower().strip() == "unknown":
#         continue
#     for name in line.split(","):
#         clean_name = name.strip().strip("'").replace(".", "")
#         if clean_name:
#             flat_actor_list.append(clean_name)
# def split_concatenated_names(text):
#     return re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', text)

# actor_names = [name for text in flat_actor_list for name in split_concatenated_names(text)]

# # remove the name tokens which are more than 3
# actor_names = [name for name in actor_names if len(name.split()) <= 3 ]

# actor_names = list(dict.fromkeys(actor_names))

# actor_names = [str(name).strip() for name in actor_names if str(name).strip()]

# def normalize_name(name):
#     name = name.lower()
#     name = re.sub(r"[^a-z0-9\s]", "", name)
#     name = re.sub(r"\s+", " ", name)
#     return name.strip()

# alias_map = {}
# visited = set()

# for name in actor_names:
#     if name in visited:
#         continue

#     matches = process.extract(name, actor_names, scorer=fuzz.token_sort_ratio, limit=None)
#     similar_names = [match for match, score, _ in matches if score >= FUZZY_THRESHOLD]

#     canonical = max(similar_names, key=lambda x: len(str(x)))

#     for alias in similar_names:
#         alias_map[alias] = canonical
#         visited.add(alias)

# alias_df = pd.DataFrame(list(alias_map.items()), columns=["alias", "canonical"])
# #alias_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

# alias_df = alias_df.sort_values(by="canonical", ascending=True)
# alias_df.reset_index(drop=True, inplace=True)

# alias_df.to_csv("actor_alias.csv", index=False, encoding="utf-8")
