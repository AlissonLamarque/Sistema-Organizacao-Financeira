from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, FieldList, FormField, DateField
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Produto

def produto_query():
    # Função para popular o campo de seleção de produtos
    return Produto.query

class ItemForm(FlaskForm):
    """Sub-formulário para um item da compra."""
    produto = QuerySelectField('Produto', query_factory=produto_query, allow_blank=False, get_label='nome', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    preco_unitario = DecimalField('Preço Unitário', places=2, validators=[DataRequired(), NumberRange(min=0.01)])

class IdaMercadoForm(FlaskForm):
    """Formulário principal para registrar a ida ao mercado."""
    nome_mercado = StringField('Nome do Mercado', validators=[DataRequired()])
    data = DateField('Data da Compra', format='%Y-%m-%d', validators=[DataRequired()])
    itens = FieldList(FormField(ItemForm), min_entries=1, label='Itens')
    submit = SubmitField('Registrar Compra')
