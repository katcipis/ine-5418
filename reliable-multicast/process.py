#!/usr/bin/env python

import socket, config
import sender, receiver, log
from message import MessageTransporter

if __name__ == '__main__':

    group = config.get_group()
    port = config.get_available_port(group)
    config.insert_proc_on_group (port)
    proc_id = config.get_uuid()
    ip = config.get_ip()
    transporter = MessageTransporter(ip, port) 

    log.log('process {proc_id} waiting for start at {ip}:{port}'.format(ip = ip, port=port, proc_id = proc_id))
    start_message = transporter.receive()
    log.log('{proc_id} received start message:[{msg}]'.format(proc_id = proc_id, msg = start_message))

    send_msgs_count = int(start_message['start'])

    #starting receiver thread
    received_msgs_count = (len(group) + 1) * send_msgs_count
    receiver = receiver.Receiver(proc_id, group, received_msgs_count, transporter)
    receiver.start()

    #starting sender thread
    sender = sender.Sender(proc_id, group, send_msgs_count, transporter)
    sender.start()

    receiver.join()
    log.log('process {proc_id} exited successfully'.format(proc_id = proc_id))
