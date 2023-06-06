import qr_code_gen as QR
import selenium_script as getLinks

linksArr = []
imagePath = "" #Add Logo path for QR code Central Image
qrFolder = QR.createFolder()

getLinks.getOneTimeLink(linksArr, 2)

QR.createQRCodes(linksArr, imagePath, qrFolder)
