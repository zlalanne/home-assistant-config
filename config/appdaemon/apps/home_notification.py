
class HomeNotification(hass.Hass):

    def initialize(self):
        self.log("Starting up")

        self.garage_door = self.args["garage_door"]
        self.lights = self.args["lights"]

    def flash(self, kwargs):
        self.toggle(self.lights)
        self.flashcount += 1
        if self.flashcount < 15:
            self.run_in(self.flash, 1)
