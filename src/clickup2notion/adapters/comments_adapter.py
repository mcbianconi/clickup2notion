from .base_adapter import ClickUpToNotionAdapter


class CommentsAdapter(ClickUpToNotionAdapter):
    def convert(self, clickup_data: dict) -> dict:
        comments = clickup_data.get("Comments", [])
        children = []
        if comments:
            children.append(
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "Comentários"},
                            },
                        ],
                        "is_toggleable": False,
                    },
                }
            )
            for comment in comments:
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"{comment["text"]} by {comment.get("by", "???")} em {comment["date"]}",
                                    },
                                }
                            ]
                        },
                    }
                )
                children.append({"object": "block", "type": "divider", "divider": {}})
        return {"children": children}
