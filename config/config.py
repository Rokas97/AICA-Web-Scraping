# Import the configparser module
import configparser
# Create a ConfigParser object
config = configparser.ConfigParser()

# Add a section for the database settings
config.add_section("DATABASE")
# Add options to the section
config.set("DATABASE", "host", "localhost")
config.set("DATABASE", "port", "3306")
config.set("DATABASE", "username", "root")
config.set("DATABASE", "password", "Test123$")
config.set("DATABASE", "database_name", "test")
config.set("DATABASE", "pool_size", "10")

# Add a section for the web driver settings
config.add_section("WEBDRIVER")
# Add options to the section
config.set("WEBDRIVER", 'driver_path', "Drivers/chromedriver.exe")
config.set("WEBDRIVER", "url", "https://www.eneba.com/lt/store/mmo-games")
config.set("WEBDRIVER", "min_price", "0.5")
config.set("WEBDRIVER", "wait_time", "15")

# Add a section for the logging settings
config.add_section("LOGGING")
# Add options to the section
config.set("LOGGING", "filename", "config.log")
config.set("LOGGING", "level", "INFO")
# config.set("LOGGING", "format", '''%(asctime)s :: %(levelname)s : %(name)s : %(message)s : line: %(lineno)d''')

# Write the config file to a path
with open("config.ini", "w") as configfile:
    config.write(configfile)

