# Remote control

Simple proof-of-concept client-server application to send commands through a
Python socket.

Tested with the Xbox Series X|S controller and a keyboard, on Linux machines.

## Install

Just clone the repo

```sh
$ git clone --recursive https://github.com/cathartyc/remote-control.git
$ cd remote-control

```
### Server

```sh
$ python3 remote_control-server.py [PORT]
```

### Client
```sh
$ python3 remote_control-client.py [HOST] [PORT]
```
(currenty tried only with IPs, not tested on domain names)

