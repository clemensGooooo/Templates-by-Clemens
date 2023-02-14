import requests

## now you can just start to defind the url

url = "https://httpbin.org/get"

r = requests.get(url)

r.status_code ## this showes the code for this request 

## 200 => Success, 400 => Bad request,500 => Internal server error, 404 => Not found,
#  401 => Unauthorized

content_type = r.headers['content-type'] ## This line returns the content type from the answer
## e.g. 'application/json; charset=utf8' means JSON as answer
