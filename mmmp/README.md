# MagicMirror Management Protocol

Manipulate MagicMirror configuration and control MagicMirror in various ways through a simple REST interface.

Requires Python3, Flask and a WSGI HTTP server such as gunicorn. Run with:

    cd MagicMirror/mmmp/
    gunicorn3 -b 0.0.0.0:5000 mmmp_server:app

Currently runs in debug mode and allows connections from any IP. Manipulates local files (config.js). Use at own risk.

Config file must be sanitized to allow parsing it with Pythons JSON module:

- Only double quotes allowed
- No comments allowed in config file
- All property names must be enclosed in double quotes, e.g. with `sed -i 's/\([a-zA-Z]\+\):/"\1":/' config.js`

Example valid config.js:

    var config = {
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
    };

    /*************** DO NOT EDIT THE LINE BELOW ***************/
    if (typeof module !== "undefined") {module.exports = config;}

Or just upload a config through the `/top/` endpoint.

Tested with Python version 3.7.4 and flask version 1.0.2.

## Top

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/ > allconf.json
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
    [tausen@tausen-t450s mmmp]$ cat allconf.json | python3 -m json.tool
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
    [tausen@tausen-t450s mmmp]$ python3 -m json.tool allconf.json | grep 8080
      "port": 8080, 
    [tausen@tausen-t450s mmmp]$ sed -i 's/8080/8081/' allconf.json 
    [tausen@tausen-t450s mmmp]$ python3 -m json.tool allconf.json | grep 8081
      "port": 8081, 
    [tausen@tausen-t450s mmmp]$ curl -d "@allconf.json" -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/ | python3 -m json.tool | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
      "port": 8081,
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK[tausen@tausen-t450s mmmp]$

## Top param

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/port/
    {
      "value": 8080
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8081}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK[tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/port/
    {
      "value": 8081
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/port/
    {
      "value": 8080
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/port/
    Found no matching params for 'port'
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/ | python3 -m json.tool | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1757  100  1757    0     0   857k      0 --:--:-- --:--:-- --:--:--  857k
      "port": 8080, 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/top/port/
    {
      "value": 8080
    }

## Modules

    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/ | python3 -m json.tool
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
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/alert/ | python3 -m json.tool
    {
      "value": {
        "module": "alert"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/clock/ | python3 -m json.tool
    {
      "value": {
        "module": "clock", 
        "position": "top_left"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/clock/position/ | python3 -m json.tool
    {
      "value": "top_left"
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": "bottom_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/clock/position/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/clock/position/ | python3 -m json.tool
    {
      "value": "bottom_left"
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "update", "value": "top_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/clock/position/
    OK[tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/clock/position/ | python3 -m json.tool
    {
      "value": "top_left"
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/clock/ | python3 -m json.tool
    {
      "value": {
        "module": "clock", 
        "position": "top_left"
      }
    }
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/ | python3 -m json.tool
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
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "add", "value": {"module": "testy", "position": "top_left", "saf": 123}}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/ | python3 -m json.tool
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
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/testy/ | python3 -m json.tool
    {
      "value": {
        "module": "testy", 
        "position": "top_left", 
        "saf": 123
      }
    }
    [tausen@tausen-t450s mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/testy/
    OK[tausen@tausen-t450s mmmp]$ 
    [tausen@tausen-t450s mmmp]$ curl http://localhost:5000/config/modules/ | python3 -m json.tool
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
