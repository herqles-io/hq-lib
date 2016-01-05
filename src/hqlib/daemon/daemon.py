#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from abc import abstractmethod, ABCMeta
import os
import signal
import threading
import sys


class Daemon(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.logger = logging.getLogger('hq.daemon')
        self.name = name

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.logger.error('Uncaught exception',
                          exc_info=(exc_type, exc_value, exc_traceback))

    def start(self):

        if not self.setup():
            sys.exit(1)

        self.configure_logging()

        sys.excepthook = self.handle_exception

        self.set_signals()

        self.logger.info('Started Daemon - HQ ' + self.name)

        with open(self.get_pid_file(), "w") as pid_file:
            pid_file.write(str(os.getpid()))

        if not self.run():
            self.stop()

        while True:
            threads = threading.enumerate()
            if len(threads) <= 1:
                break
            for t in list(threads):
                if t != threading.currentThread():
                    t.join(1)

        self.on_stop()

    @abstractmethod
    def get_log_path(self):
        return ""

    @abstractmethod
    def get_pid_file(self):
        return ""

    @abstractmethod
    def setup(self):
        return True

    @abstractmethod
    def run(self):
        return True

    @abstractmethod
    def on_shutdown(self, signum=None, frame=None):
        pass

    @abstractmethod
    def on_reload(self, signum=None, frame=None):
        pass

    def set_signals(self):

        signal.signal(signal.SIGUSR2, self.on_reload)
        signal.signal(signal.SIGINT, self.on_shutdown)
        signal.signal(signal.SIGTERM, self.on_shutdown)
        signal.signal(signal.SIGABRT, self.on_shutdown)

    def configure_logging(self):

        parent_logger = logging.getLogger('hq')
        parent_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        parent_logger.addHandler(ch)

        log_file_name = self.get_log_path() + '/' + self.name.lower() + '.log'
        fh = logging.handlers.WatchedFileHandler(log_file_name)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        parent_logger.addHandler(fh)

    def on_stop(self):
        self.logger.info('Stopped Daemon - HQ ' + self.name)
        os.remove(self.get_pid_file())

    def stop(self):
        os.kill(os.getpid(), signal.SIGTERM)
