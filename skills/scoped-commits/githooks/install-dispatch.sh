#!/usr/bin/env bash
# 전역 훅 디스패처를 설치한다. 기계당 한 번.
#
#   bash install-dispatch.sh            설치
#   bash install-dispatch.sh --uninstall  제거
#
# core.hooksPath 는 커밋으로 전파되지 않으므로, 저장소마다 켜는 대신
# 기계당 한 번 전역으로 걸고 디스패처가 저장소별 훅을 위임 실행한다.
set -euo pipefail

DEST="$HOME/.git-hooks"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dispatch"

# git 이 core.hooksPath 에서 찾는 훅 이름. 여기 없는 이름은 전역 설정
# 아래에서 아예 안 불린다 — 서버측 훅과 p4 훅까지 넉넉히 깐다.
#
# proc-receive 는 stdin/stdout 양방향 프로토콜 훅이라 읽어 뒀다 재생하면
# 협상이 깨진다. 그래서 dispatch 의 stdin 목록에서 빼 두었고, 빠져 있으면
# stdin 이 자식에게 그대로 물려져 프로토콜이 통한다. 실제 push 로 확인했다.
#
# 일부러 뺀 것:
#   fsmonitor-watchman  core.fsmonitor 설정값이 훅 경로를 직접 가리키므로
#                       core.hooksPath 를 타지 않는다. stdout 이 프로토콜
#                       응답이라 두 곳을 부르면 출력이 섞이기도 한다.
HOOKS=(
  applypatch-msg pre-applypatch post-applypatch
  pre-commit pre-merge-commit prepare-commit-msg commit-msg post-commit
  pre-rebase post-checkout post-merge pre-push
  pre-receive update proc-receive post-receive post-update
  post-rewrite pre-auto-gc sendemail-validate
  reference-transaction push-to-checkout post-index-change
  p4-changelist p4-prepare-changelist p4-post-changelist p4-pre-submit
)

if [ "${1:-}" = "--uninstall" ]; then
  current=$(git config --global core.hooksPath || true)
  if [ "$current" = "$DEST" ]; then
    git config --global --unset core.hooksPath
    echo "전역 core.hooksPath 해제됨"
  else
    echo "전역 core.hooksPath 가 이 디스패처를 가리키지 않음: ${current:-(없음)}"
  fi
  rm -rf "$DEST"
  echo "$DEST 제거됨"
  exit 0
fi

current=$(git config --global core.hooksPath || true)
if [ -n "$current" ] && [ "$current" != "$DEST" ]; then
  echo "전역 core.hooksPath 가 이미 다른 곳을 가리킵니다: $current" >&2
  echo "덮어쓰지 않았습니다. 직접 확인하고 합치십시오." >&2
  exit 1
fi

# 디스패처는 복사본으로 깐다. 심볼릭 링크로 저장소를 가리키면 갱신이 공짜지만,
# 저장소를 옮기거나 지우는 순간 전역 core.hooksPath 아래의 모든 저장소에서 커밋이
# 깨진다. 낡은 복사본보다 훨씬 나쁜 고장이라 복사를 고르고, 대신 갱신 여부를 알린다.
CORE="$DEST/lib/dispatch"

if [ ! -e "$CORE" ]; then
  state="설치"
elif cmp -s "$SRC" "$CORE"; then
  state="최신"
else
  state="갱신"
fi

mkdir -p "$DEST/lib"
# 기계 전체에 걸 자기 훅을 두는 자리. 훅 이름 자리를 직접 건드리지 않아도
# 되게 하려고 둔다 — 거기를 덮어쓰면 그 이름의 위임이 끊긴다.
mkdir -p "$DEST/user"
rm -f "$CORE"
cp "$SRC" "$CORE"
chmod +x "$CORE"

# 훅 이름마다 본체를 가리키는 작은 래퍼를 둔다. 심볼릭 링크가 아니라 실제
# 파일인 것이 요점이다 — 링크였을 때는 누가 `echo ... > ~/.git-hooks/pre-commit`
# 한 번만 해도 링크를 따라가 본체가 덮어써졌고, 그러면 훅 이름 전부가 그
# 스크립트를 실행하게 된다. 래퍼면 그 이름 하나만 바뀐다.
#
# 이름을 GIT_HOOK_NAME 으로 넘기는 이유는 dispatch 머리말에 적었다.
for h in "${HOOKS[@]}"; do
  rm -f "$DEST/$h"
  printf '#!/usr/bin/env bash\nGIT_HOOK_NAME=${0##*/} exec "%s" "$@"\n' "$CORE" > "$DEST/$h"
  chmod +x "$DEST/$h"
done

# 예전 방식으로 깔린 본체가 훅 이름 자리에 남아 있으면 치운다.
[ -e "$DEST/dispatch" ] && rm -f "$DEST/dispatch"

git config --global core.hooksPath "$DEST"

case "$state" in
  최신) echo "디스패처 이미 최신: $DEST (훅 ${#HOOKS[@]}종)" ;;
  갱신) echo "디스패처 갱신됨: $DEST (훅 ${#HOOKS[@]}종) — 낡은 복사본을 덮어썼습니다" ;;
  *)    echo "설치 완료: $DEST (훅 ${#HOOKS[@]}종)" ;;
esac
echo "전역 core.hooksPath = $(git config --global core.hooksPath)"
echo
echo "이제 저장소에 .githooks/<훅이름> 을 두면 클론 직후 설정 없이 걸립니다."
echo "저장소별 .git/hooks/ 도 함께 실행되므로 husky 같은 것이 죽지 않습니다."
echo "기계 전체에 걸 훅은 $DEST/user/<훅이름> 에 두십시오 — 저장소 훅과 함께 실행됩니다."
