#!/bin/zsh
# usage: tools/boot.sh <scenario> <wait> [cmds]  -> rebuild jar, boot 26.2 server, show mixin/crash lines
cd "${0:A:h}/.."
./build.sh build || exit 1
export JDK25=$(echo $HOME/.claude/jobs/be06d4c5/tmp/jdk25/jdk-*/Contents/Home)
T=$HOME/.claude/jobs/be06d4c5/tmp
python3 -I $T/rig/run26.py "$@" 2>&1 | tail -2
grep -vE "^\s+at |^\s+\.\.\." $T/rig/servers26/$1/console.log | grep -E "ERROR|Exception|Caused by|InvalidInjection|Done \(|FATAL" | cut -c1-330 | head -${LINES_MAX:-14}
