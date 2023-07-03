from pydantic import BaseSettings, PostgresDsn

ENV_FILE = ".env"


class PostgreSQL(BaseSettings):
    __separator = "://"

    class Config:
        env_file: str = ENV_FILE
        env_prefix: str = "POSTGRESQL_"

    dsn: PostgresDsn = "postgres://user:password@127.0.0.1:5432/db"

    def build_using_new_scheme(self, scheme: str) -> str:
        return f"{self.__separator}".join(
            [scheme, self.dsn.split(sep=self.__separator)[1]]
        )

    @property
    def using_async_driver(self):
        scheme = self.build_using_new_scheme("postgresql+asyncpg")
        return scheme


class Config(BaseSettings):
    postgresql: PostgreSQL

    @classmethod
    def create(cls):
        return Config(postgresql=PostgreSQL())
