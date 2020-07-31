from classes import *

def set_image_name(image_id, image_name):
    session.query(Image).filter(Image.id == image_id). \
        update({Image.image_name: image_name},  synchronize_session=False)
    session.commit()


def create_image_instance(user_id, image_url, thumb_url):
    instance = Image(user_id=user_id, image_url=image_url, thumb_url=thumb_url)
    session.add(instance)
    session.commit()

    image_id = session.query(Image).filter(Image.image_url == image_url).all()
    return image_id[0].id

def get_image_by_name(user_id, user_input):
    instance = session.query(Image).filter(Image.user_id == user_id, Image.image_name.like(f'%{user_input}%')).all()
    return instance
