from abc import ABC, abstractmethod

def input_int(msg, minimo=1):
    while True:
        try:
            v = int(input(msg))
            if v < minimo:
                raise ValueError
            return v
        except ValueError:
            print("Digite um valor inteiro válido.")

def input_float(msg, minimo=0):
    while True:
        try:
            v = float(input(msg))
            if v < minimo:
                raise ValueError
            return v
        except ValueError:
            print("Digite um valor numérico válido.")

def input_opcao(msg, opcoes):
    while True:
        v = input(msg)
        if v in opcoes:
            return v
        print("Opção inválida.")

class Gasto(ABC):
    def __init__(self, valor, dia, categoria):
        self.valor = valor
        self.dia = dia
        self.categoria = categoria

    @abstractmethod
    def eh_essencial(self):
        pass

class GastoEssencial(Gasto):
    def eh_essencial(self):
        return True

class GastoNaoEssencial(Gasto):
    def eh_essencial(self):
        return False

class Usuario:
    def __init__(self):
        self.salario = 0
        self.gastos = []
        self.caixinha = 0

    def definir_salario(self, valor):
        self.salario = valor + self.caixinha
        self.caixinha = 0

    def adicionar_gasto(self, gasto):
        self.gastos.append(gasto)

    def total_gastos(self):
        return sum(g.valor for g in self.gastos)

    def saldo(self):
        return self.salario - self.total_gastos()

    def limpar_gastos(self):
        self.gastos.clear()

class CicloFinanceiro:
    def __init__(self, duracao):
        self.duracao = duracao
        self.dia_atual = 1

    def avancar_dia(self):
        self.dia_atual += 1

    def acabou(self):
        return self.dia_atual > self.duracao

    def reiniciar(self):
        self.dia_atual = 1

class OrganizadorFinanceiro:
    CATEGORIAS = ["Alimentação", "Transporte", "Saúde", "Lazer", "Contas", "Casa"]

    def __init__(self, usuario, ciclo):
        self.usuario = usuario
        self.ciclo = ciclo

    def menu_operacao(self):
        print(f"\nDia {self.ciclo.dia_atual}")
        print("1 - Adicionar gasto")
        print("2 - Ver saldo")
        print("3 - Encerrar dia")

    def adicionar_gasto(self):
        print("\nCategoria:")
        for i, c in enumerate(self.CATEGORIAS, 1):
            print(f"{i} - {c}")
        cat = self.CATEGORIAS[input_int("Escolha: ", 1) - 1]

        tipo = input_opcao("Essencial (e) ou Não Essencial (n): ", ["e", "n"])
        valor = input_float("Valor do gasto: R$ ", 0.01)

        saldo = self.usuario.saldo()
        if valor > saldo:
            print(f"Aviso: este gasto gera dívida de R$ {valor - saldo:.2f}")

        gasto = GastoEssencial(valor, self.ciclo.dia_atual, cat) if tipo == "e" else GastoNaoEssencial(valor, self.ciclo.dia_atual, cat)
        self.usuario.adicionar_gasto(gasto)

    def executar(self):
        while not self.ciclo.acabou():
            self.menu_operacao()
            op = input_opcao("Opção: ", ["1", "2", "3"])

            if op == "1":
                self.adicionar_gasto()
            elif op == "2":
                print(f"Saldo atual: R$ {self.usuario.saldo():.2f}")
            else:
                self.ciclo.avancar_dia()

        self.relatorio_final()

    def relatorio_final(self):
        print("\n===== RELATÓRIO FINAL =====")

        total = self.usuario.total_gastos()
        if total == 0:
            print("Nenhum gasto registrado.")
            return
        
        ess_total = sum(g.valor for g in self.usuario.gastos if g.eh_essencial())
        nao_total = total - ess_total

        print(f"\nTotal gasto no ciclo: R$ {total:.2f}")
        print(f"Gastos Essenciais: R$ {ess_total:.2f} ({ess_total / total * 100:.1f}%)")
        print(f"Gastos Não Essenciais: R$ {nao_total:.2f} ({nao_total / total * 100:.1f}%)")


        for cat in self.CATEGORIAS:
            gastos_cat = [g for g in self.usuario.gastos if g.categoria == cat]
            if not gastos_cat:
                continue

            total_cat = sum(g.valor for g in gastos_cat)
            ess = sum(g.valor for g in gastos_cat if g.eh_essencial())
            nao = total_cat - ess

            print(f"\n{cat.upper()} — {total_cat / total * 100:.1f}% do total")
            print(f"  Essencial: R$ {ess:.2f} ({ess / total * 100:.1f}%)")
            print(f"  Não Essencial: R$ {nao:.2f} ({nao / total * 100:.1f}%)")

        saldo = self.usuario.saldo()
        print(f"\nSaldo final: R$ {saldo:.2f}")

        if saldo > 0:
            self.usuario.caixinha += saldo
            print(f"Guardado na caixinha: R$ {self.usuario.caixinha:.2f}")

def menu_inicial():
    print("\n===== MONEY WATCHER =====")
    print("1 - Iniciar ciclo")
    print("2 - Sair")
    return input_opcao("Opção: ", ["1", "2"])

def main():
    usuario = Usuario()

    while True:
        if menu_inicial() == "2":
            break

        duracao = input_int("Duração do ciclo (dias): ")
        salario = input_float("Salário (inteiro): R$ ", 0)

        ciclo = CicloFinanceiro(duracao)
        app = OrganizadorFinanceiro(usuario, ciclo)

        while True:
            usuario.limpar_gastos()
            ciclo.reiniciar()
            usuario.definir_salario(salario)
            
            app.executar()

            print("\n1 - Alterar informações do ciclo")
            print("2 - Começar proximo ciclo")
            print("3 - Sair")

            fim = input_opcao("Opção: ", ["1", "2", "3"])
            
            if fim == "1":
                break 
            elif fim == "2":
                continue
            else:
                return

if __name__ == "__main__":  
    main()