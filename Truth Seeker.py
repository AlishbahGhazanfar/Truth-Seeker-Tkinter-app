#!/usr/bin/env python
# coding: utf-8

# ## <h1><center><font color='Blue'><b>Truth Seeker<font></a>
# ### <section><center><font color='gray'>(Online Fact Checking Companion)</a>
# ### <h2><center><font color='orange'>News Sources<font></a>

# ### 1.Creating Database

# In[ ]:


import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('fact_checking.db')
c = conn.cursor()

# Create the 'ratings' table with the full schema if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_source TEXT,
    headline TEXT,
    time TEXT,
    current_time TEXT,
    reliability_rating INTEGER
)
''')

# # Optionally, check if the 'headline' and 'time' columns need to be added (if updating an old schema)
# # This part is necessary only if transitioning from an old schema that didn't include these columns
# c.execute("PRAGMA table_info(ratings)")
# columns = [row[1] for row in c.fetchall()]

# if 'headline' not in columns:
#     c.execute('ALTER TABLE ratings ADD COLUMN headline TEXT')

# if 'time' not in columns:
#     c.execute('ALTER TABLE ratings ADD COLUMN time TEXT')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()


# ### 2.Extracting Data from News sources and Creating GUI Interface

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label
import sqlite3
import webbrowser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class FactCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fact Checker')
        self.geometry('800x600')

        left_frame = ttk.Frame(self, width=600)
        right_frame = ttk.Frame(self, width=200)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame.pack(side="right", fill="both", expand=False)

        photoimage = PhotoImage(file="C:/Users/Hp/Downloads/chromedriver_win32/Logo (1).png")
        label = Label(right_frame, image=photoimage)
        label.image = photoimage
        label.pack()

        ttk.Label(left_frame, text="Select News Source:").pack(pady=10)
        self.news_source_var = tk.StringVar()
        self.news_sources = {
            'ABC News': ('https://www.abc.net.au/news/justin', '//div/div/div/div[1]/div/div[*]/div/div/div[1]/h3/span/a', '//div/div[*]/div/div/div[1]/div/span/div/time[1]', '//div/div/div/div[1]/div/div[*]/div/div/div[1]/h3/span/a'),
            '9 News': ('https://www.9news.com.au/just-in', '//div/div[1]/article[*]/div/div/h3/a/span', '//div/div[1]/article[*]/div/div/span/time', '//div/div[1]/article[*]/div/div/h3/a'),
            'NBC News': ('https://www.nbcnews.com/', '//section/div/div[2]/div[1]/ul/li[*]/div/h2/a', '//section/div/div[2]/div[1]/ul/li[*]/div/div', '//section/div/div[2]/div[1]/ul/li[*]/div/h2/a')
        }
        news_source_dropdown = ttk.Combobox(left_frame, textvariable=self.news_source_var, values=list(self.news_sources.keys()))
        news_source_dropdown.pack()

        ttk.Button(left_frame, text="Fetch News", command=self.fetch_news).pack(pady=10)
        self.news_display = tk.Text(left_frame, width=70, height=20)
        self.news_display.pack(pady=10)

        ttk.Label(left_frame, text="Rate Reliability:").pack(pady=5)
        scale_frame = ttk.Frame(left_frame)
        scale_frame.pack()
        self.rating_scale = ttk.Scale(scale_frame, from_=0, to=5, orient='horizontal', length=300)
        self.rating_scale.pack()

        label_positions = [(300 / 5) * i for i in range(6)]
        for i, pos in enumerate(label_positions):
            label = ttk.Label(scale_frame, text=str(i))
            label.place(x=pos - 10, y=30)

        ttk.Button(left_frame, text="Save Rating", command=self.save_rating).pack(pady=20)

    def configure_chrome_options(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        return options

    def fetch_news(self):
        options = self.configure_chrome_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        try:
            source = self.news_sources[self.news_source_var.get()]
            url, headline_xpath, time_xpath, details_xpath = source
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, headline_xpath)))
            headlines = driver.find_elements(By.XPATH, headline_xpath)
            times = driver.find_elements(By.XPATH, time_xpath)
            details = driver.find_elements(By.XPATH, details_xpath)
            self.news_display.delete('1.0', tk.END)
            for headline, time, detail in zip(headlines, times, details):
                details_url = detail.get_attribute('href')
                display_text = f"News Source: {url}\nHeadline: {headline.text}\nTime: {time.text}\nURL: {details_url}\n" + '-'*80 + '\n'
                self.news_display.insert(tk.END, display_text)
                button = tk.Button(self.news_display, text="Click Details", command=lambda url=details_url: self.open_url(url))
                self.news_display.window_create(tk.END, window=button)
                self.news_display.insert(tk.END, '\n\n')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to fetch news: {str(e)}')
        finally:
            driver.quit()

    def open_url(self, url):
        webbrowser.open(url)

    def save_rating(self):
        try:
            selected_text = self.news_display.get("sel.first", "sel.last-1c")
            if not selected_text.strip():
                messagebox.showerror('Error', 'Selected text is empty.')
                return
            selected_lines = selected_text.splitlines()
            if len(selected_lines) < 4:
                messagebox.showerror('Error', 'Incomplete selection. Please ensure the full news entry is selected.')
                return
            url = selected_lines[0].split(': ')[1]
            headline = selected_lines[1].split(': ')[1]
            time = selected_lines[2].split(': ')[1]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('fact_checking.db')
            c = conn.cursor()
            c.execute('INSERT INTO ratings (news_source, headline, time, current_time, reliability_rating) VALUES (?, ?, ?, ?, ?)',
                      (url, headline, time, current_time, int(self.rating_scale.get())))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Rating saved successfully!')
        except tk.TclError:
            messagebox.showerror('Error', 'No text selected. Please select a news item before saving.')

if __name__ == '__main__':
    app = FactCheckerApp()
    app.mainloop()


# #### Library Imports and Class Definition:
# 
# The code begins by importing necessary libraries such as tkinter for the GUI, sqlite3 for database operations, selenium for web scraping, and others for handling images and dates.
# FactCheckerApp is a class derived from tk.Tk, indicating it is a Tkinter application.
# 
# #### Initialization and GUI Layout:
# 
# The constructor (__init__) sets up the application window (title, size) and divides it into left and right frames using ttk.Frame.
# A PhotoImage widget is used to display a logo in the right frame.
# The left frame includes a dropdown for selecting news sources, a button to fetch news, a text widget for displaying news, and a rating scale to rate news reliability.
# 
# #### Dynamic News Source Handling:
# 
# The news_sources dictionary stores URLs and XPaths for different news sources, which are used in the fetch_news method to scrape data.
# News is fetched based on the selected source from the dropdown, utilizing Selenium to navigate web pages and scrape data such as headlines and publication times.
# 
# #### News Display and Interaction:
# 
# The fetch_news method dynamically inserts news headlines, times, and URLs into the news_display text widget. It also embeds a button in the text widget for each news item that opens the news detail page when clicked.
# The method uses web scraping to obtain and display news, showing the practical integration of web scraping in a GUI application.
# 
# #### Database Integration and Error Handling:
# 
# The save_rating method handles saving the user's reliability rating of a news article into a SQLite database. It includes error handling to ensure that the selection is not empty and is properly formatted.
# This method demonstrates how the application interacts with a local database, including inserting data and handling common user errors.

# In[ ]:




