from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from .models import IdaMercado, Produto, ItemComprado 
from .forms import IdaMercadoForm

mercado_bp = Blueprint('mercado', __name__, url_prefix='/mercado')

@mercado_bp.route('/')
def index():
    compras = IdaMercado.query.order_by(IdaMercado.data.desc()).all()
    return render_template('mercado/index.html', compras=compras)

@mercado_bp.route('/nova-compra', methods=['GET', 'POST'])
def add_trip():
    form = IdaMercadoForm()
    
    if request.method == 'POST':
        nome_mercado_form = request.form.get('nome_mercado')
        data_compra = form.data.data
        
        nova_compra = IdaMercado(nome_mercado=nome_mercado_form, data=data_compra)
        
        produtos_ids = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')
        precos_unitarios = request.form.getlist('preco_unitario')

        total_itens_validos = 0

        for i in range(len(produtos_ids)):
            if not produtos_ids[i] or not quantidades[i] or not precos_unitarios[i]:
                continue 

            try:
                produto_id_val = int(produtos_ids[i])
                quantidade_val = float(quantidades[i])
                preco_val = float(precos_unitarios[i])
                
                novo_item = ItemComprado(
                    produto_id=produto_id_val,
                    quantidade=quantidade_val,
                    preco_unitario_pago=preco_val
                )
                
                nova_compra.itens.append(novo_item)
                total_itens_validos += 1

            except ValueError:
                continue 

        if total_itens_validos > 0:
            try:
                db.session.add(nova_compra)
                db.session.commit()
                flash(f'Compra em {nome_mercado_form} registrada com sucesso!', 'success')
                return redirect(url_for('mercado.index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao salvar: {str(e)}', 'danger')
        else:
            flash('Nenhum item válido foi adicionado.', 'warning')

    produtos = Produto.query.all()
    return render_template('mercado/add_grocery_trip.html', form=form, produtos=produtos)

@mercado_bp.route('/compra/<int:trip_id>')
def trip_detail(trip_id):
    compra = IdaMercado.query.get_or_404(trip_id)
    return render_template('mercado/trip_detail.html', compra=compra)

@mercado_bp.route('/novo-produto', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome_produto = request.form.get('nome_produto')
        if nome_produto:
            if not Produto.query.filter_by(nome=nome_produto).first():
                novo_produto = Produto(nome=nome_produto)
                db.session.add(novo_produto)
                db.session.commit()
                flash('Produto adicionado com sucesso!', 'success')
            else:
                flash('Este produto já existe.', 'warning')
        return redirect(url_for('mercado.add_product'))
    
    produtos = Produto.query.all()
    return render_template('mercado/add_product.html', produtos=produtos)

@mercado_bp.route('/modal/novo-produto', methods=['POST'])
def add_product_modal():
    nome_produto = request.form.get('nome_produto')
    if nome_produto:
        if not Produto.query.filter_by(nome=nome_produto).first():
            novo_produto = Produto(nome=nome_produto)
            db.session.add(novo_produto)
            db.session.commit()
            flash('Produto adicionado com sucesso!', 'success')
        else:
            flash('Este produto já existe.', 'warning')
            
    return redirect(url_for('mercado.add_trip'))