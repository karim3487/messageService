from environs import Env

env = Env()
env.read_env()

BROKER: str = env.str("BROKER", "redis://localhost:6379")
BACKEND: str = env.str("BACKEND", "redis://localhost:6379")

BOT_TOKEN: str = env.str("BOT_TOKEN")
STUFF_TG_ID: str = env.str("STUFF_TG_ID")

ERROR_TG_TEMPLATE: str = (
    "🚨 <b>Error in project: {project_name}!</b> 🚨\n\n"
    "⚠️ There was an issue while running the <b>{project_name}</b> project:\n"
    "<b>🔴 Error:</b> <i>{body}</i>\n\n"
    "💡 Please check and resolve the issue as soon as possible.\n\n"
    "👨‍💻 <i>Contact the developer: @antoxa_tg</i>"
)

INFO_TG_TEMPLATE: str = (
    "ℹ️ <b>Project: {project_name} - Information</b> ℹ️\n\n"
    "📢 Here’s an important update about the <b>{project_name}</b> project:\n"
    "<b>📝 Info:</b> <i>{body}</i>\n\n"
    "📍 Stay informed and take necessary action if needed.\n\n"
    "👨‍💻 <i>You can reach the developer: @antoxa_tg</i>"
)
