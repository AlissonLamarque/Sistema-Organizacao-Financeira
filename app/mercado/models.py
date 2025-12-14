from app.extensions import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.nome

class IdaMercado(db.Model):
    __tablename__ = 'idas_mercado'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_mercado = db.Column(db.String(100), nullable=False) 
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

    itens = db.relationship('ItemComprado', back_populates='ida_mercado', cascade="all, delete-orphan")

    @property
    def total_calculado(self):
        return sum(item.total_item for item in self.itens)

class ItemComprado(db.Model):
    __tablename__ = 'itens_comprados'
    
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Float, nullable=False) 
    preco_unitario_pago = db.Column(db.Float, nullable=False)

    ida_mercado_id = db.Column(db.Integer, db.ForeignKey('idas_mercado.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

    ida_mercado = db.relationship('IdaMercado', back_populates='itens')
    produto = db.relationship('Produto')

    @property
    def total_item(self):
        return self.quantidade * self.preco_unitario_pago