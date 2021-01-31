# Overview

NER service (BERT). The service listens RabbitMQ queue for input documents and processes it (NER).

Tested with Nvidia GTX 1080 Ti (11Gb) GPU (CUDA 10.0).

# Run

1. Install tensorflow-1.15.2 (we use gpu).

2. Install DeepPavlov

3. Install ner_ontonotes_bert

4. Download our archive with config file and model from https://yadi.sk/d/xqNEz91Ni8GhGA.
And unzip it into `ml` dir.
   
5. Run `src/main.py`.

# Dockerfile

It is not ready yet.

# Config

Our config file contains credentials (user/passwords), so we can't set it in git repo.

But the structure of our config file:

```buildoutcfg
{
  "rabbit_mq": {
    "host": "ip",
    "port": 5672,
    "user": "user",
    "password": "password",
    "listen_queue": "rvision-hack-queue",
    "to_exchange": ""
  },
  "database_url": "postgres://<user>:<password>###@<host>:<port>/<db>",
  "local_storage_path": "./storage"
}
```