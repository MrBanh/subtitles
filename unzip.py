# unzip.py - Looks for the specified zip file. If it exists, unzips and sends the zip folder to trash.

import os, zipfile, send2trash

def unzip(directory, filename):
    filePath = os.path.join(directory, filename)
    while True:
        if os.path.isfile(filePath):
            # Extracts the zipped file
            os.chdir(directory)
            zippedFile = zipfile.ZipFile(os.path.relpath(filePath), 'r')
            zippedFile.extractall()
            zippedFile.close()
            break

    # Send the zipped file to trash
    send2trash.send2trash(filePath)