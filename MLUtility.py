import numpy as np
import torch 
from torch.utils import data # 获取迭代数据
from torch.autograd import Variable # 获取变量

class CNNnet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv1d(in_channels=1,
                            out_channels=16,
                            kernel_size=3,
                            stride=1,
                            padding=2),
            torch.nn.BatchNorm1d(16),
            torch.nn.ReLU()
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv1d(16,32,3,1,2),
            torch.nn.BatchNorm1d(32),
            torch.nn.ReLU()
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv1d(32,64,3,1,2),
            torch.nn.BatchNorm1d(64),
            torch.nn.ReLU()
        )
        self.conv4 = torch.nn.Sequential(
            torch.nn.Conv1d(64,64,2,1,0),
            torch.nn.BatchNorm1d(64),
            torch.nn.ReLU()
        )
        self.mlp1 = torch.nn.Linear(1152,100)
        self.mlp2 = torch.nn.Linear(100,1)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.mlp1(x.view(x.size(0),-1))
        x = self.mlp2(x)
        return x

def normalization(state):
    state=np.array([state])
    means=np.array([[1.6831783766488317,1.920861792019031,2.0142274382885192,2.099035853596613,2.223753461124363,\
        2.3957063177909617,11.785342967427546,1.6735022578976735,1.916759244860047,2.0219108486903,2.095517344002846,2.2175399572616663,2.4000639932270524,11.760987284327173]])
    stds=np.array([[2.2965555781311355,2.5959722979902446,2.6847805719174693,2.745832204831912,2.8541587526372196,\
        2.979194156904659,6.298355040135411,2.3016301665931884,2.5987004084829355,2.6955533493313037,2.738373835337156,2.8395994049082107,2.9842425056695507,6.301167592999449]])
    state=(state-means)/stds
    n=np.ones((128,1,1))
    state=state*n
    return state.tolist()

if __name__ == "__main__":
    model=torch.load("model")
    state=normalization([0,0,0,0,0,0,24,2,2,2,2,2,2,12])
    out = model(torch.tensor(state))
    print(out[0][0].item())