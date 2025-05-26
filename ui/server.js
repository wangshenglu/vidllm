// server.js
const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
app.use(cors());

app.get('/generate-outline', (req, res) => {
  const command = `aiq run --config_file examples/simple_calculator/src/aiq_simple_calculator/configs/config.yml --input "Based on the sound in the video, generate a structured outline of the lecture. The outline should include the main topics, subtopics, and key points under each section. Use clear section headers and bullet points. Do not include transcript text, only summarize and organize the content."`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`运行错误: ${error}`);
      res.status(500).send("AIQ命令执行失败");
      return;
    }

    // 可以进一步清洗 stdout
    res.send(stdout);
  });
});

app.listen(3000, () => {
  console.log('✅ Node 服务运行在 http://localhost:3000');
});
