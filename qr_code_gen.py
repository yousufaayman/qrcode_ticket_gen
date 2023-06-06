import os
from datetime import date
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask

# Function to create folder to store QR codes
def createFolder():
    today = date.today()
    folder_name = f'QRCODES{today}'
    os.mkdir(folder_name)
    return folder_name

#Function to create QR codes
def createQRCodes(data, innerImagePath, folder):
    for i in range(len(data)):
    
        qr = qrcode.QRCode(version = 1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size = 20, border = 2)
        qr.add_data(data[i])
        qr.make(fit = True)

        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path = innerImagePath,
                        color_mask= SolidFillColorMask(back_color=(255, 255, 255), front_color=(239, 69, 35)))
        
        img.save(f"{folder}/QR{i}.png")

