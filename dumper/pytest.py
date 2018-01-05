import subprocess
import requests
import json
import time
from django.views.decorators.csrf import csrf_exempt



# TODO:
# parallel,  max workers
# site with link list
# tcp dump rebuild nie sluchac z jakiegos tam plus arpy wyjebac

def get_state(delay):
    try:
        time.sleep(delay)
        r = requests.get('http://127.0.0.1:8000/dumper/server_state')
        json_data = json.loads(r.text)
        tcp_flag = json_data["tcp_flag"]
        filename = json_data["filename"]
        print("[Client] Flag Check: ", tcp_flag)
        return tcp_flag, filename

    except Exception:
        print("[Server Error] Can't connect with server")
        return None

if __name__ == '__main__':

    session_start_time = 0

    while True:
        tcp_flag, filename = get_state(5)
        if tcp_flag == True:
            file_path = 'user_data/' + filename
            dump_time_limit = 1000
            session_start_time = time.time()
            tcp_dump_command = "tcpdump -i any -s 0 -tttt -XX -w"
            command = "timeout {} {} {}.pcap".format(dump_time_limit, tcp_dump_command, file_path)
            p = subprocess.Popen(command, shell=True)
            while True:
                tcp_flag = get_state(1)[0]
                print("[Client] Dumping! ", tcp_flag)
                session_time = int(time.time() - session_start_time)
                if tcp_flag == False:
                    kill_tcpdump_command = "kill $(ps aux | grep " + filename + " | awk '{print $2}')"
                    subprocess.call(kill_tcpdump_command, shell=True)
                    print("[Client] Dumping is over")
                    break
                elif session_time > dump_time_limit:
                    requests.get('http://127.0.0.1:8000/dumper/dump_timeout')
                    print("session_time > dump_time_limit ", session_time)
                    break






