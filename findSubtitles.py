# findSubtitles.py - Search https://www.yify-subtitles.com/ and download the highest rated subtitle

from selenium import webdriver
import os
from unzip import unzip

def findSubtitles(movie, languageFilter='English'):

    # Obtain user's desktop directory and set it as the directory where the file will be downloaded to
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop\\')
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': desktop}
    options.add_experimental_option('prefs', prefs)

    # Starts the chrome browser
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(f'https://www.yify-subtitles.com/search?q={movie}')

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
    filteredSubs = {}
    allSubsElem = browser.find_elements_by_css_selector('.other-subs tbody tr')

    # Loop through each subtitle and determine if the language matches the specified language
    # If so, obtain the subtitle id, rating, and download link element
    for subElem in allSubsElem:
        lang = subElem.find_element_by_css_selector('.sub-lang').text   # Language of each subtitle
        if lang == languageFilter:
            subId = subElem.get_attribute('data-id')   # data-id of each subtitle
            rating = int(subElem.find_element_by_css_selector('.rating-cell').text) # rating of subtitle
            toDownloadPage = subElem.find_element_by_css_selector('a').get_attribute('href')  # subtitle's download page link

            # Stores subtitles in a dictionary
            filteredSubs[subId] = {
                'language': lang,
                'rating': rating,
                'downloadPage': toDownloadPage
                }

    # Give user an error if subtitles for the language is not available
    if not filteredSubs:
        print(f'\n{languageFilter} subtitles not available. Try again...\n')
        browser.quit()
        exit()

    # Determine the highest rated subtitle
    highestRated = None
    for subId in filteredSubs.keys():
        if highestRated == None:
            highestRated = subId
        else:
            if filteredSubs[subId]['rating'] > filteredSubs[highestRated]['rating']:
                highestRated = subId

    # Open the highest rated link
    browser.get(filteredSubs[highestRated]['downloadPage'])

    # Download the subtitle file
    clickToDownload = browser.find_element_by_partial_link_text('DOWNLOAD SUBTITLE')    # select the <a> element to download subtitle
    filename = os.path.basename(clickToDownload.get_attribute('href'))  # Obtain name of zip file based on download link
    clickToDownload.click()

    # Unzip the file
    import time
    time.sleep(1)
    unzip(desktop, filename)

    # Close the browser
    browser.quit()
    exit()