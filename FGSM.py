import torch


def FGSM_attack(model, dataloader, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	generated_images = []
	model.eval()
	percent_change = 0
	count = 0
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
		count += 1
		if count >= total_batches:
			break
	return generated_images


def PGD_attack(model, dataloader, total_batches, iterations, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	count = 0
	percent_change = 0
	generated_images = []
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
		generated_images.append(perturbed_images)
		if count >= total_batches:
			break
	return generated_images

def targeted_adversarial_attack(model, dataloader, total_batches, iterations, target_label, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss()):
	count = 0
	percent_change = 0
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		data.requires_grad = True
		original_preds = model(data)

		for i in range(iterations):
			
			outputs = model(data)
			optimizer = torch.optim.Adam(list([data, ]), maximize = False)
			if from_logits:
				outputs = torch.nn.functional.softmax(outputs, dim = 1)
			labels = target_label
			loss = loss_fn(outputs, labels)
			loss.backward()
			optimizer.step()
		new_preds = model(data)
		count += 1
		generated_images.append(data)
		if count >= total_batches:
			break

	return generated_images



  



