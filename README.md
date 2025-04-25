# V-R-Vintage

# Reddit Real Estate Keyword & Sentiment Extractor

This project analyzes Reddit posts and comments to identify user preferences for real estate (e.g., sea-facing, gated community, 2BHK) and extracts sentiment (positive, negative, neutral) based on custom keyword matching. The extracted insights are stored in an Excel file for further analysis.

## 🔧 How it Works

- Searches Reddit using `praw` for each contact's **name**, **email**, and **phone number**.
- Extracts relevant keywords from posts/comments using custom-defined keyword categories.
- Performs a basic sentiment analysis using rule-based logic.
- Saves filtered contacts and metadata (keywords, sentiment, post date) to an output Excel file.

## 📄 Files

- `app.py`: The main script for keyword & sentiment extraction.
- `graph.py`: Use this script to generate visualizations from the output Excel.

## 📥 Requirements

- You must provide a dataset file named `Contact_dataset.xlsx` (this file is **private**, so it's **not included** in the repository).
- Make sure to set up the **ChromeDriver** and place it in the same directory if you plan to scrape data with Selenium or require browser automation.

## ✅ How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up Reddit API credentials in a `.env` file:

   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   ```

3. Place your `Contact_dataset.xlsx` in the project root directory.

4. Run the extraction:

   ```bash
   python app.py
   ```

5. To generate graphs/visualizations from the output:
   ```bash
   python graph.py
   ```

## 📦 Output

The script will generate:

- `output_flat_keywords_with_sentiment.xlsx`: Filtered contact data with matched keywords, sentiment, and latest Reddit post date.

---

> ⚠️ Note: Since the dataset is private and Reddit data is dynamic, results may vary depending on what content is currently available.
