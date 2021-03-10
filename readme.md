# Simple Python Socket HTTP Server.
This is my first Lab in Computer Network (CSC10008) @ VNUHCM - University of Science, Fall 2020.

[Watch the demo video here (Vietnamese).](https://www.youtube.com/watch?v=sz-YKLhLqBA)

## Attention!
- This is a __simple__ webserver project demonstrating how socket works. Security issues ahead. _e.g_ type http://localhost:{port}/server.py.
- `download` folder contains
  - `storyInsta.mp4` - video.
  - `hello.txt` - text.
  - `dien.mp3`  - sound.
  - `AnhSang.jpg` - image.

  You can replace these files with yours to test downloading in chunks.

## Technology used:
- Python 3.7.5
- Bootstrap v4.0.0

## Description:
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
4. Files to download are in a folder named `download` __which I ignored to save spaces__.

## Remarks:
- This project __does not__ require session management & cookie management.
- This project is to __create a new simple HTTP server, using socket__, so I can't use any HTTP library.

## License
This project is under [The MIT License](https://github.com/trhgquan/simple-python-socket-http-server/blob/master/LICENSE).
