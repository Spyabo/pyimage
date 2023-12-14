import os
import pytesseract
from PIL import Image
from typing import List


# Specify the path to the images folder
images_folder = './images'

def process_images(folder):
    # Get a list of all the image files in the folder
    image_files = [file for file in os.listdir(folder) if file.endswith('.png') or file.endswith('.jpg')][::-1]

    # Load all the images in the folder
    images = []
    
    for file in image_files:
        image_path = os.path.join(folder, file)
        image = Image.open(image_path)
        images.append(image)

    return images

def extract_text(images):
    # Use tesseract to do OCR on the images
    output = []

    for image in images:
        output.append(pytesseract.image_to_string(image))

    return output

def parse_text(texts: List[str]):
    output = ""
    names = []
    urls = []

    # turn text into a comma separated line of the name and the corresponding url
    for text in texts:
        for line in text.split('\n\n'):
            if not line:
                continue
            print(line, line.startswith('http'))
            if line.startswith('http'):
                urls.append(line)
            else:
                names.append(line)
    for name, url in zip(names, urls):
        output += f"{name}, {url}\n"
        
    return output
    
def main():
    images = process_images(images_folder)
    lines = extract_text(images)
    output = parse_text(lines)

    with open('output.txt', 'w') as f:
        f.write(output)
        
if __name__ == '__main__':
    main()