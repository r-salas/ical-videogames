set -xe

heroku container:push web --app ical-videogames

heroku container:release web --app ical-videogames
