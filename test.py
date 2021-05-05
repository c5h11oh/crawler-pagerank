import requests

r = requests.get('https://pages.cs.wisc.edu/~remzi/Classes/537/Spring2018/')
print(r.text)
pass