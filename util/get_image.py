import requests
from config import user_picture_dir, chatroom_picture_dir
import cv2
import numpy as np

# change to save_img_from_url...
def get_image(url, id):
    response = requests.get(url=url)
    save_dir = user_picture_dir + '/' + str(id) + '.jpg'
    with open(save_dir, 'wb') as f:
        f.write(response.content)
    npimg = np.fromstring(response.content, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (200,200), interpolation=cv2.INTER_NEAREST)
    save_dir = user_picture_dir + '/' + str(id) + '.preview.jpg'
    cv2.imwrite(save_dir, img)

def get_image_content(content, id):
    save_dir = user_picture_dir + '/' + str(id) + '.jpg'
    with open(save_dir, 'wb') as f:
        f.write(content)
    npimg = np.fromstring(content, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (200,200), interpolation=cv2.INTER_NEAREST)
    save_dir = user_picture_dir + '/' + str(id) + '.preview.jpg'
    cv2.imwrite(save_dir, img)

def get_image_chat_content(content, id):
    save_dir = chatroom_picture_dir + '/' + str(id) + '.jpg'
    with open(save_dir, 'wb') as f:
        f.write(content)
    npimg = np.fromstring(content, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (200,200), interpolation=cv2.INTER_NEAREST)
    save_dir = chatroom_picture_dir + '/' + str(id) + '.preview.jpg'
    cv2.imwrite(save_dir, img)

    
    
if __name__ == '__main__':
    get_image("https://sprofile.line-scdn.net/0h96a3nT7_ZhlMSk9TOgwYZjwaZXNvOz8LZC0geiodPi0iKiFJNCUvd3wdbSFxeHEbZiR8LXtJPShAWRF_UhyaLUt6OC51fSBPYiQg_A", 1)