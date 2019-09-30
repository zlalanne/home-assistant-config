import appdaemon.plugins.hass.hassapi as hass


# Colors taken from:
# https://www.w3.org/TR/css-color-3/#svg-color
HOLIDAY_COLORS = {
    "New Year's Day": ["yellow"],
    "Valentine's Day": ["deeppink"],
    "Presidents' Day (regional holiday)": ["red", "white", "blue"],
    "St. Patrick's Day": ["green"],
    "Easter Sunday": ["yellow", "hotpink"],
    "Memorial Day": ["red", "white", "blue"],
    "Independence Day": ["red", "white", "blue"],
    "Halloween": ["orangered"],
    "Thanksgiving Day": ["orangered"],
    "Christmas Eve": ["red", "green", "white"],
    "Christmas Day": ["red", "green", "white"],
}


class ExteriorLightsNightRoutine(hass.Hass):
    """Set color for exterior lights at night."""

    def initialize(self):
        self.light = self.args["light"]
        self.calendar = self.args["calendar"]

        self.running = False
        self.color_index = 1

        self.run_at_sunset(self.turn_on)
        self.run_at_sunrise(self.turn_off)

    def turn_on(self, event_name, data, kwargs):
        self.running = True

        is_holiday = self.get_state(self.calendar) == "on"
        holiday = self.get_state(self.calendar, attribute="message")
        colors_for_holiday = holiday in HOLIDAY_COLORS.keys()

        if is_holiday and colors_for_holiday:
            self.colors = HOLIDAY_COLORS[holiday]
            self.call_service(
                "light/turn_on", entity_id=self.light, color_name=self.colors[0]
            )
            if len(self.colors) != 1:
                self.color_index = 1
                self.run_in(self.transition_color, 300)
        else:
            # Regular night, just turn on the lights
            self.call_service("light/turn_on", entity_id=self.light, color_name="white")

    def turn_off(self, event_name, data, kwargs):
        self.running = False
        self.call_service("light/turn_off", entity_id=self.light)

    def transition_color(self, kwargs):
        if self.running:
            self.call_service(
                "light/turn_on",
                entity_id=self.light,
                color_name=self.colors[self.color_index],
            )

            # Increment index of colors. Reset to beginning if cycled through.
            self.color_index = (self.color_index + 1) % len(self.colors)

            self.run_in(self.transition_color, 300)
