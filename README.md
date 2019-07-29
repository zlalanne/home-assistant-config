# home-assistant-config

Welcome to my Home Assistant (and various other supporting services)
configuration. The top-level `docker-compose.yml` file boots up all the
services. Check out [my blog](https://selfhostedhome.com) for tutorials and
reviews of my setup.

Services Used:
* `homeassistant` for Home Automation
* `postgres` for a storage database for Home Assistant
* `pgadmin` nice user interface for postgres
* `appdaemon` write Home Assistant automations in Python
* `influxdb` time-series database for Home Assistant
* `grafana` visualization for sensor data
* `mosquitto` MQTT broker
* `openzwave` for advanced Z-Wave configuration outside of Home Assistant
* `portainer` for monitoring Docker containers
* `esphome` for monitoring and updating esphome based devices

Most of my hardware setup is detailed [on my blog](https://selfhostedhome.com/my-setup/).

The general structure of my Home Assistant config is based off of [Frenck's configuration](https://github.com/frenck/home-assistant-config).
