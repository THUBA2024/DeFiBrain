# 激活虚拟环境
# . .\venv\Scripts\Activate.ps1

# 在后台运行 app.py，输出重定向到 burrow.log
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-u", "app.py" -RedirectStandardOutput "burrow.log" -RedirectStandardError "burrow.log"