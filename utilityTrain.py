import numpy as np
import torch 
from torch.utils import data # 获取迭代数据
from torch.autograd import Variable # 获取变量
import matplotlib.pyplot as plt

class CNNnet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv1d(in_channels=1,
                            out_channels=16,
                            kernel_size=3,
                            stride=1,
                            padding=2),
            torch.nn.ReLU()
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv1d(16,32,3,1,2),
            torch.nn.ReLU()
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv1d(32,64,3,1,2),
            torch.nn.ReLU()
        )
        self.conv4 = torch.nn.Sequential(
            torch.nn.Conv1d(64,64,2,1,0),
            torch.nn.ReLU()
        )
        self.mlp1 = torch.nn.Linear(1216,100)
        self.mlp2 = torch.nn.Linear(100,1)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.mlp1(x.view(x.size(0),-1))
        x = self.mlp2(x)
        return x



def loadDataSet(fileName,delim='\t'):	#指定文件名和每行分隔符
    fr=open(fileName)
    arr1=[line.strip().split(delim) for line in fr.readlines()]	#strip将移除最尾的换行符
    arr2=[np.array(line,dtype=float) for line in arr1]	#将数据类型转换为浮点数
    return np.array(arr2)

def normalization(dataMat):
    numFeat=dataMat.shape[1]
    for i in range(numFeat):
        meanVal=np.mean(dataMat[...,i])
        stdVal=np.std(dataMat[...,i])
        dataMat[...,i]=(dataMat[...,i]-meanVal)/stdVal
        print(meanVal,stdVal)
    return dataMat

class mySet(data.Dataset):
    def __init__(self,data):
        super().__init__()
        self.features=data[...,:-1].tolist()
        self.labels=np.squeeze(data[...,-1]).tolist()
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self,index):
        return torch.tensor([self.features[index]]),torch.tensor(self.labels[index])

if __name__=="__main__":
    model =CNNnet()

    matrix=loadDataSet("dataset.txt")
    print("Successfully load.")
    matrix=normalization(matrix)
    print("Successfully normalized.")
    myData=mySet(matrix)
    print("Successfully generate dataset.")
    train,test=data.random_split(dataset= myData, lengths=[matrix.shape[0]-200000,200000])
    train_loader=data.DataLoader(train,batch_size=128,shuffle=True)
    test_loader=data.DataLoader(test,batch_size=128,shuffle=True)
    loss_func = torch.nn.L1Loss()
    opt = torch.optim.Adam(model.parameters(),lr=0.001)
    loss_count = []
    for epoch in range(2):
        for i,(x,y) in enumerate(train_loader):
            batch_x = Variable(x)
            batch_y = Variable(y)
            out = model(batch_x)
            loss = loss_func(out,batch_y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            if i%20 == 0:
                loss_count.append(loss)
                print('{}:\t'.format(i*128), loss.item())
                torch.save(model,'model')
            if i % 100 == 0:
                for a,b in test_loader:
                    test_x = Variable(a)
                    test_y = Variable(b)
                    out = model(test_x)
                    accuracy = torch.max(out,1)[1].numpy() - test_y.numpy()
                    print('accuracy:\t',accuracy.mean())
                    break
    plt.figure('PyTorch_CNN_Loss')
    plt.plot(loss_count,label='Loss')
    plt.legend()
    plt.show()
