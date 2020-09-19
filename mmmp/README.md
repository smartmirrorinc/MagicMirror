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
                "_meta": {
                    "id": 0
                },
                "module": "alert"
            },
            {
                "_meta": {
                    "id": 1,
                    "help-url": "https://docs.magicmirror.builders/modules/clock.html",
                    "order": 100
                },
                "module": "clock",
                "position": "top_left"
            },
            {
                "_meta": {
                    "id": 2,
                    "help-url": "https://docs.magicmirror.builders/modules/calendar.html",
                    "order": 200
                },
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
                "_meta": {
                    "id": 3,
                    "help-url": "https://docs.magicmirror.builders/modules/compliments.html"
                },
                "module": "compliments",
                "position": "lower_third"
            },
            {
                "_meta": {
                    "id": 4,
                    "help-url": "https://docs.magicmirror.builders/modules/newsfeed.html"
                }
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
                "_meta": {
                    "id": 5,
                    "help-url": "https://github.com/fewieden/MMM-ip"
                },
                "module": "MMM-ip",
                "position": "bottom_right"
            },
            {
                "_meta": {
                    "id": 6,
                    "help-url": "https://docs.magicmirror.builders/modules/updatenotification.html"
                },
                "module": "updatenotification",
                "position": "top_bar"
            }
        ],
        "port": 8080,
        "timeFormat": 24,
        "units": "metric"
    };
    
    /*************** DO NOT EDIT THE LINE BELOW ***************/
    if (typeof module !== "undefined") {module.exports = config;}

Or upload a config through the `/top/` endpoint.

Tested with Python version 3.8.5/3.7.4 and flask version 1.0.2.

## Top

    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/ > allconf.json
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1346  100  1346    0     0   657k      0 --:--:-- --:--:-- --:--:-- 1314k
    [tausen@tausen-home mmmp]$ cat allconf.json | python -m json.tool
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
                "_meta": {
                    "id": 0
                },
                "module": "alert"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/clock.html",
                    "id": 1,
                    "order": 100
                },
                "module": "clock",
                "position": "top_left"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/calendar.html",
                    "id": 2,
                    "order": 200
                },
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
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/compliments.html",
                    "id": 3
                },
                "module": "compliments",
                "position": "lower_third"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/newsfeed.html",
                    "id": 4
                },
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
                "_meta": {
                    "help-url": "https://github.com/fewieden/MMM-ip",
                    "id": 5
                },
                "module": "MMM-ip",
                "position": "bottom_right"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/updatenotification.html",
                    "id": 6
                },
                "module": "updatenotification",
                "position": "top_bar"
            }
        ],
        "port": 8080,
        "timeFormat": 24,
        "units": "metric"
    }

    [tausen@tausen-home mmmp]$ python -m json.tool allconf.json | grep 8080
        "port": 8080,
    [tausen@tausen-home mmmp]$ sed -i 's/8080/8081/' allconf.json 
    [tausen@tausen-home mmmp]$ python -m json.tool allconf.json | grep 8081
        "port": 8081,
    [tausen@tausen-home mmmp]$ curl -d "@allconf.json" -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/ | python -m json.tool | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1346  100  1346    0     0  1314k      0 --:--:-- --:--:-- --:--:-- 1314k
        "port": 8081,
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK

## Top param

    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/port/
    {"value":8080}
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": 8081}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/port/
    {"value":8081}
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/port/
    {"value":8080}
    [tausen@tausen-home mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/port/
    Found no matching params for 'port'
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": 8080}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/top/port/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/ | python -m json.tool | grep port
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1346  100  1346    0     0  1314k      0 --:--:-- --:--:-- --:--:-- 1314k
        "port": 8080,
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/top/port/
    {"value":8080}

## Modules

    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   719  100   719    0     0   702k      0 --:--:-- --:--:-- --:--:--  702k
    {
        "modules": [
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/clock.html",
                    "id": 1,
                    "order": 100
                },
                "module": "clock"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/calendar.html",
                    "id": 2,
                    "order": 200
                },
                "module": "calendar"
            },
            {
                "_meta": {
                    "id": 0
                },
                "module": "alert"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/compliments.html",
                    "id": 3
                },
                "module": "compliments"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/newsfeed.html",
                    "id": 4
                },
                "module": "newsfeed"
            },
            {
                "_meta": {
                    "help-url": "https://github.com/fewieden/MMM-ip",
                    "id": 5
                },
                "module": "MMM-ip"
            },
            {
                "_meta": {
                    "help-url": "https://docs.magicmirror.builders/modules/updatenotification.html",
                    "id": 6
                },
                "module": "updatenotification"
            }
        ]
    }
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/0/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    46  100    46    0     0  46000      0 --:--:-- --:--:-- --:--:-- 46000
    {
        "value": {
            "_meta": {
                "id": 0
            },
            "module": "alert"
        }
    }
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/1/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   146  100   146    0     0   142k      0 --:--:-- --:--:-- --:--:--  142k
    {
        "value": {
            "_meta": {
                "help-url": "https://docs.magicmirror.builders/modules/clock.html",
                "id": 1,
                "order": 100
            },
            "module": "clock",
            "position": "top_left"
        }
    }
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/1/position/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    21  100    21    0     0  21000      0 --:--:-- --:--:-- --:--:-- 21000
    {
        "value": "top_left"
    }
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": "bottom_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/1/position/
    OK
    [tausen@tausen-home mmmp]$  curl http://localhost:5000/config/modules/1/position/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    24  100    24    0     0  24000      0 --:--:-- --:--:-- --:--:-- 24000
    {
        "value": "bottom_left"
    }
    [tausen@tausen-home mmmp]$ curl -d '{"action": "update", "value": "top_left"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/1/position/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/1/position/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    21  100    21    0     0  21000      0 --:--:-- --:--:-- --:--:-- 21000
    {
        "value": "top_left"
    }

    [tausen@tausen-home mmmp]$ curl -d '{"action": "add", "value": {"module": "clock", "position": "bottom_right", "someprop": 123}}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/
    {"_meta":{"id":7},"module":"clock"}
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/7/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    87  100    87    0     0  87000      0 --:--:-- --:--:-- --:--:-- 87000
    {
        "value": {
            "_meta": {
                "id": 7
            },
            "module": "clock",
            "position": "bottom_right",
            "someprop": 123
        }
    }
    [tausen@tausen-home mmmp]$ curl -d '{"action": "delete"}' -H "Content-Type: application/json" -X POST http://localhost:5000/config/modules/7/
    OK
    [tausen@tausen-home mmmp]$ curl http://localhost:5000/config/modules/7/
    Found no matching modules for '7'

## Manage

See also `/manage/start/`, `/manage/stop/` and `/manage/restart/`.

    [tausen@tausen-home mmmp]$ curl http://localhost:5000/manage/listmodules/ | python -m json.tool
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   262  100   262    0     0   127k      0 --:--:-- --:--:-- --:--:--  255k
    {
        "value": [
            "updatenotification",
            "newsfeed",
            "alert",
            "clock",
            "compliments",
            "weather",
            "currentweather",
            "weatherforecast",
            "helloworld",
            "calendar",
            "MMM-Dad-Jokes",
            "MMM-GrafanaChart",
            "MMM-ip",
            "MMM-PIR-Sensor",
            "MMM-inspirobot",
            "MMM-DarkSkyForecast",
            "MMM-CalendarExt2"
        ]
    }

