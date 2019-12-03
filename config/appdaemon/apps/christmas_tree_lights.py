import datetime
import appdaemon.plugins.hass.hassapi as hass


class ChristmasTreeLights(hass.Hass):
    """Automatically turn on Christmas Tree Lights based on presence"""

    def initialize(self):
        self.log("Starting up")

        self.lights = self.args["lights"]
        self.people = self.args["people"]

        # Turn on if someone comes home
        self.listen_state(self.turn_on, entitiy=self.people, new="home")

        # Turn off if everyone leaves home
        self.listen_state(self.turn_off, entity=self.people, new="not_home")

        # Turn on at 5 AM
        morning_time = datetime.time(5, 0, 0)
        self.run_once(self.turn_on_timer, morning_time)

        # Turn off at 10 PM
        night_time = datetime.time(22, 0, 0)
        self.run_once(self.turn_off_timer, night_time)

    def turn_on(self, entity, attribute, old, new, kwargs):
        self.turn_on_lights()

    def turn_on_timer(self, kwargs):
        # Make sure someone is home
        if self.get_state(self.people) == "home":
            self.turn_on_lights()

    def turn_on_lights(self):
        self.log("Turning on lights")
        self.call_service("light/turn_on", entity_id=self.lights, effect="Rainbow")

    def turn_off(self, entity, attribute, old, new, kwargs):
        self.turn_off_lights()

    def turn_off_timer(self, kwargs):
        self.turn_off_lights()

    def turn_off_lights(self):
        self.log("Turning off lights")
        self.call_service("light/turn_off", entity_id=self.lights)
