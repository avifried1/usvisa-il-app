usvisa-il-app
=============

**Code is for personal, non-commercial use only**

**Disclaimer**: This code is meant to facilitate scheduling meetings for the US embassy in Israel. It is not meant for abusing the appointment booking system. Please notice that you may get blocked for misusing the system. I take no responsibility for that.

Check and schedule visa appointments in the [israeli embassy site][israel embassy site]

### Requirements

* [Docker][get docker]
* Cron (to schedule)

For local dev & testing:
* Python >= 3.10 with Virtualenv
* Firefox

### Building Docker Image

```shell
docker build -t usvisa-il-app .
```

### Setting the configuration

Copy the [sample configuration](conf/config.example.yaml):

```shell
cp example.env .env
```

Inside the new `.env` file:

* Set your embassy username & password (`visa_creds_username`, `visa_creds_password`)
* Set your current appointment date (`current_appointment_year`, `current_appointment_month`, `current_appointment_day`)
* If you have a [telegram bot](#get-telegram-alerts), set the token and chat_id (`telegram_token`, `telegram_chat_id`)

### Running

Inside the main project directory:

```shell
docker run --env-file .env -v $PWD:/shared/ --rm usvisa-il-app
```

### Running on a schedule with Cron

As part of a cron:

```shell
crontab -e
```

```shell
PATH=/usr/local/bin/:$PATH
0,10,15,30,45 7-12 * * 0-5 cd /<PATH_TO>/usvisa-il-app && docker run --env-file .env -v $PWD:/shared/ --rm usvisa-il-app >> usvisa.log 2>&1
```

**note**: 1st row is where to add the docker installation location to your path. This might look different depending on your OS (the example will work in linux/mac)

### Get Telegram Alerts

If a Telegram token is set in the configuration you'll receive Telegram alerts when a new appointment is scheduled.

### Screenshot

Once a new appointment was set, a screenshot `appointment_screenshot.png` will be saved into the project's main directory, and a file `new_appointment.txt` will be saved with the appointment details

### Keep looking for earlier appointments

When the scheduler finds an appointment, it schedules it and creates a file `new_appointment.txt` with the details. This is to prevent from scheduling a new, later appointment if running afterwards (since the configuration is still set with the older appointment).

To keep rescheduling, alter the current appointment details in the configuration with the details of the new appointment, and delete `new_appointment.txt`

### Running locally

For easier testing and development cycles (no need to build a docker image) use the same [main](/src/main.py) file, but set the environment variable app_os to `macos` (currently only macOS supported):

```shell
# set up the environment
virtualenv -p python3 venv
source ./venv/bin/activate
# source ./venv/bin/activate.fish for fish CLI users
pip install -r requirements.txt

# run:
app_osx="macos"  python ./src/main.py
```

### Troubleshooting

When an error occurs while running inside a Docker container, a screenshot is saved to allow for debugging.

### TODO

- [ ] Extract current appointment data into a file to parse and update once new meeting is set
- [ ] Support choosing between TLV or Jerusalem

## Credit

Avi Friedman. Buy me a [beer][buy me coffee]!

## License

Licensed under the MIT license (see: [license](LICENSE))

[israel embassy site]: https://ais.usvisa-info.com/he-il
[get docker]: https://docs.docker.com/get-docker/
[buy me coffee]: https://www.buymeacoffee.com/avifr