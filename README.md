# RoadWeaver 26.2 port scaffold

Fabric-only, single module. Sources = upstream branch `1.21.1-Architectury` (2.3.1, commit 118e767,
MIT) with `common/` + `fabric/` merged into src/main. Loom 1.18 + Gradle 9.7.1, needs a Java 25 JDK.

    export JAVA_HOME=<jdk25>; ./gradlew --no-daemon compileJava
libs/ holds Modrinth jars (not saved): cloth-config 26.2.155, architectury-api 21.1.12, modmenu 20.0.3.
Fetch them with ../fetch.py <project> 26.2 <version> libs.

Status 2026-10-09: does not compile. 1,010 errors in 140 of 382 files (first pass, real count is higher).
