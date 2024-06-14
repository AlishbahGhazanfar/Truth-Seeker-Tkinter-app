# Truth-Seeker-Tkinter-app
# Truth Seeker

## Overview
**Truth Seeker** is an online fact-checking companion that helps you verify the reliability of news articles from various sources. The application features a graphical user interface (GUI) for easy interaction, powered by `tkinter`, and uses `selenium` for web scraping to fetch news articles. It stores user ratings on the reliability of news items in an SQLite database.

![image](https://github.com/AlishbahGhazanfar/Truth-Seeker-Tkinter-app/assets/171797920/803d3977-ce63-4721-b5aa-4ea4746e7582)


## Features
- Fetch news headlines from multiple sources.
- Display news headlines with publication times.
- Rate the reliability of news articles.
- Save ratings to a local SQLite database.
- Clickable links to read full news articles in a web browser.

## Installation

### Prerequisites
- Python 3.x
- SQLite
- Google Chrome browser

### Required Python Packages
Install the required Python packages using pip:
```sh
pip install tkinter selenium webdriver-manager
```

### Database Setup
No special setup is required for the SQLite database. The database will be created automatically when you run the application.

## Usage

### Clone the Repository
Clone this repository to your local machine:
```sh
git clone https://github.com/yourusername/truth-seeker.git
cd truth-seeker
```

### Running the Application
Execute the following command to run the application:
```sh
python Truth\ Seeker.py
```

### User Interface
- **Select News Source**: Choose a news source from the dropdown menu.
- **Fetch News**: Click the "Fetch News" button to retrieve news headlines.
- **News Display**: News headlines will be displayed in the text widget. Click "Read More" to open the full article in a web browser.
- **Rate Reliability**: Use the scale to rate the reliability of a selected news item.
- **Save Rating**: Click the "Save Rating" button to save your rating to the database.

## Screenshots
### Main Interface
![image](https://github.com/AlishbahGhazanfar/Truth-Seeker-Tkinter-app/assets/171797920/a96c872e-43e1-4591-8199-03158aaea228)


### Fetching News
1. Select any news source
2. Click Fetch Results
3. It will display the Source Name, Headline, Time and URL
4. Then you can rate it by selecting that specific source.
5. Ratings will save in database.
6. Click Details will show the full document.
   
![image](https://github.com/AlishbahGhazanfar/Truth-Seeker-Tkinter-app/assets/171797920/af33dbce-2f22-48fe-ba52-acbb33f3875b)


## Database Schema
The SQLite database `fact_checking.db` contains a table `ratings` with the following schema:
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `news_source`: TEXT
- `headline`: TEXT
- `time`: TEXT
- `current_time`: TEXT
- `reliability_rating`: INTEGER

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.
