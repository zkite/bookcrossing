def make_shelf(book_resource, book_model, book_schema, book_category_cb, book_owner_cb, book_formation_cb, category_model, user_model, user):
	""" Make books shelf and reverse it"""
	book_resource.shelf = list()
	user_books = book_model.query.filter_by(user_id=user.id).all()
	for book in user_books:
		book_resource.shelf.append(book_formation_cb(book, book_schema, book_category_cb, book_owner_cb, category_model, user_model))
	book_resource.shelf.reverse()


def get_book_category(book_object, category_model):
	""" Return book category name """
	return category_model.query.get(book_object.category_id).name


def get_book_owner(book_object, user_model):
	""" Return books owner """
	return user_model.query.get(book_object.user_id).login


def book_formation(book_object, book_schema, book_category_cb, book_owner_cb, category_model, user_model):
	""" Make book formation  """
	parsed_book = book_schema.dump(book_object).data
	parsed_book['category'] = book_category_cb(book_object, category_model)
	parsed_book['owner'] = book_owner_cb(book_object, user_model)
	return parsed_book


def update_book(book_object, title, author, publisher, category_object, db):
	""" Update fields of book object """
	book_object.title = title
	book_object.author = author
	book_object.publisher = publisher
	book_object.category_id = category_object.id
	db.session.add(book_object)
	db.session.commit()
	return book_object


def create_book(book_model, title, author, publisher, current_user, category_object, db):
	""" Create a book object """
	book_object = book_model(title, author, publisher)
	book_object.user_id = current_user.id
	book_object.category_id = category_object.id
	db.session.add(book_object)
	db.session.commit()
	return book_object


def is_category_exist(category_name, category_model, db):
	""" Detect is category exist or isn't """
	is_category = category_model.query.filter_by(name=category_name).first()
	if not is_category:
		category_object = category_model(category_name)
		db.session.add(category_object)
		db.session.commit()
	else:
		category_object = is_category
	return category_object


def get_book_by_id(book_model, id):
	"""" Get book by id """
	return book_model.query.get(id)


def delete_book_by_id(book_model, id, db):
	""" Delete book from database """
	book_object = book_model.query.get(id)
	db.session.delete(book_object)
	db.session.commit()
	return book_object


def get_category_list(category_model, category_schema):
	""" Get serialized category list from database """
	categories = list()
	category_list = category_model.query.all()
	for category in category_list:
		categories.append(category_schema.dump(category).data)
	return  categories


def search_books(pattern, book_model, book_category_cb, book_owner_cb, book_formation_cb, book_schema, category_model, user_model):
	""" Get all books that matches pattern from searching form """
	serched_books = book_model.query.filter(book_model.title.like('%'+pattern+'%'))
	if serched_books:
		books = list()
		for book in serched_books:
			formed_book = book_formation_cb(book, book_schema, book_category_cb, book_owner_cb, category_model, user_model)
			books.append(formed_book)
		return books
	else:
		return None


def get_books_by_category(category_name, category_model, book_model, book_schema, book_owner_cb, book_category_cb, book_formation_cb, user_model):
	""" Get books by category from select form """
	books = list()
	category = category_model.query.filter_by(name=category_name).first()
	selected_books = book_model.query.filter_by(category_id=category.id).all()
	if selected_books:
		for book in selected_books:
			formed_book = book_formation_cb(book, book_schema, book_category_cb, book_owner_cb, category_model, user_model)
			books.append(formed_book)
		return books
	else:
		return None


def get_all_books(book_model, book_schema, book_category_cb, book_owner_cb, book_formation_cb, category_model, user_model):
	""" Get all books """
	books = list()
	all_books = book_model.query.all()
	if all_books:
		for book in all_books:
			formed_book = book_formation_cb(book, book_schema, book_category_cb, book_owner_cb, category_model, user_model)
			books.append(formed_book)
		return books
