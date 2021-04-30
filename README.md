usvisa-il-app
=============

Check and schedule visa appointments in the [israeli embassy site][israel embassy site]

### Requirements

* [Geckodriver][geckodriver bins] (for armv6 arch - look [here][armv6 geckodriver bins])
* python > 2.7
* virtualenv
* FireFox (for Pi: `sudo apt-get install firefox-esr`)
* cron (to schedule)

For RaspberryPi (currently in development):

* xvfb

```shell
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install firefox-esr xvfb 
```

**Currently only works with Mac**

### Installing dependencies

```shell
virtualenv venv
source ./venv/bin/activate # for fish shell: source ./venv/bin/activate.fish
pip3 install -r requirements.txt
```

### config

* Set your username & password
* Set your current appointment date

### Running

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

## Credit

Avi Friedman. Buy me a [beer][buy me coffee]!

## License

Licensed under the MIT license (see: [license](LICENSE))

[israel embassy site]: https://ais.usvisa-info.com/he-il
[armv6 geckodriver bins]: https://github.com/d0ku/GeckoDriver_ARMv6
[geckodriver bins]: https://github.com/mozilla/geckodriver/releases
[buy me coffee]: https://www.buymeacoffee.com/avifr