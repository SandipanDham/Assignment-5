import tkinter as tk
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt

# Function to generate response using Hugging Face API
def generate_response(input_text):
    api_url = "https://api-inference.huggingface.co/models/gpt-3.5-turbo"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace YOUR_API_KEY with your actual API key

    payload = {
        "inputs": input_text,
        "parameters": {
            "max_new_tokens": 150,
            "return_full": False
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["generated_text"]
    else:
        return "Error: Failed to generate response"

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to update the sentiment analysis report
def update_report(sentiment):
    if sentiment == "Positive":
        report["Positive"] += 1
    elif sentiment == "Negative":
        report["Negative"] += 1
    else:
        report["Neutral"] += 1

# Function to update data visualizations
def update_visualizations():
    plt.clf()
    plt.pie([report["Positive"], report["Negative"], report["Neutral"]], labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%")
    plt.title("Sentiment Analysis Report")
    plt.savefig("sentiment_analysis_report.png")

# Create main window
window = tk.Tk()
window.title("GPT-3 Conversation")

# Text input field
entry = tk.Entry(window, width=50)
entry.pack(padx=10, pady=10)

# Submit button
def process_input():
    user_input = entry.get()
    conversation_display.insert(tk.END, f"You: {user_input}\n")

    response = generate_response(user_input)
    conversation_display.insert(tk.END, f"Bot: {response}\n\n")

    sentiment = analyze_sentiment(response)
    conversation_display.insert(tk.END, f"Sentiment: {sentiment}\n\n")
    update_report(sentiment)
    update_visualizations()

    entry.delete(0, tk.END)  # Clear input field

submit_button = tk.Button(window, text="Submit", command=process_input)
submit_button.pack(pady=5)

# Conversation display area
conversation_display = tk.Text(window, width=60, height=20)
conversation_display.pack(padx=10, pady=10)

# Initialize sentiment analysis report
report = {"Positive": 20, "Negative": 8, "Neutral": 5}

# Run the main loop
window.mainloop()
