from enum import Enum
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cpu"
save_model_dir = "models/model-test"


class SpecialTokens(Enum):
    bos_token = "<BOS>"
    eos_token = "<EOS>"
    pad_token = "<PAD>"
    ingrs_start = "<INGRS_START>"
    ingrs_end = "<INGRS_END>"
    ingrs_next = "<INGRS_NEXT>"
    instr_start = "<INSTR_START>"
    instr_end = "<INSTR_END>"
    instr_next = "<INSTR_NEXT>"
    title_start = "<TITLE_START>"
    title_end = "<TITLE_END>"


class GenerationModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(save_model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(save_model_dir)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.special_tokens = SpecialTokens
        self.sep = ";"

    def generate_recipe(self, ingrs):
        """Generate recipe from input ingredients."""
        if ingrs == "":
            raise Exception("empty ingredients")

        t = self.special_tokens
        ingrs_text = self.sep.join([i.strip() for i in ingrs.split(",")])

        # seq = f"{bos_token}{ingrs_start}{ingrs}{ingrs_end}{instr_start}{instructions}{instr_end}{title_start}{title}{title_end}{eos_token}"
        prompt = f"{t.bos_token.value}{t.ingrs_start.value}{ingrs_text}{t.ingrs_end.value}{t.instr_start.value}"
        inputs = self.tokenizer(
            prompt, return_tensors="pt", padding=True, truncation=True
        )
        input_ids = inputs.input_ids.to(device)
        attention_mask = inputs.attention_mask.to(device)

        output = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=300,
            num_beams=5,
            no_repeat_ngram_size=2,
            top_k=60,
            top_p=0.95,
            temperature=0.8,
            do_sample=True,
            eos_token_id=self.tokenizer.eos_token_id,
            early_stopping=True,
        )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=False)
        print(generated_text)
        return self.parse_recipe(generated_text)

    def parse_recipe(self, text):
        """Parses a structured recipe text into a dictionary."""
        recipe = {}
        t = self.special_tokens

        # Extract ingredients
        ingrs_start = text.find(t.ingrs_start.value) + len(t.ingrs_start.value)
        ingrs_end = text.find(t.ingrs_end.value)
        ingredients = text[ingrs_start:ingrs_end].split(";")
        recipe["ingredients"] = [ingredient.strip() for ingredient in ingredients]

        # Extract instructions
        instr_start = text.find(t.instr_start.value) + len(t.instr_start.value)
        instr_end = text.find(t.instr_end.value)
        instructions = text[instr_start:instr_end].split(t.instr_next.value)
        recipe["instructions"] = [
            instruction.strip() for instruction in instructions if instruction.strip()
        ]

        ## Extract title
        title_start = text.find(t.title_start.value) + len(t.title_start.value)
        title_end = text.find(t.title_end.value)
        title = text[title_start:title_end]
        recipe["title"] = title

        return recipe
