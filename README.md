# iCal video games
Track upcoming video game release dates directly in your calendar.

## Cloud
Go to [ical-videogames.onrender.com](https://ical-videogames.onrender.com/)

## Self-Hosted
Build dockerfile
```console
$ docker build -t ical-videogames .
```
Run dockerfile
```console
$ docker run -d -p 5000:5000 ical-videogames
```

## Usage

1. Open the website:
   - Cloud: [ical-videogames.onrender.com](https://ical-videogames.onrender.com/)
   - Self-Hosted: [localhost:5000](http://localhost:5000/)

2. Choose platforms/region and copy the URL.
![Web platform](media/web.png)

3. Add URL to your calendar:
![Calendar](media/calendar.png)

## Development
### Installation
```
$ pip install -r requirements.txt
```
### Usage
```console
$ flask run --reload --debug
```
