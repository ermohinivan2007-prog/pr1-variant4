"""Протокол RPC по варианту 4 (Таблица 4 из методички).

ЗАПРОС:
    смещение 0, размер 5 байт — размер тела запроса
    смещение 5, размер 2 байта — код операции
    смещение 7, размер N байт  — тело в формате XML

ОТВЕТ:
    смещение 0, размер 4 байта — размер тела ответа
    смещение 4, размер 2 байта — код операции
    смещение 6, размер N байт  — тело в формате XML

Порядок байт: от старшего к младшему (Big-Endian).
"""
import xml.etree.ElementTree as ET


#Коды операций (10 штук для RPC)
OP_CREATE_MEMBER = 1
OP_GET_MEMBERS = 2
OP_GET_MEMBER_BY_ID = 3
OP_UPDATE_MEMBER = 4
OP_CREATE_ASSIGNMENT = 5
OP_GET_ASSIGNMENTS = 6
OP_GET_ASSIGNMENT_BY_ID = 7
OP_UPDATE_ASSIGNMENT = 8
OP_CREATE_OUTPUT = 9
OP_GET_OUTPUTS = 10


# Сериализация запроса
def encode_request(op_code: int, body_xml: str) -> bytes:
    body = body_xml.encode("utf-8")
    size_bytes = len(body).to_bytes(5, "big")   
    op_bytes = op_code.to_bytes(2, "big")        
    return size_bytes + op_bytes + body


def decode_request_header(header: bytes):
    """header — первые 7 байт запроса."""
    size = int.from_bytes(header[:5], "big")
    op = int.from_bytes(header[5:7], "big")
    return size, op


#Сериализация ответа
def encode_response(op_code: int, body_xml: str) -> bytes:
    body = body_xml.encode("utf-8")
    size_bytes = len(body).to_bytes(4, "big")    # 4 байта
    op_bytes = op_code.to_bytes(2, "big")         # 2 байта
    return size_bytes + op_bytes + body


def decode_response_header(header: bytes):
    """header — первые 6 байт ответа."""
    size = int.from_bytes(header[:4], "big")
    op = int.from_bytes(header[4:6], "big")
    return size, op


#XML утилиты 
def dict_to_xml(data: dict, root_name: str = "data") -> str:
    root = ET.Element(root_name)
    for k, v in data.items():
        el = ET.SubElement(root, k)
        # Убираем управляющие символы, недопустимые в XML 1.0
        text = "" if v is None else str(v)
        clean = "".join(
            ch for ch in text
            if ch == "\t" or ch == "\n" or ch == "\r" or ord(ch) >= 0x20
        )
        el.text = clean
    return ET.tostring(root, encoding="unicode")

def xml_to_dict(xml_str: str) -> dict:
    if not xml_str.strip():
        return {}
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}