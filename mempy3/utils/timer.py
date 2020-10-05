from datetime import datetime


class Timer:
    def __init__(self, start=True, vocal=True):
        self.vocal=vocal
        if start:
            self.start()

    def start(self):
        self.start_time = datetime.now()
        self.step_time = self.start_time
        self.steps = [self.step_time]
        if self.vocal:
            print(f'Starting timer. Local time: {self.start_time}')

    #returns total time since start
    def get_run_time(self):
        return datetime.now()-self.start_time

    # adds a new step and returns time since last step
    def step(self, flavor='Step!'):
        prev_step = self.step_time
        self.step_time = datetime.now()
        self.steps.append(self.step_time)
        curr_step_time = self.step_time - prev_step
        if self.vocal:
            print(f'{flavor} Step time: {curr_step_time} - Total time {self.get_run_time()}')
        return curr_step_time

    # returns a list with all the step times, starting with start
    def get_steps(self):
        return self.steps

    def now(self):
        return datetime.now().strftime("%H:%M:%S")

