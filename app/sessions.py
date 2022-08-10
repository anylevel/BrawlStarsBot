class Sessions:
    items = {}

    def __init__(self, session, name):
        self.name = name
        self.session = session
        Sessions.items[name] = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self):
        await self.session.close()
        self.session = None

    @staticmethod
    def get_response(name, url):
        try:
            return Sessions.items[name].get(url=url)
        except KeyError:
            print("Такой сессии не существует!")
