
    content_object = database.session.execute(database.select(Content)).scalars().all()[-1]