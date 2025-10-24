from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.products import Products
from database import engine
from sqlalchemy.orm import Session

product_bp = Blueprint('products', __name__)

@product_bp.route('/register_product', methods=['GET', 'POST'])
@login_required
def register_product():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        user_id = current_user.id

        with Session(bind=engine) as session:
            produto = Products(nome=nome, preco=preco, user_id=user_id)
            session.add(produto)
            session.commit()

        flash('Produto adicionado com sucesso!', category='success')
        return redirect(url_for('products.products'))
    
    return render_template('products/register.html')

@product_bp.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    with Session(bind=engine) as session:
        products = session.query(Products).all()

        return render_template('products/products.html', products=products)