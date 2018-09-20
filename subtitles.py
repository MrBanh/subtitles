#! python3

# subtitles.py - Search https://www.yify-subtitles.com/ and download the highest rated
#               english subtitle

from selenium import webdriver

movie = "Deadpool"
browser = webdriver.Chrome()
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
    print(f'\Results found for "{movie}" keyword:')
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

# TODO: Click on the English subtitle link with the highest rating
# TODO: Download the subtitle file
# TODO: Implement the ability to search for movie subtitles via command prompt
# TODO: Unzip the file (different python script)
# TODO: Send the zip file to trash (different python script)