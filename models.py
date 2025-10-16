from flask_sqlalchemy import SQLAlchemy
import abc
from datetime import datetime

# A instância do SQLAlchemy é inicializada aqui e configurada no system.py
db = SQLAlchemy()

# --- Implementação do Padrão Composite ---
# A classe ComponenteCusto serve como uma definição de interface, mas não precisa
# ser herdada diretamente pelos modelos do SQLAlchemy para evitar o conflito de metaclasse.
class ComponenteCusto(abc.ABC):
    """
    A interface 'Component' declara um método comum para folhas e compostos.
    """
    @abc.abstractmethod
    def get_custo(self):
        pass

class Produto(db.Model):
    """
    Representa um produto cadastrado no sistema.
    """
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.nome

class IdaMercado(db.Model):
    """
    Representa uma ida ao mercado. Esta é a nossa classe 'Composite',
    pois agrupa vários 'ItemComprado'.
    """
    __tablename__ = 'idas_mercado'
    id = db.Column(db.Integer, primary_key=True)
    nome_mercado = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

    itens = db.relationship('ItemComprado', back_populates='ida_mercado', cascade="all, delete-orphan")

    def get_custo(self):
        """
        O custo de um 'Composite' é a soma do custo de todos os seus filhos.
        Este método garante que a classe se comporte como um ComponenteCusto (Duck Typing).
        """
        return sum(item.get_custo() for item in self.itens)

class ItemComprado(db.Model):
    """
    Representa um item específico comprado em uma IdaMercado.
    Esta é a nossa classe 'Leaf' (folha).
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
        """
        O custo de uma 'Folha' é seu próprio valor calculado.
        Este método garante que a classe se comporte como um ComponenteCusto (Duck Typing).
        """
        return self.quantidade * self.preco_unitario_pago

