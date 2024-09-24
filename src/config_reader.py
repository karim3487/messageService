from environs import Env

env = Env()
env.read_env()

BROKER: str = env.str("BROKER", "redis://localhost:6379")
BACKEND: str = env.str("BACKEND", "redis://localhost:6379")

BOT_TOKEN: str = env.str("BOT_TOKEN")
STUFF_TG_ID: str = env.str("STUFF_TG_ID")

ERROR_TG_TEMPLATE: str = (
    "<b>Error in project {project_name}!</b>\n"
    "There was a problem when running the {project_name} project:\n"
    "<b>Error:</b> {body}\n\n"
    "<i>Please contact the developer @antoxa_tg.</i>"
)

INFO_TG_TEMPLATE: str = (
    "<b>Information for project {project_name}!</b>\n"
    "Here is some important information regarding the {project_name} project:\n"
    "<b>Info:</b> {body}\n\n"
    "<i>You can contact the developer @antoxa_tg.</i>"
)
