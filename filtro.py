from flask import Flask, render_template, redirect, url_for, request
from instanciador import sujetos
from instanciador import evaluaciones
from datetime import datetime, date
from terminos import terminos
import string

pruebasdisponibles=['WATBA_R', 'Matrices', 'Vocabulario', 'ACE/ACE-R', 'IFS', 'Relatos', 'Relatos Neuropsi', 'RAVLT', 'Córdoba', 'Token', 'Fluencia Fonológica', 'Fluencia Semántica', 'Dígitos adelante', 'Dígitos adelante Neuropsi', 'Dígitos atrás', 'DigitosWAIS', 'Ordenamiento N-L', 'Aritmética', 'Hayling Test', 'ROCF', 'TMT', 'Dígitos-Símbolo', 'Búsqueda de Simbolos', 'STROOP', 'WCST', 'HOTEL', 'TAP', 'Faux Pas', 'Caras', 'EYES', 'VOICE', 'TASIT', 'WAIS']

class Filtro():
    def set_filtro(self,evaluacion,lista):
        self.evaluacion=evaluacion
        self.lista=lista
        self.output=[self.evaluacion.datosPersonales]
        for x in self.lista:
            self.output.append(self.evaluacion.pruebas[x])
        return self.output

filtro1=Filtro()
print(filtro1.set_filtro(evaluaciones["19191919-20-06-23"],["Matrices","RAVLT"]))


