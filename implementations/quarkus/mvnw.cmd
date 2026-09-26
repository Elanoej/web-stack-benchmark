@REM Licensed to the Apache Software Foundation (ASF) under one
@REM or more contributor license agreements.  See the NOTICE file
@REM distributed with this work for additional information
@REM regarding copyright ownership.  The ASF licenses this file
@REM to you under the Apache License, Version 2.0 (the
@REM "License"); you may not use this file except in compliance
@REM with the License.  You may obtain a copy of the License at
@REM
@REM   http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing,
@REM software distributed under the License is distributed on an
@REM "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
@REM KIND, either express or implied.  See the License for the
@REM specific language governing permissions and limitations
@REM under the License.
@REM
@REM ----------------------------------------------------------------------------
@REM Maven Start Up Batch script
@REM
@REM Required ENV vars:
@REM ------------------
@REM   JAVA_HOME - location of a JDK home dir
@REM
@REM Optional ENV vars
@REM -----------------
@REM   M2_HOME - location of a maven2 installation
@REM   MAVEN_OPTS - parameters passed to the Java VM when running Maven
@REM     e.g. to debug Maven itself, use
@REM       set MAVEN_OPTS=-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000
@REM   MAVEN_SKIP_RC - flag to disable loading of mavenrc files
@REM ----------------------------------------------------------------------------

@echo off

setlocal enabledelayedexpansion

set MAVEN_CMD_LINE_ARGS=%*

set MAVEN_SKIP_RC=%MAVEN_SKIP_RC%
if not "%MAVEN_SKIP_RC%"=="" goto skipRc

if exist "%HOME%\mavenrc_pre.bat" call "%HOME%\mavenrc_pre.bat"
if exist "%HOME%\mavenrc.bat" call "%HOME%\mavenrc.bat"
if exist "%HOME%\mavenrc_post.bat" call "%HOME%\mavenrc_post.bat"

:skipRc

set ERROR_CODE=0

REM ==== START VALIDATION ====

if not "%JAVA_HOME%"=="" goto validateJavaHome

for %%i in (java.exe) do set JAVA_HOME=%%~$PATH:i
if not "%JAVA_HOME%"=="" goto validateJavaHome

echo.
echo Error: JAVA_HOME not found in your environment. >>&2
echo Please set the JAVA_HOME variable in your environment to match the >>&2
echo location of your Java installation. >>&2
echo. >>&2
goto error

:validateJavaHome

if exist "%JAVA_HOME%\bin\java.exe" goto init
if exist "%JAVA_HOME%\jre\bin\java.exe" goto init
echo.
echo Error: JAVA_HOME is set to an invalid directory. >>&2
echo JAVA_HOME = "%JAVA_HOME%" >>&2
echo Please set the JAVA_HOME variable in your environment to match the >>&2
echo location of your Java installation. >>&2
echo. >>&2
goto error

:init

set MAVEN_HOME=%~dp0..

if not "%M2_HOME%"=="" goto validateM2Home
set M2_HOME=%MAVEN_HOME%
:validateM2Home

if exist "%M2_HOME%\bin\mvn" goto runMaven
if exist "%M2_HOME%\bin\mvn.bat" goto runMaven
if exist "%M2_HOME%\bin\mvn.cmd" goto runMaven

echo.
echo Error: M2_HOME is set to an invalid directory. >>&2
echo M2_HOME = "%M2_HOME%" >>&2
echo Please set the M2_HOME variable in your environment to match the >>&2
echo location of your Maven installation. >>&2
echo. >>&2
goto error

:runMaven

set CLASSPATH=%M2_HOME%\boot\plexus-classworlds-2.9.1.jar

"%JAVA_HOME%\bin\java" %MAVEN_OPTS% -classpath "%CLASSPATH%" "-Dclassworlds.conf=%M2_HOME%\bin\m2.conf" "-Dmaven.home=%M2_HOME%" "-Dmaven.multiModuleProjectDirectory=%CD%" org.codehaus.plexus.classworlds.launcher.Launcher %MAVEN_CMD_LINE_ARGS%

if errorlevel 1 goto error

goto end

:error
set ERROR_CODE=1

:end
endlocal & exit /b %ERROR_CODE%