# YouTube Influencer Discovery & Analysis Tool

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![YouTube API](https://img.shields.io/badge/YouTube_API-v3-red)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-API-green)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-orange)

A Python automation tool to identify niche-specific YouTube influencers using advanced content and engagement filters. Designed for agencies, marketers, and content managers.


## 🚀 Features
- **Keyword-Driven Search**: Scrape 500+ channels using custom queries (e.g., "tech, AI, coding").
- **Multi-Layer Filtering**:
  - **Subscriber Threshold**: Keep channels with 50K–100K subs.
  - **View Consistency**: Analyze last 10 videos for sustained views (>40K/video).
  - **Content Genre Match**: Validate alignment with search keywords via descriptions/video titles.
  - **Upload Schedule**: Filter channels uploading ≥1x/month.
- **Automated Reporting**: Export results to Google Sheets with metrics like avg. views, subs, and content descriptions.


## 🛠️ Tech Stack
- **Python 3.9+**: Core scripting and data processing.
- **YouTube Data API v3**: Channel/video metadata extraction.
- **Google Sheets API**: Automated report generation.
- **Pandas**: Data filtering and analysis.
