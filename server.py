from socket import *

# Check if a file exist in directory
from pathlib import Path

# used for recognising files.
import re


INDEX_FILE     = "index.html"
PROFILE_FILE   = "infos.html"
NOT_FOUND_FILE = "404.html"
DOWNLOAD_FILE  = "files.html"

def generate200Response(path):
  response = "HTTP/1.1 200 OK\r\n"

  print("Path: ", path)
  fileType = path.suffix[1:]

  response += "content-type: text/" + fileType + "; charset=utf-8\r\n"
  response += "\r\n"
  
  file = open(path, "r")
  response += file.read()
  response += "\r\n\r\n"

  return response

def generate404Response():
  response = "HTTP/1.1 404 Not Found\r\n"
  response += "content-type: text/html; charset=utf-8\r\n"
  response += "\r\n"

  file = open(NOT_FOUND_FILE, "r")
  response += file.read()
  response += "\r\n\r\n"

  return response

def generate301Response(content):
  response = "HTTP/1.1 303 See Other\r\n"
  response += "Location: /" + content

  return response

def getRequestMethod(request):
  # GET(POST) /url => split using space.
  return request[0].split(" ")[0]

def getRequestFile(request):
  # GET /index.html => /index.html => index.html
  return request[0].split(" ")[1][1:]

def authorize(requestData):
  requestData = requestData.split("&")

  if len(requestData) == 2:
    username = requestData[0].split("=")

    if len(username) == 2:
      username = username[1]
    else: return False

    password = requestData[1].split("=")

    if len(password) == 2:
      password = password[1]
    else: return False

    if (username == "admin") and (password == "admin"): return True
    return False
  else: return False

def createServer():
  server = socket(AF_INET, SOCK_STREAM)
  try :
    server.bind(("", 9000))
    server.listen(5)

    while True:
      (client, address) = server.accept()

      decodedReceive = client.recv(5000).decode()
      pieces = decodedReceive.split("\n")

      data = ""

      # Process those requests
      if len(pieces) > 0 and len(pieces[0]) > 0:
        requestMethod = getRequestMethod(pieces)

        if requestMethod == "POST":
          if authorize(pieces[-1]):
            data = generate301Response(PROFILE_FILE)
          else:
            data = generate404Response()

        else:
          fileRequested = Path(getRequestFile(pieces))

          if fileRequested.is_file():
            data = generate200Response(fileRequested)
          else:
            data = generate404Response()

      else:
        data = generate404Response()
        
      client.sendall(data.encode())
      client.shutdown(SHUT_WR)

  except KeyboardInterrupt :
    print("\nShutting down...\n");

  server.close()

def main():
  print("Access http://localhost:9000")
  createServer()

if __name__ == "__main__":
  main()
