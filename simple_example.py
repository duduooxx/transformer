#!/usr/bin/python3

from train import *
from modules.transformer import Transformer
import torch

def data_gen(n_vocab, batch_size, n_batch, device):
    for i in range(n_batch):
        data = torch.randint(2, n_vocab, [batch_size, 10])
        data[:, 0] = 1
        data[:, -2:] = 0
        data = data.to(device)
        yield Batch(data, data)


if __name__ == '__main__':
    n_vocab = 10

    model = Transformer(n_vocab)
    criterion = LabelSmoothing(n_vocab, 0.)
    optimizer = scheduled_adam_optimizer(model)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #device = 'cpu'
    model.to(device)
    
    for epoch in range(10):
        print("Epoch: {}".format(epoch))
        data_iter = data_gen(n_vocab, 128, 10000, device)
        run_epoch(data_iter, model, criterion, optimizer)

    in_seq = torch.LongTensor([[1, 7, 5, 2, 3, 4, 5, 0]]).to(device)
    out_seq = torch.zeros([1, 20], dtype=torch.int64).to(device)
    out_seq[:, 0] = 1
    model.eval()
    
    for i in range(19):
        pred = model(in_seq, out_seq[:, :i+1])
        out_seq[0, i + 1] = torch.argmax(pred, dim=2)[0][-1]
    print(out_seq)
