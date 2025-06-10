# repository/image_repository.py
def save_image_url(db: Session, user_id: int, image_url: str):
    db_image = ImageModel(user_id=user_id, url=image_url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
