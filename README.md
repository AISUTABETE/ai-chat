# AI Chat

## 项目简介

这是一个用于学习 AI 后端开发的练手项目，主要用于熟悉 Python 后端开发、FastAPI 以及 AI 模型 API 的调用流程。

本人自 2024 年从最后一份 Java 开发工作离职后，几乎没有再系统学习开发相关内容。最近重新开始学习 AI 应用开发，发现自己似乎仍然对开发保有热情。

这个项目会在学习过程中持续迭代。

## 当前功能

目前项目仍处于早期阶段，已实现：

* 基于 `conversation_id` 的会话管理
* 多轮对话上下文
* 不同会话之间的消息隔离
* 调用 OpenAI 兼容 API 进行模型对话
* 异步 API 调用

目前暂未实现数据持久化，聊天记录仅保存在应用运行期间的内存中，应用重启后数据会丢失。

前端暂未开发，目前主要通过 FastAPI 自动生成的接口文档测试 API。

## 技术栈

* **Python**：主要开发语言
* **FastAPI**：构建 Web API
* **Pydantic**：请求参数和响应数据校验
* **OpenAI Python SDK**：封装模型 API 的 HTTP 调用
* **AsyncOpenAI**：异步调用模型 API
* **SiliconFlow**：提供 OpenAI 兼容的模型 API 服务

## 请求流程

```text
客户端
  ↓
HTTP POST 请求
  ↓
FastAPI 路由
  ↓
Pydantic 请求参数校验
  ↓
会话历史管理
  ↓
OpenAI 兼容 SDK
  ↓
模型 API
  ↓
返回模型响应
  ↓
Pydantic 响应模型
  ↓
FastAPI
  ↓
HTTP JSON 响应
```

## API 接口

### `POST /chat`

发送一条消息并获取模型回复。

请求示例：

```json
{
  "conversation_id": null,
  "message": "你好，请介绍一下自己！"
}
```

首次请求时，`conversation_id` 可以为空，服务端会自动生成新的会话 ID。

后续请求携带相同的 `conversation_id`，即可继续之前的多轮对话。

响应示例：

```json
{
  "conversation_id": "xxx",
  "answer": "你好！很高兴认识你。"
}
```

## 如何运行

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd ai-chat
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
SILICONFLOW_API_KEY=your_api_key
```

### 4. 启动服务

```bash
uvicorn main:app --reload
```

服务启动后，可以通过 FastAPI 自动生成的接口文档测试 API。

## 后续计划

* [ ] 开发简单前端交互页面
* [ ] 实现流式对话
* [ ] 添加模型角色设置
* [ ] 支持更多模型参数自定义
* [ ] 添加图片和语音输入
* [ ] 使用数据库持久化聊天记录
* [ ] 优化上下文管理和 Token 使用
* [ ] 接入 RAG 等 AI 应用能力
