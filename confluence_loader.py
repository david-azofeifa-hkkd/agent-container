from langchain_community.document_loaders import ConfluenceLoader
import os
from dotenv import load_dotenv

load_dotenv()
loader = ConfluenceLoader(
    url="https://hakkoda.atlassian.net/wiki/",
    space_key="CCU",
    page_ids=["95223812"],
    username=f"{os.environ["CONFLUENCE_USERNAME"]}",
    api_key=f"{os.environ["CONFLUENCE_API_KEY"]}"
)
documents = loader.load(include_attachments=False, limit=50)

for document in documents:
    print(document)