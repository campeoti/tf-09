# tf-09 - Atalho na árvore de arquivos

Encapsulamento: quem usa o Atalho só precisa ler o `destino` e chamar `redirecionar()`. O atributo `__destino` e a checagem que impede apontar para ele mesmo ou para uma pasta acima dele ficam dentro da classe.

Herança: o Atalho usa `nome`, `pai`, `mover_para()` e `caminho()` como qualquer Item. Quem implementa isso é o Item, o Atalho só herda e não reescreve nada.

Polimorfismo: quem chama pede `tamanho()` ou `mostrar()` sem saber o tipo do item. O Atalho devolve 1 byte e imprime `nome -> caminho do destino`, enquanto Pasta e Arquivo fazem do jeito deles. Por isso o `espaco_total()` aceitou o Atalho sem eu mudar nada nele.
