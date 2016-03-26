Criptoanálisis de cifrados modulares
====

> Mariano Palomo Villafranca

## Descripción del problema
El [cifrado modular o afín](https://es.wikipedia.org/wiki/Cifrado_af%C3%ADn) es una variante del [cifrado de cesar](https://es.wikipedia.org/wiki/Cifrado_C%C3%A9sar), en el que introducimos dos parámetros en la llave, uno de ellos en forma multiplicativa.

Nuestro problema consiste en intentar obtener los parámetros de la llave (a y b) a partir, únicamente, del texto cifrado. Para ello, el **criptoanálisis** consistirá en analizar las distribuciones de la frecuencia de las letras y encontrar una asignación tentativa con la que resolver un sistema modular de 2 ecuaciones.

En primer lugar, tomaremos el texto cifrado y anotatemos la destribución de frecuencia dada en el mismo. A continuación, irémos realizando asignaciones en función de las frecuencias obtenidas y las letras más frecuentes en el idioma analizado (inglés en nuestro caso). Una vez hecho esto, intentaremos resolver el sistema y, si este tiene solución (a tiene inverso), trataremos de desencriptar el texto con los parámetros obtenidos y comprobar si se trata de un texto con sentido.

## Solución y descripción del algoritmo
Ya hemos indicado en qué consiste el problema, ahora veamos cómo abordarlo desde el punto de vista de la programación. Para ello, diseñaremos un algorimo: `break_affine(text, m)`, que recibe como entrada un texto cifrado y el número de letras que contiene el abecedario del idioma al que pertenece el texto llano. En nuestro caso, como se trata de inglés, `m` valdrá 26.

Para ello, nuestro algoritmo seguirá los siguientes pasos:

1. Contar las ocurrencias de caracteres en el texto y ordenarlas de mayor a menor
2. Realizar todas las posibles asignaciones de las letras obtenidas con las letras más comunes del idioma.
3. Resolver el sistema dado para cada asignación.
4. Si el sistema tiene solución, descifrar el texto con los valores de `a` y `b` obtenidos.
5. Comprobar si el texto obtenido tiene sentido en el idioma elegido (inglés) y, en caso de tenerlo, mostrar dicho texto y la pareja de valores `a` y `b`. Volver al paso 3 hasta que se hayan evaluado todas las asignaciones.

Para el diseño del algoritmo, se han programado funciones adifionales como son:

- `lcm(a, b)`: implementación del cálculo del mínimo común múltiplo de a y b.
- `extended_gcd`: adaptación del cálculo del máximo común divisor para el cálculo del inverso modular.
- `mod_inv(a, b)`: implementación del cáldulo del inverso modular.
- `system_solver(a1, a2, a3, b1, b2, b3, m)`: implementación de la resolución de sistemas modulares de 2 ecuaciones.
- `char_count(text)`: contador de caracteres del texto `text`.
- `decipher(text, a, b, m)`: implementación del desencriptado de un cifrado modular, conocidos `a` y `b`.

Además, hacemos uso de un par de funciones auxiliares, que nos facilitan la tarea de eliminar los espacios del texto y detectar textos en inglés: `infer_spaces(s)` y `isEnglish(message)`.

## Ejemplo de uso
El algoritmo ha sido programado en python y, a continuación se muestra un ejemplo de uso del programa. Tener en cuenta que el texto a descifrar debe introducirse en la función `main`  dentro de la variable `text`, que es de tipo String.

Para este ejemplo, la variable `text` contendrá el siguiente texto:

```python
text = 'WZDUY ZZYQB OTHTX ZDNZD KWQHI BYQBP WZDUY ZXZDSS'
```

Para ejecutar el programa, escribimos en la terminal:

```
$ python breakAffine.py
do unto others as you would have them do unto you xx -> a=5;b=7; Z=O;Y=T
do unto others as you would have them do unto you xx -> a=5;b=7; Z=O;U=N
do unto others as you would have them do unto you xx -> a=5;b=7; Z=O;O=R
do unto others as you would have them do unto you xx -> a=5;b=7; Y=T;Z=O
do unto others as you would have them do unto you xx -> a=5;b=7; Y=T;B=E
do unto others as you would have them do unto you xx -> a=5;b=7; Y=T;H=A
do unto others as you would have them do unto you xx -> a=5;b=7; B=E;Y=T
do unto others as you would have them do unto you xx -> a=5;b=7; B=E;U=N
do unto others as you would have them do unto you xx -> a=5;b=7; H=A;Y=T
do unto others as you would have them do unto you xx -> a=5;b=7; H=A;O=R
do unto others as you would have them do unto you xx -> a=5;b=7; U=N;Z=O
do unto others as you would have them do unto you xx -> a=5;b=7; U=N;B=E
do unto others as you would have them do unto you xx -> a=5;b=7; O=R;Z=O
do unto others as you would have them do unto you xx -> a=5;b=7; O=R;H=A
```
Como vemos, el programa reconoce, de entre todas las opciones, cual de ellas es un texto en inglés y lo representa ya descifrado y con sus respectivos espacios, además de indicar cuales son los a y b con los que se cifró y la asignación de letras a partir de las cuales se ha resulto el sistema.

## Código fuente

[Enlace al código fuente del programa](./break_affine/breakAffine.py).

## Referencias
1. Cifrado afín: [https://es.wikipedia.org/wiki/Cifrado_af%C3%ADn](https://es.wikipedia.org/wiki/Cifrado_af%C3%ADn)

2. Google-1000-English: [https://github.com/first20hours/google-10000-english/edit/master/google-10000-english.txt](https://github.com/first20hours/google-10000-english/edit/master/google-10000-english.txt)

3. Stackoverflow - How to split text without spaces into list of words: [http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words](http://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words)

4. Invent with Python - hacking: [http://inventwithpython.com/hacking](http://inventwithpython.com/hacking)

5. Asweigart - Codebreaker Repository: [https://github.com/asweigart/codebreaker](https://github.com/asweigart/codebreaker)

6. English dictionary: [http://invpy.com/dictionary.txt](http://invpy.com/dictionary.txt)
