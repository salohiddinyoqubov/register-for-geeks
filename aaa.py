import http.client
import mimetypes
from codecs import encode

conn = http.client.HTTPConnection("127.0.0.1:8000")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=username;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("test23"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=password;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("m6232971"))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=password_confirm;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("m6232971"))
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
   'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/api/users/", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))