from flask_sqlalchemy import SQLAlchemy
import abc
from datetime import datetime

db = SQLAlchemy()

# --- Implementação do Padrão Composite ---
class ComponenteCusto(abc.ABC):
    """
    A interface 'Component' declara um método comum para folhas e compostos
    """
    @abc.abstractmethod
    def get_custo(self):
        pass

class Produto(db.Model):
    """
    Representa um produto cadastrado no sistema
    """
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.nome

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

