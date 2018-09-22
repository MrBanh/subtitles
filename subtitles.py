#! python3

# subtitles.py - Search https://www.yify-subtitles.com/ and download the highest rated
#               english subtitle

from selenium import webdriver
import os

movie = "Deadpool 2"
languageFilter = "English"

# Obtain user desktop as the directory to download files to
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
options = webdriver.ChromeOptions()
prefs = {'download.default_directory': desktop}
options.add_experimental_option('prefs', prefs)

# Starts the chrome browser
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://www.yify-subtitles.com/')
searchBar = browser.find_element_by_id('qSearch')   # Select the search bar
searchBar.send_keys(movie)  # type to the search bar
searchBar.submit()  # start the search

# Gather all search results that match the movie that the user searched for
movieLinks = browser.find_elements_by_css_selector('a div h3[itemprop="name"]')

if len(movieLinks) == 0:
    # Did not find subtitles for movie
    print(f'No results for "{movie}"')
    browser.quit()  # close the browser

elif len(movieLinks) == 1:
    # Only 1 result for movie searched. Open the link
    movieLinks[0].click()

else:
    # Multiple results for movie searched. List out each result for user to select from
    print(f'Results found for "{movie}" keyword:')
    for i in range(len(movieLinks)):
        print(f'\t{str(i + 1) + ".":<3}', movieLinks[i].text)
    print()

    while True:
        try:
            # Have user choose the movie from search results
            movieChosen = int(input(f'Please choose a movie (1 - {len(movieLinks)}): '))

            # Validate user input: must be integer, and within range of movies listed
            if movieChosen < 1 or movieChosen > len(movieLinks) or isinstance(movieChosen, float):
                raise Exception

            break   # Exits loop
        except (ValueError, Exception):
            print('Invalid input.', end=' ')

    # Click on the selected movie link
    movieLinks[movieChosen - 1].click()

# Select all available subtitles
allSubs = {}
availableLanguages = [] # Used to validate language filter
allSubsElem = browser.find_elements_by_css_selector('.other-subs tbody tr')

# Loop through each subtitle and obtain: subtitle id, language, rating, and download link element
for subElem in allSubsElem:
    subId = subElem.get_attribute('data-id')   # data-id of each subtitle
    lang = subElem.find_element_by_css_selector('.sub-lang').text   # Language of each subtitle
    rating = int(subElem.find_element_by_css_selector('.rating-cell').text) # rating of subtitle
    downloadLink = subElem.find_element_by_css_selector('a').get_attribute('href')  # download link element

    # Stores all subtitles in a dictionary
    allSubs[subId] = {
        'language': lang,
        'rating': rating,
        'link': downloadLink
        }

    # Appends language to availableLanguages list if not yet present
    if lang not in availableLanguages:
        availableLanguages.append(lang)

# Validate language filter
if languageFilter not in availableLanguages:
    print(f'\n{languageFilter} subtitles not available. Try again...\n')
    browser.quit()
    exit()

# Determine the highest rated subtitle
highestRated = None
for subId in allSubs.keys():
    if allSubs[subId]['language'] == languageFilter:
        if highestRated == None:
            highestRated = subId
        else:
            if allSubs[subId]['rating'] > allSubs[highestRated]['rating']:
                highestRated = subId

# Open the highest rated link
browser.get(allSubs[highestRated]['link'])

# Download the subtitle file
clickToDownload = browser.find_element_by_link_text('DOWNLOAD SUBTITLE')
clickToDownload.click()

# TODO: Implement the ability to search for movie subtitles via command prompt
# TODO: Unzip the file (different python script)
# TODO: Send the zip file to trash (different python script)