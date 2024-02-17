import torch


def FGSM_attack(model, dataloader, total_batches, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	generated_images = []
	original_labels = []
	model.eval()
	percent_change = 0
	count = 0
	running_loss = 0
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		original_preds = model(data)
		data.requires_grad = True
		outputs = model(data)
		if from_logits:
			outputs = torch.nn.functional.softmax(outputs, dim = 1)
		loss = loss_fn(outputs, y)
		loss.backward()
		data_grad = data.grad.data
		perturbed_images = data + epsilon * data_grad.sign()
		generated_images.append(perturbed_images)

		original_labels.append(y)
		count += 1

		new_preds = model(perturbed_images)
		new_loss = loss_fn(new_preds, y)
		loss_change = new_loss.item() - loss.item()
		running_loss += loss_change
		if count >= total_batches:
			break
	running_loss /= count
	return generated_images, original_labels, running_loss


def PGD_attack(model, dataloader, total_batches, iterations, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	count = 0
	running_loss = 0

	generated_images = []
	original_labels = []
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		data.requires_grad = True
		original_preds = model(data)

		for i in range(iterations):			
			outputs = model(data)
			if from_logits:
				outputs = torch.nn.functional.softmax(outputs, dim = 1)
			loss = loss_fn(outputs, y)
			loss.backward()
			data_grad = data.grad.data
			perturbed_images = data + epsilon * data_grad
		count += 1

		new_preds = model(perturbed_images)
		new_loss = loss_fn(new_preds, y)
		loss_change = new_loss.item() - loss.item()
		running_loss += loss_change

		generated_images.append(perturbed_images)
		original_labels.append(y)

		if count >= total_batches:
			break

	running_loss /= count

	return generated_images, original_labels, running_loss

def targeted_adversarial_attack(model, dataloader, total_batches, iterations, target_label, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss()):
	count = 0
	percent_change = 0
	generated_images = []
	original_labels = []
	running_loss = 0
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		data.requires_grad = True
		original_preds = model(data)
		optimizer = torch.optim.Adam(list([data, ]), maximize = False)

		for i in range(iterations):
			optimizer.zero_grad()
			outputs = model(data)
			
			if from_logits:
				outputs = torch.nn.functional.softmax(outputs, dim = 1)
			labels = target_label
			loss = loss_fn(outputs, labels)
			loss.backward()
			optimizer.step()
		new_preds = model(data)
		new_loss = loss_fn(new_preds, labels)
		running_loss = new_loss.item() - loss.item()
		count += 1
		generated_images.append(data)
		original_labels.append(y)
		if count >= total_batches:
			break


	return generated_images, original_labels, running_loss



  



