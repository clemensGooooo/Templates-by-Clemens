import request

## now you can just start to defind the url

url = "https://httpbin.org/get"

r = request.get(url)

r.status_code ## this showes the code for this request