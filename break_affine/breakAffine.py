#!/usr/bin/python
# -*- coding: utf-8 -*-

# Seguridad y Protección de Sistemas de Información (SPSI)
# Copyright (C) 2015 - MPVillafranca (mpvillafranca@correo.ugr.es)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Este programa descifra textos cifrados mediante cifrado modular.

import fractions
import itertools
from detectEnglish import *
from inferSpaces import *

# Variables globales
L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Abecedario inglés [Ordenado] -> 26
F = 'ETRINOA'  # Letras más frecuentes del abecedario inglés en orden


def lcm(a, b):
    """Función que calcula el minimo común divisor de a y b"""
    return abs(a * b) / fractions.gcd(a, b) if a and b else 0


def extended_gcd(a, b):
    """Adaptación del cálculo del máximo común multiplo para el cálculo del
    inverso modular"""
    lastremainder, remainder = abs(a), abs(b)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, \
            divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if a < 0 else 1), \
        lasty * (-1 if b < 0 else 1)


def mod_inv(a, m):
    """Función que calcula el inverso de a (mod m)"""
    g, x, y = extended_gcd(a, m)
    if g != 1:  # Si mcd(a,m)!=1
        return -1  # Error, no existe inverso
    else:
        return x % m  # Inverso


def system_solver(a1, a2, a3, b1, b2, b3, m):
    """Función que resuelve el sistema a1=a2*a+a3*b; b1=b2*a+b3*b, mod m"""
    lcmvar = lcm(a3, b3)  # Calculamos el mcm de los coedicientes de la b
    aux1 = lcmvar / a3
    aux2 = lcmvar / b3
    a1 = (a1 * aux1) % m  # Multiplicamos la primera ecuación
    a2 = (a2 * aux1) % m
    a3 = (a3 * aux1) % m
    b1 = (b1 * aux2) % m  # Multiplicamos la segunda ecuación
    b2 = (b2 * aux2) % m
    b3 = (b3 * aux2) % m

    c1 = b1 - a1  # Restamos a la segunda ecuación la primera
    c2 = b2 - a2

    # Calculamos el inverso del coeficiente de la a, mod m
    inv = mod_inv(c2, m)
    if inv != -1:
        a = (c1 * inv) % m  # Calculamos a
        b = (a1 - (a2 * a)) % m	 # Calculamos b
    else:
        a = -1
        b = -1

    return a, b


def char_count(text):
    """Función que cuenta la cantidad de cada letra de un texto y lo almacena
    en un array"""
    occurrences = []
    i = 0
    for c in L:  # Recorremos el abecedario letra a letra
        # Por cada letra comprobamos cuantas veces aparece en el texto
        s = text.count(c)
        occurrences.append(s)  # Almacenamos el valor en un array
    return occurrences


def decipher(text, a, b, m):
    """Función que descifra un texto cifrado con cifrado modular, pasándole
    los valores a y b de la clave y el número de letras del alfabeto"""
    detext = ""
    for c in text:
        if (ord(c) - 65) != -33:
            newc = (((ord(c) - 65) - b) * mod_inv(a, m)) % m  # Caracteres
        else:
            newc = ord(c) - 65  # Espacios
        newc = chr(newc + 65)
        detext = detext + newc
    return detext


def break_affine(text, m):
    """Función que rompe el cifrado modular de un texto"""
    occurrences = char_count(text)
    sorted_occurrences = []
    for i in sorted(occurrences, reverse=True):
        aux = occurrences.index(i)
        if aux != 0:
            occurrences[occurrences.index(i)] = -1
            auxlist = [str(unichr(aux + 65)), i]
            sorted_occurrences.append(auxlist)

    Ffix = [(ord(c) - 65) for c in F]

    auxsorted = []
    for i in range(len(sorted_occurrences)):
        auxsorted.append(sorted_occurrences[i][0])

    auxF = []
    for c in F:
        auxF.append(c)

    auxproduct = [auxsorted, auxF]
    for element in itertools.product(*auxproduct):
        for element2 in itertools.product(*auxproduct):
            if element[0] != element2[0] and element[1] != element2[1]:
                a1 = ord(element[0])-65
                a2 = ord(element[1])-65
                b1 = ord(element2[0])-65
                b2 = ord(element2[1])-65
                a, b = system_solver(a1, a2, 1, b1, b2, 1, m)
                if a != -1 and b != -1:
                    detext = decipher(text, a, b, m)
                    if isEnglish(detext):
                        print infer_spaces(detext.lower()) + " -> a=" + str(a) + \
                            ";b=" + str(b) + "; " + \
                            element[0] + "=" + element[1] + ";" + \
                            element2[0] + "=" + element2[1]


def main():
    text = 'WZDUY ZZYQB OTHTX ZDNZD KWQHI BYQBP WZDUY ZXZDSS'
    text = text.replace(" ", "")
    break_affine(text, len(L))


# Lanzamos la ejecución
if __name__ == "__main__":
    main()

