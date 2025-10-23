from flask import Blueprint
from database import *
from app import *


book_bp = Blueprint('books', __name__, template_folder='templates')

@book_bp.route('/register_book', methods=['GET', 'POST'])
def register_book():
    if request.method == 'POST':
        titulo = request.form['titulo']
        user_id = current_user.id

        with Session(bind=engine) as session:
            book = session.query(Book).filter_by(titulo=titulo).first()

            if not book:
                new_book = Book(titulo=titulo, user_id=user_id)
                session.add(new_book)
                session.commit()

                flash('Livro adicionado com sucesso!', category='success')
                return redirect(url_for('books.books'))
            
            flash('O livro não pode ser adicionado...', category='error')
            return redirect(url_for('books.register_book'))
    
    return render_template('register_book.html')

@book_bp.route('/books')
def books():
    with Session(bind=engine) as session:
        books = session.query(Book).all()

        return render_template('books.html', books=books)