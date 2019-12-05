import datetime
import random
import appdaemon.plugins.hass.hassapi as hass
import sys


class ChristmasTreeLights(hass.Hass):
    """Automatically turn on Christmas Tree Lights based on presence"""

    def initialize(self):
        self.log("Starting up")

        self.lights = self.args["lights"]
        self.people = self.args["people"]
        self.randomize = self.args["randomize"]

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

        # Initialize a timer handle for random effects
        self.random_timer_handle = None

    def turn_on(self, entity, attribute, old, new, kwargs):
        self.turn_on_lights()

    def turn_on_timer(self, kwargs):
        # Make sure someone is home
        if self.get_state(self.people) == "home":
            self.turn_on_lights()

    def turn_on_lights(self):
        self.log("Turning on lights")

        # List of effects to choose from. Tuples of (effect, color).
        effects = [
            ("Rainbow", None),
            ("Solid", [255, 238, 142]),
            ("Merry Christmas", None),
            # Railway with white
            ("Railway", [255, 240, 255]),
            # Railway with green
            ("Railway", [4, 92, 18]),
        ]

        # Should we randomize the lights?
        if self.get_state(self.randomize) == "on":
            effect, color = random.choice(effects)
            self.log("Going to change it to {} effect".format(effect))
            if color:
                self.call_service(
                    "light/turn_on",
                    entity_id=self.lights,
                    effect=effect,
                    rgb_color=color,
                )
            else:
                self.call_service("light/turn_on", entity_id=self.lights, effect=effect)
            # Randomly change the effect in an hour
            self.random_timer_handle = self.run_in(self.turn_on_timer, 60 * 60)
        else:
            self.call_service(
                "light/turn_on", entity_id=self.lights, effect="Merry Christmas"
            )

    def turn_off(self, entity, attribute, old, new, kwargs):
        self.turn_off_lights()

    def turn_off_timer(self, kwargs):
        self.turn_off_lights()

    def turn_off_lights(self):
        self.log("Turning off lights")
        self.call_service("light/turn_off", entity_id=self.lights)
        self.cancel_timer(self.random_timer_handle)
        self.log("Random timer handle is now: {}".format(self.random_timer_handle))
