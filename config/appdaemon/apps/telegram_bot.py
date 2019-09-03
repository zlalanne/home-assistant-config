import appdaemon.plugins.hass.hassapi as hass


class TelegramBotEventListener(hass.Hass):
    """Event listener for Telegram bot events."""

    def initialize(self):
        """Listen to Telegram Bot events of interest."""
        self.listen_event(self.receive_telegram_command, "telegram_command")
        self.listen_event(self.receive_telegram_callback, "telegram_callback")

    def garage_command(self, user_id):
        state = self.get_state(self.args["garage"])

        msg = "The garage is currently {}".format(state)

        if state == "closed":
            keyboard = [[("Open", "/open_garage"), ("Do Nothing", "/do_nothing")]]
        else:
            keyboard = [[("Close", "/close_garage"), ("Do Nothing", "/do_nothing")]]

        self.call_service(
            "telegram_bot/send_message",
            target=user_id,
            message=msg,
            disable_notification=True,
            inline_keyboard=keyboard,
        )

    def receive_telegram_command(self, event_id, payload_event, *args):
        assert event_id == "telegram_command"
        user_id = payload_event["user_id"]
        command = payload_event["command"]

        if command == "/garage":
            self.garage_command(user_id)

    def receive_telegram_callback(self, event_id, payload_event, *args):
        assert event_id == "telegram_callback"
        data_callback = payload_event["data"]
        callback_id = payload_event["id"]

        if data_callback == "/open_garage":
            self.call_service(
                "telegram_bot/answer_callback_query",
                message="Opening the garage!",
                callback_query_id=callback_id,
            )
            self.call_service("cover/open_cover", entity_id=self.args["garage"])

        elif data_callback == "/close_garage":
            self.call_service(
                "telegram_bot/answer_callback_query",
                message="Closing the garage!",
                callback_query_id=callback_id,
            )
            self.call_service("cover/close_cover", entity_id=self.args["garage"])

        elif data_callback == "/do_nothing":
            self.call_service(
                "telegram_bot/answer_callback_query",
                message="OK, you said no!",
                callback_query_id=callback_id,
            )
