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

# git 이 부르는 클라이언트 사이드 훅 이름. 여기 없는 이름은 전역 설정
# 아래에서 아예 안 불린다 — 그래서 넉넉히 깐다.
HOOKS=(
  applypatch-msg pre-applypatch post-applypatch
  pre-commit pre-merge-commit prepare-commit-msg commit-msg post-commit
  pre-rebase post-checkout post-merge pre-push
  post-rewrite pre-auto-gc sendemail-validate
  reference-transaction push-to-checkout post-index-change
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

mkdir -p "$DEST"
cp "$SRC" "$DEST/dispatch"
chmod +x "$DEST/dispatch"
for h in "${HOOKS[@]}"; do
  ln -sf dispatch "$DEST/$h"
done
git config --global core.hooksPath "$DEST"

echo "설치 완료: $DEST (훅 ${#HOOKS[@]}종)"
echo "전역 core.hooksPath = $(git config --global core.hooksPath)"
echo
echo "이제 저장소에 .githooks/<훅이름> 을 두면 클론 직후 설정 없이 걸립니다."
echo "저장소별 .git/hooks/ 도 함께 실행되므로 husky 같은 것이 죽지 않습니다."
