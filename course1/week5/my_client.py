# Dmitry Shereshevskiy
# coursera, course 1, week 5
import time
import socket


class Client:
    """
    В класс инкапсулировано соединение с сервером, клиентский сокет и методы для получения и отправки метрик на сервер
    """

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metric_name, metric_value, timestamp=None):
        """

        :param metric_name:
        :param metric_value:
        :param timestamp:
        :return:
        """

        if timestamp is None:
            timestamp = str(int(time.time()))

        host = self.host
        port = self.port
        timeout = self.timeout

        with socket.create_connection((host, port), timeout) as sock:
            # set socket read timeout
            sock.settimeout(timeout)
            try:
                sock.send("put {} {} {}\n".format(metric_name, metric_value, timestamp).encode("utf8"))
                answer = sock.recv(1024)
                if answer == "error\nwrong command\n\n":
                    raise ClientError
            except socket.timeout:
                raise ClientError


    def get(self, metric_name):
        host = self.host
        port = self.port
        timeout = self.timeout
        get_data = {}

        def get_metric_tuple(string):
            metric_list = string.split(" ")
            return (metric_list[0], (int(metric_list[2]), float(metric_list[1])))

        with socket.create_connection((host, port), timeout) as sock:
            # set socket read timeout
            sock.settimeout(timeout)
            try:
                sock.send("get {}\n".format(metric_name).encode("utf8"))
                data = sock.recv(1024)
                get_list = data.decode("utf8").split("\n")[1:-2]
                for item in get_list:
                    metric_tuple = get_metric_tuple(item)
                    get_data.setdefault(metric_tuple[0], []).append(metric_tuple[1])
                for key in get_data:
                    get_data[key] = sorted(get_data[key], key=lambda x: x[0])
                return get_data
            except socket.timeout:
                raise ClientError


class ClientError(Exception):

    pass
