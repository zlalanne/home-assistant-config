import appdaemon.plugins.hass.hassapi as hass


class HomeNotification(hass.Hass):
    def initialize(self):
        self.log("Starting up")

        self.garage_door = self.args["garage_door"]
        self.lights = self.args["lights"]

        self.listen_state(self.start_toggle, entity=self.garage_door, new="open")

    def start_toggle(self, entity, attribute, old, new, kwargs):
        self.log("Garage door open, starting to toggle lights")
        self.flashcount = 0
        self.run_in(self.flash, 1)

    def flash(self, kwargs):
        self.toggle(self.lights)
        self.flashcount += 1
        if self.flashcount < 6:
            self.run_in(self.flash, 1)
