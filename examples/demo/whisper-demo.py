

cc = OpenCC('t2s')  # 从繁体转简体（traditional to simplified）


# 加载模型（可选 tiny, base, small, medium, large），根据电脑配置选择
model = whisper.load_model("medium") 

# 加载音频并自动转为合适格式
result = model.transcribe(".\\examples\\demo\\mysqlvideo.wav", language="zh")

simplified = cc.convert(result["text"])
print(simplified)
