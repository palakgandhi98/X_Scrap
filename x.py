import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Path to the CSV file
csv_file_path = r'C:\Users\Strimmerz\Downloads\scrap\X_Scrapper\twitter_links - twitter_links.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Check if the 'url' column exists
if 'link' not in df.columns:
    raise KeyError("The column 'url' does not exist in the CSV file.")

# Extract the URLs from the 'url' column and store them in a list
target_urls = df['link'].tolist()

# Initialize the list to store profile data
profile_list = []

# Initialize the WebDriver
driver = webdriver.Firefox()

for target_url in target_urls:
    # Initialize the dictionary to store profile data
    profile_data = {}

    # Open the target URL
    driver.get(target_url)
    time.sleep(2)

    # Get the page source
    resp = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(resp, 'html.parser')

    # Extract profile information
    try:
        profile_data["Profile_Name"] = soup.find("div", {"class": "r-1vr29t4"}).text
    except Exception as e:
        profile_data["Profile_Name"] = None
        print(f"Error extracting Profile_Name: {e}")

    try:
        profile_data["Profile_Handle"] = soup.find("div", {"class": "r-1wvb978"}).text
    except Exception as e:
        profile_data["Profile_Handle"] = None
        print(f"Error extracting Profile_Handle: {e}")

    try:
        profile_data["Bio"] = soup.find("div", {"data-testid": "UserDescription"}).text
    except Exception as e:
        profile_data["Bio"] = None
        print(f"Error extracting Bio: {e}")

    try:
        profile_data["Location"] = soup.find("span", {"data-testid": "UserLocation"}).text
    except Exception as e:
        profile_data["Location"] = None
        print(f"Error extracting Location: {e}")

    profile_header = soup.find("div", {"data-testid": "UserProfileHeader_Items"})

    try:
        profile_data["Website"] = profile_header.find('a').get('href')
    except Exception as e:
        profile_data["Website"] = None
        print(f"Error extracting Website: {e}")

    try:
        profile_data["Following_Count"] = soup.find_all("a", {"class": "r-rjixqe"})[0].text
    except Exception as e:
        profile_data["Following_Count"] = None
        print(f"Error extracting Following_Count: {e}")

    try:
        profile_data["Followers_Count"] = soup.find_all("a", {"class": "r-rjixqe"})[1].text
    except Exception as e:
        profile_data["Followers_Count"] = None
        print(f"Error extracting Followers_Count: {e}")

    # Append the profile data to the list
    profile_list.append(profile_data)

# Close the WebDriver
driver.quit()

# Convert the list of dictionaries to a Pandas DataFrame
df_profiles = pd.DataFrame(profile_list)

# Specify the output directory and create it if it doesn't exist
output_dir = r'C:\Users\Strimmerz\Downloads\scrap\X_Scrapper'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the DataFrame to a CSV file
df_profiles.to_csv(os.path.join(output_dir, 'twitter_profile_data.csv'), index=False)

print(df_profiles)
