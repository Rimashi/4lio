from app.extensions import db
from app.models.book import Book
from app.models.collection import Collection


class CollectionService:
    @staticmethod
    def get_collection(collection_id: int) -> Collection:
        return Collection.query.get_or_404(collection_id)

    @staticmethod
    def get_user_collections(user_id: int):
        return (
            Collection.query
            .filter_by(user_id=user_id)
            .order_by(Collection.id.desc())
            .all()
        )

    @staticmethod
    def create_collection(user_id: int, name: str) -> Collection:
        if not name.strip():
            raise ValueError('Название подборки не может быть пустым')
        collection = Collection(name=name.strip(), user_id=user_id)
        db.session.add(collection)
        db.session.commit()
        return collection

    @staticmethod
    def delete_collection(collection: Collection) -> None:
        db.session.delete(collection)
        db.session.commit()

    @staticmethod
    def add_book_to_collection(collection: Collection, book_id: int) -> None:
        book = Book.query.get_or_404(book_id)
        if book not in collection.books:
            collection.books.append(book)
            db.session.commit()

    @staticmethod
    def remove_book_from_collection(collection: Collection, book_id: int) -> None:
        book = Book.query.get_or_404(book_id)
        if book in collection.books:
            collection.books.remove(book)
            db.session.commit()

    @staticmethod
    def get_collection_books(collection: Collection):
        return collection.books