class Sessions:
    items = []

    def __init__(self, session, name):
        self.name = name
        self.session = session
        Sessions.items.append(self)

    async def __aenter__(self):
        return self.session

    async def __aexit__(self):
        await self.session.close()
        self.session = None

    @staticmethod
    def get_response(name, url):
        for item in Sessions.items:
            if item.name == name:
                return item.session.get(url=url)
        raise ValueError("Такой сессии не существует!")
