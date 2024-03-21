"""Default driver for color mixing experiments """


class driver():

    def __init__(self, config):

        """ things to set in config:
        self.executor_address = 
        self.executor_port
        self.optimizer_address
        self.optimizer_port
        self.data_processor_address
        self.data_processor_port

        self.database_access ...


        """

    def initialize_optimization_campaign(target_color, starter_data):

        # get a new UUID for campaign
        # initialize a new BO instance on BO executor
        