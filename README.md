# 🧩 Sistema de Registro de Compras no Mercado

## 🧠 Padrões de Projeto Implementados

### 1. **Facade Pattern**

📄 **Arquivo:** `patterns/facade.py`

O padrão Facade foi utilizado para simplificar o processo de registrar uma compra, 
centralizando a lógica de criação de objetos e persistência no banco de dados em uma única classe.

#### 💡 Trecho de Código:
```python
# patterns/facade.py
from models import db, IdaMercado, ItemComprado, Produto

class MercadoFacade:
    def registrar_compra(self, nome_mercado, data, itens_data):
        if not itens_data:
            return None, "Nenhum item foi adicionado à compra."

        nova_ida_mercado = IdaMercado(nome_mercado=nome_mercado, data=data)
        valor_total_calculado = 0
        objetos_para_salvar = [nova_ida_mercado]

        for item_info in itens_data:
            produto = Produto.query.get(item_info['produto_id'])
            if not produto:
                continue

            novo_item = ItemComprado(
                quantidade=item_info['quantidade'],
                preco_unitario_pago=item_info['preco_unitario'],
                produto=produto,
                ida_mercado=nova_ida_mercado
            )
            valor_total_calculado += novo_item.get_custo()
            objetos_para_salvar.append(novo_item)

        nova_ida_mercado.valor_total = valor_total_calculado

        try:
            db.session.add_all(objetos_para_salvar)
            db.session.commit()
            return nova_ida_mercado, "Compra registrada com sucesso!"
        except Exception as e:
            db.session.rollback()
            return None, f"Erro ao registrar compra: {e}"

# routes/base.py
@main_bp.route('/add-trip', methods=['GET', 'POST'])
def add_trip():
    form = IdaMercadoForm()
    if request.method == 'POST':
        nome_mercado = request.form.get('nome_mercado')
        data = form.data.data

        produtos_ids = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')
        precos_unitarios = request.form.getlist('preco_unitario')

        itens_data = []
        for i in range(len(produtos_ids)):
            try:
                produto_id = int(produtos_ids[i])
                quantidade = float(quantidades[i])
                preco_unitario = float(precos_unitarios[i])
            except ValueError:
                continue 

            itens_data.append({
                "produto_id": produto_id,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario
            })

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
```

### 1. **Composite Pattern**

📄 **Arquivo:** `models.py`

O padrão Composite é usado para tratar objetos individuais e composições de objetos de forma uniforme.
Neste caso, tanto itens quanto grupos de custos implementam o método get_custo().

#### 💡 Trecho de Código:
```python
# --- Implementação do Padrão Composite ---
class ComponenteCusto(abc.ABC):
    """
    A interface 'Component' declara um método comum para folhas e compostos
    """
    @abc.abstractmethod
    def get_custo(self):
        pass

class IdaMercado(db.Model):
    """
    Representa uma ida ao mercado
    """
    __tablename__ = 'idas_mercado'
    id = db.Column(db.Integer, primary_key=True)
    nome_mercado = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

    itens = db.relationship('ItemComprado', back_populates='ida_mercado', cascade="all, delete-orphan")

    def get_custo(self):
        return sum(item.get_custo() for item in self.itens)

class ItemComprado(db.Model):
    """
    Representa um item específico comprado em uma IdaMercado
    """
    __tablename__ = 'itens_comprados'
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario_pago = db.Column(db.Float, nullable=False)

    ida_mercado_id = db.Column(db.Integer, db.ForeignKey('idas_mercado.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

    ida_mercado = db.relationship('IdaMercado', back_populates='itens')
    produto = db.relationship('Produto')

    def get_custo(self):
        return self.quantidade * self.preco_unitario_pago

```
