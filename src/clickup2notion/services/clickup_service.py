import asyncio
import logging
from aiohttp_client_cache import CachedSession
from aiohttp_client_cache.backends.filesystem import FileBackend

logger = logging.getLogger("clickup_service")

attachment_semaphore = asyncio.Semaphore(value=3)
_attachments_store = {}

ATTACHMENT_DELAY_SECONDS = 1


def get_session(api_token) -> CachedSession:
    return CachedSession(
        headers={"Authorization": api_token},
        cache=FileBackend(cache_name="clickup-cache", allowable_codes=(200, 404)),
    )


async def get_task_attachments(session, task):
    url = f"https://api.clickup.com/api/v2/task/{task["id"]}"
    async with attachment_semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            clickup_task_data = await response.json()
            attachments = clickup_task_data["attachments"]
            if len(attachments) > 0:
                _attachments_store[task["id"]] = attachments
            logger.info(
                f"Encontrados {len(clickup_task_data["attachments"])} anexos na tarefa {task["id"]}"
            )

            await asyncio.sleep(ATTACHMENT_DELAY_SECONDS)


async def get_clickup_tasks(session, list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task?include_markdown_description=true"
    query = {"page": "0", "archived": "false", "include_markdown_description": "true"}
    tasks = []

    while True:
        async with session.get(url, params=query) as response:
            response.raise_for_status()
            list_data = await response.json()
            tasks.extend(list_data["tasks"])
            if list_data["last_page"]:
                break
            query["page"] = str(int(query["page"]) + 1)

    logger.info(f"Encontradas {len(tasks)} tarefas no ClickUp")
    return tasks
