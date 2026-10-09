# RoadWeaver (26.2 server-only port)

Unofficial, server-only port of [RoadWeaver](https://github.com/shiroha-233/RoadWeaver) 2.3.1 to
Minecraft 26.2 for private testing. All credit for the mod goes to its upstream author.
MIT licensed, see LICENSE and NOTICE. If upstream ships a 26.x build, use that instead.

# RoadWeaver 26.2 port scaffold

Fabric-only, single module. Sources = upstream branch `1.21.1-Architectury` (2.3.1, commit 118e767,
MIT) with `common/` + `fabric/` merged into src/main. Loom 1.18 + Gradle 9.7.1, needs a Java 25 JDK.

    export JAVA_HOME=<jdk25>; ./gradlew --no-daemon compileJava
libs/ holds Modrinth jars (not saved): cloth-config 26.2.155, architectury-api 21.1.12, modmenu 20.0.3.
Fetch them with ../fetch.py <project> 26.2 <version> libs.

Status 2026-10-09: does not compile. 1,010 errors in 140 of 382 files (first pass, real count is higher).

## Update
Server-only port compiles and boots on 26.2. See ../FINDINGS.md. Helpers: tools/fix.py (error-driven
renames), tools/boot.sh (rebuild + boot a 26.2 server, needs rig/run26.py and jars26 in the job tmp dir,
paths are hardcoded in boot.sh and need editing on another machine).
