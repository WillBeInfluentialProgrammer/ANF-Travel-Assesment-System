:: GTAS Login Shortcut
:: Opens the local GTAS login page in the default browser
:: Shows default credentials for quick access during development
@echo off
echo ====================================
echo GTAS Login Page Access
echo ====================================
echo.
echo URL: http://localhost:8080/gtas/login
echo.
echo Default Login:
echo Username: admin
echo Password: password
echo.
echo Press any key to open in browser...
pause
start http://localhost:8080/gtas/login
