
"""
Represents one configuration chosen at runtime.
and Inputs the MLP a dictionary Object.
"""
class SMARTClassifierConfig:
    def __init__(self, iterations=0, hidden_layer_sizes=None):
        if hidden_layer_sizes is None:
            hidden_layer_sizes = []
        self.num_iterations = iterations
        self.hidden_layer_sizes = hidden_layer_sizes

    def to_dict(self):
        #MLP loves a dictionary params, LOL
        return {
            "max_iter": self.num_iterations,
            "hidden_layer_sizes": self.hidden_layer_sizes
        }
