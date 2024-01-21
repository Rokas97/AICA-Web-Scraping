# AICA-Web-Scraping

This program scrapes gaming from [MMO ir MMORPG Vaizdo Žaidimai - Žema kaina! - ENEBA.url](..%2F..%2F..%2F..%2FAppData%2FLocal%2FTemp%2FMMO%20ir%20MMORPG%20Vaizdo%20%8Eaidimai%20-%20%8Eema%20kaina%21%20-%20ENEBA.url) 
website and saves the data in .csv file.


To launch this code, you need to:
* Install Python and the selenium package on your computer.
* Have the chromedriver.exe file in the same folder as your code, or change the path accordingly.
* How to launch main.py code in pycharm you can find it here: [git - Import Github repository to PyCharm - Stack Overflow.url](..%2F..%2F..%2F..%2FAppData%2FLocal%2FTemp%2Fgit%20-%20Import%20Github%20repository%20to%20PyCharm%20-%20Stack%20Overflow.url)
* PyCharm should automatically detect requirements.txt file and suggest to install it.
* The run the main.py.
* This will create an instance of the EnebaScraper class and call its start method, which will launch a Chrome browser and scrape the games from the Eneba website.
* The scraped data will be stored in the class attributes.
* The data will also be saved as a csv file named eneba_games.csv in the same folder as your code.
* You can also access the logs\error.log file to see the logging error messages.