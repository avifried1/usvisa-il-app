usvisa-il-app
=============

Check and schedule visa appointments in the [israeli embassy site][israel embassy site]

### Requirements

* Docker
* cron (to schedule)

### Building Docker Image

```shell
docker build -t usvisa-il-app .
```

### Setting the configuration

Copy the [sample configuration](conf/config.example.yaml):

```shell
cp example.env .env
```

inside the new `.env` file:

* Set your embassy username & password (`visa_creds_username`, `visa_creds_password`)
* Set your current appointment date (`current_appointment_year`, `current_appointment_month`, `current_appointment_day`)
* If you have a [telegram bot](#get-telegram-alerts), set the token and chat_id (`telegram_token`, `telegram_chat_id`)

### Running

inside the main project directory:

```shell
docker run --env-file .env -v $PWD:/shared/ --rm usvisa-il-app
```

### Running on a schedule with Cron

As part of a cron:

```shell
crontab -e
```

```shell
0,10,15,30,45 7-12 * * 0-5 cd /<PATH_TO>/usvisa-il-app && docker run --env-file .env -v $PWD:/shared/ --rm usvisa-il-app >> usvisa.log 2>&1
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

- [ ] Extract current appointment data into a file to parse and update once new meeting is set


## Credit

Avi Friedman. Buy me a [beer][buy me coffee]!

## License

Licensed under the MIT license (see: [license](LICENSE))

[israel embassy site]: https://ais.usvisa-info.com/he-il
[armv6 geckodriver bins]: https://github.com/d0ku/GeckoDriver_ARMv6
[geckodriver bins]: https://github.com/mozilla/geckodriver/releases
[buy me coffee]: https://www.buymeacoffee.com/avifr