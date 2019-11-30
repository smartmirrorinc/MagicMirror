# MagicMirror Management Protocol

Manipulate MagicMirror configuration and control MagicMirror in various ways through a simple REST interface.

Requires Python3 and Flask. Run with:

    cd MagicMirror/mmmp/
    python3 mmmp_server.py

Currently runs in debug mode and uses unsafe webserver. Manipulates local files (config.js). Use at own risk.

Config file must be sanitized to allow parsing it with Pythons JSON module:

- Only double quotes allowed
- No comments allowed in config file
- All property names must be enclosed in double quotes, e.g. with `sed -i 's/\([a-zA-Z]\+\):/"\1":/' config.js`

Tested with Python version 3.7.4 and flask version 1.1.1.

## Top

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/ > allconf.json
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
    [tausen@tausen-t450s mmmp]$ cat allconf.json 
    {
      "address": "localhost", 
      "ipWhitelist": [
        "127.0.0.1", 
        "::ffff:127.0.0.1", 
        "::1"
      ], 
      "language": "da", 
      "modules": [
        {
          "module": "alert"
        }, 
        {
          "module": "clock", 
          "position": "top_left"
        }, 
        {
          "config": {
            "calendars": [
              {
                "symbol": "calendar-check", 
                "url": "webcal://www.calendarlabs.com/ical-calendar/ics/43/Denmark_Holidays.ics"
              }
            ]
          }, 
          "header": "DK Holidays", 
          "module": "calendar", 
          "position": "top_left"
        }, 
        {
          "module": "compliments", 
          "position": "lower_third"
        }, 
        {
          "config": {
            "appid": "3637dbfe421257bc0195ee40facc8bfc", 
            "location": "Aalborg", 
            "locationID": "2624886"
          }, 
          "module": "currentweather", 
          "position": "top_right"
        }, 
        {
          "config": {
            "appid": "3637dbfe421257bc0195ee40facc8bfc", 
            "location": "Aalborg", 
            "locationID": "2624886"
          }, 
          "header": "Weather Forecast", 
          "module": "weatherforecast", 
          "position": "top_right"
        }, 
        {
          "config": {
            "broadcastNewsFeeds": true, 
            "broadcastNewsUpdates": true, 
            "feeds": [
              {
                "title": "DR", 
                "url": "http://www.dr.dk/nyheder/service/feeds/allenyheder"
              }
            ], 
            "showPublishDate": true, 
            "showSourceTitle": true
          }, 
          "module": "newsfeed", 
          "position": "bottom_bar"
        }, 
        {
          "module": "MMM-ip", 
          "position": "bottom_right"
        }, 
        {
          "module": "updatenotification", 
          "position": "top_bar"
        }
      ], 
      "port": 8081, 
      "timeFormat": 24, 
      "units": "metric"
    }
    [tausen@tausen-t450s mmmp]$ grep 8080 allconf.json 
      "port": 8080, 
    [tausen@tausen-t450s mmmp]$ sed -i 's/8080/8081/' allconf.json 
    [tausen@tausen-t450s mmmp]$ grep 8081 allconf.json 
      "port": 8081, 
    [tausen@tausen-t450s mmmp]$ curl -d "@allconf.json" -H "Content-Type: application/json" -X POST http://localhost:5000/top/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/ | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
      "port": 8081,
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/top/port/
    OK[tausen@tausen-t450s mmmp]$

## Top param

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/port/
    {
      "value": 8080
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8081}' -H "Content-Type: application/json" -X POST http://localhost:5000/top/port/
    OK[tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/port/
    {
      "value": 8081
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/port/
    {
      "value": 8080
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/port/
    ...
    KeyError: 'port'
    ...
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/ | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
      "port": 8080, 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/top/port/
    {
      "value": 8080
    }

## Modules

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/
    {
      "modules": [
        "alert", 
        "clock", 
        "calendar", 
        "compliments", 
        "currentweather", 
        "weatherforecast", 
        "newsfeed", 
        "MMM-ip", 
        "updatenotification"
      ]
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/alert/
    {
      "value": {
        "module": "alert"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/clock/
    {
      "value": {
        "module": "clock", 
        "position": "top_left"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/clock/position/
    {
      "value": "top_left"
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": "bottom_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/modules/clock/position/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/clock/position/
    {
      "value": "bottom_left"
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": "top_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/modules/clock/position/
    OK[tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/clock/position/
    {
      "value": "top_left"
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/clock/
    {
      "value": {
        "module": "clock", 
        "position": "top_left"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/
    {
      "modules": [
        "alert", 
        "clock", 
        "calendar", 
        "compliments", 
        "currentweather", 
        "weatherforecast", 
        "newsfeed", 
        "MMM-ip", 
        "updatenotification"
      ]
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "add", "value": {"module": "testy", "position": "top_left", "saf": 123}}' -H "Content-Type: application/json" -X POST http://localhost:5000/modules/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/
    {
      "modules": [
        "alert", 
        "clock", 
        "calendar", 
        "compliments", 
        "currentweather", 
        "weatherforecast", 
        "newsfeed", 
        "MMM-ip", 
        "updatenotification", 
        "testy"
      ]
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/testy/
    {
      "value": {
        "module": "testy", 
        "position": "top_left", 
        "saf": 123
      }
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/modules/testy/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/modules/
    {
      "modules": [
        "alert", 
        "clock", 
        "calendar", 
        "compliments", 
        "currentweather", 
        "weatherforecast", 
        "newsfeed", 
        "MMM-ip", 
        "updatenotification"
      ]
    }
