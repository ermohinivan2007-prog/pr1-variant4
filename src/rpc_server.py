"""RPC-сервер на TCP. Вариант 4.

Слушает порт 9090. Принимает запросы, парсит их по протоколу,
вызывает соответствующую функцию модели, отправляет ответ.
Все запросы и ответы пишутся в файл journal.log.
"""
import socket
import threading
from src import data_model
from src import rpc_protocol as proto

HOST = "127.0.0.1"
PORT = 9090
JOURNAL = "journal.log"


def log(text: str):
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def handle_request(op: int, params: dict) -> dict:
    """Диспетчер: вызывает функцию модели по коду операции."""
    if op == proto.OP_CREATE_MEMBER:
        uid = data_model.create_member(
            int(params["timestamp"]),
            params.get("locale", ""),
            params.get("platform", ""),
            params.get("user_agent", ""))
        return {"uid": uid}

    if op == proto.OP_GET_MEMBERS:
        return {"result": repr(data_model.get_members())}

    if op == proto.OP_GET_MEMBER_BY_ID:
        return {"result": repr(data_model.get_member_by_id(int(params["uid"])))}

    if op == proto.OP_UPDATE_MEMBER:
        ok = data_model.update_member(
            int(params["uid"]),
            int(params["timestamp"]) if "timestamp" in params else None,
            params.get("locale"),
            params.get("platform"),
            params.get("user_agent"))
        return {"ok": ok}

    if op == proto.OP_CREATE_ASSIGNMENT:
        uid = data_model.create_assignment(
            int(params["timestamp"]),
            params.get("input", ""),
            int(params["member"]),
            params.get("status", ""))
        return {"uid": uid}

    if op == proto.OP_GET_ASSIGNMENTS:
        return {"result": repr(data_model.get_assignments())}

    if op == proto.OP_GET_ASSIGNMENT_BY_ID:
        return {"result": repr(data_model.get_assignment_by_id(int(params["uid"])))}

    if op == proto.OP_UPDATE_ASSIGNMENT:
        ok = data_model.update_assignment(
            int(params["uid"]),
            int(params["timestamp"]) if "timestamp" in params else None,
            params.get("input"),
            int(params["member"]) if "member" in params else None,
            params.get("status"))
        return {"ok": ok}

    if op == proto.OP_CREATE_OUTPUT:
        uid = data_model.create_output(
            int(params["timestamp"]),
            params.get("response", ""),
            params.get("status", ""),
            params.get("exception", ""),
            int(params["assignment"]),
            int(params["cache_hit"]))
        return {"uid": uid}

    if op == proto.OP_GET_OUTPUTS:
        return {"result": repr(data_model.get_outputs())}

    raise ValueError(f"Unknown op code: {op}")


def handle_client(conn: socket.socket):
    try:
        # Читаем заголовок запроса — 7 байт
        header = b""
        while len(header) < 7:
            chunk = conn.recv(7 - len(header))
            if not chunk:
                return
            header += chunk

        size, op = proto.decode_request_header(header)

        # Читаем тело запроса
        body = b""
        while len(body) < size:
            chunk = conn.recv(size - len(body))
            if not chunk:
                break
            body += chunk

        params = proto.xml_to_dict(body.decode("utf-8"))
        log(f"[REQUEST] op={op} params={params}")

        try:
            result = handle_request(op, params)
        except Exception as e:
            result = {"error": str(e)}

        # Отправляем ответ
        response_xml = proto.dict_to_xml(result, root_name="response")
        response_bytes = proto.encode_response(op, response_xml)
        conn.sendall(response_bytes)
        log(f"[RESPONSE] op={op} body={response_xml}")
    finally:
        conn.close()


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"RPC server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start()