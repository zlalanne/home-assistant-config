import datetime
import random
import sys

import appdaemon.plugins.hass.hassapi as hass

MORNING_TIME = datetime.time(5, 0, 0)
NIGHT_TIME = datetime.time(22, 0, 0)


class ChristmasTreeLights(hass.Hass):
    """Automatically turn on Christmas Tree Lights based on presence"""

    def initialize(self):
        self.log("Starting up")

        self.lights = self.args["lights"]
        self.people = self.args["people"]
        self.randomize = self.args["randomize"]

        # Turn on if someone comes home
        self.listen_state(self.turn_on, entitiy=self.people, new="home", old="not_home")

        # Turn off if everyone leaves home
        self.listen_state(self.turn_off, entity=self.people, new="not_home", old="home")

        self.run_daily(self.turn_on_timer, MORNING_TIME)
        self.run_daily(self.turn_off_timer, NIGHT_TIME)

        # Initialize a timer handle for random effects
        self.random_timer_handle = None

        # Keep a variable to determine if the lights are already on
        self.on = False

        # Should we turn on lights at startup
        if self.get_state(self.people) == "home":
            now = self.time()
            if now < NIGHT_TIME and now > MORNING_TIME:
                self.turn_on_lights()

    def turn_on(self, entity, attribute, old, new, kwargs):
        # Check if lights are already on
        if not self.on:
            self.turn_on_lights()

    def turn_on_timer(self, kwargs):
        # Make sure someone is home
        self.log("Random light timer expired")
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
            if self.random_timer_handle:
                self.cancel_timer(self.random_timer_handle)
            self.random_timer_handle = self.run_in(self.turn_on_timer, 60 * 60)
        else:
            self.call_service(
                "light/turn_on", entity_id=self.lights, effect="Merry Christmas"
            )
        self.on = True

    def turn_off(self, entity, attribute, old, new, kwargs):
        self.turn_off_lights()

    def turn_off_timer(self, kwargs):
        self.turn_off_lights()

    def turn_off_lights(self):
        self.log("Turning off lights")
        self.call_service("light/turn_off", entity_id=self.lights)
        self.cancel_timer(self.random_timer_handle)
        self.random_timer_handle = None
        self.on = False
