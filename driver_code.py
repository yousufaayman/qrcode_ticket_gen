#Essential
import os
import time
#Selenium
import pyperclip 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#QR Libraries
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from matplotlib import colors
#Performance
import threading
from multiprocessing import cpu_count, Process


#Function to create folder to store QR codes
def createFolder():
    today = str(time.ctime(time.time()))
    today = today.replace(":",".")
    folder_name = f'QRCODES {today}'
    os.mkdir(folder_name)
    return folder_name

#Generating Links for QR Codes 
def retriveLink(links_arr, link_password, expirey_date, confirmation_email, custom_message, amount_of_links):
      
    print("Generating Links for QR Codes, please wait...")       
    
    
    
    cTime = time.ctime(time.time())
    
    driverOpts = Options()
    
    driverOpts.headless = False
    
    driver = webdriver.Chrome(options= driverOpts)
        
    driver.get("https://singleuse.link/")
    
    for iterations in range(amount_of_links):
        
        if iterations >= 1 :
            driver.back()
            driver.refresh()
        else:
            pass
        
        # Secret Message Box
        try:
            if custom_message == "":
                driver.find_element("id", "data").send_keys(cTime)
            else:
                driver.find_element("id", "data").send_keys(custom_message)
        except:
            pass
        
        # Link Pass
        try:
            if link_password == "": 
                pass
            else:
                driver.find_element("id", "inputPassword").send_keys(link_password)
        except:
            pass  
        
        #Email Alert
        try:
            if confirmation_email == "":
                pass
            else:    
                driver.find_element("id", 'inputEmail').send_keys(confirmation_email)
        except:
            pass
        
        #Drop down for link expirey
        grade_dropdown = Select(driver.find_element("id", "select"))
        grade_dropdown.select_by_visible_text(expirey_date)
        
        #Radio Button selection
        driver.find_element("id", 'optionsRadios1').click()
        
        #Create Button click
        driver.find_element("id", "createbtn2").click()
        
        #Copy to CLipboard
        driver.find_element(By.XPATH, "/html/body/div[2]/button").click();
        
        link = pyperclip.paste()
        
        links_arr.append(link)
        
        print(iterations + 1)
        
    driver.close()


#Function to create QR codes
def createQRCodes(data, innerImagePath, folder, foreground_color, background_color):
    
    if len(set(data)) != len(data):
        raise Exception("There was an issue ")
         
    
    foreground = list(colors.to_rgb(foreground_color))
    background = list(colors.to_rgb(background_color))

    for i in range(len(foreground)):
        foreground[i] = int(foreground[i] * 255)    
    for i in range(len(background)):
        background[i] = int(background[i] * 255)

    foreground = tuple(foreground)
    background = tuple(background)
    
    
    print("Generating QR Codes, please wait...")
    
    for i in range(len(data)):
    
        qr = qrcode.QRCode(version = 1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size = 20, border = 2)
        qr.add_data(data[i])
        qr.make(fit = True)

        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path = innerImagePath,
                        color_mask= SolidFillColorMask(back_color= background, front_color = foreground))
        
        img.save(f"{folder}/QR{i}.png")

def getOneTimeLink(functionToCall, argList, numOfLinks):
    
    numCorrection = lambda threads : numOfLinks % threads
    
    threads = []
    
    if numOfLinks <= 10:
        argTuple = tuple(argList.append(numOfLinks))
        th1 = threading.Thread(target = functionToCall, args=(argTuple))
        
        threads.append(th1)
        
    elif numOfLinks <= 50:
        numOfLinksPerThread = (numOfLinks - numCorrection(2)) / 2
        argTuple = tuple(argList.append(numOfLinksPerThread))
        argTupleMod = tuple(argList.append(numOfLinksPerThread + numCorrection(2)))
        
        th1 = threading.Thread(target = functionToCall, args=(argTuple))
        th2 = threading.Thread(target = functionToCall, args=(argTupleMod))
        
        threads.extend([th1, th2])
        
    elif numOfLinks <= 150:
        
        numOfLinksPerThread = (numOfLinks - numCorrection(3)) / 2
        argTuple = tuple(argList.append(numOfLinksPerThread))
        argTupleMod = tuple(argList.append(numOfLinksPerThread + numCorrection(3)))
        
        th1 = threading.Thread(target = functionToCall, args=(argTuple))
        th2 = threading.Thread(target = functionToCall, args=(argTuple))
        th3 = threading.Thread(target = functionToCall, args=(argTupleMod))
        
        threads.extend([th1, th2, th3])
        
    else:
        numOfLinksPerThread = (numOfLinks - numCorrection(2)) / 2
        argTuple = tuple(argList.append(numOfLinksPerThread))
        argTupleMod = tuple(argList.append(numOfLinksPerThread + numCorrection(4)))
        
        th1 = threading.Thread(target = functionToCall, args=(argTuple))
        th2 = threading.Thread(target = functionToCall, args=(argTuple))
        th3 = threading.Thread(target = functionToCall, args=(argTuple))
        th4 = threading.Thread(target = functionToCall, args=(argTupleMod))
        
        threads.extend([th1, th2, th3, th4])
            
    for i in threads:
        i.start()
        
def main() :
    try:
        linksArr = []

#Welcome Text
        print("Welcome to the QR Ticket Generator ::")
        print("How it works :: \n #You will be asked to add your customization options \n #The program then will run to create your QR codes \n #Codes will be stored in a folder with today's date in the same directory as the script folder")
        print("******************************************************************************************")

#Adding an Image
        imagePath = input("If you would like to add a logo to the center of your QR Code please input it here (must be png) (if not leave it blank) :: ")
        if imagePath == "":
            imagePath = "defaultLogo.png"
        else:
            if os.path.exists(imagePath):        
                ext = list(os.path.splitext(imagePath))
                ext = ext[-1].lower()
                if ext != '.png':
                    print(f"*X* File{imagePath} is not a png \n *X*defaulting to stock logo \n")
                    imagePath = "defaultLogo.png"
                else:
                    pass
            else: 
                print(f"*X* File{imagePath} does not exist \n *X*defaulting to stock logo")
                imagePath = "defaultLogo.png"

        print("******************************************************************************************")

#Numbers of Qr Codes
        while True:
            try:
                numOfLinks = int(input("Please enter the number of links you would like to generate :: "))
            except:
                print("Please enter a whole number (no decimals, and no characters!) \n Please Try Again :(")
            else: 
                break
        
        print("******************************************************************************************")
        
#Adding a Password
        linkPassword = input("If you would like to add a password to expire your qr codes, add it here (If not leave it blank) :: ")
        
        print("******************************************************************************************")
        
#Selecting a Expirey Date
        expireyDate = {1 : "12 hours", 2 : "1 day", 3 : "2 weeks", 4 : "1 month"}
        
        while True:
            try:
                optExpireyDate = int(input("Select an expirey date \n (1 = 12 Hours) (2 = 1 Day) (3 = 2 Weeks) (4 = 1 Month) (5 = 3 Months) :: "))
            except:
                print("Please select one of these options (1 = 12 Hours) (2 = 1 Day) (3 = 2 Weeks) (4 = 1 Month) (5 = 3 Months)  \n Please Try Again :( :: ")
            else: 
                break
            
        if expireyDate.get(optExpireyDate) == None :
           expireyDate = "3 month"
        else:
            expireyDate = expireyDate.get(optExpireyDate)

        print("******************************************************************************************")
        
#Adding a Confirmation Email
        confirmationEmail = input("If you would like to be sent a confirmation email once a qr code is expired input it here (if not leave it blank) :: ")
        
        print("******************************************************************************************")
        
#Adding a custom message
        
        customMessage = input("If you would like to add a custom message to be displayed once a code is expired input it here (If not leave it blank; default is today's date) :: ")

        print("******************************************************************************************")

        colors =['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']

#Add Foreground Color
        while True:
            foregroundColor = str(input("If you would like to add a custom color to your QR code foreground input it here (If not leave it blank; default is black) \n Colors(blue, green, red, cyan, magenta, yellow, black, white) \n or enter a custom color with a hex value (#000000):: "))
            if foregroundColor == "":
                foregroundColor = "black"
                break
            elif foregroundColor.lower() in colors or (foregroundColor[0] == "#" and foregroundColor.length() == 7):
                break
            else:
                print(f"You entered {foregroundColor} which is invalid! \n Please select one of the available colors \n or make sure of your hex syntax ex.(#000000) ::")

        print("******************************************************************************************")
        
#Add Background Color        
        while True:
            backgroundColor = str(input("If you would like to add a custom color to your QR code background input it here (If not leave it blank; default is black) \n Colors(blue, green, red, cyan, magenta, yellow, black, white) \n or enter a custom color with a hex value (#000000):: "))
            if backgroundColor == "":
                backgroundColor = "white"
                break
            elif backgroundColor.lower() in colors or (backgroundColor[0] == "#" and backgroundColor.length() == 7):
                break
            else:
                print(f"You entered {backgroundColor} which is invalid! \n Please select one of the available colors \n or make sure of your hex syntax ex.(#000000) ::")
        
        print("******************************************************************************************")


#Generating Links For Qr Codes
        linkInfo = (linksArr, linkPassword, expireyDate, confirmationEmail, customMessage)
        getOneTimeLink(retriveLink, linkInfo, numOfLinks)
        
        print(f" QR Code Details :: \n Amount of Links : {numOfLinks} \n Link Password : {linkPassword} \n Expirey Date : {expireyDate} \n Confirmation Email : {confirmationEmail} \n Custom Message : {customMessage}")
        print("******************************************************************************************")


#Generate Qr Codes
        qrFolder = createFolder()
        createQRCodes(linksArr, imagePath, qrFolder, foregroundColor, backgroundColor)
        
    except:
        try:
            os.path.exists(qrFolder)
        except:
            pass
        else:
            os.rmdir(qrFolder)
        
        print("\n ********************** \n Oops there seems to be a problem :/ \n Please follow all instructions carefully and try again!")
    else:
        print(f"\n Congratulations your QR codes have been created !! \n You will find them in the '{qrFolder}' folder \n Good Bye :)")

main()

if main == __name__ :
    main()
    
