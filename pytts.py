import numpy as np
import soundfile as sf
import yaml

import tensorflow as tf

from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

from tensorflow_tts.configs import HifiGANGeneratorConfig
from tensorflow_tts.models import TFHifiGANGenerator

from playsound import playsound

ADUIO_OUTPUT_NAME = "output_file.wav"


class TTS:
    def __init__(self) -> None:
        # fastspeech2 model.
        self.fastspeech2 = None

        # mel_to_audio_generator model
        self.mel_to_audio_generator = None

        # melgan model
        self.mb_melgan = None

        # inference
        self.processor = None

        self.input_ids = None

        self.load_models()

    def load_models(self):
        # initialize fastspeech2 model.
        self.fastspeech2 = TFAutoModel.from_pretrained(
            "tensorspeech/tts-fastspeech2-ljspeech-en")

        with open('./examples/hifigan/conf/hifigan.v1.yaml') as f:
            fs_config = yaml.load(f, Loader=yaml.Loader)
        fs_config = HifiGANGeneratorConfig(
            **fs_config["hifigan_generator_params"])
        self.mel_to_audio_generator = TFHifiGANGenerator(
            config=fs_config, name="hifigan_generator")
        self.mel_to_audio_generator._build()
        self.mel_to_audio_generator.load_weights(
            "./examples/hifigan/exp/checkpoints/generator-8000.h5")

        # initialize mb_melgan model
        self.mb_melgan = TFAutoModel.from_pretrained(
            "tensorspeech/tts-mb_melgan-ljspeech-en")

        # inference
        self.processor = AutoProcessor.from_pretrained(
            "tensorspeech/tts-fastspeech2-ljspeech-en")

    def text_to_speech(self, text, use_my_model=False):
        if text:
            input_ids = self.processor.text_to_sequence(text)

            # fastspeech inference

            mel_before, mel_after, duration_outputs, _, _ = self.fastspeech2.inference(
                input_ids=tf.expand_dims(
                    tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
                speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
                speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
                f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
                energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
            )

            # melgan inference
            #audio_before = self.mel_to_audio_generator.inference(mel_before)[0, :, 0]
            if use_my_model:
                audio_after = self.mel_to_audio_generator(mel_after)[0, :, 0]
            else:
                audio_after = self.mb_melgan.inference(mel_after)[
                    0, :, 0]

            # save to file
            #sf.write(f'./audio_before.wav', audio_before, 22050, "PCM_16")
            sf.write(ADUIO_OUTPUT_NAME, audio_after, 22050, "PCM_16")
            playsound(ADUIO_OUTPUT_NAME)
        else:
            print("Input text is empty.")
