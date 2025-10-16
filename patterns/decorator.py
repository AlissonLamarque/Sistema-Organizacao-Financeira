class Relatorio:
    """
    O 'Component' define a interface para objetos que podem ter
    responsabilidades adicionadas a eles.
    """
    def gerar(self, ida_mercado):
        return ""

class RelatorioSimples(Relatorio):
    """
    O 'ConcreteComponent' é o objeto inicial ao qual funcionalidades
    serão adicionadas.
    """
    def gerar(self, ida_mercado):
        output = "--- Itens da Compra ---\n"
        for item in ida_mercado.itens:
            output += f"- {item.produto.nome}: {item.quantidade} x R$ {item.preco_unitario_pago:.2f} = R$ {item.get_custo():.2f}\n"
        return output

class DecoradorRelatorio(Relatorio):
    """
    O 'Decorator' base segue a mesma interface que o Component.
    Ele mantém uma referência ao objeto Component que ele envolve.
    """
    _relatorio: Relatorio = None

    def __init__(self, relatorio: Relatorio) -> None:
        self._relatorio = relatorio

    def gerar(self, ida_mercado):
        return self._relatorio.gerar(ida_mercado)

class RelatorioComCabecalho(DecoradorRelatorio):
    """
    'ConcreteDecorators' adicionam funcionalidades. Eles executam o método
    do objeto envolvido e adicionam seu próprio comportamento.
    """
    def gerar(self, ida_mercado):
        cabecalho = f"Compra em: {ida_mercado.nome_mercado}\nData: {ida_mercado.data.strftime('%d/%m/%Y')}\n\n"
        conteudo_original = super().gerar(ida_mercado)
        return cabecalho + conteudo_original

class RelatorioComRodapeTotal(DecoradorRelatorio):
    """
    Outro 'ConcreteDecorator' que adiciona o valor total no final.
    """
    def gerar(self, ida_mercado):
        conteudo_original = super().gerar(ida_mercado)
        total = ida_mercado.get_custo() # Usando o método do padrão Composite!
        rodape = f"\n--- VALOR TOTAL: R$ {total:.2f} ---"
        return conteudo_original + rodape
