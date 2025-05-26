# OnlineStudyHelper



在线教学视频笔记生成工具

## 项目背景与动机



在线教学视频已经成为在线教育平台最重要的内容形式之一。然而，对于学生来说，快速理解视频内容结构、把握重点仍然是一个痛点。他们更希望有一个自动化手段来生成视频大纲，以便快速预览内容、整理知识点。 因此，我们尝试将音视频处理技术与大型语言模型（LLM）结合，构建一个能够自动从教学视频中提取内容大纲的系统。我们构建两个可由LLM调用的工具（tool）：一个利用 ffmpeg 和 moviepy 提取与预处理音频，另一个利用 Whisper 实现自动语音识别（ASR）。LLM通过调用这两个工具，能够获取教学视频的音频文本内容，并进一步生成结构化的提纲。

## 系统架构



以 nVidia 的 AI Toolkit 作为 Model Context Protocol (MCP) Server，部署如下： LLM：位于架构的中心，负责理解上下文、进行决策和生成提纲，并通过 AIQ被赋予了调用外部 tools 能力。其接受用户指令（prompt），选择对应视频文件，能够智能判断何时以及如何调用注册的工具。 音视频预处理工具（Tool 1）：基于 ffmpeg 和 moviepy，该 tool 负责从原始教学视频中提取音频轨道，并进行必要的音频格式转换与处理。输入为视频文件地址（由 LLM 告知），输出为音频文件地址（返回 LLM）。 语音识别工具（Tool 2）：接收预处理后的音频文件地址，利用 OpenAI Whisper 模型进行 ASR，将音频内容转换为文本并返回 LLM。 在获取到视频的文本转录后，LLM 从文本中提取关键主题、识别内容结构，最终生成视频提纲。 此外，我们设计了简单的UI界面，方便用户使用。

## 关键组件说明



我们通过 AIQ 的注册机制，将上述两个 tools 封装为一个可供 LLM 调用的“工具”。以语音识别工具为例，其在 register.py 中的实现示意如下：

```python
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
        model = None

    async def _audio_to_text_tool(audio_file_path: str) -> str:
        if model is None:
            return "Error: Whisper model not loaded. Cannot transcribe."
        try:
            result = model.transcribe(audio_file_path, language="zh")
            transcribed_text = result["text"]
            simplified_text = cc.convert(transcribed_text)
            print(f"text: {simplified_text}")
            return simplified_text
        except FileNotFoundError:
            return f"Error: Audio file not found at {audio_file_path}"

    yield FunctionInfo.from_fn(
        _audio_to_text_tool,
        description=("A tool that transcribes an audio file to text using Whisper "
                     "Takes an audio file path as input.")
    )
```
