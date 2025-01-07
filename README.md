# Short Youtube Video

- This is a project to download and convert YouTube videos into `MP3` and `MP4` formats.
- The project is built with FastAPI (Python) and Electrum.Js (JavaScript)

## How it works and how to run it
1. Copy the URL of the video or music you want from YouTube
2. Run the frontend interface
```shell
npx electron . 
```
3. And run backend server in `./backend`
```shell
uvicorn main:app --reload
```
4. Paste the URL and be happy 