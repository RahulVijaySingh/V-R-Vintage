
import pandas as pd
import praw
import re
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# === Keyword Categories ===
KEYWORD_CATEGORIES = {
    "Location_Preference": ["sea-facing", "seafacing", "sea facing", "near school", "nearschool", "near college", "nearcollege", "close to college", "close to school"],
    "Property_Type": ["plot", "land plot", "apartment", "flat", "home", "house", "villa", "bungalow", "2bhk", "3bhk", "two bhk", "three bhk", "2 bedroom", "3 bedroom"],
    "Price_Sensitivity": ["budget", "low budget", "affordable", "lakhs", "crores"],
    "Noise_Preference": ["quiet area", "quiet-area", "noise free", "low noise", "lownoise", "peaceful", "calm area", "quiet"],
    "Other_Likes_Dislikes": ["gated community", "secure society", "compound", "furnished", "semi furnished", "fully furnished", "bed", "bedroom"]
}

# === Simple Sentiment Analysis ===
def simple_sentiment(text):
    positives = ["interested", "looking for", "want", "love", "like", "prefer", "must", "wish", "plan"]
    negatives = ["don't want", "hate", "dislike", "avoid", "noisy", "problem", "issue", "against", "bad", "expensive"]

    text = text.lower()
    pos_hits = any(word in text for word in positives)
    neg_hits = any(word in text for word in negatives)

    if pos_hits and not neg_hits:
        return "Positive"
    elif neg_hits and not pos_hits:
        return "Negative"
    elif pos_hits and neg_hits:
        return "Mixed"
    else:
        return "Neutral"

# === Reddit Setup ===
# Reddit setup using env variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# === Search Reddit Function ===
def search_reddit_and_extract(name, email, phone):
    search_queries = [name, email, phone]
    matched_entries = []

    for query in search_queries:
        for submission in reddit.subreddit("all").search(query, limit=5):
            text = submission.title + " " + submission.selftext
            date = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d')
            matched_entries.append((text, date))
        for comment in reddit.subreddit("all").comments(limit=100):
            if query.lower() in comment.body.lower():
                text = comment.body
                date = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d')
                matched_entries.append((text, date))

    return matched_entries

# === Extract Preferences + Sentiment ===
def extract_preferences(matched_entries):
    found_tokens = set()
    actual_lines = []
    latest_date = None
    sentiments = []

    for text, date in matched_entries:
        lower_text = text.lower()
        found_any = False

        for category, keywords in KEYWORD_CATEGORIES.items():
            for word in keywords:
                if re.search(rf"\b{re.escape(word)}\b", lower_text):
                    found_tokens.add(word)
                    found_any = True

        if found_any:
            actual_lines.append(text.strip())
            sentiment = simple_sentiment(text)
            sentiments.append(sentiment)
            if latest_date is None or date > latest_date:
                latest_date = date

    overall_sentiment = sentiments[0] if sentiments else "Neutral"
    return list(found_tokens), actual_lines, overall_sentiment, latest_date or "NA"

# === Main Function ===
# def main():
#     df = pd.read_excel("Contact_dataset.xlsx").head(2)

#     keyword_tokens_col = []
#     # actual_lines_col = []
#     sentiment_col = []
#     post_dates_col = []

#     for idx, row in df.iterrows():
#         print(f"🔍 Extracting for {row['Name']}...")
#         matched_entries = search_reddit_and_extract(row["Name"], row["Email"], str(row["Phone"]))
#         tokens, lines, sentiment, last_date = extract_preferences(matched_entries)

#         keyword_tokens_col.append(", ".join(tokens) if tokens else "Not Found")
#         # actual_lines_col.append("\n---\n".join(lines) if lines else "NA")
#         sentiment_col.append(sentiment)
#         post_dates_col.append(last_date)

#     df["Keywords_Found"] = keyword_tokens_col
#     # df["Actual_Lines"] = actual_lines_col
#     df["Sentiment"] = sentiment_col
#     df["Post_Date"] = post_dates_col

#     df.to_excel("output_flat_keywords_with_sentiment.xlsx", index=False)
#     print("✅ Done! Output saved to 'output_flat_keywords_with_sentiment.xlsx'.")
# === Main Function ===
# === Main Function ===
def main():
    df = pd.read_excel("Contact_dataset.xlsx").head(400)

    filtered_rows = []

    for idx, row in df.iterrows():
        print(f"🔍 Extracting for {row['Name']}...")
        matched_entries = search_reddit_and_extract(row["Name"], row["Email"], str(row["Phone"]))
        tokens, lines, sentiment, last_date = extract_preferences(matched_entries)

        if tokens:  # Only keep rows where keywords were matched
            updated_row = row.to_dict()  # Keep all original columns
            updated_row["Keywords_Found"] = ", ".join(tokens)
            updated_row["Sentiment"] = sentiment
            updated_row["Post_Date"] = last_date
            filtered_rows.append(updated_row)

    if filtered_rows:
        output_df = pd.DataFrame(filtered_rows)
        output_df.to_excel("output_flat_keywords_with_sentiment.xlsx", index=False)
        print("✅ Done! Output saved to 'output_flat_keywords_with_sentiment.xlsx'.")
    else:
        print("⚠️ No relevant posts found for any contacts.")


if __name__ == "__main__":
    main()


