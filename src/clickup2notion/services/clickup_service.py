import asyncio
import csv
import logging
from aiohttp_client_cache import CachedSession
from aiohttp_client_cache.backends.filesystem import FileBackend
import json

logger = logging.getLogger("clickup_service")

attachment_semaphore = asyncio.Semaphore(value=3)
_attachments_store = {}

ATTACHMENT_DELAY_SECONDS = 1


def get_session(api_token) -> CachedSession:
    return CachedSession(
        headers={"Authorization": api_token},
        cache=FileBackend(cache_name="clickup-cache", allowable_codes=(200, 404)),
    )


async def get_task_attachments(clickup_session, clickup_task):
    url = f"https://api.clickup.com/api/v2/task/{clickup_task["id"]}"
    async with attachment_semaphore:
        async with clickup_session.get(url) as response:
            response.raise_for_status()
            fetched_data = await response.json()
            attachments = fetched_data["attachments"]
            if len(attachments) > 0:
                _attachments_store[clickup_task["id"]] = attachments
            logger.info(
                f"Encontrados {len(fetched_data["attachments"])} anexos na tarefa {clickup_task["id"]}"
            )
            clickup_task["attachments"] = attachments

            # await asyncio.sleep(ATTACHMENT_DELAY_SECONDS)


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


def parse_csv_tasks(clickup_csv_path):
    all_tasks = []

    with open(clickup_csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader: # Modelo padrão exportado pelo clickup
            task = {
                "Task ID": row["Task ID"],
                "Task Custom ID": row["Task Custom ID"],
                "Task Name": row["Task Name"],
                "Task Content": row["Task Content"],
                "Status": row["Status"],
                "Date Created": row["Date Created"],
                "Date Created Text": row["Date Created Text"],
                "Due Date": row["Due Date"],
                "Due Date Text": row["Due Date Text"],
                "Start Date": row["Start Date"],
                "Start Date Text": row["Start Date Text"],
                "Parent ID": row["Parent ID"],
                "Attachments": json.loads(row["Attachments"]),
                "Assignees": row["Assignees"],
                "Tags": row["Tags"].strip("[]").split(",") if row["Tags"] else [],
                "Priority": row["Priority"],
                "List Name": row["List Name"],
                "Folder Name": row["Folder Name"],
                "Space Name": row["Space Name"],
                "Time Estimated": row["Time Estimated"],
                "Time Estimated Text": row["Time Estimated Text"],
                "Checklists": row["Checklists"],
                "Comments": json.loads(row["Comments"]),
                "Assigned Comments": row["Assigned Comments"],
                "Time Spent": row["Time Spent"],
                "Time Spent Text": row["Time Spent Text"],
                "Rolled Up Time": row["Rolled Up Time"],
                "Rolled Up Time Text": row["Rolled Up Time Text"],
            }
            all_tasks.append(task)
    logger.info(f"Encontradas {len(all_tasks)} tarefas no CSV")
    return all_tasks
