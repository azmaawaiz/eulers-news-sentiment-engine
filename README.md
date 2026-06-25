# Euler's News Sentiment Engine

A real-time financial market intelligence system designed to monitor breaking news, classify affected assets, and generate sentiment-driven trading insights.

## Overview

The engine continuously monitors financial headlines using the Finnhub API and performs real-time sentiment analysis using VADER NLP.

For every incoming headline the system:

* Calculates sentiment
* Identifies affected instruments
* Detects macroeconomic events
* Maps news to relevant asset classes
* Generates trading bias information

## Features

### News Monitoring

* Historical news retrieval
* Real-time news monitoring
* Breaking news alerts

### Sentiment Analysis

* Bullish classification
* Bearish classification
* Neutral classification

### Asset Classification

#### Forex

* EURUSD
* GBPUSD
* USDJPY
* AUDUSD
* NZDUSD
* USDCAD

#### Commodities

* XAUUSD (Gold)
* XAGUSD (Silver)

#### Safe Haven Assets

* USDCHF
* USDJPY
* Gold

### Event Detection

* Federal Reserve announcements
* ECB announcements
* BOE announcements
* BOJ announcements
* Geopolitical events
* Commodity-related developments

## Technologies

* Python
* Asyncio
* Aiohttp
* NLTK VADER
* Finnhub API

## Example Output

SOURCE: LIVE BREAKING NEWS

SENTIMENT: BULLISH

AFFECTED PAIRS:
EURUSD, GBPUSD, XAUUSD

HEADLINE:
Federal Reserve signals potential rate cuts later this year




Developed by Euler's Quantitative Traders (EQT).

