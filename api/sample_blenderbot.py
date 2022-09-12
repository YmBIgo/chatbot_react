import torch
from base_model import BaseModel
from transformers import (
	BlenderbotSmallForConditionalGeneration,
	BlenderbotSmallTokenizer,
	BlenderbotForConditionalGeneration,
	BlenderbotTokenizer
)

class BlenderBot(BaseModel):
	def __init__(self, size, device, max_context_length=1024):
		assert size in ["small", "medium", "large"], "model size must be one of ['small', 'medium', 'large']"
		if size == "small":
			super().__init__("facebook/blenderbot_small-90M")
			self.model = BlenderbotForConditionalGeneration.from_pretrained(self.name).to(device)
		else:
			if size == "medium":
				super().__init__("facebook/blenderbot-400M-distill")
			elif size == "large":
				super().__init__("facebook/blenderbot-1B-distill")
			self.model = BlenderbotForConditionalGeneration.from_pretrained(self.name).to(device)
			self.tokenizer = BlenderbotTokenizer.from_pretrained(self.name)
		
		self.device = device.lower()

		self.max_context_length = max_context_length
		self.eos = "</s><s>"
		self.history_human = {}
		self.history_bot = {}

	@torch.no_grad()
	def predict(
		self,
		user_id: str,
		text: str,
		num_beams: int = 5,
		top_k: int = 1,
		top_p: float = None,
		) -> str:

		torch.cuda.empty_cache()
		input_ids_list: list = []
		num_of_stacked_tokens: int = 0

		if user_id not in self.history_human.keys():
			self.history_human[user_id] = []
			self.history_bot[user_id] = []

		user_histories = reversed(self.history_human[user_id])
		bot_histories = reversed(self.history_bot[user_id])

		for user, bot in zip(user_histories, bot_histories):
			user_tokens = self.tokenizer.encode(user, return_tensors="pt")
			bot_tokens = self.tokenizer.encode(bot, return_tensors="pt")
			num_of_stacked_tokens += user_tokens.shape[-1] + bot_tokens.shape[-1]

			if num_of_stacked_tokens <= self.max_context_length:
				input_ids_list.append(bot_tokens)
				input_ids_list.append(user_tokens)
			else:
				break

		input_ids_list = list(reversed(input_ids_list))
		new_input = text + self.eos
		input_tokens = self.tokenizer.encode(new_input, return_tensors='pt')
		input_ids_list.append(input_tokens)
		input_tokens = torch.cat(input_ids_list, dim=-1)
		input_tokens = input_tokens.to(self.device)

		output_ids = self.model.generate(
			input_tokens,
			max_length=1024,
			num_beams=num_beams,
			top_k=top_k,
			top_p=top_p,
			no_repeat_ngram_size=4
		)[0]

		next_utterance = self.tokenizer.decode(
			output_ids.tolist(),
			skip_special_tokens=True
		).replace("Ġ", "").replace("  ", "")

		print(next_utterance)

		self.history_human[user_id].append(text + self.eos)
		self.history_bot[user_id].append(next_utterance + self.eos)

		return next_utterance

# b = BlenderBot(size="medium", device="cpu")
# while True:
# 	print("[ please input string ]")
# 	input_string = input()
# 	b.predict("hogehoge", input_string)

