#!/usr/bin/env bash
celery multi stopwait storescraper --logfile=./%n.log --pidfile=./%n.pid
