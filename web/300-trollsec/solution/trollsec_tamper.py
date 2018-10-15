#!/usr/bin/env python

from lib.core.data import kb
from lib.core.enums import PRIORITY
import string

import pytesseract
import requests
from PIL import Image
import io

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    url = 'http://127.0.0.1:10101/token'
    data = requests.get(url).content
    img = Image.open(io.BytesIO(data))
    text = pytesseract.image_to_string(img)

    #print payload
    kwargs['headers']['token']=text
    print kwargs
    #return "&token=" + text + "&id=" + payload

    return payload
    

