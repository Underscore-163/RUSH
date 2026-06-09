import time

class PerformanceTimer:
    instance=None
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(PerformanceTimer,cls).__new__(cls)
            return cls.instance
        else:
            return cls.instance
    def __init__(self):
        if not hasattr(self, "initialised"):
            self.laps={}
            self.initialised=True

    def start(self):
        self.laps["Start"]=time.time()
    def lap(self,name):
        self.laps[name]=time.time()
    def end(self,filter=False):
        self.lap("End")
        lap_names=list(self.laps.keys())
        lap_times=list(self.laps.values())
        lap_deltas=[0]
        for i in range(len(lap_times)):
            if lap_names[i]!="Start":
                lap_deltas.append(lap_times[i]-lap_times[i-1])
                if "e" in str(lap_deltas[i]):
                    lap_deltas[i]=0
            if not filter or lap_deltas[i]!=0:
                print(f"{lap_names[i]}: {float(lap_deltas[i]):.7}")
        print("total",lap_times[-1]-lap_times[0])

