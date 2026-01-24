python3 Server/initialiseDatabase.py

SERVER_SCRIPT = Documents/\"Personal Files\"/FastPass/Server/fpServer.py

currDir = $(pwd)

osascript <<EOF
tell application "Terminal"
    activate
    do script "cd $currDir" &
    do script "python3 Server/fpServer.py \"Pirates\" 100"
end tell
EOF