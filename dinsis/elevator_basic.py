"""
This program is a worker responsible for allways running and taking periodically requests from a flask server
It simulates an elevator going up and down
The elevator can open and close doors, wait for requests, update its status and remove entries from a queue
Moving between floors takes 3 seconds and stoping on a floor takes 5 seconds
"""

import time
import os


curr_floor = 0
direction = "up"
queue_down = []
queue_up = []
folder = "./queue/"
extention = ".q"


# get requests from server queue folder, each file is an entry to the queue
# the files also allow the server to know if a button is locked or not
def process_requests(directory, ext):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                add_to_queue(int(file.strip(ext)))


# add entrants to queue by comparing current building and direction to queue
def add_to_queue(floor):
    global curr_floor, queue_down, queue_up
    if curr_floor > floor:
        if floor not in queue_down:
            queue_down.append(floor)
        else:
            return "already exists in queue, button locked"
    else:
        if floor not in queue_up:
            queue_up.append(floor)
        else:
            return "already exists in queue, button locked"

def seek(floor):
    global direction, queue_up, queue_down
    #scan algorithm
    if direction == "up":
        if len(queue_up) != 0:
            if floor in queue_up:
                # elevator is here
                stop_elevator(floor)
                # remove from queue
                queue_up.remove(floor)
            # are there any more requests above me?
            if max(queue_up, default=curr_floor) > floor:
                return 1
            # no more requests above so direction should be down
            else:
                direction = "down"
                return 99
        else:
            # its not up so it must be down
            direction = "down"
            return 99
    elif direction == "down":
        if len(queue_down) != 0:
            if floor in queue_down:
                # elevator is here
                stop_elevator(floor)
                # remove from queue
                queue_down.remove(floor)
            # are there any more requests bellow me?
            if min(queue_down, default=curr_floor) < floor:
                return -1
            # no more requests bellow so direction should be up
            else:
                direction = "up"
                return 99
        else:
            # its not down so it must be up
            direction = "up"
            return 99

def stop_elevator(floor):
    global folder, extention
    # remove file from server queue
    if os.path.exists(folder+str(floor)+extention):
        os.remove(folder+str(floor)+extention)
    else:
        return
    # idle door opening time
    log("Opening doors")
    time.sleep(5)
    log("Closing doors")

# saves the latest log message on a file in the server so the server can know the current elevator status
# it also adds a line with the current floor for elvator animation display purposes
def log(message):
    global curr_floor, direction
    floor = str(curr_floor)+"\n"
    try:
        with open("./queue/elevator.log", "w") as fo:
            fo.write(floor)
            fo.write(message)
    except IOError:
        print("log file problem: %s" % IOError)

if __name__ == '__main__':
    running = True
    while running:
        log("elevator is on floor : %s" % curr_floor)
        # read requests from server queue file
        process_requests(folder, extention)
        # evaluate max queue and direction and check respective queue to see if any entrant matches current floor
        # if an entrant matches the current floor stop the elevator for x seconds and remove them from the list
        increment = seek(curr_floor)
        # increment position
        # bugfix: python evaluates 0 as none for some weird reason so a 99 code was implemented
        # not pretty or pythonic but works
        if increment != 99:
            curr_floor += increment
            log("moving %s 1 floor" % direction)
        else:
            log("elevator is waiting on floor %s" % curr_floor)
        # time that the elevator takes to travel
        time.sleep(3)
