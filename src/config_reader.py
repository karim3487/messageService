from environs import Env

env = Env()
env.read_env()

BROKER: str = env.str("BROKER", "redis://localhost:6379")
BACKEND: str = env.str("BACKEND", "redis://localhost:6379")
