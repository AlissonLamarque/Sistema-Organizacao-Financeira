from models import db, IdaMercado, ItemComprado, Produto

class MercadoFacade:
    def registrar_compra(self, nome_mercado, data, itens_data):
        if not itens_data:
            return None, "Nenhum item foi adicionado à compra."

        # 1. Cria o objeto principal 'IdaMercado'
        nova_ida_mercado = IdaMercado(
            nome_mercado=nome_mercado,
            data=data
        )

        valor_total_calculado = 0
        objetos_para_salvar = [nova_ida_mercado]

        # 2. Itera sobre os itens para criar os objetos 'ItemComprado'
        for item_info in itens_data:
            produto = Produto.query.get(item_info['produto'].id)
            if not produto:
                continue

            novo_item = ItemComprado(
                quantidade=item_info['quantidade'],
                preco_unitario_pago=item_info['preco_unitario'],
                produto=produto,
                ida_mercado=nova_ida_mercado # Associa à ida ao mercado
            )
            valor_total_calculado += novo_item.get_custo()
            objetos_para_salvar.append(novo_item)

        # 3. Atribui o valor total calculado
        nova_ida_mercado.valor_total = valor_total_calculado

        # 4. Salva tudo no banco de uma vez
        try:
            db.session.add_all(objetos_para_salvar)
            db.session.commit()
            return nova_ida_mercado, "Compra registrada com sucesso!"
        except Exception as e:
            db.session.rollback()
            return None, f"Erro ao registrar compra: {e}"
