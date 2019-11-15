import appdaemon.plugins.hass.hassapi as hass


class BathroomVentFan(hass.Hass):
    def initialize(self):

        self.fan = self.args["fan"]
        self.trend_sensor = self.args["trend_sensor"]
        self.humidity_sensor = self.args["humidity_sensor"]

        self.timer_handle = None
        self.humidity = None
        self.fan_running = False

        self.listen_state(self.turn_on, entity=self.trend_sensor, new="On")
        self.listen_state(self.humidity_change, entity=self.humidity_sensor)

    @attribute
    def humidity_max(self):
        return self.humidity * 1.05

    def turn_on(self):

        # Check if we are already running
        if self.fan_running:
            return

        self.call_serivce("fan/turn_on", entity_id=self.fan)
        self.fan_running = True

        # Save the current humidity reading so we can run the fan until we are
        # close to this again.
        self.humidity = self.get_state(self.humidity_sensor)

        # Set a timer to not run the fan for more than an hour
        self.timer_handle = self.run_in(self.turn_off, 60 * 60)

    def turn_off(self):
        self.call_service("fan/turn_off", entity_id=self.fan)

        # If we were turned off before the timer expired, cancel it
        self.cancel_timer(self.timer_handle)

        # Reset variables
        self.timer_handle = None
        self.humidity = None
        self.fan_running = False

    def humidity_change(self):
        if self.fan_running:
            if self.get_state(self.humidity_sensor) < self.humidity_max:
                self.turn_off()
