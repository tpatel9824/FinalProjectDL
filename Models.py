import sys
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.models as models
import os
import matplotlib.pyplot as plt

from CNN_CLASSIFIER import  Net
if __name__ == '__main__':
    from main import DDataset
    import torch
    import pandas as pd
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    directory = r'C:\Users\91875\OneDrive\Desktop\3D_RECONSTRUCTION\Training'
    DataFrame = pd.read_csv(r'C:\Users\91875\OneDrive\Desktop\3D_RECONSTRUCTION\Training\Annotations.csv')
    Data = DDataset(DataFrame, directory)
    train_loader = torch.utils.data.DataLoader(Data, batch_size=10, num_workers=2, shuffle=True)

    # Ensure the code below is only executed after DataLoader is initialized
    train_features, train_labels = next(iter(train_loader))
    train_features,train_labels=train_features.to(device),train_labels.to(device)
    print("Feature Batch Shape", train_labels)
    for batch in train_loader:
        images,label=batch
        print("Size Of A Batch Is",images.shape)
        break

    net=Net().to(device)
    net.Temp(net)

    Loss=[]
    Epoch=[]
    Val_Loss=[]
    for epoch in range(20):
        net.train()
        running_loss=0.0
        for i,data in enumerate(train_loader):
            inputs,label=data
            batch_size=inputs.shape[0]

            inputs, label = inputs.to(device), label.to(device)

            inputs=inputs.view(batch_size, 5 * 3, 214, 214)
            running_loss += net.Backward(net,inputs,label,)
        print(f"Epoch:{epoch},Running_Loss:{running_loss}")
        Loss.append(running_loss)
        Epoch.append(epoch)
    fig,axs=plt.subplots(1,2)
    axs[0].plot(Epoch,Loss)
    axs[0].set_title("Training Loss Over Epochs")
    for ax in axs.flat:
        ax.set(xlabel='Epoch',ylabel='Loss')
    plt.show()
    sys.exit()
    directory = r'C:\Users\91875\OneDrive\Desktop\3D_OBJECT\3DImageReconstruction\SAVED_MODELS'
    os.makedirs(directory, exist_ok=True)

    PATH = os.path.join(directory, "model.pth")

    torch.save(net.state_dict(), PATH)