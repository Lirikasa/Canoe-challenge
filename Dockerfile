# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN python3 -m pip install --no-cache-dir requests supabase tenacity flask

# Make port 80 available to the world outside this container
EXPOSE 80

# Run reddit_fetcher.py when the container launches
CMD ["python3", "app.py"]
