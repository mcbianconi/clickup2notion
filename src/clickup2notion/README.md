# ClickUp to Notion Migration

This project provides a way to migrate tasks from ClickUp to Notion using Python.

## Structure

- **adapters**: Contains the adapter classes to convert data from ClickUp format to Notion format.
- **factories**: Contains the factory class to manage adapters.
- **services**: Contains the service classes to interact with ClickUp and Notion APIs.
- **utils**: Contains utility functions and logger setup.
- **main.py**: The entry point of the application.

## How to Run

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Set up environment variables in a `.env` file:
    ```
    CLICKUP_API_TOKEN=your_clickup_api_token
    NOTION_API_TOKEN=your_notion_api_token
    ```

3. Run the migration:
    ```sh
    python main.py --clickup_list_id your_clickup_list_id --notion_database_id your_notion_database_id
    ```

## License

This project is licensed under the MIT License.
