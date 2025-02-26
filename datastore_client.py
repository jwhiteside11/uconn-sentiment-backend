from google.cloud import datastore
from typesense_client import NewsDocument, TypesenseClient, doc1

class DatastoreClient:
    def __init__(self):
        self.client = datastore.Client()
    
    def createNewsStoryEntity(self, news_doc: NewsDocument, id: str = ""):
        if id:
            story = datastore.Entity(self.client.key("newsJDWpoc", id))
        else:
            story = datastore.Entity(self.client.key("newsJDWpoc"))
        story.update(news_doc.__dict__)
        self.client.put(story)

    def getNewsDocByID(self, id: str) -> NewsDocument:
        key = self.client.key("newsJDWpoc", id)
        story = self.client.get(key)
        return NewsDocument(**{pair[0]: pair[1] for pair in story.items()})


if __name__ == "__main__":
    # 1) Create clients
    ds = DatastoreClient()
    ts = TypesenseClient()

    # 2) Create entity
    # ds.createNewsStoryEntity(doc1, "testStory")

    # 3) Fetch entity
    docFetched = ds.getNewsDocByID("testStory")

    # 4) Index into typesense
    ts.deleteNewsColletion()
    ts.createNewsCollection()
    ts.createNewsDocument(docFetched)

    # 5) Search documents
    res = ts.searchNews(ticker="WBS", search_term="AI")
    print(res)