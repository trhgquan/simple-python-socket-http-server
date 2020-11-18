from socket import *

# Check if a file exist in directory
from pathlib import Path

def generateResponse(status, content):
  response = ""

  if status == 301:
    response = "HTTP/1.1 303 See Other\r\n"
    response += "Location: /" + content

  else:
    if status == 200:
      response = "HTTP/1.1 200 OK\r\n"
    
    elif status == 404:
      response = "HTTP/1.1 404 Not Found\r\n"

    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += "\r\n"
    response += content
    response += "\r\n\r\n"

  return response

def getRequestMethod(request):
  # GET(POST) /url => split using space.
  return request[0].split(" ")[0]

def getRequestFile(request):
  return request[0].split(" ")[1]

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
            data = generateResponse(301, "infos.html")
          else:
            f = open("404.html", "r")
            data = generateResponse(404, f.read())
            f.close()
        else:
          fileRequested = Path(getRequestFile(pieces)[1:])

          if fileRequested.is_file():
            f = open(fileRequested, "r")
            data = generateResponse(200, f.read())
            f.close()
          else:
            f = open("404.html", "r")
            data = generateResponse(404, f.read())
            f.close()

      else:
        generateResponse(404, "<h1>An error occurs, but you did nothing wrong, its the universe.</h1>")
        
      client.sendall(data.encode())
      client.shutdown(SHUT_WR)

  except KeyboardInterrupt :
    print("\nShutting down...\n");

  server.close()

print('Access http://localhost:9000')
createServer()
