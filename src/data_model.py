#Этап 1. Вариант 4.
import time

members = []       
assignments = []   
outputs = []       

_next_member_uid = 1
_next_assignment_uid = 1
_next_output_uid = 1


#Задание 2
def create_member(timestamp, locale, platform, user_agent):
    global _next_member_uid
    uid = _next_member_uid
    _next_member_uid += 1
    members.append([uid, timestamp, locale, platform, user_agent])
    return uid

def get_members():
    return members

def get_member_by_id(uid):
    for m in members:
        if m[0] == uid:
            return m
    return None

def update_member(uid, timestamp=None, locale=None, platform=None, user_agent=None):
    m = get_member_by_id(uid)
    if m is None:
        return False
    if timestamp is not None:  m[1] = timestamp
    if locale is not None:     m[2] = locale
    if platform is not None:   m[3] = platform
    if user_agent is not None: m[4] = user_agent
    return True


def create_assignment(timestamp, input_data, member, status):
    global _next_assignment_uid
    uid = _next_assignment_uid
    _next_assignment_uid += 1
    assignments.append([uid, timestamp, input_data, member, status])
    return uid

def get_assignments():
    return assignments

def get_assignment_by_id(uid):
    for a in assignments:
        if a[0] == uid:
            return a
    return None

def update_assignment(uid, timestamp=None, input_data=None, member=None, status=None):
    a = get_assignment_by_id(uid)
    if a is None:
        return False
    if timestamp is not None:  a[1] = timestamp
    if input_data is not None: a[2] = input_data
    if member is not None:     a[3] = member
    if status is not None:     a[4] = status
    return True


def create_output(timestamp, response, status, exception, assignment, cache_hit):
    global _next_output_uid
    uid = _next_output_uid
    _next_output_uid += 1
    outputs.append([uid, timestamp, response, status, exception, assignment, cache_hit])
    return uid

def get_outputs():
    return outputs

def get_output_by_id(uid):
    for o in outputs:
        if o[0] == uid:
            return o
    return None

def update_output(uid, timestamp=None, response=None, status=None,
                  exception=None, assignment=None, cache_hit=None):
    o = get_output_by_id(uid)
    if o is None:
        return False
    if timestamp is not None:  o[1] = timestamp
    if response is not None:   o[2] = response
    if status is not None:     o[3] = status
    if exception is not None:  o[4] = exception
    if assignment is not None: o[5] = assignment
    if cache_hit is not None:  o[6] = cache_hit
    return True


#Задание 3

def select_recent_assignments():
    now = int(time.time())
    threshold = now - 7 * 60
    result = []
    for a in assignments:
        if a[1] > threshold:
            m = get_member_by_id(a[3])
            if m is not None:
                result.append([a[2], m[4]])  
    return result


#Задание 4

def repl():
    while True:
        user_command = input()
        match user_command:

            case 'create_member':
                print(create_member(int(input()), input(), input(), input()))
            case 'get_members':
                print(get_members())
            case 'get_member_by_id':
                print(get_member_by_id(int(input())))
            case 'update_member':
                uid = int(input())
                ts, loc, plat, ua = input(), input(), input(), input()
                kw = {}
                if ts:   kw['timestamp'] = int(ts)
                if loc:  kw['locale'] = loc
                if plat: kw['platform'] = plat
                if ua:   kw['user_agent'] = ua
                print(update_member(uid, **kw))

            case 'create_assignment':
                print(create_assignment(int(input()), input(), int(input()), input()))
            case 'get_assignments':
                print(get_assignments())
            case 'get_assignment_by_id':
                print(get_assignment_by_id(int(input())))
            case 'update_assignment':
                uid = int(input())
                ts, inp, mem, st = input(), input(), input(), input()
                kw = {}
                if ts:  kw['timestamp'] = int(ts)
                if inp: kw['input_data'] = inp
                if mem: kw['member'] = int(mem)
                if st:  kw['status'] = st
                print(update_assignment(uid, **kw))

            case 'create_output':
                ts, resp, st, exc = int(input()), input(), input(), input()
                asg, ch = int(input()), int(input())
                print(create_output(ts, resp, st, exc, asg, ch))
            case 'get_outputs':
                print(get_outputs())
            case 'get_output_by_id':
                print(get_output_by_id(int(input())))
            case 'update_output':
                uid = int(input())
                ts, resp, st, exc, asg, ch = input(), input(), input(), input(), input(), input()
                kw = {}
                if ts:   kw['timestamp'] = int(ts)
                if resp: kw['response'] = resp
                if st:   kw['status'] = st
                if exc:  kw['exception'] = exc
                if asg:  kw['assignment'] = int(asg)
                if ch:   kw['cache_hit'] = int(ch)
                print(update_output(uid, **kw))

            case 'select_recent_assignments':
                print(select_recent_assignments())

            case 'exit':
                break
            case _:
                print("Unknown command")


repl()