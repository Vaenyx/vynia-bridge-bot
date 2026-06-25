import os

_MISSING = object()


class ConfigKey:
    def __init__(self, parser, default=_MISSING, *, list_type=None):
        self.parser = parser
        self.default = default if default is not _MISSING else ""
        self.required = default is ...
        self.list_type = list_type

    def __set_name__(self, owner, name):
        self.name = name

    def parse(self, raw):
        if raw in ("", None):
            if self.required:
                raise NameError(
                    f"Missing required environment variable "
                    f"BRIDGE_{self.owner.BASE_KEY.upper()}_{self.name.upper()}"
                )
            return self.default

        if self.parser is bool:
            return raw.lower() == "true"

        if self.parser is list:
            if raw.strip() == "":
                return []

            values = [item.strip() for item in raw.split(",")]

            if self.list_type is None:
                return values

            return [self.list_type(v) for v in values]

        return self.parser(raw)

    def __get__(self, instance, owner):
        return owner._values[self.name]


class ConfigObject:
    BASE_KEY = ""
    _values: dict[str, object]
    keys: dict[str, ConfigKey]

    def __init_subclass__(cls, *, base_key: str, **kwargs):
        super().__init_subclass__(**kwargs)

        cls.BASE_KEY = base_key

        cls.keys = {
            key: value
            for key, value in vars(cls).items()
            if isinstance(value, ConfigKey)
        }

        cls._values = {}

        for key, cfg in cls.keys.items():
            cfg.owner = cls

    @classmethod
    def refresh(cls):
        for key, cfg in cls.keys.items():
            env = os.getenv(f"BRIDGE_{cls.BASE_KEY.upper()}_{key.upper()}")
            cls._values[key] = cfg.parse(env)


class ServerConfig(ConfigObject, base_key="server"):
    host: str = ConfigKey(str, "mc.hypixel.net")
    port: int = ConfigKey(int, 25565)


class AccountConfig(ConfigObject, base_key="account"):
    email: str = ConfigKey(str)


class DataConfig(ConfigObject, base_key="data"):
    current_version: str = ConfigKey(str, "")
    latest_version: str = ConfigKey(str, "")


class DiscordConfig(ConfigObject, base_key="discord"):
    token: str = ConfigKey(str)
    channel: int = ConfigKey(int)
    ownerId: int | None = ConfigKey(int, None)
    prefix: str = ConfigKey(str, "!")
    serverName: str | None = ConfigKey(str, None)


class RedisConfig(ConfigObject, base_key="redis"):
    host: str | None = ConfigKey(str, None)
    port: int = ConfigKey(int, 6379)
    password: str | None = ConfigKey(str, None)
    clientName: str | None = ConfigKey(str, None)
    recieveChannel: str | None = ConfigKey(str, None)
    sendChannel: str | None = ConfigKey(str, None)


for section in (
    ServerConfig,
    AccountConfig,
    DataConfig,
    DiscordConfig,
    RedisConfig,
):
    section.refresh()
