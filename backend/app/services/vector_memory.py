import chromadb

from app.core.config import settings


class VectorMemory:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.chroma_path)
        self.collection = self.client.get_or_create_collection("task_context")

    def add_task_text(self, task_id: int, raw_text: str, parsed_intent: str) -> None:
        self.collection.upsert(
            ids=[str(task_id)],
            documents=[raw_text],
            metadatas=[{"parsed_intent": parsed_intent}],
        )

    def update_task_text(self, task_id: int, raw_text: str, parsed_intent: str) -> None:
        self.add_task_text(task_id=task_id, raw_text=raw_text, parsed_intent=parsed_intent)

    def remove_task_text(self, task_id: int) -> None:
        self.collection.delete(ids=[str(task_id)])

    def recall(self, query: str, limit: int = 3) -> list[dict]:
        result = self.collection.query(query_texts=[query], n_results=limit)
        docs = result.get("documents", [[]])
        ids = result.get("ids", [[]])
        metadata = result.get("metadatas", [[]])
        if not docs:
            return []

        output: list[dict] = []
        for idx, doc in enumerate(docs[0]):
            output.append(
                {
                    "task_id": ids[0][idx] if ids and ids[0] else "",
                    "raw_text": doc,
                    "meta": metadata[0][idx] if metadata and metadata[0] else {},
                }
            )
        return output
