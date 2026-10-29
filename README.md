# tf-09 - Atalho na árvore de arquivos

- **Encapsulamento:** quem usa o Atalho só precisa saber ler `destino` e chamar `redirecionar()`; o atributo `__destino` e a validação que impede apontar para ele mesmo ou para uma pasta acima dele ficam escondidos dentro da classe.
- **Herança:** a interface é a mesma de qualquer Item (`nome`, `pai`, `mover_para()`, `caminho()`); a implementação disso tudo fica no Item, e o Atalho só herda, sem reescrever nada.
- **Polimorfismo:** quem chama só pede `tamanho()` e `mostrar()`, sem perguntar o tipo; por baixo o Atalho responde 1 byte e imprime `nome -> caminho do destino`, enquanto Pasta e Arquivo respondem do jeito deles.
- Por isso o `espaco_total()` aceita o Atalho sem mudar uma linha: ele conhece só o contrato do `Medivel`, não a implementação.
