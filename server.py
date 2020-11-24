#
# Code by Quan, Tran Hoang (student code: 19120338)
# VNUHCM - University of Science
#
# https://github.com/trhgquan
#

from socket import *

# Check if a file exist in directory
from pathlib import Path

# This is just a C/C++ ways to declare constants.
INDEX_FILE     = "index.html"
PROFILE_FILE   = "infos.html"
NOT_FOUND_FILE = "404.html"
DOWNLOAD_FILE  = "files.html"

# These file extensions will not be delivered as chunks.
streamingLiveSupported = {
  "html" : "html",
  "text" : "text",
  "css" : "css",
  "js" : "javascript"
}

class simpleSocketHttpServer:
  # Initialise
  def __init__(self, hostName, port, packageSize):
    self.hostName = hostName
    self.port = port
    self.packageSize = packageSize

  # Create a new server.
  def create(self):
    self.server = socket(AF_INET, SOCK_STREAM)
    self.server.bind((self.hostName, self.port))
    self.server.listen(5)

  # Handle requests.
  def handle(self):
    client, address = self.server.accept()

    # Receive and decode packages.
    decodedReceive = client.recv(self.packageSize).decode()

    # Split packages into pieces.
    dataPieces = decodedReceive.split("\n")

    if len(dataPieces) > 0 and len(dataPieces[0]) > 0:
      if self.getRequestMethod(dataPieces) == "POST":
        self.handleLoginRequest(client, dataPieces)
      else:
        self.handleNormalRequest(client, dataPieces)
    else:
      self.handleErrorRequest(client)

  # Send full data, not chunks
  def send(self, client, data):
    client.sendall(data.encode())
    client.shutdown(SHUT_WR)

  # Send data in chunks
  def sendChunked(self, client, path):
    # First, create and send header. After a whole Sunday suffering,
    # I finally realised we just need 1 header for a whole response.

    response = "HTTP/1.1 200 OK\r\n"
    response += "content-type: text/plain\r\n"

    # This line told browsers to download the file instead of opening it.
    response += "content-disposition: attachment;\r\n"

    # Required for transfering chunks.
    response += "transfer-encoding: chunked\r\n"
    response += "\r\n"

    client.send(response.encode())

    # Then, open the requested file and read byte by bytes
    # I can read this into buffer, but I don't good at math.

    file = open(path, "rb")

    byte = file.read(1)

    while byte:
      try:
        # Send byte by byte.

        client.sendall("1\r\n".encode())
        client.sendall(byte)
        client.sendall("\r\n".encode())
        byte = file.read(1)
      except ConnectionAbortedError:
        # If user canceled the download process,
        # break.
        print("user canceled")

        file.close()
        client.shutdown(SHUT_WR)

        return False

    # Close the file handler and send terminate chunks.
    
    file.close()
    
    client.sendall("0\r\n\r\n".encode())

    print("transfer success: \"" + str(path) + "\"")
    
    client.shutdown(SHUT_WR)

    return True

  # Start a new server, stop on KeyboardInterrupt.
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

  # Authenticate user.
  def authenticate(self, requestData):
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

  # Get request method.
  def getRequestMethod(self, requestData):
    return requestData[0].split(" ")[0]

  # Get request location
  def getRequestLocation(self, requestData):
    return requestData[0].split(" ")[1][1:]

  # Create a HTTP/1.1 200.
  # Notice this is not how we send a chunked response.
  def create200Response(self, path):
    # Generate a 200 response code.

    print("200", path)

    fileType = path.suffix[1:]

    response = "HTTP/1.1 200 OK\r\n"
    response += "content-type: text/" + streamingLiveSupported[fileType] + "; charset=utf-8\r\n"
    response += "\r\n"
      
    file = open(path, "r")

    response += file.read()    
    response += "\r\n\r\n"

    return response

  # Create a HTTP/1.1 302.
  def create302Response(self, content):
    # Generate a 302 response code.

    print("302", content)

    response = "HTTP/1.1 302 Found\r\n"
    response += "Location: " + content

    return response

  # Create a HTTP/1.1 404.
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

  # Handling error request.
  def handleErrorRequest(self, client):
    return self.send(client, self.create404Response("unknown error"))

  # Handling login request.
  def handleLoginRequest(self, client, requestData):
    if self.authenticate(requestData[-1]):
      return self.send(client, self.create302Response(PROFILE_FILE))
    return self.send(client, self.create404Response("authentication error"))

  # Handling other requests.
  def handleNormalRequest(self, client, requestData):
    fileRequested = Path(self.getRequestLocation(requestData))

    if fileRequested.is_file():
      if fileRequested.suffix[1:] in streamingLiveSupported.keys():
        return self.send(client, self.create200Response(fileRequested))
      return self.sendChunked(client, fileRequested)
    return self.send(client, self.create404Response("Not found: \"" + str(fileRequested) + "\""))

# Main driver.
if __name__ == "__main__":
  server = simpleSocketHttpServer("", 9000, 5000)
  server.start()
