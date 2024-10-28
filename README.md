# Canoe Intelligence Challenge 

This project utilizes Supabase as the database. For that reason, I created a simple web app to help you fetch and visualize the data. 
I have provided the credentials via email.
## How to use

1. **Build the Docker image:**

   ```bash
   docker build -t reddit-fetcher .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 80:80 -e SUPABASE_URL=email_supabase_url -e SUPABASE_KEY=email_supabase_key reddit-fetcher
   ```

   Replace `email_supabase_url` and `email_supabase_key` with the credentials provided in the email.

3. **Access the web interface:**

   Open a web browser and go to `http://localhost:80` to view the fetched Reddit posts.


## License

Agustin Basile
