dir_path="$(dirname ${BASH_SOURCE[0]})";

for script in $dir_path/discordbots/*; do nohup python3 $script/main.py > ~/logs/bots.txt & done;

for module in $dir_path/modules/*; do pip3 install -e $module/; done

nohup python3 $dir_path/email_server.py > logs/email_server.txt 2>&1 &