class sell():
    api = None
    sell_option = None
    sell_list = None
    def __new__(self, api):
        self.api = api