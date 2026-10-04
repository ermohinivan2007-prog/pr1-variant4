"""RPC-клиент. Имена методов совпадают с функциями модели данных."""
import socket
from src import rpc_protocol as proto


class RPCClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 9090):
        self.host = host
        self.port = port

    def _call(self, op: int, params: dict) -> dict:
        """Отправляет запрос и получает ответ."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            req = proto.encode_request(op, proto.dict_to_xml(params, "request"))
            s.sendall(req)

            # Читаем заголовок ответа — 6 байт
            header = b""
            while len(header) < 6:
                chunk = s.recv(6 - len(header))
                if not chunk:
                    break
                header += chunk
            size, _ = proto.decode_response_header(header)

            # Читаем тело ответа
            body = b""
            while len(body) < size:
                chunk = s.recv(size - len(body))
                if not chunk:
                    break
                body += chunk

            return proto.xml_to_dict(body.decode("utf-8"))

    #10 методов RPC 
    def create_member(self, timestamp: int, locale: str, platform: str, user_agent: str):
        return self._call(proto.OP_CREATE_MEMBER, {
            "timestamp": timestamp, "locale": locale,
            "platform": platform, "user_agent": user_agent})

    def get_members(self):
        return self._call(proto.OP_GET_MEMBERS, {})

    def get_member_by_id(self, uid: int):
        return self._call(proto.OP_GET_MEMBER_BY_ID, {"uid": uid})

    def update_member(self, uid: int, **kwargs):
        return self._call(proto.OP_UPDATE_MEMBER, {"uid": uid, **kwargs})

    def create_assignment(self, timestamp: int, input_data: str, member: int, status: str):
        return self._call(proto.OP_CREATE_ASSIGNMENT, {
            "timestamp": timestamp, "input": input_data,
            "member": member, "status": status})

    def get_assignments(self):
        return self._call(proto.OP_GET_ASSIGNMENTS, {})

    def get_assignment_by_id(self, uid: int):
        return self._call(proto.OP_GET_ASSIGNMENT_BY_ID, {"uid": uid})

    def update_assignment(self, uid: int, **kwargs):
        return self._call(proto.OP_UPDATE_ASSIGNMENT, {"uid": uid, **kwargs})

    def create_output(self, timestamp: int, response: str, status: str,
                      exception: str, assignment: int, cache_hit: int):
        return self._call(proto.OP_CREATE_OUTPUT, {
            "timestamp": timestamp, "response": response,
            "status": status, "exception": exception,
            "assignment": assignment, "cache_hit": cache_hit})

    def get_outputs(self):
        return self._call(proto.OP_GET_OUTPUTS, {})