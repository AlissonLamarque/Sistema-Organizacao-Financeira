from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, IdaMercado, Produto
from forms import IdaMercadoForm
from patterns.facade import MercadoFacade
from patterns.decorator import RelatorioSimples, RelatorioComCabecalho, RelatorioComRodapeTotal

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    compras = IdaMercado.query.order_by(IdaMercado.data.desc()).all()
    return render_template('index.html', compras=compras)

@main_bp.route('/add-trip', methods=['GET', 'POST'])
def add_trip():
    form = IdaMercadoForm()
    if form.validate_on_submit():
        
        # Utilizando padrão facade
        facade = MercadoFacade()
        nova_compra, mensagem = facade.registrar_compra(
            nome_mercado=form.nome_mercado.data,
            data=form.data.data,
            itens_data=form.itens.data
        )

        if nova_compra:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
        else:
            flash(mensagem, 'danger')

    return render_template('add_grocery_trip.html', form=form)

@main_bp.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    compra = IdaMercado.query.get_or_404(trip_id)

    # Base para desenvolvimento do padrão Decorator
    relatorio_base = RelatorioSimples()
    relatorio_com_cabecalho = RelatorioComCabecalho(relatorio_base)
    relatorio_final = RelatorioComRodapeTotal(relatorio_com_cabecalho)

    texto_relatorio = relatorio_final.gerar(compra)

    return render_template('trip_detail.html', relatorio=texto_relatorio, compra=compra)

@main_bp.route('/add-product', methods=['GET', 'POST'])
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
        return redirect(url_for('main.add_product'))
    
    produtos = Produto.query.all()
    return render_template('add_product.html', produtos=produtos)
