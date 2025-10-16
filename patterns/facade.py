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
