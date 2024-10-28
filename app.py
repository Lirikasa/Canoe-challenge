import os
from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
from fetcher import RedditFetcher

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)


@app.route('/clear', methods=['POST'])
def clear_data():
    supabase.table("posts").delete().neq("id", 0).execute()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'subreddits' not in session:
        default_subreddits = [] # You could add a list of default subreddits
        session['subreddits'] = default_subreddits
    if request.method == 'POST':
        subreddits = request.form.get('subreddits')
        if subreddits:
            subreddit_list = subreddits.split(',')
            session['subreddits'].extend(subreddit_list)
            fetcher = RedditFetcher(session['subreddits'])
            fetcher.fetch_and_store()
            return redirect(url_for('index'))

    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter')
    if filter_type and filter_value:
        response = supabase.table("posts").select("*").eq(filter_type, filter_value).execute()
    else:
        response = supabase.table("posts").select("*").execute()
    posts = response.data
    return render_template('index.html', posts=posts, subreddits=session['subreddits'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
