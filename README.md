# qrcode_ticket_gen

Python script to create single use qr codes. The script uses selenium and the "singleuse.link" website to create QR codes which expire after being scanned.

# Requirments :: Python 3, Selenium, Selenium Driver for browser of choice, python qr-code library, python qr-code-styles library, python pyperclip library

# How to use::
1- Open the driver_code.py file
2-Adjust the "getLinks.getOneTimeLink" function as you please, in this format : "getLinks.getOneTimeLink(linksArr, "number of qr codes you want input as an int")
# Note :: If you wish to add an image to your QR code, add image path to the imagePath variable
