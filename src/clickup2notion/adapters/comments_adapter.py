from .base_adapter import ClickUpToNotionAdapter


class CommentsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        comments = clickup_data.get("comments", [])
        notion_comments = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": comment["comment_text"],
                            },
                        }
                    ]
                },
            }
            for comment in comments
        ]
        return {"children": notion_comments}
