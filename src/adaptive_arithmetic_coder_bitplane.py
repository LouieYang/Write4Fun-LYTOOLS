import numpy as np

class BitplaneAdaptiveArithmeticCoder:
    """
        Adaptive Arithmetic Coder for bitplane coder
    """

    def __init__(self):
        self.intervals = [(0, 1)]

    def encode(self, bit_tensor, prob_tensor):
        """
            Args:
                prob_tensor: the probability of 1 for bit_tensor
        """
        self.bit_tensor = np.array(bit_tensor)
        self.prob_tensor = np.array(prob_tensor)

        self.shape = np.shape(self.bit_tensor)
        self.bit_flatten = self.bit_tensor.flatten()
        self.prob_flatten = self.prob_tensor.flatten()




if __name__ == "__main__":
    X = np.array([[1, 2, 3], [2, 3, 4]])
    S = np.shape(X)
    Y = X.flatten()
    X_ = Y.reshape(S)
    print X
    print S
    print Y
