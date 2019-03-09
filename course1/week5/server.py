import asyncio


class ClientServerProtocol(asyncio.Protocol):
    store = []
    # def __init__(self):
    #     super().__init__()
    #     self.store = []

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, message):
        """
        Process of data from client: store to the structure of data and forming of the answer to the client
        (will be returned)
        :param message: str
        command from client
        :return: str
        answer for client
        """
        command = message.split(" ")[0]
        if command == "put":
            _, key, value, timestamp= message[:-1].split(" ")
            self.store.append((key, timestamp, value))
            answer = "ok\n\n"
        elif command == "get":
            _, key = message[:-1].split(" ")
            metric_messages = ""
            if key == "*":
                for metric in self.store:
                    key, timestamp, value = metric
                    metric_message = "{} {} {}\n".format(key, value, timestamp)
                    metric_messages += metric_message
            else:
                for metric in self.store:
                    if key == metric[0]:
                        key, timestamp, value = metric
                        metric_message = "{} {} {}\n".format(key, value, timestamp)
                        metric_messages += metric_message
            answer = "ok\n" + metric_messages + "\n"
        else:
            answer = "error\nwrong command\n\n"

        return answer


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
