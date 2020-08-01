from classes import *

def set_image_name(image_id, image_name):
    try:
        session.query(Image).filter(Image.id == image_id). \
            update({Image.image_name: image_name},  synchronize_session=False)
        session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()
        return


def create_image_instance(user_id, image_url, thumb_url):
    try:
        instance = Image(user_id=user_id, image_url=image_url, thumb_url=thumb_url)
        session.add(instance)
        session.commit()

        image_id = session.query(Image).filter(Image.image_url == image_url).all()
        return image_id[0].id
    except Exception as ex:
        print(ex)
        session.rollback()
        return

def get_image_by_name(user_id, user_input):
    try:
        instance = session.query(Image).filter(Image.user_id == user_id, Image.image_name.like(f'%{user_input}%')).all()
        return instance
    except Exception as ex:
        print(ex)
        session.rollback()
        return
