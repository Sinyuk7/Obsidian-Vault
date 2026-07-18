---
title: AI视频生成提示词标准化规范
aliases:
  - AI视频提示词规范
  - AI Video Prompt Standardization
tags:
  - AIGC
  - AIGC/AI-Video
  - AIGC/Prompt-Engineering
created: 2026-05-31
source_titles:
  - AI视频提示词标准化文档生成
  - AI视频生成标准化提示词规范
source_status: consolidated_from_deleted_inbox_materials
---

# AI视频生成提示词标准化规范

> [!summary]
> AI 视频 prompt 的核心不是把静态图像 prompt 加上 `movement`，而是把主体、空间、动作、镜头、光影、风格和约束组织成同一条可拍摄、可推演、可检查的时间序列。

这份规范用于把 AI 视频生成需求写成稳定、可迁移、可复用的提示词结构。它适合 Sora、Wan、Seedance、可灵等视频模型的共性 prompt 设计，但不把任何单一平台的 UI、参数或版本能力当成通用规则。

## 核心原则

### 1. 视频 prompt 优先描述时空关系

视频模型需要可推演的运动关系。有效 prompt 不只说明“画面里有什么”，还要说明：

- 主体是谁，哪些特征必须保持一致。
- 主体在空间中的位置、朝向、姿态和相对关系。
- 动作从哪里开始、如何变化、在哪里结束。
- 镜头如何运动，是否与主体运动相容。
- 光源、遮挡、接触、重力、惯性和背景变化是否连续。

如果只写最终画面，模型会自行补全时间过程，结果更容易出现身份漂移、动作跳变、镜头混乱或空间关系断裂。

### 2. 主体、动作、镜头必须绑定

主体不能只作为名词出现，动作也不能作为孤立动词追加。每个核心动作都应绑定执行者、方向、节奏和空间结果。

| 维度 | 弱写法 | 稳定写法 |
|---|---|---|
| 主体 | a woman, walking | a woman in a red coat walks from the left side of the frame toward the camera |
| 动作 | slowly moving | she raises her right hand from waist level to shoulder level, pauses, then lowers it |
| 镜头 | cinematic camera | medium shot, camera slowly dollies backward while keeping her centered |
| 空间 | in a street | wet narrow street at night, neon signs reflected on the pavement behind her |

主体运动与镜头运动要形成同一个空间逻辑。例如“相机向前推进、主体向后退、背景快速放大”可能互相冲突；如果要这样写，必须明确它是主观镜头、变焦效果，还是空间压缩效果。

### 3. 每个镜头只承载一个核心动作

短视频生成中，一个镜头同时承载多段叙事会降低可控性。复杂故事应拆成镜头单元，而不是塞进一个长句。

```mermaid
flowchart LR
    A["任务意图"] --> B["主体与不可变特征"]
    B --> C["场景与空间关系"]
    C --> D["动作时间线"]
    D --> E["镜头语法"]
    E --> F["光影与视觉风格"]
    F --> G["技术与安全约束"]
    G --> H["质量检查"]
```

多镜头需求应按 `Shot 1 / Shot 2 / Shot 3` 分段。每个镜头只写一个主要动作、一个主要景别和一组镜头运动。

## 七层 prompt 骨架

| 层级 | 作用 | 必写信息 | 常见失败 |
|---|---|---|---|
| 任务意图 | 定义生成目标 | 视频类型、用途、时长倾向、单镜头或多镜头 | 只写风格，不写要完成什么 |
| 主体 | 锁定身份与连续性 | 人物、物体、服装、不可变特征、姿态 | 主体漂移、服装变形、身份不稳定 |
| 场景 | 建立空间逻辑 | 地点、时代、天气、背景层次、相对位置 | 背景跳变、空间关系不成立 |
| 动作 | 描述时间序列 | beginning、middle、end，动作方向与节奏 | 只有终态，没有过程 |
| 镜头 | 控制观看方式 | 景别、机位、镜头运动、构图焦点 | wide shot、close-up、macro 混写 |
| 视觉风格 | 约束可见结果 | 光影、色彩、材质、摄影术语、后期质感 | 依赖 beautiful、epic、cinematic 等空泛词 |
| 技术与安全约束 | 管理边界 | 画幅、时长、清晰度、平台支持参数、合规边界 | 参数替代语义，或跨平台误用参数 |

> [!tip]
> 通用层写语义与画面控制；平台差异只写在模型支持时才成立的参数或限制。不要把某个模型的参数习惯升级成跨平台规范。

## 标准生成流程

### 1. 定义任务类型

先判断需求属于哪一类：

- 单镜头氛围视频：强调主体状态、微动作、光影和镜头稳定性。
- 动作视频：强调起点、过程、终点、速度和接触关系。
- 参考图驱动视频：先锁定参考对象与不可变特征，再写允许变化的动作。
- 多主体互动：必须写相对位置、接触关系、视线关系和动作先后。
- 多镜头叙事：拆成镜头单元，分别写每个镜头的动作和镜头语法。

### 2. 锁定主体和不可变特征

主体描述要服务于连续性，而不是堆外观词。优先保留：

- 身份：角色、职业、年龄段、物种或对象类型。
- 不可变特征：服装、发型、颜色、标志物、道具。
- 姿态和微动作：posture、gesture、gaze、breathing。
- 多主体关系：谁在左、谁在右、谁接触谁、谁看向谁。

静态主体也应有微运动，否则视频容易变成“静态图轻微晃动”。例如写呼吸、眨眼、衣料轻动、手指轻微调整等。

### 3. 写动作时间线

动作复杂时，用三段式描述：

```text
Beginning: 主体从什么状态开始，位于画面哪里。
Middle: 主体如何移动、转身、抬手、奔跑、交互或改变姿态。
End: 主体停在哪里，最终姿态、视线和空间关系是什么。
```

动作必须可拍摄、可连续、可被短视频时长承载。过长动作会被压缩或省略；互斥动作会导致模型随机取舍。

### 4. 写镜头语法

镜头描述应比“电影感”更具体：

- 景别：wide shot、medium shot、close-up、macro 等不要混在同一镜头。
- 机位：eye-level、low angle、over-the-shoulder、top-down。
- 镜头运动：dolly in、dolly out、pan、tilt、tracking shot、handheld。
- 构图焦点：主体居中、三分构图、前景遮挡、背景纵深。
- 与动作的关系：相机跟随、相机固定、主体穿过画面、相机反向移动。

如果任务强调电影感，优先写镜头、光影、材质和色彩，而不是单独写 `cinematic`。

### 5. 写正向约束

负面提示词不是主要控制手段。更稳的方式是把不希望出现的结果改写成可见的正向状态。

| 目标 | 不稳写法 | 正向替代 |
|---|---|---|
| 避免脸部变形 | no distorted face | stable facial structure, natural eye alignment, consistent facial features |
| 避免多余手指 | no extra fingers | both hands visible with five natural fingers on each hand |
| 避免镜头跳变 | no sudden cuts | single continuous shot, smooth camera movement |
| 避免主体漂移 | do not change clothes | same red coat, same hairstyle, same silver necklace throughout the shot |

涉及人物、版权、未成年人、敏感场景或平台政策时，约束应优先写成合规边界，而不是绕过审核或规避检测的技巧。

## 可复用 prompt 模板

```text
Task:
Create a [single-shot / multi-shot] AI video of [task intention], about [duration] seconds, in [aspect ratio].

Subject:
[main subject], with [immutable identity features: clothing, hair, object, color, posture]. Maintain the same identity and appearance throughout the shot.

Setting:
[location], [time of day / era], [weather / atmosphere], with [foreground / background / spatial relationship].

Action Timeline:
Beginning: [initial position and state].
Middle: [core action, direction, speed, interaction, physical continuity].
End: [final position, posture, gaze, object state, or emotional beat].

Camera:
[shot size], [camera angle], [camera movement], keeping [composition focus] consistent with the subject movement.

Lighting and Visual Style:
[key light], [color palette], [material texture], [photographic or film reference], [visible style result].

Technical Constraints:
[resolution / aspect ratio / duration / model-supported parameters only].

Safety Constraints:
[positive compliance boundaries, identity preservation, no unsafe or policy-violating content].
```

> [!example]- 单镜头示例
> ```text
> Create a single continuous 6-second video in 16:9.
>
> Subject: A young woman in a red raincoat, short black hair, holding a transparent umbrella. Keep the same face, coat, umbrella, and hairstyle throughout the shot.
>
> Setting: A narrow city street at night after rain, neon shop signs reflected on wet pavement, soft mist in the background.
>
> Action Timeline:
> Beginning: She stands near the left third of the frame, looking down at the pavement.
> Middle: She slowly lifts her gaze toward the camera, takes two steps forward, and adjusts the umbrella with her right hand.
> End: She stops at the center of the frame, the umbrella edge catching blue neon light, her expression calm.
>
> Camera: Medium shot, camera slowly dollies backward to maintain distance, smooth handheld feel, no cuts.
>
> Lighting and Visual Style: Soft blue and red neon reflections, wet fabric texture, shallow depth of field, realistic night photography.
>
> Technical Constraints: 6 seconds, 16:9, single shot.
>
> Safety Constraints: Natural facial structure, five natural fingers on each visible hand, stable clothing and umbrella design.
> ```

## 质量检查

生成前逐项检查：

- 主体是否唯一，且不可变特征足够明确。
- 动作是否有起点、过程和终点。
- 动作是否符合重力、惯性、接触、遮挡和空间连续性。
- 镜头运动是否与主体运动相容。
- 每个镜头是否只有一个核心动作和一个主要景别。
- 风格描述是否能转化为可见的光影、色彩、材质或摄影结果。
- 技术参数是否为目标模型真实支持的参数。
- 约束是否以正向可见状态表达。
- 是否写入必要的合规边界，而不是规避策略。

## 常见反模式

| 反模式 | 问题 | 修正方向 |
|---|---|---|
| 静态图 prompt 加 movement | 缺少时间线和镜头逻辑 | 补全 beginning、middle、end 与镜头持续方式 |
| 堆叠抽象形容词 | 模型无法稳定执行 | 改写为光影、材质、色彩、镜头和构图 |
| 多镜头混写成一句话 | 时间段互相污染 | 拆成 Shot 1、Shot 2、Shot 3 |
| 主体和动作分离 | 动作随机附着或主体漂移 | 把动作绑定到具体主体和空间位置 |
| 参数替代描述 | 跨平台失效，语义不足 | 先写语义，再补模型支持的参数 |
| 否定约束堆叠 | 模型反而关注负面对象 | 改写为正向、可见、可检查状态 |
| 忽略输出时长 | 动作被压缩或省略 | 按时长缩小动作范围 |

## 文档化规则

当把一次 prompt 经验整理成知识库文档时，保留可复用层，删除一次性上下文：

- 保留概念、原则、机制、模板、失败原因和检查清单。
- 保留模型差异，但只作为“平台特定层”，不要混入共性规范。
- 示例只服务于抽象规则，不要让文档退化成样例堆。
- 未验证的效果写成倾向，不写成事实。
- 不保留绕过审核、规避检测或弱化安全边界的策略。

相关笔记：[[ai_video_prompt_engineering]]
