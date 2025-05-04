FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Copy the token file (ensure this file is present in the same directory as the Dockerfile)
COPY token.txt .

# Copy the Twitch usernames file
COPY twitch_usernames.json .

# Command to run the bot
CMD ["python", "src/main.py"]