"""Этап 3. MBT-тесты для RPC (вариант 4).

Сервер запускается в фоновом потоке ВНУТРИ pytest,
чтобы coverage видел его код.
"""
import socket
import threading
import time

from hypothesis import settings, HealthCheck
from hypothesis.stateful import (
    RuleBasedStateMachine, rule, run_state_machine_as_test
)
from hypothesis import strategies as st

from src.rpc_client import RPCClient
from src import rpc_server


HOST = "127.0.0.1"
PORT = 9091   


# Запуск сервера в фоновом потоке ВНУТРИ того же процесса 
def _start_server():
    rpc_server.HOST = HOST
    rpc_server.PORT = PORT
    t = threading.Thread(target=rpc_server.start, daemon=True)
    t.start()
    return t


def _wait_for_port(timeout: float = 5.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


# Запускаем сервер при импорте модуля (один раз)
_start_server()
if not _wait_for_port():
    raise RuntimeError(f"RPC-сервер не поднялся на {HOST}:{PORT}")


#Стратегии для генерации данных
safe_text = st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Cc"),
        blacklist_characters=("\x00",),
    ),
    min_size=0,
    max_size=5,
)

safe_text_nonempty = st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Cc"),
        blacklist_characters=("\x00",),
    ),
    min_size=1,
    max_size=5,
)


#State Machine
class RPCStateMachine(RuleBasedStateMachine):
    """Модель поведения клиента RPC."""

    def __init__(self):
        super().__init__()
        self.client = RPCClient(host=HOST, port=PORT)

    @rule(ts=st.integers(min_value=0, max_value=2_000_000_000),
          loc=safe_text, plat=safe_text, ua=safe_text)
    def create_member(self, ts, loc, plat, ua):
        resp = self.client.create_member(ts, loc, plat, ua)
        assert "uid" in resp
        assert int(resp["uid"]) > 0

    @rule()
    def get_members(self):
        resp = self.client.get_members()
        assert "result" in resp

    @rule(uid=st.integers(min_value=1, max_value=20))
    def get_member_by_id(self, uid):
        resp = self.client.get_member_by_id(uid)
        assert "result" in resp

    @rule(uid=st.integers(min_value=1, max_value=20), loc=safe_text_nonempty)
    def update_member(self, uid, loc):
        resp = self.client.update_member(uid, locale=loc)
        assert "ok" in resp

    @rule(ts=st.integers(min_value=0, max_value=2_000_000_000),
          inp=safe_text, mem=st.integers(min_value=1, max_value=20),
          status=safe_text)
    def create_assignment(self, ts, inp, mem, status):
        resp = self.client.create_assignment(ts, inp, mem, status)
        assert "uid" in resp

    @rule()
    def get_assignments(self):
        resp = self.client.get_assignments()
        assert "result" in resp

    @rule(uid=st.integers(min_value=1, max_value=20))
    def get_assignment_by_id(self, uid):
        resp = self.client.get_assignment_by_id(uid)
        assert "result" in resp

    @rule(uid=st.integers(min_value=1, max_value=20), status=safe_text_nonempty)
    def update_assignment(self, uid, status):
        resp = self.client.update_assignment(uid, status=status)
        assert "ok" in resp

    @rule(ts=st.integers(min_value=0, max_value=2_000_000_000),
          resp_text=safe_text, status=safe_text, exc=safe_text,
          asg=st.integers(min_value=1, max_value=20),
          ch=st.integers(min_value=0, max_value=1))
    def create_output(self, ts, resp_text, status, exc, asg, ch):
        resp = self.client.create_output(ts, resp_text, status, exc, asg, ch)
        assert "uid" in resp

    @rule()
    def get_outputs(self):
        resp = self.client.get_outputs()
        assert "result" in resp


def test_rpc_mbt():
    settings_obj = settings(
        max_examples=30,
        stateful_step_count=20,
        suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
        deadline=None,
    )
    run_state_machine_as_test(RPCStateMachine, settings=settings_obj)