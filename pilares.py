# Os pilares na árvore de arquivos: herança, polimorfismo, abstração e interface.
# Rodar no terminal: python3 pilares.py
#
# O Item da Aula 08 tinha um booleano (eh_pasta) e vários "if eh_pasta".
# Aqui ele vira três classes: Item (o geral), Pasta e Arquivo (os específicos),
# e quem usa a árvore deixa de perguntar "você é pasta?".
from abc import ABC, abstractmethod


# INTERFACE: contrato puro, sem estado e sem implementação.
# Quem assina promete saber dizer o próprio tamanho em bytes.
class Medivel(ABC):
    __slots__ = ()

    @abstractmethod
    def tamanho(self):
        pass


# ABSTRAÇÃO + HERANÇA: o que toda pasta e todo arquivo têm em comum.
# Não dá para criar um Item "solto": ele é só o recorte do essencial.
class Item(Medivel):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__validar_nome(nome)
        self.__nome = nome
        self.__pai = None

        if pai is not None:
            self.mover_para(pai)

    def __validar_nome(self, nome):
        if nome == "" or "/" in nome:
            raise ValueError("nome inválido: " + repr(nome))

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        self.__validar_nome(novo_nome)
        self.__nome = novo_nome

    @property
    def pai(self):
        return self.__pai

    def mover_para(self, destino):
        if destino is self.__pai:
            return

        destino._receber(self)          # cada tipo decide se aceita
        if self.__pai is not None:
            self.__pai._soltar(self)
        self.__pai = destino

    # PROTEGIDO: o gancho que as filhas sobrescrevem. Por padrão, recusa.
    def _receber(self, item):
        raise ValueError(self.__nome + " é um arquivo, não pode conter itens")

    def caminho(self):
        if self.__pai is None:
            return self.__nome
        return self.__pai.caminho() + "/" + self.__nome

    def profundidade(self):
        if self.__pai is None:
            return 0
        return self.__pai.profundidade() + 1

    @abstractmethod
    def mostrar(self):
        pass


class Arquivo(Item):
    __slots__ = ("__bytes",)

    def __init__(self, nome, tamanho_bytes, pai=None):
        if tamanho_bytes < 0:
            raise ValueError("tamanho não pode ser negativo")
        self.__bytes = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        return self.__bytes

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " (" + str(self.tamanho()) + " B)")


class Pasta(Item):
    __slots__ = ("__filhos",)

    def __init__(self, nome, pai=None):
        self.__filhos = []
        super().__init__(nome, pai)

    @property
    def filhos(self):
        return tuple(self.__filhos)

    # OVERRIDE do gancho protegido: a pasta aceita, desde que não crie um ciclo.
    def _receber(self, item):
        ancestral = self
        while ancestral is not None:
            if ancestral is item:
                raise ValueError("não dá para mover " + item.nome + " para dentro dela mesma")
            ancestral = ancestral.pai
        self.__filhos.append(item)

    def _soltar(self, item):
        self.__filhos.remove(item)

    # POLIMORFISMO: a pasta soma o que tem dentro; nenhum filho é perguntado
    # se é pasta ou arquivo, cada um responde do seu jeito.
    def tamanho(self):
        total = 0
        for filho in self.__filhos:
            total = total + filho.tamanho()
        return total

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + "/ (" + str(self.tamanho()) + " B)")
        for filho in self.__filhos:
            filho.mostrar()


# Outra classe que assina o contrato SEM ser da árvore: a Lixeira.
class Lixeira(Medivel):
    __slots__ = ("__descartados",)

    def __init__(self):
        self.__descartados = []

    def descartar(self, arquivo):
        self.__descartados.append(arquivo)

    def tamanho(self):
        total = 0
        for arquivo in self.__descartados:
            total = total + arquivo.tamanho()
        return total


# Quem usa o contrato não sabe (nem quer saber) quem está do outro lado.
def espaco_total(coisas):
    total = 0
    for coisa in coisas:
        total = total + coisa.tamanho()
    return total


def tentar(rotulo, acao):
    try:
        acao()
        print(rotulo, "-> passou (!)")
    except Exception as erro:
        print(rotulo, "->", type(erro).__name__ + ":", erro)


# Atalho: um item da árvore que aponta para outro item (o destino), igual ao
# atalho do Windows ou ao link simbólico do Linux. Nome, pai, mover_para e
# caminho já vêm do Item, então aqui só tem o que é do atalho.
class Atalho(Item):
    __slots__ = ("__destino",)

    # Valida o destino primeiro. Se der erro, o atalho nem entra na pasta.
    # É a mesma validação que o redirecionar usa.
    def __init__(self, nome, destino, pai=None):
        self.__validar_destino(destino, pai)
        self.__destino = destino
        super().__init__(nome, pai)

    # O destino não pode ser o próprio atalho nem uma pasta acima dele,
    # porque aí o atalho ia apontar pra onde ele mesmo está.
    # Sobe de pai em pai comparando cada um com o destino.
    def __validar_destino(self, destino, pai):
        if destino is self:
            raise ValueError("um atalho não pode apontar para ele mesmo")
        ancestral = pai
        while ancestral is not None:
            if ancestral is destino:
                raise ValueError("o atalho não pode apontar para " + destino.nome + ", que é uma pasta acima dele")
            ancestral = ancestral.pai

    # Só leitura. Como não tem setter, atalho.destino = x dá erro.
    @property
    def destino(self):
        return self.__destino

    # Único jeito de trocar o destino, sempre passando pela validação.
    def redirecionar(self, novo_destino):
        self.__validar_destino(novo_destino, self.pai)
        self.__destino = novo_destino

    # O atalho ocupa 1 byte, seja qual for o tamanho do destino.
    def tamanho(self):
        return 1

    # Mostra com o mesmo recuo dos outros itens e para onde o atalho aponta.
    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " -> " + self.destino.caminho())

    # Atalho não guarda itens. A mensagem do Item fala em "arquivo",
    # então troquei por uma que fala em "atalho".
    def _receber(self, item):
        raise ValueError(self.nome + " é um atalho, não pode conter itens")


disco = Pasta("C:")
usuarios = Pasta("Users", disco)
rodrigo = Pasta("RodrigoCampeoti", usuarios)
desktop = Pasta("Desktop", rodrigo)
faculdade = Pasta("Faculdade", rodrigo)
trabalhos = Pasta("Trabalhos", faculdade)
anotacoes = Arquivo("anotacoes.txt", 300, faculdade)
tf = Arquivo("tf-09.py", 2500, trabalhos)
boletim = Arquivo("boletim.pdf", 7000, trabalhos)

atalho_tf = Atalho("tf-09 - atalho", tf, desktop)
atalho_trabalhos = Atalho("Trabalhos - atalho", trabalhos, desktop)

disco.mostrar()

lixeira = Lixeira()
lixeira.descartar(Arquivo("versao_antiga.py", 1200))
print(espaco_total([anotacoes, desktop, lixeira]))   # 300 + 2 + 1200 = 1502

tentar("atalho_tf.destino = boletim", lambda: setattr(atalho_tf, "destino", boletim))
tentar("atalho para si mesmo", lambda: atalho_tf.redirecionar(atalho_tf))
tentar("atalho para a propria pasta", lambda: atalho_trabalhos.redirecionar(desktop))
