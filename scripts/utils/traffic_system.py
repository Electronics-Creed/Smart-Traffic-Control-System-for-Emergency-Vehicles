class TrafficSignal:
    def __init__(self, initial_state, NUM_TRAFFIC_LIGHTS):
        self.state = initial_state  # state of the system
        self.counter = 0  # counter for traffic signal
        self.CYCLE_TIME = 24  # time taken for complete cycle in ready state
        self.NUM_TRAFFIC_LIGHTS = NUM_TRAFFIC_LIGHTS  # number of traffic lights in the traffic signal

    def if_change_state(self):  # check if the state has to change
        self.counter = self.counter % self.CYCLE_TIME
        if self.counter % (self.CYCLE_TIME / self.NUM_TRAFFIC_LIGHTS) == 0:
            self.change_state()

    def change_state(self, state=None):  # change the state
        if not state:
            ind = int(self.counter // (self.CYCLE_TIME / self.NUM_TRAFFIC_LIGHTS))
            self.state = [False for _ in range(self.NUM_TRAFFIC_LIGHTS)]
            self.state[ind] = True
        else:
            self.state = state  # change the state directly when siren is detected
