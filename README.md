usvisa-il-app
=============

Check and schedule visa appointments in the [israeli embassy site][israel embassy site]

### Requirements

* [Geckodriver][geckodriver bins] (for armv6 arch - look [here][armv6 geckodriver bins])
* python > 2.7
* virtualenv
* FireFox (for Pi: `sudo apt-get install firefox-esr`)
* cron (to schedule)

**Currently only works with Mac** (see [todo](#todo))

### Installing dependencies

```shell
virtualenv venv
source ./venv/bin/activate # for fish shell: source ./venv/bin/activate.fish
pip3 install -r requirements.txt
```

### Setting the configuration

Copy the [sample configuration](conf/config.example.yaml):

```shell
cp conf/config.example.yaml conf/config.yaml
```

inside the new `conf/config.yaml` file:

* Set your embassy username & password
* Set your current appointment date
* If you have a [telegram bot](#get-telegram-alerts), set the token and chat_id

### Running

inside the main project directory:

```shell
source ./venv/bin/activate
python ./src/usvisa.py
```

### Running on a schedule with Cron

As part of a cron:

```shell
crontab -e
```

```shell
PATH=/usr/local/bin/:$PATH
0,10,15,30,45 0-4 * * 0-5 cd /<PATH_TO>/usvisa-il-app && source ./venv/bin/activate && python ./src/usvisa.py >> usvisa.log 2>&1
```

### Get Telegram Alerts

If a Telegram token is set in the configuration you'll receive Telegram alerts when a new appointment is scheduled.

### Keep looking for earlier appointments

When the scheduler finds an appointment, it schedules it and creates a file `new_appointment.txt` with the details. This is to prevent from scheduling a new, later appointment if running afterwards (since the configuration is still set with the older appointment).

To keep rescheduling, alter the current appointment details in the configuration with the details of the new appointment, and delete `new_appointment.txt`

### Running with Docker (work in progress)

```shell
cp example.env .env
```

Set the environment variables.

```shell
docker build -t usvisa-il-app .
docker run --env-file .env --rm usvisa-il-app
```

### TODO

- [ ] Dockerize for running in RasPi
- [ ] Extract current appointment data into a file to parse and update once new meeting is set


## Credit

Avi Friedman. Buy me a [beer][buy me coffee]!

## License

Licensed under the MIT license (see: [license](LICENSE))

[israel embassy site]: https://ais.usvisa-info.com/he-il
[armv6 geckodriver bins]: https://github.com/d0ku/GeckoDriver_ARMv6
[geckodriver bins]: https://github.com/mozilla/geckodriver/releases
[buy me coffee]: https://www.buymeacoffee.com/avifr