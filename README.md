# AI Chat

## 项目简介

这是一个用于学习 AI 后端开发的练手项目，主要用于熟悉 Python 后端开发、FastAPI 以及 AI 模型 API 的调用流程。

本人自 2024 年从最后一份 Java 开发工作离职后，几乎没有再系统学习开发相关内容。最近重新开始学习 AI 应用开发，在实践过程中重新梳理后端开发中的架构设计、数据管理以及服务拆分。

这个项目会在学习过程中持续迭代。

## 当前功能

目前项目已实现：

* 基于 `conversation_id` 的会话管理
* 多轮对话上下文
* 不同会话之间的消息隔离
* 调用 OpenAI 兼容 API 进行模型对话
* 异步调用模型 API
* 流式输出模型响应
* SQLite 数据持久化
* 基于 Repository 层封装数据库操作
* 会话历史管理与消息数量控制

当前项目结构：

```text
ai-chat
│
├── main.py              # FastAPI 应用入口
├── chat.py              # 聊天流程控制
├── llm.py               # 模型调用封装
├── conversation.py      # 会话业务逻辑
├── repository.py        # 数据访问层
├── database.py          # 数据库连接与初始化
└── chat.db              # SQLite 数据库文件
```

目前暂未实现：

* 用户系统
* 前端交互页面
* 完整的数据库迁移方案

## 技术栈

* **Python**：主要开发语言
* **FastAPI**：构建 Web API
* **Pydantic**：请求参数和响应数据校验
* **OpenAI Python SDK**：调用 OpenAI 兼容接口
* **AsyncOpenAI**：异步模型调用
* **SQLite**：本地数据持久化
* **SiliconFlow / OpenAI 兼容 API**：提供模型服务

## 请求流程

```text
客户端
  ↓
HTTP 请求
  ↓
FastAPI 路由
  ↓
chat 服务
  ↓
conversation 会话管理
  ↓
repository 数据访问层
  ↓
SQLite 数据库

同时：

chat
  ↓
llm
  ↓
OpenAI 兼容 API
  ↓
模型响应
```

## 数据设计

当前主要包含两个核心数据：

### conversation

用于保存会话信息。

示例字段：

```text
id
created_at
```

### message

用于保存聊天消息。

示例字段：

```text
id
conversation_id
role
content
created_at
```

消息通过 `conversation_id` 与会话关联。

## API 接口

### `POST /chat`

发送消息并获取模型回复。

请求示例：

```json
{
  "conversation_id": null,
  "message": "你好，请介绍一下自己！"
}
```

首次请求时：

* `conversation_id` 可以为空
* 服务端创建新的会话

后续请求携带相同的：

```json
{
  "conversation_id": "xxx",
  "message": "继续刚才的话题"
}
```

即可继续多轮对话。

响应示例：

```json
{
  "conversation_id": "xxx",
  "answer": "你好！很高兴认识你。"
}
```

流式接口会以分块形式持续返回模型生成内容。

## 数据持久化

项目使用 SQLite 保存：

* 会话信息
* 历史消息

应用启动时初始化数据库。

数据库文件：

```text
chat.db
```

SQLite 无需单独启动数据库服务，应用通过 Python 标准库直接访问数据库文件。

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

创建 `.env`：

```env
SILICONFLOW_API_KEY=your_api_key
```

### 4. 启动服务

```bash
uvicorn main:app --reload
```

启动后可以通过 FastAPI 自动生成的接口文档测试 API：

```text
/docs
```

## 后续计划

* [ ] 优化 system prompt 与 conversation 数据设计
* [ ] 完善数据库迁移方案
* [ ] 开发简单前端交互页面
* [ ] 支持更多模型参数配置
* [ ] 添加模型切换能力
* [ ] 添加用户系统
* [ ] 实现长期记忆（Memory）
* [ ] 接入 RAG 等 AI 应用能力
* [ ] 探索 AI Agent 与 Workflow 架构
