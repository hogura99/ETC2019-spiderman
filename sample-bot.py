#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import _thread

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="SPIDERMAN"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=2
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

list_lock = False
msg_list = []

def lock_list():
    global list_lock
    while list_lock:
        pass
    list_lock = True

def unlock_list():
    global list_lock
    list_lock = False

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
<<<<<<< HEAD
    return json.loads(exchange.readline())

# ~~~~~============== STRATEGY ===============~~~~~
def parseBook(book):
    maxBuyer = [0, 0]
    minSeller = [10000000, 0]
    if book.symbol == "BOND":
        for buyer in book.buy:
            if buyer[0] > maxBuyer[0]:
                maxBuyer = buyer
        for seller in book.sell:
            if seller[0] < minSeller[0]:
                minSeller = seller
    return {
        maxBuyer: maxBuyer,
        minSeller: minSeller
    }

=======
    msg = json.loads(exchange.readline())
    lock_list()
    msg_list.append(msg)
    unlock_list()
>>>>>>> 78f98904660a2cc96d83d859d0380e49c06bcb35

# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    _thread.start_new_thread(read_from_exchange, (exchange))
    #current_msg.append(read_from_exchange(exhange))
    order_id = 0
    while True:
        # hello_from_exchange = read_from_exchange(exchange)
        cmd = input()
        if (cmd == 's'):
            break
        order_id += 1
        lock_list()
        print(msg_list)
        unlock_list()

if __name__ == "__main__":
    main()
