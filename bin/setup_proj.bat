@set BIN_DIR=%~dp0
@set BASE_DIR=%BIN_DIR%..\
@set WIN_PROJ_DIR=%BASE_DIR%\client
@set ANDROID_PROJ_DIR=%BASE_DIR%\clientAndroid

@rem use only pc build

mkdir %ANDROID_PROJ_DIR%
mklink /j %ANDROID_PROJ_DIR%\Assets %WIN_PROJ_DIR%\Assets
mklink /j %ANDROID_PROJ_DIR%\ProjectSettings %WIN_PROJ_DIR%\ProjectSettings

