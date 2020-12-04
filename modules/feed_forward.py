import torch
from torch import nn
#from torch import functional as F

class FeedForwardNetwork(nn.Module):
    """
    Position-wise Feed-Forward Network
    Apply the following operation
    f(x) = max(0, xW1 + b1) * W2 + b2

    Attributes
    ----------
    l1 : nn.Linear (in_features=d_model, out_features=d_ff)
    l2 : nn.Linear (in_features=d_ff, out_features=d_model)
    """
    
    def __init__(self, d_model, d_ff):
        """
        Parameters
        ----------
        d_model : int
            embedding length
        d_ff    : int
            size of intermediate activation
        """
        super(FeedForwardNetwork, self).__init__()
        self.l1 = torch.nn.Linear(d_model, d_ff)
        self.l2 = torch.nn.Linear(d_ff, d_model)

    def forward(self, x):
        return self.l2(torch.relu(self.l1(x)))
