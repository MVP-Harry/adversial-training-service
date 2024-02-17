import torch


def FGSM_attack(model, dataloader, from_logits = True, loss_fn = torch.nn.CrossEntropyLoss()):
	for batch in dataloader:
		x, y = batch
		data = x.clone().detach()
		data.requires_grad = True
		outputs = model(data)
		if from_logits:
			outputs = torch.nn.functional.sigmoid(outputs)
		loss = torch.nn.CrossEntropyLoss(outputs, y)
		data_grad = data.grad.data
		grad_sign = data_grad.sign()
		perturbed_image = torch.clip()