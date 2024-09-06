# Introduction

This is a simple python application that allows you to generate images using the Flux.1 GGUF models on a Mac Silicon Mx. It is built with Panel and uses the stable-diffusion.cpp command line tool.
I gives a way to use Flux.1 models without comfyui in a simple way.

# Setup

## Prerequisites

- Huggingface CLI
	brew install huggingface-cli
	Create a Hugginface Token 
	https://huggingface.co/settings/tokens
	hugginface-cli login 
	Enter your token

- Stable Diffusion.cpp
    GitHub 
    https://github.com/leejet/stable-diffusion.cpp

# Installation
	mkdir flux.1
	cd flux.1
	mkdir models

	git clone --recursive https://github.com/leejet/stable-diffusion.cpp
	cd stable-diffusion.cpp
	mkdir build
	cmake .. -DSD_METAL=ON
	cmake --build . --config Release

# Download models & lora

    ## Flux.1 Dev & Schnell GGUF
	cd ../../models

	huggingface-cli download --local-dir ./ leejet/FLUX.1-schnell-gguf flux1-schnell-q8_0.gguf
	huggingface-cli download --local-dir ./ leejet/FLUX.1-dev-gguf flux1-dev-q8_0.gguf

	## Vae 
	huggingface-cli download --local-dir ./ black-forest-labs/FLUX.1-dev ae.safetensors

	## clip_l
	huggingface-cli download --local-dir ./ comfyanonymous/flux_text_encoders clip_l.safetensors

	##t5xxl
	huggingface-cli download --local-dir ./ comfyanonymous/flux_text_encoders t5xxl_fp16.safetensors

	## Lora
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection anime_lora_comfy_converted.safetensors
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection art_lora_comfy_converted.safetensors
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection disney_lora_comfy_converted.safetensors
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection mjv6_lora_comfy_converted.safetensors
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection realism_lora_comfy_converted.safetensors
	huggingface-cli download --local-dir ./ XLabs-AI/flux-lora-collection scenery_lora_comfy_converted.safetensors@

# Create a virtual environment and install dependencies
	python3 -m venv flux.1    
	source ./flux.1/bin/activate
	pip install panel param

# Run the app
    python3 app.py
