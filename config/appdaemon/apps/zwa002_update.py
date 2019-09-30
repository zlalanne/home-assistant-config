import appdaemon.plugins.hass.hassapi as hass


class ZWA002UpdateListener(hass.Hass):
    """Event listener to keep ZWA002 light bulbs up to date without polling"""

    def initialize(self):
        self.light = self.args["light"]
        current_color = self.get_state(self.light, attribute="rgb_color")
        self.listen_event(
            self.change_color_callback, event="call_service", domain="light"
        )

    def change_color_callback(self, event_name, data, kwargs):
        # Make sure the callback is servicing the light for this application
        if data["service_data"]["entity_id"] != self.light:
            return

        self.last_state = self.get_state(self.light, attribute="rgb_color")
        self.tries = 4

        self.run_in(self.check_if_state_is_consistent, 4)

    def check_if_state_is_consistent(self, kwargs):
        self.log("Running timer callback")

        self.current_state = self.get_state(self.light, attribute="rgb_color")

        if (self.current_state != self.last_state) and self.tries:
            self.call_service("zwave/refresh_entity", entity_id=self.light)
            self.last_state = self.current_state
            self.tries = self.tries - 1
            self.run_in(self.check_if_state_is_consistent, 8)
