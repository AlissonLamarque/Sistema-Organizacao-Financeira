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
    if request.method == 'POST':
        nome_mercado = request.form.get('nome_mercado')
        data = form.data.data

        # Captura listas com todos os itens do formulário
        produtos_ids = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')
        precos_unitarios = request.form.getlist('preco_unitario')

        # Monta lista de dicionários com os dados
        itens_data = []
        for i in range(len(produtos_ids)):
            if not produtos_ids[i] or not quantidades[i] or not precos_unitarios[i]:
                continue  # ignora campos vazios

            try:
                produto_id = int(produtos_ids[i])
                quantidade = float(quantidades[i])
                preco_unitario = float(precos_unitarios[i])
            except ValueError:
                continue  # ignora se algum dado for inválido

            itens_data.append({
                "produto_id": produto_id,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario
            })

        # Usa o padrão Facade para registrar a compra
        facade = MercadoFacade()
        nova_compra, mensagem = facade.registrar_compra(
            nome_mercado=nome_mercado,
            data=data,
            itens_data=itens_data
        )

        if nova_compra:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
        else:
            flash(mensagem, 'danger')

    produtos = Produto.query.all()
    return render_template('add_grocery_trip.html', form=form, produtos=produtos)

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

@main_bp.route('/add-product-modal', methods=['POST'])
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
    return redirect(url_for('main.add_compra'))  # volta para a tela de nova compra
