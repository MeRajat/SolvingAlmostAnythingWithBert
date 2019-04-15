def train(model, iterator, optimizer, criterion, device = 'gpu'):
    model.train()

    for i, batch in enumerate(iterator):
        input_ids, segment_ids, input_mask, labels = [t.to(device) for t in batch]

        optimizer.zero_grad()
        loss =  model(input_ids, segment_ids, input_mask, labels)

        loss.backward()
        optimizer.step()

    if i %10 == 0:
        print(f"step {i}, loss: {loss.item()}")

    


