#!/bin/zsh
# usage: ./build.sh [gradle task]   (default compileJava). Needs a Java 25 JDK: set JDK25 or edit below.
cd "${0:A:h}"
export JAVA_HOME=${JDK25:-$(echo $HOME/.claude/jobs/be06d4c5/tmp/jdk25/jdk-*/Contents/Home)}
export PATH=$JAVA_HOME/bin:$PATH
./gradlew --no-daemon -q ${1:-compileJava} > build.log 2>&1; rc=$?
echo "exit=$rc errors=$(grep -c 'error:' build.log) files=$(grep -E '^\s*/.*\.java:[0-9]+: error' build.log | sed -E 's|:[0-9]+: error.*||' | sort -u | wc -l)"
