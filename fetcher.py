import requests
import logging
from supabase import create_client, Client
import os
from datetime import datetime
from tenacity import retry, wait_exponential, stop_after_attempt


class APIClientFactory:
    @staticmethod
    def get_client(api_name):
        if api_name == "reddit":
            return RedditFetcher
        # Future API clients can be added here
        raise ValueError(f"Unknown API client: {api_name}")
        
class RedditFetcher:
    def __init__(self, subreddits=None):
        self.subreddits = subreddits
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Supabase client initialized.")

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
    def fetch_subreddit(self, subreddit):
        response = requests.get(f'https://www.reddit.com/r/{subreddit}.json', headers={'User-agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.json()

    def fetch_and_store(self):
        for subreddit in self.subreddits:
            try:
                data = self.fetch_subreddit(subreddit)
                for post in data['data']['children']:
                    self.store_post(subreddit, post['data']['title'], post['data']['author'])
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data for {subreddit}: {e}")

    def store_post(self, subreddit, title, author):
        existing_posts = self.supabase.table("posts").select("*").eq("title", title).eq("author", author).execute()
        if existing_posts.data:
            logging.info(f"Post already exists: {title} by {author}. Skipping insertion.")
            return

        data = {
            "subreddit": subreddit,
            "title": title,
            "author": author,
            "url": f'https://www.reddit.com/r/{subreddit}',
            "date": datetime.now().isoformat()
        }
        response = self.supabase.table("posts").insert(data).execute()
        logging.info(f"Response: {response}")
        if response.data:
            logging.info(f"Inserted post: {title} by {author} into the database.")
        else:
            logging.error(f"Failed to insert post: {title} by {author}. Error: {response.data}")


if __name__ == "__main__":
    api_client = APIClientFactory.get_client("reddit")
    client_instance = api_client([]) 
    client_instance.fetch_and_store()


