class DiscordError(Exception):
    """
    Base class of all discord errors
    """


class DiscordHTTPError(DiscordError):
    """
    Discord errors raised on http.
    """


class DiscordComponentError(DiscordError):
    """
    Discord component errors.
    """


class NestedActionRowNotAllowed(DiscordComponentError):
    """
    Error raised when action rows are nested,
    """
    def __init__(self):
        super(NestedActionRowNotAllowed, self).__init__('Cannot contain ActionRow inside ActionRow!')
