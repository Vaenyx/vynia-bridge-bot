from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any, ClassVar, Generic, TypeVar, cast, overload

T = TypeVar("T")
OwnerT = TypeVar("OwnerT", bound="ConfigObject")
_MISSING = object()


class ConfigKey(Generic[T]):
    def __init__(
        self,
        parser: Callable[[str], T],
        default: T | object = _MISSING,
        *,
        list_type: Callable[[str], Any] | None = None,
    ) -> None:
        self.parser = parser
        self.default = "" if default is _MISSING or default is ... else default
        self.required = default is ...
        self.list_type = list_type
        self.name = ""
        self.owner: type[ConfigObject]

    def __set_name__(self, owner: type[ConfigObject], name: str) -> None:
        self.name = name

    def parse(self, raw: str | None) -> T:
        if raw is None or raw == "":
            if self.required:
                raise NameError(
                    f"Missing required environment variable "
                    f"BRIDGE_{self.owner.BASE_KEY.upper()}_{self.name.upper()}"
                )
            return cast(T, self.default)

        if self.parser is bool:
            return cast(T, raw.lower() == "true")

        if self.parser is list:
            if raw.strip() == "":
                return cast(T, [])

            values = [item.strip() for item in raw.split(",")]

            if self.list_type is None:
                return cast(T, values)

            return cast(T, [self.list_type(v) for v in values])

        return self.parser(raw)

    @overload
    def __get__(self, instance: None, owner: type[OwnerT]) -> T: ...

    @overload
    def __get__(self, instance: OwnerT, owner: type[OwnerT]) -> T: ...

    def __get__(self, instance: OwnerT | None, owner: type[OwnerT]) -> T:
        return cast(T, owner._values[self.name])


class ConfigObject:
    BASE_KEY: ClassVar[str] = ""
    _values: ClassVar[dict[str, object]]
    keys: ClassVar[dict[str, ConfigKey[Any]]]

    def __init_subclass__(cls, *, base_key: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        cls.BASE_KEY = base_key
        cls.keys = {
            key: value
            for key, value in vars(cls).items()
            if isinstance(value, ConfigKey)
        }
        cls._values = {}

        for cfg in cls.keys.values():
            cfg.owner = cls

    @classmethod
    def refresh(cls) -> None:
        for key, cfg in cls.keys.items():
            env = os.getenv(f"BRIDGE_{cls.BASE_KEY.upper()}_{key.upper()}")
            cls._values[key] = cfg.parse(env)


class ServerConfig(ConfigObject, base_key="server"):
    host: str = cast(str, ConfigKey(str, "mc.hypixel.net"))
    port: int = cast(int, ConfigKey(int, 25565))


class AccountConfig(ConfigObject, base_key="account"):
    email: str = cast(str, ConfigKey(str))


class DataConfig(ConfigObject, base_key="data"):
    current_version: str = cast(str, ConfigKey(str, ""))
    latest_version: str = cast(str, ConfigKey(str, ""))


class DiscordConfig(ConfigObject, base_key="discord"):
    token: str = cast(str, ConfigKey(str))
    channel: int = cast(int, ConfigKey(int))
    ownerId: int | None = cast(int | None, ConfigKey(int, None))
    prefix: str = cast(str, ConfigKey(str, "!"))
    serverName: str | None = cast(str | None, ConfigKey(str, None))


class RedisConfig(ConfigObject, base_key="redis"):
    host: str | None = cast(str | None, ConfigKey(str, None))
    port: int = cast(int, ConfigKey(int, 6379))
    password: str | None = cast(str | None, ConfigKey(str, None))
    clientName: str | None = cast(str | None, ConfigKey(str, None))
    recieveChannel: str | None = cast(str | None, ConfigKey(str, None))
    sendChannel: str | None = cast(str | None, ConfigKey(str, None))


for section in (
    ServerConfig,
    AccountConfig,
    DataConfig,
    DiscordConfig,
    RedisConfig,
):
    section.refresh()
