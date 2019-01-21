# findSubtitles.py - Search https://www.yify-subtitles.com/ and download the
# highest rated subtitle

from selenium import webdriver
import os
from unzip import unzip


def find_subs(movie, language_filter='English'):

    # Obtain user's desktop directory and set it as the directory where the
    # file will be downloaded to
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop\\')
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': desktop}
    options.add_experimental_option('prefs', prefs)

    # Starts the chrome browser
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(f'https://www.yify-subtitles.com/search?q={movie}')

    # Gather all search results that match the movie searched for
    search_results = browser.find_elements_by_css_selector('.media-list \
                                                .media.media-movie-clickable')

    if len(search_results) == 0:
        # Did not find subtitles for movie
        print(f'No results for "{movie}"')
        browser.quit()  # close the browser

    elif len(search_results) == 1:
        # Only 1 result for movie searched. Open the link
        search_results[0].click()

    else:
        # Multiple results for movie searched. List out each result for user
        # to select from
        print(f'Results found for "{movie}" keyword:')
        for i in range(len(search_results)):
            movie_name = search_results[i].find_element_by_css_selector(
                    'h3[itemprop="name"]').text
            movie_year = search_results[i].find_element_by_css_selector(
                    '.movinfo-section').text[0:4]
            print(f'\t{str(i + 1) + ".":<3} {movie_name} ({movie_year})')
        print()

        while True:
            try:
                # Have user choose the movie from search results
                movie_chosen = int(input(f'Please choose a movie'
                                         f' (1 - {len(search_results)}): '))

                # Validate user input: must be integer, and within range of
                # movies listed
                if movie_chosen < 1 or movie_chosen > len(search_results) \
                        or isinstance(movie_chosen, float):
                    raise Exception

                break   # Exits loop
            except (ValueError, Exception):
                print('Invalid input.', end=' ')

        # Click on the selected movie link
        search_results[movie_chosen - 1].click()

    # Select all available subtitles
    filtered_subs = {}
    all_subs_elem = browser.find_elements_by_css_selector(
            '.other-subs tbody tr')

    # Loop through each subtitle and determine if the language matches the
    # specified language. If so, obtain the subtitle id,
    # rating, and download link element
    for subElem in all_subs_elem:
        # Language of each subtitle
        lang = subElem.find_element_by_css_selector('.sub-lang').text
        if lang == language_filter:

            # data-id of each subtitle
            sub_id = subElem.get_attribute('data-id')

            # rating of subtitle
            rating = int(subElem.find_element_by_css_selector(
                    '.rating-cell').text)

            # subtitle's download page link
            to_dl_page = subElem.find_element_by_css_selector(
                    'a').get_attribute('href')

            # Stores subtitles in a dictionary
            filtered_subs[sub_id] = {
                'language': lang,
                'rating': rating,
                'downloadPage': to_dl_page
                }

    # Give user an error if subtitles for the language is not available
    if not filtered_subs:
        print(f'\n{language_filter} subtitles not available. Try again...\n')
        browser.quit()
        exit()

    # Determine the highest rated subtitle
    highest_rated = None
    for sub_id in filtered_subs.keys():
        if highest_rated is None:
            highest_rated = sub_id
        else:
            if filtered_subs[sub_id]['rating'] > \
                    filtered_subs[highest_rated]['rating']:
                highest_rated = sub_id

    # Open the highest rated link
    browser.get(filtered_subs[highest_rated]['downloadPage'])

    # Download the subtitle file
    click_to_download = browser.find_element_by_partial_link_text(
            'DOWNLOAD SUBTITLE')    # select the <a> element to download

    # Obtain name of zip file based on download link
    filename = os.path.basename(click_to_download.get_attribute('href'))

    print('Downloading subtitles...')
    click_to_download.click()

    # Unzip the file
    import time
    time.sleep(1)
    print('Unzipping zipped file...')
    unzip(desktop, filename)

    # Close the browser
    print('Done!')
    browser.quit()
    exit()
