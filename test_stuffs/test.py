import requests

# from urllib.parse import *

r = requests.head('http://pages.cs.wisc.edu/~yxy/')
print(r.headers)
