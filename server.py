from socket import *

# Check if a file exist in directory
from pathlib import Path

INDEX_FILE     = "index.html"
PROFILE_FILE   = "infos.html"
NOT_FOUND_FILE = "404.html"
DOWNLOAD_FILE  = "files.html"

class simpleSocketHttpServer:
  def __init__(self, hostName, port, packageSize):
    self.hostName = hostName
    self.port = port
    self.packageSize = packageSize

  def create(self):
    self.server = socket(AF_INET, SOCK_STREAM)
    self.server.bind((self.hostName, self.port))
    self.server.listen(5)

  def handle(self):
    client, address = self.server.accept()

    decodedReceive = client.recv(self.packageSize).decode()

    dataPieces = decodedReceive.split("\n")

    if len(dataPieces) > 0 and len(dataPieces[0]) > 0:
      requestMethod = self.getRequestMethod(dataPieces)

      if requestMethod == "POST":
        data = self.handleLoginRequest(dataPieces)
      else:
        data = self.handleNormalRequest(dataPieces)

    else:
      data = self.create404Response("return empty")

    self.send(client, data)

    # client.sendall(data.encode())
    # client.shutdown(SHUT_WR)

  def send(self, client, data):
    # Do something here.
    client.sendall(data.encode())
    client.shutdown(SHUT_WR)

  def sendChunked(self, client, data):
    # Do here.
    pass

  def start(self):
    print("Starting server on port {port}".format(port = self.port))
    self.create()

    while True:
      try:
        self.handle()
      except KeyboardInterrupt:
        print("Shutting down..")
        break

    self.server.close()



  def authorize(self, requestData):
    # Authentication: check if username == "admin" && password == "admin"

    # username=abc&password=xyz => ["username=abc", "password=xyz"]
    requestData = requestData.split("&")

    if len(requestData) != 2: return False

    # username=abc => ["username", "abc"]
    username = requestData[0].split("=")

    if len(username) != 2: return False

    # username = "abc"
    username = username[1]

    # password=xyz => ["password", "xyz"]
    password = requestData[1].split("=")

    if len(password) != 2: return False

    # password = "xyz"
    password = password[1]

    if (username != "admin") or (password != "admin"): return False

    return True

  def getRequestMethod(self, requestData):
    return requestData[0].split(" ")[0]

  def getRequestLocation(self, requestData):
    return requestData[0].split(" ")[1][1:]

  def create200Response(self, path):
    # Generate a 200 response code.

    print("200", path)

    response = "HTTP/1.1 200 OK\r\n"

    fileType = path.suffix[1:]

    response += "content-type: text/" + fileType + "; charset=utf-8\r\n"
    response += "\r\n"

    file = open(path, "r")
    response += file.read()
    response += "\r\n\r\n"

    return response

  def create302Response(self, content):
    # Generate a 302 response code.

    print("302", content)

    response = "HTTP/1.1 302 Found\r\n"
    response += "Location: " + content

    return response

  def create404Response(self, content = "error"):
    # Generate a 404 response code.

    print("404", content)

    response = "HTTP/1.1 404 Not Found\r\n"
    response += "content-type: text/html; charset=utf-8\r\n"
    response += "\r\n"

    file = open(NOT_FOUND_FILE, "r")
    response += file.read()
    response += "\r\n\r\n"

    return response

  def handleLoginRequest(self, requestData):
    if self.authorize(requestData[-1]):
      return self.create302Response(PROFILE_FILE)
    return self.create404Response()

  def handleNormalRequest(self, requestData):
    fileRequested = Path(self.getRequestLocation(requestData))

    if fileRequested.is_file():
      return self.create200Response(fileRequested)
    return self.create404Response("Not found: \"" + str(fileRequested) + "\"")

if __name__ == "__main__":
  server = simpleSocketHttpServer("", 9000, 5000)
  server.start()
