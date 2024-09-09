import panel as pn
import param
import subprocess
import os
from typing import List, Tuple
from panel.widgets import Spinner
from threading import Thread

class StableDiffusionApp(param.Parameterized):
    model = param.ObjectSelector(default="Flux1 Dev", objects=["Flux1 Dev", "Flux1 Schnell"])
    lora_adapters = param.ObjectSelector(default=None, objects=["None"])
    prompt = param.String(default="")
    negative_prompt = param.String(default="")
    resolution = param.ObjectSelector(default="512x512", objects=["512x512", "1024x1024"])
    steps = param.Integer(default=4, bounds=(1, 100))
    seed = param.Integer(default=-1)
    command_line = param.String(default="")
    image_pane = param.ClassSelector(class_=pn.pane.Image, default=pn.pane.Image(sizing_mode='scale_both', min_height=512))
    command_output = param.String(default="")

    def __init__(self, **params):
        super(StableDiffusionApp, self).__init__(**params)
        self.generate_button = pn.widgets.Button(name="Generate Image", button_type="primary")
        self.generate_button.on_click(self.run_generation)
        self.loading_spinner = pn.indicators.LoadingSpinner(value=False, size=25)
        self.image_pane = pn.pane.Image(sizing_mode='scale_both', min_height=512)
        self.output_image = ""
        self.update_lora_adapters()

    def update_lora_adapters(self) -> None:
        """Update the list of available LoRA adapters."""
        if not os.path.exists("./models"):
            print("Models directory not found. Please create it and add LoRA adapter files.")
            return
        lora_files = ["None"] + [f for f in os.listdir("./models") if "lora" in f.lower() and f.endswith(".safetensors")]
        self.param.lora_adapters.objects = lora_files
        if lora_files:
            self.lora_adapters = "None"
        else:
            print("No LoRA adapter files found in the models directory.")

    def generate_command(self) -> str:
        """Generate the stable-diffusion.cpp command line."""
        width, height = map(int, self.resolution.split('x'))
        lora_name = self.lora_adapters.replace('.safetensors', '') if self.lora_adapters != "None" else "no_lora"
        self.output_image = f"{self.prompt.replace(' ', '_')}_{self.seed}_{lora_name}_{width}x{height}_{self.steps}steps.png"
        
        # Update prompt with LoRA information
        effective_prompt = self.prompt
        if self.lora_adapters != "None":
            effective_prompt += f" <{lora_name}:1>"

        cmd = [
            "./stable-diffusion.cpp/build/bin/sd",
            f"--diffusion-model ./models/{self.model.replace(' ', '-').lower()}-q8_0.gguf",
            f"--prompt '{effective_prompt}'",
            f"--negative-prompt '{self.negative_prompt}'",
            f"-W {width}",
            f"-H {height}",
            f"--steps {self.steps}",
            f"--seed {self.seed}",
            "--vae ./models/ae.safetensors",
            "--clip_l ./models/clip_l.safetensors",
            "--t5xxl ./models/t5xxl_fp16.safetensors",
            "--lora-model-dir ./models",
            "--cfg-scale 1.0",
            "--sampling-method euler",
            f"-o {self.output_image}",
            "-v"
        ]

        return " ".join(cmd)

    @param.depends('model', 'lora_adapters', 'prompt', 'negative_prompt', 'resolution', 'steps', 'seed', watch=True)
    def update_command_line(self):
        """Update the command line preview."""
        if not hasattr(self, '_updating_command_line'):
            self._updating_command_line = True
            try:
                self.command_line = self.generate_command()
            finally:
                del self._updating_command_line

    def run_generation(self, event):
        """Run the stable-diffusion.cpp command and update the output image."""
        cmd = self.generate_command()
        self.command_output = ""
        print(cmd)
        # Disable button and start spinner
        self.generate_button.disabled = True
        self.loading_spinner.value = True
        
        def run_command():
            try:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.command_output += output
                        self.param.trigger('command_output')
                
                stderr = process.stderr.read()
                if stderr:
                    print(f"Error: {stderr}")
                    self.error_message = f"Error: {stderr}"
                    # Use pn.io.add_periodic_callback instead of push_notebook
                self.image_pane.object = self.output_image  # Set the new image
                self.param.trigger('image_pane')
            except subprocess.CalledProcessError as e:
                self.output_image = ""
            finally:
                # Re-enable button and stop spinner
                self.generate_button.disabled = False
                self.loading_spinner.value = False
                pn.io.push_notebook()

        # Run the command in a separate thread
        Thread(target=run_command).start()


    @param.depends('model', 'lora_adapters', 'prompt', 'negative_prompt', 'resolution', 'steps', 'seed', 'image_pane', watch=True)
    def view(self):
        """Create the main view of the application."""
        input_column = pn.Column(
            pn.pane.Markdown("# Flux.1 Cpp"),
            pn.Param(self.param, 
                     parameters=['model', 'lora_adapters', 'prompt', 'negative_prompt', 'resolution', 'steps', 'seed'],
                     widgets={
                        'model': pn.widgets.Select,
                        'lora_adapters': pn.widgets.Select,
                        'prompt': pn.widgets.TextAreaInput,
                        'negative_prompt': pn.widgets.TextAreaInput,
                        'resolution': pn.widgets.Select,
                        'steps': pn.widgets.IntSlider,
                        'seed': pn.widgets.IntInput,
                     },
                     show_name=False),

            pn.Row(self.generate_button, self.loading_spinner),
        )

        output_column = pn.Column(
            pn.pane.Markdown("## Generated Image"),
            self.image_pane,
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("## Command Preview"),
                    pn.widgets.TextAreaInput(value=self.param.command_line, disabled=True, height=100),
                ),
                pn.Column(
                    pn.pane.Markdown("## Command Output"),
                    pn.widgets.TextAreaInput(value=self.param.command_output, disabled=True, height=100, width=400, max_length=10000),
                )
            )   
        )

        return pn.Row(input_column, output_column)

# Create and show the app
app = StableDiffusionApp()
pn.serve(app.view, port=5006, show=True)