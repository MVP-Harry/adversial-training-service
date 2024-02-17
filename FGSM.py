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
			outputs = torch.nn.functional.sigmoid(outputs)
		loss = torch.nn.CrossEntropyLoss(outputs, y)
		data_grad = data.grad.data
		perturbed_image = data + epsilon * data_grad.sign()
		new_preds = model(perturbed_image)
		generated_images.append(perturbed_images)
		percent_change += torch.sum(torch.heaviside(torch.abs(new_preds - original_preds), values = 0)) / original_preds.size()[0]
		count += 1
	percent_change = percent_change / count
	return generated_images, percent_change


def PGD_attack(model, dataloader, iterations, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss(), epsilon = 0.001):
	for batch in dataloader:
		original_preds = model(data)
		for i in range(iterations):
			x, y = batch
			data = x.clone().detach()
			data.requires_grad = True
			outputs = model(data)
			if from_logits:
				outputs = torch.nn.functional.sigmoid(outputs)
			loss = torch.nn.CrossEntropyLoss(outputs, y)
			data_grad = data.grad.data
			perturbed_image = data + epsilon * data_grad
		new_preds = model(perturbed_image)
		percent_change += torch.sum(torch.heaviside(torch.abs(new_preds - original_preds), values = 0)) / original_preds.size()[0]
		count += 1
	return generated_images, percent_change
