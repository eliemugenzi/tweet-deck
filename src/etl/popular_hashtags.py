from ..models.models import PopularHashTag, db

def load_popular_hashtags(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        itemList = file.readlines()

        print(f"Popular HashTags: {itemList}")

        for hashtag in itemList:
            hash = PopularHashTag(name=hashtag)
            db.session.add(hash)
            db.session.commit()
        return itemList
