import cv2
import pytesseract
import os

file = open("data.txt", "w")


# Path to the image file
image_path = r".\Photos-001\IMG_20210807_090141.jpg"
image_path = os.path.join(image_path)
# Opening the image & storing it in an image object 
img = cv2.imread(image_path)

# Providing the tesseract executable 
# location to pytesseract library 
# pytesseract.tesseract_cmd = path_to_tesseract 

# Passing the image object to image_to_string() function 
# This function will extract the text from the image 
# custom_config = r' -l eng -c preserve_interword_spaces=1'
text = pytesseract.image_to_string(img)

# text = text.replace("\n", " ")
# Displaying the extracted text 
file.write(text)
print("=====>>>>> DONE! >>>>>=====")
