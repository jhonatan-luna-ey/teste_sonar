```python
import easyocr
import os
import re
from datetime import datetime
from PIL import Image, ImageDraw
import cv2 as cv

path_image = "C://Users//NZ366ES//OneDrive - EY//Documents//Projeto Interno - Ciencia de Dados//EasyOCR//pictures//cnh"

PATTERN_NOME = r"(?im)NOME\s*(?P<nome>.+)\s*DOC."
PATTERN_RG = r"(?im)EMISSOR[A-Z\s]*(?P<rg>\d{6,9})\s*(?P<org_emissor>\w+)\s*CPF"
PATTERN_CPF = r"(?im)CPF.+(?P<cpf>\d{3}[\s|.]*\d{3}[\s|.]*\d{3}[\s|-]*\d{2}).+FILIA"
PATTERN_DTNASCIMENTO = r"(?im)(?P<dt_nascimento>\d{2}/\d{2}/\d{4})\s?FILIAÇÃO"
PATTERN_FILIACAO = r"(?im)FILIAÇÃO(?P<filiacao>.+)\s?PERMISSÃO"
PATTERN_NUM_REGISTRO = r"(?im)(?P<no_registro>\d{11})"
PATTERN_CAT_HAB = r"(?im)CAT. HAB..+(?P<categoria>\bAB\b|\bA\b|\bB\b|\bC\b|\bD\b|\bE\b)\s+"
PATTERN_VALIDADE_1A_HABILITACAO = r"(?im)VALIDADE[A-Z0-9ÇÃª\s]+(?P<validade>\d{2}/\d{2}/\d{4})\s?" \
                                  r"(?P<primeirahabilitacao>\d{2}/\d{2}/\d{4})"
PATTERN_STARTS_WITH_VALIDADE = r"(?im)VALIDADE.+"

dict_campos = {}

def draw_boxes(image, bounds, color='red', width=5):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image

def exporta_cnh_texto(texto, nome_arquivo):
    with open(f'{nome_arquivo}.txt', 'w', encoding="ISO-8859-1") as f:
        f.writelines(texto)

def ajeitar_cpf(cpf):
    PATTERN_CPF_GROUPED = r"(?im)CPF.+(?P<PtUm>\d{3})[\s|.]*(?P<PtDois>\d{3})[\s|.]*(?P<PtTres>\d{3})[\s|-]*(?P<digitoVerif>\d{2}).+FILIA"
    PATTERN_CPF_FIXED = r"\g<PtUm>.\g<PtDois>.\g<PtTres>-\g<digitoVerif>"
    return re.sub(PATTERN_CPF_GROUPED, PATTERN_CPF_FIXED, cpf)

def extrair_rg_org_emissor(match):
    for key, value in match.groupdict().items():
        print(f"{key}:{value}")
        dict_campos[key] = value

def extrair_validade_1a_habilitacao(value):
    pattern_data = r"(?im)\d{2}/\d{2}/\d{4}"
    lista_datas = []

    try:
        match_iter = re.finditer(pattern_data, value)
        for match