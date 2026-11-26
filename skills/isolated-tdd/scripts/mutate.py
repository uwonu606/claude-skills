"""usage: mutate.py <impl.py> <test-path> [<test-path> ...]

impl.py 에 버그를 하나씩 넣어 테스트를 돌린다. 테스트가 잡지 못한(살아남은) 버그를 줄 번호와 바뀐 코드로 적는다.
"""
import ast
import os
import shutil
import subprocess
import sys
import tempfile

SWAP_CMP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}
SWAP_BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.FloorDiv: ast.Mult, ast.Mult: ast.FloorDiv}
SWAP_BOOL = {ast.And: ast.Or, ast.Or: ast.And}


def sites(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for i, op in enumerate(node.ops):
                if type(op) in SWAP_CMP:
                    yield node, ("cmp", i)
        elif isinstance(node, ast.BinOp) and type(node.op) in SWAP_BIN:
            yield node, ("bin", None)
        elif isinstance(node, ast.BoolOp) and type(node.op) in SWAP_BOOL:
            yield node, ("bool", None)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            yield node, ("not", None)
        elif isinstance(node, ast.Constant) and type(node.value) is int:
            yield node, ("int", None)
        elif isinstance(node, ast.Constant) and type(node.value) is bool:
            yield node, ("bool_const", None)
        elif isinstance(node, ast.keyword) and node.arg == "reverse":
            yield node, ("reverse", None)


def mutate(node, kind):
    k, i = kind
    if k == "cmp":
        node.ops[i] = SWAP_CMP[type(node.ops[i])]()
    elif k == "bin":
        node.op = SWAP_BIN[type(node.op)]()
    elif k == "bool":
        node.op = SWAP_BOOL[type(node.op)]()
    elif k == "not":
        return node.operand
    elif k == "int":
        node.value = node.value + 1
    elif k == "bool_const":
        node.value = not node.value
    elif k == "reverse":
        node.value = ast.UnaryOp(op=ast.Not(), operand=node.value)
    return node


def build(src, index):
    tree = ast.parse(src)
    targets = list(sites(tree))
    node, kind = targets[index]
    line = node.lineno
    before = ast.unparse(node)
    new = mutate(node, kind)
    if new is not node:
        for parent in ast.walk(tree):
            for field, value in ast.iter_fields(parent):
                if value is node:
                    setattr(parent, field, new)
                elif isinstance(value, list):
                    for j, v in enumerate(value):
                        if v is node:
                            value[j] = new
    after = ast.unparse(new)
    return ast.unparse(tree), line, before, after


def run_tests(workdir, tests):
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "--tb=no", "-p", "no:cacheprovider",
                            "-c", os.devnull, "--rootdir", workdir, *tests],
                           cwd=workdir, env=dict(os.environ, PYTHONPATH=workdir, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1"), capture_output=True, timeout=20)
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def main():
    impl, tests = os.path.abspath(sys.argv[1]), [os.path.abspath(t) for t in sys.argv[2:]]
    src = open(impl, encoding="utf-8").read()
    n = len(list(sites(ast.parse(src))))
    work = tempfile.mkdtemp()
    name = os.path.basename(impl)
    shutil.copy(impl, os.path.join(work, name))
    copied = []
    for k, t in enumerate(tests):
        dest = os.path.join(work, f"t{k}")
        os.makedirs(dest)
        files = [t] if os.path.isfile(t) else [os.path.join(t, f) for f in os.listdir(t)]
        for f in files:
            if os.path.basename(f).startswith("test_") and f.endswith(".py"):
                shutil.copy(f, dest)
        copied.append(dest)
    tests = copied
    if not run_tests(work, tests):
        print("원래 구현에서 테스트가 실패한다. 먼저 모두 통과시킨 뒤 돌린다.")
        sys.exit(2)
    survivors = []
    for i in range(n):
        code, line, before, after = build(src, i)
        if code == ast.unparse(ast.parse(src)):
            continue
        open(os.path.join(work, name), "w", encoding="utf-8").write(code)
        if run_tests(work, tests):
            survivors.append((line, before, after))
    shutil.rmtree(work, ignore_errors=True)
    print(f"버그 {n}개 중 테스트가 잡은 것 {n - len(survivors)}, 살아남은 것 {len(survivors)}")
    for line, before, after in survivors:
        print(f"- {name}:{line}  `{before}` -> `{after}`")


if __name__ == "__main__":
    main()
