---
title: Z-Image Prompt Engineering 使用指南
aliases:
  - Z-Image 提示词工程
  - Z-Image-Turbo Prompt Guide
tags:
  - AIGC
  - AIGC/Z-Image
  - AIGC/Prompt-Engineering
  - model-notes
created: 2026-05-31
updated: 2026-05-31
source_files:
  - doc_zimage_architecture_policy.md
  - prohibited_guidelines.md
  - z-image_prompt_knowledge.md
source_status: original_inbox_sources_deleted_after_curation
---

# Z-Image Prompt Engineering 使用指南

> [!summary]
> `Z-Image-Turbo` 的核心用法是：用一段自然语言正向 prompt 完成主体、场景、光影、风格和约束控制，`guidance_scale` 保持 `0.0`，不要依赖 negative prompt。普通 `Z-Image` 不是同一套参数逻辑：它支持 CFG 和 negative prompting，推荐 `guidance_scale` 约 `3.0-5.0`、`28-50` steps。

这份笔记把原始 inbox 目录下的三份 `Z-Image` 材料合并为一份可复用操作指南，并用官方资料校正了一个关键混淆：**Turbo 规则不能直接套到 Base 模型，Base 规则也不能反套到 Turbo**。

## 先区分模型版本

| 版本 | 定位 | CFG / guidance | Negative prompt | Steps / NFE | 适合场景 |
|---|---|---:|---|---:|---|
| `Z-Image-Turbo` | 蒸馏快模型 | `guidance_scale=0.0` | 不作为控制入口 | 官方称 8 NFE；Diffusers 示例可用 `num_inference_steps=8` 或 `9` | 快速生成、写实图像、中英文字渲染、强指令跟随 |
| `Z-Image` | 非蒸馏 foundation model | 推荐 `3.0-5.0` | 支持，且可用于压制不想要的内容 | 推荐 `28-50` steps | 高质量生成、多样性探索、LoRA / ControlNet 等下游开发 |
| `Z-Image-Edit` | 编辑模型 | 官方模型表显示支持 CFG | 视具体 pipeline | 约 50 steps | 图像编辑、基于自然语言的局部/整体改动 |

> [!warning] 关键纠偏
> 源材料中“z-image 不使用 CFG / negative prompt”的判断只适用于 `Z-Image-Turbo` 或 `guidance_scale < 1` 的运行方式。官方 `Z-Image` 页面明确把 Base 模型列为支持 CFG 与 negative prompting。

## Turbo 的推理策略

`Z-Image-Turbo` 是少步蒸馏版本，默认应把控制压力放到正向 prompt 上，而不是通过传统 SD/SDXL 的“双轨 prompt”策略解决。

推荐基础参数：

| 参数 | 推荐值 | 用法 |
|---|---:|---|
| `guidance_scale` | `0.0` | Turbo 官方示例明确要求 Guidance 为 0。 |
| `negative_prompt` | 留空 | 在无 guidance 时不应作为控制入口。 |
| `num_inference_steps` | `8` 或接近 8 NFE 的设置 | Diffusers 文档示例使用 `8`；官方 README 示例中 `9` 会实际产生 8 次 DiT forward。 |
| `seed` | 迭代时固定，探索时随机 | 固定 seed 便于比较 prompt 改动；随机 seed 便于探索构图、身份与光影变化。 |
| `max_sequence_length` | 默认 `512`，长 prompt 再上调 | 超出默认长度会截断后段描述，尤其影响末段约束。 |

```python
image = pipe(
    prompt=prompt,
    height=1024,
    width=1024,
    num_inference_steps=8,
    guidance_scale=0.0,
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]
```

## Prompt 的主结构

Z-Image 系列更适合自然语言 prompt，而不是 Danbooru / Pony / SDXL 式 tag 堆叠。写法上先建立画面，再逐层加约束。

```mermaid
flowchart LR
    A["镜头与主体"] --> B["成人身份与外观"]
    B --> C["服装与覆盖"]
    C --> D["环境与空间关系"]
    D --> E["光影与氛围"]
    E --> F["风格或媒介"]
    F --> G["技术与清理约束"]
```

| Prompt 部分 | 作用 | 写法要点 |
|---|---|---|
| 镜头与主体 | 决定画面框架 | `medium-shot portrait`、`full-body studio photo`、`wide establishing shot`。 |
| 成人身份与外观 | 降低年龄和身份歧义 | 写清 `adult woman in her 30s`、发型、表情、2-3 个核心视觉特征。 |
| 服装与覆盖 | 控制安全边界和角色气质 | 把 `fully clothed`、`modest professional outfit`、具体衣物放到主体段附近。 |
| 环境与空间 | 锚定上下文 | 用 `modern office`、`quiet classroom`、`plain studio background` 等明确场景词。 |
| 光影与氛围 | 提升画面质感 | `soft diffused daylight`、`studio portrait lighting`、`rim lighting`、`noir high-contrast lighting`。 |
| 风格或媒介 | 控制渲染方式 | `realistic photography`、`cinematic digital art`、`ink illustration`。 |
| 清理约束 | 收束伪影和多余元素 | 放在末段，例如 `clean background`、`text-free`, `sharp focus`。 |

## 正向约束，而不是负向堆叠

Turbo 没有传统 negative prompt 通道，但正向 prompt 里仍可以写约束性描述。实践上要区分两件事：

- `negative_prompt` 参数：Turbo 不应依赖；在 Diffusers 里当 `guidance_scale < 1` 时 negative prompt 会被忽略。
- prompt 内的约束短语：可以写进正向描述，但优先使用肯定、具体、可视觉化的词。

| 不稳定写法 | 更稳写法 | 原因 |
|---|---|---|
| `no people` | `empty street`, `uninhabited room` | 用目标状态替代排除条件。 |
| `no blur` | `sharp focus`, `crisp facial details` | 肯定目标比否定错误更直接。 |
| `no text` | `plain text-free background` | 把“没有文字”变成背景属性。 |
| `not messy` | `simple uncluttered desk` | 把抽象否定改成具体场景。 |
| `no revealing clothing` | `fully clothed, modest professional outfit, arms and legs covered` | 安全边界需要正向服装描述支撑。 |

> [!tip]
> 如果必须用 `no text`、`no watermark`、`no logos` 这类短语，把它们放在 prompt 末段，并同时提供正向替代词，例如 `clean image, plain text-free background, no logos or watermark`。

## 不要把这些当增强器

| 类型 | 问题 | 处理方式 |
|---|---|---|
| Meta quality tags | `8K`、`masterpiece`、`best quality` 信息密度低，容易挤占有效描述。 | 用具体摄影、材质、光影、镜头语言替代。 |
| Tag list | `1girl, solo, long hair` 这类列表来自不同模型生态，句法不适配自然语言 caption。 | 改写成完整句子。 |
| SDXL 权重语法 | `(keyword:1.2)`、`[keyword]` 未必被 Z-Image 语义理解。 | 用更明确的主句和位置顺序控制权重。 |
| 抽象隐喻 | `dreamlike atmosphere`、`ethereal beauty` 不够可视化。 | 拆成光线、色温、背景、表情、材质。 |
| 短而空的 prompt | `a beautiful girl` 会让模型自动补全大量隐含属性。 | 写清身份、年龄、服装、场景、光影、媒介。 |
| 互斥目标 | 同时要求多个主体、多个主视角、多个排版焦点。 | 一张图只保留一个主焦点，其他元素降级为背景或辅助。 |

## 人物与安全边界

人物类 prompt 的安全性和可控性主要靠“身份、服装、场景、姿态”四层共同锁定。

可复用模式：

```text
A medium-shot portrait of an adult woman in her 30s, medium-length brown hair, friendly confident expression, wearing a dark business suit and white shirt, fully clothed with a modest professional outfit, standing in a modern office with a simple uncluttered background, soft diffused daylight, realistic photography with shallow depth of field, clean image, plain text-free background.
```

写人物时优先补齐：

- **成人身份**：`adult woman in her 30s`、`adult man in his 40s`，不要只写 `girl`、`young`、`student`。
- **服装覆盖**：具体衣物优先，例如 `long-sleeve blazer and trousers`，再追加 `fully clothed`。
- **非性化上下文**：办公室、课堂、街景、工作室等场景比暧昧场景更稳。
- **姿态**：`standing upright`、`hands relaxed at sides`、`looking at camera with calm expression`。

## 文字渲染任务

Z-Image-Turbo 的强项之一是中英文字渲染，但 prompt 不能只写 `poster with text`。要明确文本内容、语言、层级、位置和排版关系。

| 需要控制的项 | 示例 |
|---|---|
| 主文本 | `the main title reads "Z-IMAGE"` |
| 次级文本 | `a smaller subtitle below reads "Efficient Image Generation"` |
| 语言与大小写 | `uppercase English letters`, `Chinese characters "造相"` |
| 位置 | `centered at the top`, `bottom-right corner` |
| 字体风格 | `bold sans-serif typography`, `clean editorial layout` |
| 排他性 | `only these two text elements appear`、`plain text-free background outside the title area` |

示例：

```text
A clean technology poster for an image generation model. The main title at the top reads "Z-IMAGE" in bold uppercase sans-serif letters. A smaller subtitle below reads "Efficient Image Generation". The center shows a single abstract camera aperture made of silver and cyan glass, floating above a dark matte surface. Minimal editorial layout, strong alignment, cool studio lighting, high contrast edges, only the specified title and subtitle appear, plain text-free background outside the typography area.
```

## 常见问题诊断

| 症状 | 优先检查 | Prompt 修正 |
|---|---|---|
| 手部或肢体错误 | 是否缺少姿态、手部数量、遮挡关系 | 写 `both hands visible, fingers naturally relaxed, arms hanging at sides`。 |
| 多出人物 | 是否只写了模糊群体或背景人群 | 写 `single main subject`, `empty background`, `no background crowd`，或改成 `one adult person standing alone`。 |
| 背景杂乱 | 场景词是否开放过大 | 改成 `simple uncluttered background`, `plain studio wall`, `clear spatial separation`。 |
| 文本错误 | 是否没有指定准确文本和位置 | 限制文本数量，逐条写出主文本、次文本、位置、大小写。 |
| 风格漂移 | 是否混用了多个媒介和风格词 | 保留一个主媒介，例如只用 `realistic photography` 或只用 `ink illustration`。 |
| 约束无效 | 是否放在过长 prompt 的末尾被截断 | 压缩次要修饰，保留核心主体与末段约束；必要时上调 `max_sequence_length`。 |

## Prompt Enhancer 的边界

Prompt Enhancer 可以把短 prompt 扩展成更细的视觉描述，但它不能替用户改变核心意图。

PE 应遵守：

- 不改变主体、数量、动作、状态、IP 名称、颜色和指定文字。
- 只输出处理后的 prompt 字符串，不附加解释、标题或包装文本。
- 把抽象词转换成可见元素，而不是添加新的剧情。
- 对人物、服装、年龄和安全边界做显式化，而不是弱化约束。

> [!example]- 短 prompt 扩展示例
> 输入：
>
> ```text
> a professional portrait of a software developer
> ```
>
> 输出：
>
> ```text
> A medium-shot professional portrait of an adult software developer in their 30s, short dark hair, glasses, calm focused expression, wearing a dark hoodie over a plain shirt, fully clothed, seated at a clean desk with a laptop in a modern office, soft diffused daylight from the side, realistic photography with shallow depth of field, simple uncluttered background, sharp focus, clean image, plain text-free background.
> ```

## 实用写作准则

1. 先写主体和画面框架，再加细节，不要先堆形容词。
2. 用“具体视觉事实”替代“抽象审美判断”。
3. 人物 prompt 永远显式写成人身份、服装和非性化上下文。
4. Turbo 用单轨正向 prompt；Base 模型可以使用 CFG 与 negative prompt。
5. 固定 seed 用于 AB test，随机 seed 用于探索。
6. 文字渲染任务要写准确文字，不要让模型猜。
7. 避免把审核规避、边界绕过或不安全内容生成写成技巧；安全边界应作为 prompt 约束的一部分。

## Sources

- [Tongyi-MAI/Z-Image GitHub README](https://github.com/Tongyi-MAI/Z-Image)
- [Tongyi-MAI/Z-Image-Turbo Hugging Face model card](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)
- [Tongyi-MAI/Z-Image Hugging Face model card](https://huggingface.co/Tongyi-MAI/Z-Image)
- [Hugging Face Diffusers Z-Image pipeline docs](https://huggingface.co/docs/diffusers/main/en/api/pipelines/z_image)
