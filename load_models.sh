
huggingface-cli download --local-dir ./models leejet/FLUX.1-schnell-gguf flux1-schnell-q8_0.gguf
huggingface-cli download --local-dir ./models leejet/FLUX.1-dev-gguf flux1-dev-q8_0.gguf

## Vae 
huggingface-cli download --local-dir ./models black-forest-labs/FLUX.1-dev ae.safetensors

## clip_l
huggingface-cli download --local-dir ./models comfyanonymous/flux_text_encoders clip_l.safetensors

##t5xxl
huggingface-cli download --local-dir ./models comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors

## Lora
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection anime_lora_comfy_converted.safetensors
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection art_lora_comfy_converted.safetensors
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection disney_lora_comfy_converted.safetensors
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection mjv6_lora_comfy_converted.safetensors
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection realism_lora_comfy_converted.safetensors
huggingface-cli download --local-dir ./models XLabs-AI/flux-lora-collection scenery_lora_comfy_converted.safetensors