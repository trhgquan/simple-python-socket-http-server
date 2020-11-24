# Simple Python Socket HTTP Server.
This is my final Lab Project in Computer Network (CSC10008) @ VNUHCM - University of Science, winter 2020.

## Description
- `index.html`: Login page.
- `404.html`: Not found page.
- `files.html`: Download page.
- `infos.html`: Profile page.
- `server.py`: Server file.

1. From `index.html`, user log in to the system with username `admin` and password `admin`. This action use the HTTP POST method.

    a. If user is logged in, redirect (HTTP/1.1 302) to `infos.html`.

    b. Otherwise, HTTP/1.1 404 returned.

2. `infos.html` is the information of students worked on this project.
3. `files.html` displays a list of files that user can download. These files are delivered in `transfer-encoding: chunked` format, not `content-length`.
4. Files to download are in a folder named `download` __which I ignored__.

## Remarks
- This project __does not__ require session management & cookie management.
- This project is to __create a new simple HTTP server, using socket__, so I can't use any HTTP library.
