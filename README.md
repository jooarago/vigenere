vigenere.py é um programa em python3 que cifra e decifra seguindo a cifra de Vigenère, além de implementar um ataque a textos cifrados baseado em índices de coincidência, teste qui-quadrado e frequência média de caracteres -- na língua portuguesa e inglesa.
Há um PDF neste repositório que explica cada função de vigenere.py com um pouco mais de detalhes.

Para rodar o programa é necessário a instalação do unidecode. Em linux se instala usando o seguinte comando:

``` pip install unidecode ```

ou ainda:

``` pip3 install unidecode ```

O programa tem três modos: encrypt, decrypt e get_key. Para rodar o programa, utilize um dos seguintes formatos:

```
1. python3 vigenere.py encrypt [texto1] [senha1]
2. python3 vigenere.py decrypt [texto2] [senha2]
3. python3 vigenere.py get_key [filename] [senha3] [lingua]
```

texto1, senha1, texto2, senha2 e senha3 precisam ser strings somente com caracteres alfabéticos A-Z maiúsculos. em [lingua] pode-se colocar `PTBR` ou `EN`. 
Exemplo de comandos válidos:

```
1. python3 vigenere.py encrypt ATACARBASESUL LIMAO
2. python3 vigenere.py decrypt LBMCOCJMSSDCX LIMAO
3. python3 vigenere.py get_key ceia.txt LIMAO PTBR
```