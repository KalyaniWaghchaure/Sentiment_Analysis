# Sentiment Analysis API with LLM Integration

## Overview
This project implements a sentiment analysis API using Flask that processes customer reviews from XLSX or CSV files. The API integrates with the Groq API to analyze sentiment and returns structured JSON results.

## Features
- Accepts both XLSX and CSV files containing customer reviews.
- Performs sentiment analysis using Groq API.
- Returns sentiment scores in a structured JSON format.

## Requirements
- Python 3.7 or higher
- The following Python packages (install via `pip install -r requirements.txt`):
  - Flask
  - pandas
  - openpyxl
  - requests
  - python-dotenv
  - groq

