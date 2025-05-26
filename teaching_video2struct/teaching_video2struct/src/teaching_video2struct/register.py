# SPDX-FileCopyrightText: Copyright (c) 2024-2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig

import whisper
from opencc import OpenCC
from moviepy.editor import AudioFileClip

logger = logging.getLogger(__name__)


def validate_number_count(numbers: list[str], expected_count: int, action: str) -> str | None:
    if len(numbers) < expected_count:
        return f"Provide at least {expected_count} numbers to {action}."
    if len(numbers) > expected_count:
        return f"This tool only supports {action} between {expected_count} numbers."
    return None


class InequalityToolConfig(FunctionBaseConfig, name="calculator_inequality_num"):
    pass


@register_function(config_type=InequalityToolConfig)
async def calculator_inequality_num(config: InequalityToolConfig, builder: Builder):

    import re

    async def _calculator_inequality_num(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        validation_error = validate_number_count(numbers, expected_count=2, action="compare")
        if validation_error:
            return validation_error
        a = int(numbers[0])
        b = int(numbers[1])
        if a > b:
            return f"First number {a} is greater than the second number {b}"
        if a < b:
            return f"First number {a} is less than the second number {b}"

        return f"First number {a} is equal to the second number {b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_inequality_num,
        description=("This is a mathematical tool used to perform an inequality comparison between two numbers. "
                     "It takes two numbers as an input and determines if one is greater or are equal."))


class MultiplyToolConfig(FunctionBaseConfig, name="calculator_multiply"):
    pass


@register_function(config_type=MultiplyToolConfig)
async def calculator_multiply(config: MultiplyToolConfig, builder: Builder):

    import re

    async def _calculator_multiply(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        validation_error = validate_number_count(numbers, expected_count=2, action="multiply")
        if validation_error:
            return validation_error
        a = int(numbers[0])
        b = int(numbers[1]) 

        return f"The product of {a} * {b} is {a * b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_multiply,
        description=("This is a mathematical tool used to multiply two numbers together. "
                     "It takes 2 numbers as an input and computes their numeric product as the output."))


class DivisionToolConfig(FunctionBaseConfig, name="calculator_divide"):
    pass


@register_function(config_type=DivisionToolConfig)
async def calculator_divide(config: DivisionToolConfig, builder: Builder):

    import re

    async def _calculator_divide(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        validation_error = validate_number_count(numbers, expected_count=2, action="divide")
        if validation_error:
            return validation_error
        a = int(numbers[0])
        b = int(numbers[1])

        return f"The result of {a} / {b} is {a / b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_divide,
        description=("This is a mathematical tool used to divide one number by another. "
                     "It takes 2 numbers as an input and computes their numeric quotient as the output."))


class SubtractToolConfig(FunctionBaseConfig, name="calculator_subtract"):
    pass


@register_function(config_type=SubtractToolConfig)
async def calculator_subtract(config: SubtractToolConfig, builder: Builder):

    import re

    async def _calculator_subtract(text: str) -> str:
        numbers = re.findall(r"\d+", text)
        validation_error = validate_number_count(numbers, expected_count=2, action="subtract")
        if validation_error:
            return validation_error
        a = int(numbers[0])
        b = int(numbers[1])

        return f"The result of {a} - {b} is {a - b}"

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _calculator_subtract,
        description=("This is a mathematical tool used to subtract one number from another. "
                     "It takes 2 numbers as an input and computes their numeric difference as the output."))




class VideoToAudioConfig(FunctionBaseConfig, name="video_to_audio_tool"):
    pass

@register_function(config_type=VideoToAudioConfig)
async def video_to_audio_tool(config: VideoToAudioConfig, builder: Builder):

    async def _video_to_audio_tool(video_file_path: str) -> str:

        my_audio_clip = AudioFileClip(".\\examples\\teaching_video2struct\\src\\teaching_video2struct\\data\\ml.mp4")
        my_audio_clip.write_audiofile(".\\examples\\teaching_video2struct\\src\\teaching_video2struct\\data\\ml.mp3")
        return f"Audio extracted and saved to ml.mp3"

    yield FunctionInfo.from_fn(
        _video_to_audio_tool,
        description=("A tool that extracts audio from a video file (e.g., MP4) and saves it as an audio file (e.g., MP3)."
                     " It takes a video file path as input and outputs the audio file path.")
    )








class AudioToTextConfig(FunctionBaseConfig, name="audio_to_text_tool"):
    pass

@register_function(config_type=AudioToTextConfig)
async def audio_to_text_tool(config: AudioToTextConfig, builder: Builder):
    cc = OpenCC('t2s')  # Traditional to Simplified

    try:
        model = whisper.load_model("medium")
        print("Whisper model 'medium' loaded successfully.")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        # Handle model loading failure appropriately, perhaps by yielding an error state
        # or raising an exception that the framework can catch.
        # For this example, we'll let it proceed and it will fail during transcription.
        model = None

    async def _audio_to_text_tool(audio_file_path: str) -> str:
        if model is None:
            return "Error: Whisper model not loaded. Cannot transcribe."
        try:
            print(f"Transcribing audio file: {audio_file_path} with language: zh")
            result = model.transcribe(".\\examples\\teaching_video2struct\\src\\teaching_video2struct\\data\\ml.mp3", language="zh")
            transcribed_text = result["text"]
            print(f"Original transcription: {transcribed_text}")

            simplified_text = cc.convert(transcribed_text)
            print(f"Simplified text: {simplified_text}")
            return simplified_text
        except FileNotFoundError:
            return f"Error: Audio file not found at {audio_file_path}"
        except Exception as e:
            return f"An error occurred during transcription or conversion: {e}"

    # 3. Yield FunctionInfo
    yield FunctionInfo.from_fn(
        _audio_to_text_tool,
        description=("A tool that transcribes an audio file to text using Whisper "
                     "and then converts the transcription from Traditional Chinese "
                     "to Simplified Chinese. Takes an audio file path as input.")
    )


