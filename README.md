<div align="center">

# Awesome GPT-Image-2

### GPT-Image-2 提示词完全教程

从零到一掌握 OpenAI 最新图像生成模型的提示词技巧

整合自 6 篇深度实测文章 | 30+ 精选提示词 | 覆盖 10 大场景

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-2ea44f?style=for-the-badge)](https://xianyu110.github.io/awesome-gptimage2/)
[![GPT-Image-2](https://img.shields.io/badge/Model-GPT--Image--2-blue?style=for-the-badge)](https://chatgpt.com)

</div>

---

## 使用方法

GPTImage2 模型五种使用方法：

- 官网使用: https://chatgpt.com/
- 国内使用地址：https://chatgpt-plus.top/list/#/home
- API 使用地址：https://apipro.maynor1024.live/
- Codex 使用：https://maynorai.jichiyun.sbs/buy/13
- 国外使用地址：https://gptimage2.asia/

---

## 目录

- [GPT-Image-2 是什么](#gpt-image-2-是什么)
- [核心能力概览](#核心能力概览)
- [两种模式](#两种模式)
- [提示词框架](#提示词框架)
- [提示词合集](#提示词合集)
  - [电商与产品](#一电商与产品)
  - [品牌海报设计](#二品牌海报设计)
  - [创意字体](#三创意字体)
  - [知识科普与信息图](#四知识科普与信息图)
  - [UI 界面复刻](#五ui-界面复刻)
  - [真实摄影](#六真实摄影)
  - [角色与一致性](#七角色与一致性)
  - [图片编辑与参考](#八图片编辑与参考)
  - [艺术创作](#九艺术创作)
  - [趣味玩法](#十趣味玩法)
- [高级技巧](#高级技巧)
- [局限性](#局限性)
- [API 定价](#api-定价)
- [补充案例拆解](#补充案例拆解)

---

## GPT-Image-2 是什么

2026 年 4 月 22 日，OpenAI 正式发布 **ChatGPT Images 2.0**（API 模型名 `gpt-image-2`），奥特曼称之为「从 GPT-3 到 GPT-5 的飞跃」。

它是 OpenAI 首个具备**思考能力**的图像模型，在 Arena 盲测榜单中以断层优势登顶全球第一，领先第二名 Nano Banana 2 超过 240 分。

**关键参数：**

| 特性 | 详情 |
|------|------|
| 知识截止 | 2025 年 12 月 |
| 最大分辨率 | 2K（API Beta） |
| 宽高比 | 3:1 ~ 1:3 |
| 单次生成 | 最多 8 张连贯图（Thinking 模式） |
| 生成速度 | 约 3 秒/张（Instant 模式） |
| 多语言 | 中文、日文、韩文、印地语等 |
| 入口 | ChatGPT / Codex / API |

---

## 核心能力概览

### 1. 文字渲染（质的飞跃）

文字渲染一直是 AI 图像模型最大的痛点。GPT-Image-2 在中文渲染上实现了质的突破：

- 可以**默写出师表**，绝大多数文字保持稳定
- 能生成完整的**中文报纸**、**数学试卷**
- 支持**红楼梦关系图**等复杂信息图表
- 从一张照片直接生成**完整的电商产品详情页**

> **关键提示：** 中文文字不再是「贴图感」，而是真正融入了视觉设计的骨架。

### 2. 世界知识（最强护城河）

这是 GPT-Image-2 与其他模型拉开差距最大的能力。它对真实世界长什么样有着极其精准的理解：

- 生成 YouTube 首页截图 — 正确的布局、按钮样式、图标位置
- 生成小红书/B 站个人主页 — 甚至会自动编造完整的人设
- 游戏代肝海报 — 自动补充「1000 万哈夫币比 56 人民币」等专业文案
- 汽车官网 — 仅凭一张车辆照片就生成完整的品牌官网

### 3. 修改精准度

对你意图的理解达到了一个离谱的程度：

- 一张手机随手拍的产品照 → 两句话 → 完整的电商详情页
- 上传电影截图 + 参考图 → 替换人物并保持场景一致
- 上传产品图 → 精修白底电商主图（白色背景、柔光、阴影自然）

### 4. 审美进化

最大的审美进化是学会了保留**「不完美」**：

- 胶片颗粒感、闪光灯硬阴影、手持拍摄轻微失焦
- 风格覆盖极广：电影静帧、复古胶片、时尚摄影、像素画、漫画
- **最有效的关键词就是 `photorealistic`** — 模型会主动规避塑料感

### 5. 界面与布局生成

全新的能力维度，能精准复刻各种数字界面：

- 社交媒体截图（抖音、小红书、B 站、TikTok、YouTube）
- App UI 界面（电商首页、音乐播放器）
- 游戏画面（黑悟空等）
- 桌面环境（macOS 浏览器截图、Terminal）

---

## 两种模式

### Instant 模式（即时模式）

- 对所有 ChatGPT 用户开放
- 生成速度约 3 秒/张
- 适合日常快速出图

### Thinking 模式（思考模式）

- 需要 ChatGPT Plus / Pro / Business 账户
- 模型会先**联网搜索**、**规划结构**、**自我核查**
- 单次最多生成 **8 张角色和对象连贯**的系列图片
- 适合复杂信息图、教育内容、多图连贯场景

---

## 提示词框架

经过大量实测，以下提示词框架效果最佳：

```
[任务类型] + [主体描述] + [风格定义] + [技术参数] + [输出规格]
```

### 五要素详解

| 要素 | 说明 | 示例 |
|------|------|------|
| 任务类型 | 告诉模型做什么 | 海报设计 / 信息图 / 界面截图 / 摄影照片 |
| 主体描述 | 画面核心内容 | 产品、人物、场景、信息结构 |
| 风格定义 | 视觉风格和调性 | 新中式轻奢 / 胶片纪实 / 极简科技 / 手绘水彩 |
| 技术参数 | 光影、材质、构图 | 柔光打光 / 浅景深 / 电影级打光 / octane 渲染 |
| 输出规格 | 比例和分辨率 | 3:4 / 9:16 / 4K / 8K |

### 核心原则

1. **具体 > 模糊**：描述越具体，输出越精准
2. **中文直接说**：不需要翻译成英文，中文提示词效果一样好
3. **给出文字内容**：直接把需要出现在图中的文字写在提示词里
4. **指定风格参考**：用「参考 XX 风格」来锚定审美方向
5. **标注比例和分辨率**：如 `3:4, 4K` 可以控制输出尺寸

---

## 提示词合集

> 以下提示词均可直接复制到 ChatGPT 中使用。点击代码块右上角即可复制。

### 一、电商与产品

#### 1.1 香水电商详情页

```text
（有香水垫图）给这个香水产品生成电商中文详情页，9:16，4k
```

![香水电商详情页](https://upload.maynor1024.live/file/1776831281195_wx_003_09ee24278e.png)
![香水电商详情页-长图](https://upload.maynor1024.live/file/1776831281454_wx_005_d0df16a605.jpg)

#### 1.2 产品精修白底图

```text
帮我生成一张图片，将该产品进行精修，可重新打光，精修优化，白色的背景。
```

![产品精修白底图-原图](https://upload.maynor1024.live/file/1776831496827_wx_057_b9f505e33e.jpg)
![产品精修白底图-效果](https://upload.maynor1024.live/file/1776831501923_wx_058_991727c87e.png)

#### 1.3 产品详情长图

```text
帮我做一张这个产品的电商详情页海报。
```

![产品详情长图](https://upload.maynor1024.live/file/1776831510634_wx_059_d6a1b6d749.png)

#### 1.4 护肤品电商首图

```text
高端护肤品电商首图海报，产品名为 澄光维稳精华。整体风格干净、轻奢、科学护肤感强，画面中心是一瓶半透明磨砂玻璃精华液，带淡金色液体和水珠反光，背景为奶白到暖灰渐变，局部有液体流动与微观分子结构装饰。要求同时具备品牌感和卖货感。

海报必须包含以下文案：
澄光 维稳精华
修护屏障 舒缓泛红 细腻透亮
第 2 代升级配方
核心成分 神经酰胺 泛醇 B5 积雪草提取物 微囊脂质体
适合人群 敏感肌 熬夜肌 换季不稳定肌
限时到手价 229 元 买 1 送 3
赠洁面 15ml 赠精华 5ml 赠面霜 10g
左下角小字：实际效果因人而异，请坚持使用

要求重点测试商品卖点、价格、赠品列表、产品名与功能短句的层级。整体要高级，不能土，不要过度直播间风格。
```

![护肤品电商首图-GPT](https://upload.maynor1024.live/file/1776480570690_img_048.png)
![护肤品电商首图-Banana对比](https://upload.maynor1024.live/file/1776480180588_img_012.png)

#### 1.5 高保真电商 App 首页

```text
生成一张高保真移动端电商 App 首页界面截图，整体风格参考 2026 年主流中文电商 App，要求界面极其真实，具有完整的手机应用 UI 逻辑与商业设计感。页面顶部为状态栏，包含时间 9:41、5G 信号、电量图标。下面是搜索框区域，左侧为城市选择 杭州，中央是圆角搜索框，提示词为 搜索耳机、咖啡机、运动鞋，右侧有消息图标和扫一扫图标。搜索区下方是横向分类标签，包含 推荐、数码、家电、服饰、美妆、食品、运动、家居，其中 推荐 高亮选中。

首页主体内容必须包含以下结构并排版清晰：
顶部轮播 Banner 一张，主题为 618 预售开启，副标题 每满300减50，画面带商品海报和红色促销氛围
Banner 下方为 10 宫格功能区，图标风格统一，包含 超市、百亿补贴、秒杀、直播、充值中心、到家、领券、品牌馆、全球购、排行榜
中部为 限时秒杀 模块，左侧标题，右侧倒计时 02:14:39，下方三件商品卡片横向排列，每件商品含商品图、标题、现价、原价、已售进度条
下方为 猜你喜欢 双列商品瀑布流，至少 6 张商品卡，每张卡片包含商品图、两行商品标题、价格、月销、店铺名、好评率、券后价标签
底部固定 Tab Bar，包含 首页、分类、购物车、消息、我的，其中 首页 为高亮状态

要求：所有中文文字清晰、可读、接近真实字体，图标统一，间距合理，留白真实，卡片阴影、圆角、分隔线、标签样式高度像真实 App，不要生成手机外壳，只输出纯界面截图，整体必须让人一眼觉得是真实电商 App 截图，而不是概念图
```

![电商App首页-GPT](https://upload.maynor1024.live/file/1776480347969_img_025.png)
![电商App首页-Banana对比](https://upload.maynor1024.live/file/1776480513320_img_041.png)

#### 1.6 招聘海报（含完整 JD）

```text
（附上职位 JD 文字）请根据以上职位描述生成招聘海报
```

![招聘海报-GPT](https://upload.maynor1024.live/file/1776480424783_img_033.jpg)
![招聘海报-Banana对比](https://upload.maynor1024.live/file/1776480204166_img_014.png)
![招聘海报-卡兹克版](https://upload.maynor1024.live/file/1776831481746_wx_052_6f6930ac10.png)

#### 1.7 茶饮新品上市海报

```text
请设计一张 3:4 竖版国潮茶饮新品上市海报，品牌名为 山川茶事。整体风格新中式、轻奢、克制，颜色以墨绿、米白、金色为主，融合宣纸肌理、留白、淡雅山水、现代版式设计。画面主体是一杯高颜值冷泡茶与茶叶、柑橘、冰块、金箔元素，画面必须兼具商业感与审美感。

海报中必须准确呈现以下文字：
山川茶事 山柚观音 冷泡系列 新品上市
一口清醒，半城入夏
限定尝鲜价 中杯 16 元 大杯 19 元
门店活动 第二杯半价 加 3 元升级轻乳版
每日前 100 名赠限定杯套
推荐风味 观音茶底 / 西柚果香 / 轻乳云顶 / 冰感回甘
活动时间 4月20日 至 5月10日
扫码点单 SHANCHUAN TEA
底部小字：图片仅供参考，请以门店实际售卖为准

要求海报具备明显促销信息层级，同时依旧精致，不要做成廉价电商海报。
```

![茶饮海报-GPT](https://upload.maynor1024.live/file/1776480372187_img_027.png)
![茶饮海报-Banana对比](https://upload.maynor1024.live/file/1776480582117_img_049.png)

---

### 二、品牌海报设计

#### 2.1 品牌入驻宣传海报

```text
生成【茶颜悦色】2026.5.1入驻深圳万象天地的宣传海报，3:4，4k
```

![茶颜悦色海报](https://upload.maynor1024.live/file/1776831281454_wx_005_d0df16a605.jpg)

#### 2.2 定制 T 恤宣传图

```text
为科技自媒体量子位设计定制T恤，生成宣传图
```

![量子位定制T恤](https://upload.maynor1024.live/file/1776831573117_wx_075_530b0ce4a7.png)

#### 2.3 迪特拉姆斯设计十戒海报

```text
迪特拉姆斯的设计十戒做一张海报，每条戒律都配上博朗的超级经典的产品。灵感参考奏笙。
```

![迪特拉姆斯设计十戒](https://upload.maynor1024.live/file/1776831295835_wx_010_e3e82879b5.jpg)

#### 2.4 书籍封面设计

```text
书籍封面设计：标题为"阿勒泰的角落"，作者"李娟"。以广袤的绿色草地为主背景，深浅不一的草叶构成自然层次感，远处绘制若隐若现的山脉轮廓。画面中央放置孤立的白羊剪影，上方用简洁白色字体呈现中英文书名"The Corner of Altay"。整体采用清新自然的森系配色，营造出空灵悠远的文学意境
```

![阿勒泰的角落-书籍封面](https://upload.maynor1024.live/file/1776831299547_wx_011_91db5d4dd0.jpg)

#### 2.5 K-POP 概念海报

```text
生成一张 K-POP 女团第三张迷你专辑的概念海报，专辑名 ECLIPSE。所有人都穿黑色系造型，打光是侧逆光加柔焦，整体色调偏冷灰蓝，肢体、影子自然真实，脸部细节、发丝、饰品光泽、布料褶皱质感精致，每个人有不同的 pose 和表情。
```

![K-POP概念海报](https://upload.maynor1024.live/file/1776831522030_wx_065_a4d181f295.jpg)

#### 2.6 论文宣传海报

```text
（上传论文 PDF）请根据这篇论文生成对应的宣传海报
```

![论文宣传海报](https://upload.maynor1024.live/file/1776831579409_wx_076_204bdd9bf8.png)
![论文海报-官方Demo](https://upload.maynor1024.live/file/1776831828931_wx_126_04f0238e6a.png)

---

### 三、创意字体

#### 3.1 城市创意字体 — 杭州

```text
字体设计，创意字体插画，将文字"杭州"作为主体画面，以文字为画布进行深度重构。
"杭"字内部融合杭州标志性建筑轮廓与场景元素，如西湖断桥、雷峰塔、湖岸柳树与远山轮廓，所有元素顺应笔画走势自然生成，结构一体化，不可拼贴堆砌。
"州"字内部融合地域文化符号与生活意象，如西湖龙井茶叶、丝绸飘带、水乡屋檐、小桥流水，元素与字体笔画交织生长，形成有机结构。
整体风格为江南水乡意境，线条柔和流动，辅以西湖水波纹理在笔画间隐约扩散，增强空间层次与韵律感。
色彩以低饱和东方配色为主（青灰、淡绿、米白、浅墨色），营造温润、诗意、含蓄的视觉氛围。
背景为干净米白色宣纸质感，带轻微纸张纹理。3:2,4k
画面要求：高精细插画风格，结构清晰但富有艺术表现力，元素融合自然，无明显边界，避免卡通化与过度装饰，整体具有高级设计感与文化审美。
```

![GitHub链接生成主页](https://upload.maynor1024.live/file/1776831318135_wx_017_c335b14da9.jpg)

![杭州创意字体](https://upload.maynor1024.live/file/1776831289910_wx_006_765d19045a.jpg)

> **替换技巧：** 将「杭州」替换为任意城市名，并将对应的建筑、文化符号进行替换即可生成其他城市的创意字体。

---

### 四、知识科普与信息图

#### 4.1 科普百科图 — 萨摩耶

```text
请根据【萨摩耶】生成一张高质量竖版「科普百科图」。

这张图不是普通海报，也不是单纯插画，而是一张兼具"图鉴感、百科感、信息结构感、收藏感"的模块化科普信息图。整体风格参考高级博物图鉴、现代百科书页、生活方式知识卡和社交媒体高传播信息图的结合。

请让画面包含：
- 一个清晰漂亮的主题主视觉
- 若干局部特征放大细节
- 多个圆角模块化信息分区
- 清楚的标题层级与重点标签
- 简洁但丰富的百科内容
- 可视化评分、要点总结或 Top 5 模块

内容栏目请根据主题自动适配，优先从这些方向中选择并合理组合：
基础档案、分类信息、外观特征、习性/生态、形成机制/结构组成、生长或使用条件、养护或维护建议、风险与注意事项、适合人群或适用场景、优缺点对比、快速评分卡。

视觉要求：浅色干净背景，柔和配色，轻阴影，精致小图标，圆角信息框，整洁排版，信息密度高但不拥挤，阅读体验好。整体必须像真正可以发布、阅读、收藏、系列化生产的科普百科卡，而不是广告图。
请不要做成普通商业宣传海报。要突出"知识整理 + 模块信息 + 图鉴式展示"的特征。
```

![萨摩耶科普百科图](https://upload.maynor1024.live/file/1776831306943_wx_012_0a46c0f1cc.png)

> **替换技巧：** 将「萨摩耶」替换为任何主题（动物、植物、产品、技术概念等），即可生成对应主题的科普百科图。

#### 4.2 心肺复苏急救讲解图

```text
生成 "心肺复苏急救步骤"讲解图，技术词汇用大众词汇替代，中文对白，整体用 Chiikawa 作为形象引导，纯中文，信息要足够详细准确，比例 9:16，4k
```

![心肺复苏急救讲解图](https://upload.maynor1024.live/file/1776831293062_wx_008_64263de1fa.png)

#### 4.3 咖啡科普信息长图

```text
中文信息图海报，主题为 一杯咖啡如何来到你手里。风格为高级信息设计，兼具科普感与商业视觉感，版式清晰，带有路径箭头、数据框、图标、简洁插画和模块化卡片。色调以咖啡棕、奶白、墨黑、少量铜色点缀。要求图文并重，信息非常多，但仍然好看。

海报必须完整展示以下内容：
一杯咖啡 如何来到你手里
01 种植 海拔 1200 至 2200 米 适宜温度 18℃ 至 24℃ 采摘期通常集中在 11 月至次年 3 月
02 处理 日晒 水洗 蜜处理
03 烘焙 浅烘 更明亮 中烘 更平衡 深烘 更浓郁
04 研磨 手冲偏粗 意式偏细 冷萃中粗
05 萃取 粉水比 水温 时间 都会影响风味
风味关键词 花香 / 柑橘 / 坚果 / 焦糖 / 巧克力 / 烟熏
你喝到的每一口 都来自一连串精密选择
底部小字：适合用于咖啡入门科普与门店展示

重点测试长信息图、数字、温度、编号、短说明、斜杠风味词和多模块排版。要让它看起来像高质量展板，不要像课堂PPT。
```

![咖啡科普信息长图-GPT](https://upload.maynor1024.live/file/1776480487938_img_040.png)
![咖啡科普信息长图-Banana对比](https://upload.maynor1024.live/file/1776480520485_img_042.png)

#### 4.4 植物光合作用科普图

```text
用中文给我制作一张科普图片，讲述详细的植物进行光合作用的原理
```

![光合作用科普图-GPT](https://upload.maynor1024.live/file/1776480243135_img_017.png)
![光合作用科普图-Banana对比](https://upload.maynor1024.live/file/1776480298004_img_021.png)

#### 4.5 五代十国历史演示图

```text
生成一张【五代十国】的历史演示图，保证信息准确清晰，3:4,4k
```

![五代十国历史图](https://upload.maynor1024.live/file/1776831312682_wx_014_552e4c3807.jpg)

#### 4.6 Mariah Carey 信息长图

```text
生成一张 Mariah Carey 90 年代生涯图的中文信息长图
```

![Mariah Carey信息长图](https://upload.maynor1024.live/file/1776831533822_wx_066_832cf34e82.jpg)

#### 4.7 原神推荐海报

```text
生成关于原神玩法的推荐海报，官方设定风格
```

![原神推荐海报](https://upload.maynor1024.live/file/1776831585290_wx_077_ed366cc331.png)

---

### 五、UI 界面复刻

#### 5.1 TikTok 视频截图

```text
生成一张 TikTok 的妆教视频截图
```

![TikTok妆教截图](https://upload.maynor1024.live/file/1776831565116_wx_073_1bf5c77bf8.jpg)
![TikTok对比-真实vs生成](https://upload.maynor1024.live/file/1776831573593_wx_074_47bc06e053.png)

#### 5.2 GPT 对话截图

```text
生成一张和 GPT 的对话截图
```

![GPT对话截图](https://upload.maynor1024.live/file/1776831559892_wx_072_2467589688.png)
![macOS浏览器ChatGPT截图](https://upload.maynor1024.live/file/1776831771912_wx_114_6109d12b51.png)

#### 5.3 音乐 App 播放页

```text
生成一张高保真中文音乐 App 播放页界面截图，移动端竖屏，视觉精致，风格接近现代流媒体播放器。整体以深色模式为主，背景来自专辑封面的模糊扩散色，中央是大尺寸方形专辑封面，带微弱阴影和圆角。顶部状态栏时间 18:26。导航栏左侧返回箭头，中间标题 正在播放，右侧更多操作图标。

页面需包含以下信息并排版真实：
歌曲名：海边的晚风 歌手：林秋 专辑名：夏夜实验室
播放进度条，当前时间 01:42，总时长 04:18
控制按钮包括 随机、上一首、播放暂停、下一首、循环
下方有歌词区域，显示 5 到 7 行滚动歌词，其中当前播放行高亮，其余行弱化
再下方有 喜欢、评论、下载、收藏到歌单、分享 按钮行
页面底部有设备投放与播放队列入口

要求：歌词排版要有真实的音乐播放器体验，深色层级、按钮图标、进度条反光与阴影要真实，中英文数字混排自然，整体像可直接上架的产品界面，而不是 Dribbble 概念稿
```

![音乐App播放页-GPT](https://upload.maynor1024.live/file/1776480546859_img_045.png)
![音乐App播放页-Banana对比](https://upload.maynor1024.live/file/1776480322063_img_024.png)

#### 5.4 游戏画面复刻

```text
生成黑悟空神话，被二郎神打飞的游戏画面
```

![黑悟空游戏画面-GPT](https://upload.maynor1024.live/file/1776480398301_img_029.jpg)
![黑悟空游戏画面-Banana对比](https://upload.maynor1024.live/file/1776480546209_img_044.png)

#### 5.5 macOS 浏览器截图

```text
生成一张 macOS 浏览器中 ChatGPT 窗口的截图，桌面杂乱，后台开着终端等随机窗口
```

![macOS浏览器截图](https://upload.maynor1024.live/file/1776831359629_wx_023_73568a3498.jpg)

---

### 六、真实摄影

#### 6.1 商场纪实抓拍

```text
生成一张极其真实的商场纪实摄影照片，场景是周末傍晚的大型购物中心扶梯口，一位 30 岁左右的亚洲男性刚从上行扶梯走下来，左手拎着购物袋，右手正在低头回消息，神态自然，没有看镜头。他穿深灰色连帽卫衣外搭黑色薄夹克，下身是宽松卡其裤和轻微磨损的运动鞋，头发略乱，脸上有一点出油感和下巴胡茬。商场灯光是复杂的混合光，顶部暖白灯、品牌橱窗冷白灯、远处广告屏彩色光同时存在，地面是高反光瓷砖，能看到模糊但真实的倒影。背景里有经过的人群、奶茶店招牌、玻璃护栏、模糊品牌海报。要求像摄影师在商场里抓拍的真实瞬间，不能像时尚街拍摆拍，皮肤、衣服、鞋面、购物袋折痕、玻璃反射都要非常真实。
```

![商场纪实-GPT](https://upload.maynor1024.live/file/1776480142529_img_008.jpg)
![商场纪实-Banana对比](https://upload.maynor1024.live/file/1776480459907_img_037.jpg)

#### 6.2 便利店群像

```text
生成一张超真实的城市街头群像照片，场景是夏夜十点的便利店门口，三到四个年轻人正在门口短暂停留聊天，有人拿着饮料，有人坐在店外塑料椅上，有人站着低头看手机。便利店的玻璃门和橱窗透出明亮白光，外面路边则是暖黄街灯和远处车灯。人物穿搭非常日常，包含 T 恤、衬衫、短裤、牛仔裤、运动鞋，不要网红穿搭感，脸部状态和体态都要像真实路人，不能每个人都过于精致。环境要有真实便利店元素，冰柜贴纸、促销海报、垃圾桶、门口地垫、玻璃倒影、路边共享单车、地面饮料瓶水珠。画面像摄影师在城市里拍到的一张非常真实的生活切片，重点测试多人自然互动、夜间便利店灯光、玻璃反射和普通人气质的还原能力。
```

![便利店群像-GPT](https://upload.maynor1024.live/file/1776480162164_img_010.jpg)
![便利店群像-Banana对比](https://upload.maynor1024.live/file/1776480308544_img_022.png)

#### 6.3 四季眼部特写

```text
超写实眼部特写，macro 极致微距摄影，皮肤纹理清晰可见，睫毛细节真实，虹膜高精度细节，镜头紧贴眼睛，画面极致精致与通透，梦幻光影氛围，电影级打光，浅景深，背景虚化，光斑柔和，四屏竖向分割构图（3:4 比例），从上到下依次为春、夏、秋、冬，每一屏保持同一只眼睛的一致性

春：粉色樱花环绕，花瓣漂浮，蝴蝶点缀，柔和暖光，粉色与金色微光粒子，梦幻浪漫氛围；夏：绿色植物、露珠、水汽，清透高光，阳光穿透感，蜻蜓或荷花元素，清新明亮；秋：橙红枫叶，暖金色阳光，落叶环绕，光影浓郁，温暖厚重的氛围，蝴蝶或飞叶动态；冬：冰霜、雪花结晶覆盖睫毛与皮肤，冷蓝色调，雾气与寒气，细腻冰晶结构，高对比冷光。每一屏加入对应季节英文+中文文字（SPRING 春 / SUMMER 夏 / AUTUMN 秋 / WINTER 冬），轻微融入画面，高细节 3:4，8K，cinematic lighting，unreal detail，photorealistic，volumetric light，global illumination
```

![四季眼部特写](https://upload.maynor1024.live/file/1776831287228_wx_007_8fe3f95823.jpg)

#### 6.4 胶片质感抓拍

```text
一张写实风格的旅行抓拍：阴天清晨，一个人站在海边路旁的观景停车带，用 35mm 胶片拍摄。构图自然、略有瑕疵，颗粒感明显，环境光漫射，色调低饱和，衣物和发丝随风飘动，带着纪录片式的电影质感，像是某段真实生活留下的影像。
```

![胶片质感抓拍](https://upload.maynor1024.live/file/1776831365390_wx_027_704e3946d9.jpg)

#### 6.5 photorealistic 关键词

```text
photorealistic
```

> OpenAI 研究员 Alex 透露：**想让输出最自然，最有效的关键词就是 `photorealistic`**。只要打出这个词，模型就会主动规避塑料感，复刻那些让照片「看起来是照片」的真实特征。

---

### 七、角色与一致性

#### 7.1 八套穿搭一致性

```text
（上传一张人物照片）请根据这张照片，生成八套夏日穿搭方案
```

![八套夏日穿搭](https://upload.maynor1024.live/file/1776831377557_wx_030_f3ed0f1175.png)
![穿搭多角度展示](https://upload.maynor1024.live/file/1776831381499_wx_031_671c4b4aef.png)

#### 7.2 十六宫格动漫表情包

```text
生成一个有着银色长发和蓝色眼瞳的二次元动漫少女的十六宫格表情图。她的脸型、发型、服装必须在所有格子里保持高度一致。十六个表情需要包含：开心、难过、愤怒、惊讶、害羞、无语、坏笑、沉思、好奇、得意、委屈、鄙视、困惑、害怕、流泪、以及一个爱心的表情。
```

![十六宫格表情包-GPT](https://upload.maynor1024.live/file/1776480562503_img_047.png)
![十六宫格-参考图](https://upload.maynor1024.live/file/1776480440768_img_035.jpg)
![十六宫格-Banana对比](https://upload.maynor1024.live/file/1776480154322_img_009.jpg)

#### 7.3 杂志封面（多人一致）

```text
（上传四人合照）根据这张照片生成一张杂志封面
```

![杂志封面](https://upload.maynor1024.live/file/1776831738119_wx_110_90c91e28cc.png)
![杂志封面-细节](https://upload.maynor1024.live/file/1776831746143_wx_111_b4a4a2fe96.png)

---

### 八、图片编辑与参考

#### 8.1 宠物联名海报

```text
以「77（猫的名字）X 肯德基」联名企划为主题，围绕同一只宠物（形象、花色等与上传图片绝对一致）生成一张联名海报。统一宠物形象与肯德基品牌识别（红白配色、经典 LOGO、餐厅场景等）的前提下，让小猫穿肯德基员工制服、带上肯德基员工帽子，佩戴工牌站在柜台前、兜售炸鸡、汉堡和套餐、与炸鸡桶、薯条、汽水等元素互动等。画面风格活泼、有趣、具有商业联名感，适合用于线上宣传与活动海报。然后自由的为这张海报添加合适的中文内容。
```

![宠物联名海报-GPT](https://upload.maynor1024.live/file/1776480357820_img_026.png)
![宠物联名海报-原图](https://upload.maynor1024.live/file/1776480139049_img_007.jpg)
![宠物联名海报-Banana对比](https://upload.maynor1024.live/file/1776480282909_img_020.png)

#### 8.2 海报风格复刻

```text
（上传一张风格化海报）请参考这张海报的风格，保持排版、字体、构图的一致性，将春天场景改为冬天场景后重新生成
```

![海报复刻-原图](https://upload.maynor1024.live/file/1776480232760_img_016.png)
![海报复刻-GPT](https://upload.maynor1024.live/file/1776480461550_img_036.jpg)
![海报复刻-Banana对比](https://upload.maynor1024.live/file/1776480090260_img_002.jpg)

#### 8.3 漫画上色翻译

```text
给这张漫画页上色并翻译成中文放到图中原来的位置，保持构图和图片细节的一致
```

![漫画上色-原图](https://upload.maynor1024.live/file/1776480214370_img_015.png)
![漫画上色-Banana](https://upload.maynor1024.live/file/1776480298004_img_021.png)
![漫画上色-GPT](https://upload.maynor1024.live/file/1776480383663_img_028.jpg)

#### 8.4 电影截图换人

```text
（上传《闪灵》经典画面 + 迪迦奥特曼参考图 + 黄色猫咪参考图）请将门缝里的人物替换为迪迦奥特曼
```

![闪灵换人-参考图](https://upload.maynor1024.live/file/1776831508063_wx_060_abc2ec5dcb.png)
![闪灵换人-效果](https://upload.maynor1024.live/file/1776831512087_wx_061_445b06e867.png)
![闪灵换人-奥特曼版](https://upload.maynor1024.live/file/1776831516785_wx_062_37013926d4.png)

#### 8.5 GitHub 链接生成主页

```text
https://github.com/你的用户名/你的仓库 根据这个 GitHub 链接，生成一张个人 AI 自媒体介绍主页，9:16, 4k，要日式侘寂风格作为背景，内容分类艺术拼贴。（垫一张 IP 形象图）
```

#### 8.6 公众号封面（人物 + 主题互动）

```text
（垫一张人物 IP 图）设计做 1 张 21:9 的公众号封面，大标题是"又被 GPT image 2 硬控了"，需要你将图片人物（换个艺术穿搭，保持人物一致性的半身照）与封面主题设计的有互动搭配，用白色线条描绘人物最外面的轮廓，适配标题去搭高级浅色背景和标题元素，4k 输出。
```

![公众号封面-GPT Image 2硬控](https://upload.maynor1024.live/file/1776831323900_wx_018_16e48490f1.png)

---

### 九、艺术创作

#### 9.1 海贼王 3D 纸雕

```text
平视视角，正面直视一个高饱和度 3D 多层纸雕场景。
整体为灰蓝、奶油白、深森林绿，点缀琥珀色暖光。所有元素必须是实体纸张分层结构，边缘为硬切割效果，并清晰可见厚纸横截面。
极致丰富构图，一个高能量的海盗群像场景，发生在混乱的海上冒险中。多个风格化海盗角色以夸张动作呈现，中层核心是一位戴草帽的年轻船长向前冲刺，周围是姿态鲜明的船员。
分层的船只、翻涌海浪和旋转洋流贯穿前中后景，多艘船在不同空间层中碰撞倾斜，船帆破损、旗帜飞扬。
背景层中出现体型巨大的对立角色剪影，增强压迫感和空间层级。
前景堆满叙事元素：宝箱、金币、地图、木桶、绳索、灯笼，以及一张带笑脸海盗的通缉令。角落放置一个吉祥物式小角色作为视觉锚点。
所有氛围元素以纸雕形式呈现：海浪、水花、烟雾、碎片、动势线，强化混乱与动感。
主体位于中层，元素跨层互动，通过重叠和空间关系表达运动感。
单一方向柔光，形成清晰层间投影。整体为哑光纸张质感，无发光、无柔边、无体积光。
octane 渲染，8K，细节清晰 3:4
```

![海贼王3D纸雕](https://upload.maynor1024.live/file/1776831295947_wx_009_83a98eb04d.jpg)

#### 9.2 花卉 Knolling 解构

```text
Knolling 风格摄影，一朵被完全解构的【蓝花楹】，植物解剖学概念，严格垂直顶视，平铺摆放。花瓣大量铺陈，整体以 Bento Grid 作为排列逻辑，同时带有自然轻微随机性。花瓣从大到小、从深到浅呈渐变规律，局部方向略有偏转。包括雄蕊簇、花萼、叶片、花茎横切面等组件，位置不刻意对称但保持整体秩序。每一张的右下角用中文行书小字展示鲜花的名称。

画面边缘需保留一处用于放置金属镊子，镊子为不锈钢材质、细长直形，轻轻置于边缘，与花瓣布局保持协调，不抢主体，方向自然，光影一致。镊子位置固定在画面外缘附近，但不遮挡任何花瓣或标签。

光影与质感：从边缘到边缘填满画面，无留白；柔和影棚布光，无硬阴影；8k 超高清、超写实微距质感，天鹅绒花瓣细节清晰；纯白背景，比例 3:4。
```

![蓝花楹Knolling解构](https://upload.maynor1024.live/file/1776831307340_wx_013_c3c9376556.jpg)

#### 9.3 手绘涂鸦读书笔记

```text
请根据"【防颓指南】混一天和努力一天看不到任何差别，三天看不到任何变化，七天也可以说看不到任何距离。但是一个月后悔看到话题不同，三个月后悔看到气场不同，半年后会看到一定距离，一年后会看到人生道路不同。你继续堕落下去的话，你的天赋就会被全部收走，你身边原本比你差的人也会靠努力一个一个超越你，你继续差的话也没人会等你。所以请不要在该吃苦的年纪选择安逸，走自己的路为自己的梦想奋斗，即使有人亏待你，时间和人生也不会亏待你。"输入内容,生成一张手绘涂鸦风格的读书笔记信息图,并严格遵循以下风格:

1. 整体风格与媒介: 采用充满活力的手绘涂鸦笔记风格,专业知识笔记的学霸风格,不要太卡通。黑色使用深棕、橙黄或海军蓝,轻微水彩进行填色,并搭配柔和的黑色或深棕色细线等勾勒轮廓。竖版(3:4)构图。
2. 配色方案(关键):整张图都应该是彩色的,采用明亮、清新、和谐的色彩组合(海军蓝、浅蓝、金色、奶油色背景)背景应有淡淡纸张纹理的米色,或者直接留白,但画面主体必须是五彩斑斓的。颜色填充应模仿彩铅或水彩的质感,带有自然的笔触感,而不是均匀的数字平涂。
3. 线条特征: 所有轮廓线都必须是不完美、略带抖动的手绘线条,给人一种柔软、亲切的感觉。
4. 字体风格:所有文字都必须是彩色的手写体,绝对不要使用任何电脑字体。标题和关键词使用加粗的、或带有简单边框的手写艺术字来突出。正文和注释使用清晰、自然的个人笔记手写体。
```

#### 9.4 田园水彩旅行攻略

```text
【24号：早教场中路看花--文化巷/云南大学--翠湖公园--昆明老街--南强夜市 25号:上午打车去捞鱼河湿地公园（包含有风小院花田、古桩月季园）--斗南花市 26号：盘龙江看花--篆新农贸市场--然后12点之前出发去机场】

就以上的文字不要增减，生成一张田园水彩速写 / 自然风物图鉴风格的竖版信息图，比例为 3:4，4k。

视觉风格规范：
构图逻辑：采用分点式构图，有框线，序号。
背景与色彩：画面底背使用干净的米白色或原木浆草纸纹理，无需任何方框束缚。色彩采用自然原生色系，如草木绿、番茄红、泥土棕、暖阳黄。上色需呈现水彩特有的轻薄透气感、水渍边缘以及随性的色彩飞溅。
绘画风格：摒弃幼态卡通或扁平化图标，采用钢笔淡彩技法。使用松弛、利落、带有速写感的不规则深色线条勾勒轮廓，画面充满艺术写生感和手作温度。
场景演绎（核心）：绝对不要使用名人画像或现代 UI 图标。将文字信息全部转化为具象的自然事物、劳作场景或局部特写。
版式细节：整体排版自由、松弛、透气，仿佛是一页生动精美的自然观察日记或农庄手记。
```

![田园水彩旅行攻略](https://upload.maynor1024.live/file/1776831317590_wx_015_b59a25e9a4.jpg)

#### 9.5 暗黑风格插画

```text
生成一张暗黑风格的金克斯（Jinx）插画，要求画面呼吸感和节奏顺畅，细节精致，具有游戏原画级别的完成度
```

![金克斯暗黑风格插画](https://upload.maynor1024.live/file/1776831537718_wx_067_d80aa1ad9c.png)

#### 9.6 中国传统长卷山水画

```text
生成一张横版中国传统长卷山水画，笔墨晕染和留白
```

![中国传统长卷山水画](https://upload.maynor1024.live/file/1776831787179_wx_118_51623d8b22.png)

---

### 十、趣味玩法

#### 10.1 生成作业

```text
生成一份高中数学试卷
```

![高中数学试卷](https://upload.maynor1024.live/file/1776831586695_wx_078_62681d312e.jpg)
![数学试卷-另一版](https://upload.maynor1024.live/file/1776831470992_wx_049_890df7bf90.png)

#### 10.2 360 度全景图

```text
生成一张人类登月的 360 度全景图
```

![登月360度全景图](https://upload.maynor1024.live/file/1776831763812_wx_113_bf646f5279.gif)
![登月全景-静态](https://upload.maynor1024.live/file/1776831416957_wx_038_a30f854725.png)

#### 10.3 四格漫画

```text
（上传团队合照）根据这张照片生成一张四格漫画
```

![团队四格漫画](https://upload.maynor1024.live/file/1776831594736_wx_080_a5f98eed6d.png)
![奥特曼团队漫画](https://upload.maynor1024.live/file/1776831651486_wx_097_7f7cf5404f.png)

#### 10.4 中文书法默写

```text
用普通人的笔迹抄写《定风波·莫听穿林打叶声》
```

![定风波书法默写](https://upload.maynor1024.live/file/1776831381902_wx_032_473fc25dea.png)
![出师表默写](https://upload.maynor1024.live/file/1776831460090_wx_047_591ffaf023.jpg)

#### 10.5 红楼梦关系图

```text
生成一张红楼梦人物关系图
```

![红楼梦人物关系图](https://upload.maynor1024.live/file/1776831475649_wx_051_3161a27532.jpg)

#### 10.6 情书生成

```text
帮我写一封情书，用精美的信纸和手写字体的风格呈现
```

![情书手写风格](https://upload.maynor1024.live/file/1776831470428_wx_050_77d5d0ad4f.png)

#### 10.7 Sam Altman 微信朋友圈

```text
生成 OpenAI CEO Sam Altman 在微信朋友圈用中文介绍宣传 ChatGPT Images 2.0，底下马斯克评论发「？？？」，Demis Hassabis 评论称：「我觉得不如 Nano Banana Pro」，图片比例为 16:9
```

---

## 高级技巧

### 技巧 1：photorealistic 是万能钥匙

```
想让输出最自然，最有效的关键词就是 photorealistic。
模型会主动规避塑料感，复刻真实照片的特征。
```

### 技巧 2：善用 Thinking 模式

- 需要联网信息（如品牌知识、人物背景）时，开启 Thinking 模式
- 需要多张连贯图片（如穿搭系列、社交媒体素材）时，开启 Thinking 模式
- 简单出图用 Instant 模式即可，速度快

### 技巧 3：给文字，不要描述文字

```text
# 错误示范
生成一张有促销信息的奶茶海报

# 正确示范
生成一张奶茶海报，品牌名为"山川茶事"，新品名为"山柚观音冷泡系列"，价格"中杯 16 元 大杯 19 元"，活动"第二杯半价"
```

### 技巧 4：指定审美方向

```text
# 通过风格参考锚定审美
"参考 1960 年代法国新浪潮电影海报风格"
"采用钢笔淡彩（Pen and wash）技法"
"新中式、轻奢、克制"
"像素画风格 / 复古胶片 / 极简科技"
```

### 技巧 5：垫图 + 编辑，效果翻倍

1. 先上传参考图（垫图）
2. 让 GPT-Image-2 生成初稿
3. 点击图片左下角的「编辑」功能进行精细修改
4. 修改可以针对特定区域（如替换品牌、改文字、换人物）

### 技巧 6：利用世界知识

```text
# 模型已经知道这些，不需要你详细描述：
- 各大 App 的界面布局
- 品牌的视觉识别系统
- 历史事件和人物关系
- 产品类型和行业惯例

# 所以你可以直接说：
"生成一张特斯拉官网的截图"
"生成一张微信聊天记录"
"帮我做一张这个产品的电商详情页"
```

### 技巧 7：信息图三要素

制作高质量信息图的公式：

```
模块化分区 + 圆角信息框 + 层级分明的标题
+ 浅色干净背景 + 精致小图标 + 适当留白
```

### 技巧 8：比例选择指南

| 比例 | 适用场景 |
|------|---------|
| 1:1 | 社交媒体头像、产品主图 |
| 3:4 | 海报、信息图、插画 |
| 9:16 | 手机壁纸、故事/短视频封面 |
| 21:9 | 公众号封面、电影感横幅 |
| 3:1 | 全景图、长卷 |

---

## 局限性

GPT-Image-2 虽然强大，但仍有以下局限：

1. **三维物理逻辑**：折纸步骤图、魔方复原过程等需要极度严密三维物理逻辑的任务，容易翻车
2. **密集纹理**：倾斜表面上的微小细节、极度密集的重复纹理仍会触碰计算边界
3. **精确箭头图表**：涉及精确箭头的图表，建议人工核查
4. **亚洲人一致性**：对亚洲人面部的一致性保持不如欧美面孔
5. **2K+ 分辨率**：API 端的 2K 以上分辨率仍在 Beta 阶段，偶尔不够稳定
6. **高风险内容**：证件、试卷等高风险内容的生成应谨慎传播

---

## API 定价

| 画质 | 分辨率 | 输入价格 | 输出价格 |
|------|--------|---------|---------|
| Low | 1024x1024 | $2.00 / 1M tokens | $8.00 / 1M tokens |
| Medium | 1536x1536 | $2.00 / 1M tokens | $16.00 / 1M tokens |
| High | 2048x2048 | $2.00 / 1M tokens | $32.00 / 1M tokens |

> Token 输入/输出价格相比前代没有上涨。

---


## 实景效果展示

以下为 6 篇原文中的更多示例图片，展示 GPT-Image-2 的综合能力。

### 世界知识与界面复刻

![小红书/B站个人主页](https://upload.maynor1024.live/file/1776831492381_wx_054_3289e65a1c.jpg)
![游戏代肝海报](https://upload.maynor1024.live/file/1776831492836_wx_055_cad73eddcb.png)
![汽车官网生成](https://upload.maynor1024.live/file/1776831493207_wx_056_18cd9b1683.png)
![YouTube首页截图](https://upload.maynor1024.live/file/1776831488303_wx_053_2bafb78225.png)
![影视飓风首页](https://upload.maynor1024.live/file/1776480315853_img_023.png)

### 文字渲染能力

![中文报纸](https://upload.maynor1024.live/file/1776831460254_wx_048_05ab5cbe8c.jpg)
![稳稳地接住你-官方玩梗](https://upload.maynor1024.live/file/1776831383838_wx_033_18ce83744c.png)
![中文漫画-陈博远](https://upload.maynor1024.live/file/1776831693064_wx_103_f710ee99af.png)
![大米刻字-GPT image 2](https://upload.maynor1024.live/file/1776831387114_wx_034_b28df15e9d.png)

### 胶片质感与摄影

![35mm胶片抓拍](https://upload.maynor1024.live/file/1776831365224_wx_026_b585044656.jpg)
![一次性相机风格](https://upload.maynor1024.live/file/1776831779929_wx_117_6f6c3484ca.png)
![复古电影海报](https://upload.maynor1024.live/file/1776831797012_wx_119_cbd6bb438c.png)
![装饰艺术书签](https://upload.maynor1024.live/file/1776831801474_wx_120_e22999f9d0.png)

### 更多创意作品

![Anthropic生成图-以假乱真](https://upload.maynor1024.live/file/1776831458877_wx_046_2e0ca5002d.png)
![恋与深空老登版](https://upload.maynor1024.live/file/1776831433192_wx_043_c7958dca21.png)
![卡兹克版](https://upload.maynor1024.live/file/1776831432997_wx_044_9c5ec162ed.png)
![马斯克库克连麦PK](https://upload.maynor1024.live/file/1776831450804_wx_045_4be4a7ae55.png)
![康托尔对角线证明](https://upload.maynor1024.live/file/1776831369722_wx_028_c89e366a62.webp)
![维基百科信息图](https://upload.maynor1024.live/file/1776831379205_wx_029_23c7081a2d.jpg)

### 产品精修与编辑

![宠物联名-编辑功能演示](https://upload.maynor1024.live/file/1776480099150_img_004.jpg)
![海报风格切换](https://upload.maynor1024.live/file/1776480439516_img_034.jpg)
![爱马仕联名](https://upload.maynor1024.live/file/1776480120546_img_006.jpg)
![圆桌对谈](https://upload.maynor1024.live/file/1776831517286_wx_063_52bf07d583.png)

### 官方发布相关

![Arena盲测榜单](https://upload.maynor1024.live/file/1776831642578_wx_094_504603186b.png)
![API定价表](https://upload.maynor1024.live/file/1776831842038_wx_130_ff645557f7.png)
![2015年OpenAI成立](https://upload.maynor1024.live/file/1776831748266_wx_112_0c18e4678c.png)
![Brooklyn抹茶店广告素材](https://upload.maynor1024.live/file/1776831820073_wx_125_c84ab578e3.png)
![全日语少年漫画](https://upload.maynor1024.live/file/1776831694503_wx_106_6ac2dcf700.png)
![多语言书店封面](https://upload.maynor1024.live/file/1776831718180_wx_107_30d146f1e5.png)
![韩语韩屋广告](https://upload.maynor1024.live/file/1776831716035_wx_108_e12e784741.png)

## 补充案例拆解

### AI新榜《GPT Image 2刷屏一天了，我们总结了8个最热玩法》

- 原文链接：https://mp.weixin.qq.com/s/PKO6EVXRarRe4ToP7srgxA
- 公众号：AI新榜
- 作者：Kino 懒人
- 本次补充提取：37 张正文图片，5 条文中明确出现的提示词
- 说明：这里只收录正文里明确写出“提示词：”的内容，不对作者未明写的 prompt 做猜测补全

#### 提示词摘录

1. 提示词：请生成一张高质量竖版科普百科图，介绍GPT image 2。这是一张兼具“图鉴感、百科感、信息结构感、收藏感”的模块化科普信息图。整体风格参考高级博物图鉴、现代百科书页、生活方式知识卡和社交媒体高传播信息图的结合，全中文。
2. 提示词：围绕上面的形象，设计一个IP
3. 提示词：一块中英双语咖啡馆菜单黑板，上面有中文今日特调和英文Daily Special
4. 提示词：生成一张手绘子弹笔记风格的记录去上海旅游3天的手账。
5. 提示词：图1、图2、图3的人物仿照图4的三只猫拍vlog图片

#### 根据图片反推的提示词（推测版）

> 下面这些不是原文明确给出的 prompt，而是结合正文语境和成图效果反推出来的“可复用写法”。

1. 社交媒体截图与假新闻玩法（#05-#10）
   - 生成一张“罗永浩接任 Apple CEO”的中文人物海报，科技发布会视觉，人物半身特写，舞台灯光，带 Apple 风格标题与社交媒体传播感。
   - 生成一张抖音直播间截图，Sam Altman 和 Elon Musk 正在中文直播带货，画面里要有主播头像、弹幕、商品卡片、点赞评论和平台 UI。
   - 生成一张“Tim Cook 加入华为”的微博官宣图和热搜图，包含多个衍生热搜词条，看起来像真实中文互联网截图。
   - 生成一张《葬送的芙莉莲》角色的微信朋友圈截图，头像、配图、文案、评论都符合人物设定。
   - 生成一张五条悟的 X 账号主页截图，头像、简介、置顶内容和时间线风格贴近角色气质。
2. 电商与品牌设计（#11-#14）
   - 根据服装平铺图生成模特上身图，服饰细节 1:1 还原，场景自然，像真实棚拍或街拍。
   - 假如鸡毛掸子是 Apple 的产品，请生成一张 Apple 官网风格的 Landing Page，极简排版，大面积留白，带幽默文案。
   - 生成一张更本土化的 618 电商商品详情页，带价格、优惠券、卖点模块和中文电商视觉层级。
3. 信息图、游戏 UI 与漫画分镜（#15-#17）
   - 生成一张介绍 GPT Image 2 核心能力的中文百科/信息图海报，模块化布局，图鉴感强。
   - 生成一张特朗普变成《原神》大 Boss 的实机演示截图，完整复刻战斗 UI、小地图、角色栏、血条和 UID。
   - 生成一页全中文漫画分镜，主题是“哆啦A梦被夜神月威胁利用”，要求角色一致、剧情连贯、气泡和分镜完整。
4. IP 联名与文字渲染（#18-#23）
   - 参考一张办公桌上的周边随手拍，为它设计一个完整 IP：三视图、表情、角色设定和衍生周边。
   - 围绕这个 IP 再设计星巴克联名和泡泡玛特联名，分别输出饮品、杯子、挂件、盲盒和海报物料。
   - 生成一块中英双语咖啡馆菜单黑板，中文今日特调和英文 Daily Special 要自然融入排版。
   - 生成一张手绘子弹笔记风格的上海 3 日旅行手账，包含路线、美食、照片、花费和心情记录。
5. 多图融合与娱乐化创作（#24-#31）
   - 上传三张人物单人照和一张参考合照，让前三个人物模仿参考图里的姿势，一起拍 vlog 合照。
   - 保留一个核心人物，换另外三位不同肤色或性别的人物参考，生成中国元素更强的麻将场景合照。
   - 生成一张猫咪主演的武侠电影海报，老港片/江湖片质感，标题夸张，人物关系复杂。
   - 生成一组追星直拍/偶像应援海报，拼贴构图，强舞台灯光，中文应援字样。
   - 根据人物设定生成一页专属漫画拼贴或角色故事板，带多格内容和统一美术风格。
   - 生成一张 Arena 榜单或模型对比走势图，适合做 AI 产品成绩单展示。
6. 说明
   - #01-#04 更偏文章头图、概览图或导流图，适合按“发布会截图 / GPT Image 2 能力概览 / 社交动态界面”去写。
   - #32-#37 是作者卡、二维码和文末推广素材，不建议强行补 prompt。

#### 对应案例图

- 科普信息图：#15
- IP 设计延展：#19、#20、#21
- 中英双语咖啡馆菜单：#22
- 上海旅游手账：#23
- 仿三只猫拍 vlog：#24、#25、#26、#27

![AI新榜案例-15-科普信息图](https://upload.maynor1024.live/file/1776925334708_15.png)
![AI新榜案例-19-IP设计](https://upload.maynor1024.live/file/1776925353853_19.png)
![AI新榜案例-22-双语菜单](https://upload.maynor1024.live/file/1776925357255_22.png)
![AI新榜案例-23-上海旅游手账](https://upload.maynor1024.live/file/1776925368474_23.png)
![AI新榜案例-25-vlog案例](https://upload.maynor1024.live/file/1776925380623_25.png)

<details open>
<summary>查看全部图片（37 张，不省略）</summary>

<table>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925266347_01.png" alt="发布会视频截图" width="220" /><br><sub>#01 发布会视频截图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925269246_02.png" alt="GPT Image 2 中文科普海报" width="220" /><br><sub>#02 GPT Image 2 中文科普海报</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925279235_03.jpg" alt="多场景能力拼图" width="220" /><br><sub>#03 多场景能力拼图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925283819_04.png" alt="社交动态界面图" width="220" /><br><sub>#04 社交动态界面图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925286078_05.jpg" alt="罗永浩接任 Apple CEO 海报" width="220" /><br><sub>#05 罗永浩接任 Apple CEO 海报</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925289291_06.jpg" alt="Sam Altman 和马斯克直播带货" width="220" /><br><sub>#06 Sam Altman 和马斯克直播带货</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925296390_07.png" alt="马斯克直播带货特斯拉周边" width="220" /><br><sub>#07 马斯克直播带货特斯拉周边</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925297066_08.png" alt="Tim Cook 加入华为热搜图" width="220" /><br><sub>#08 Tim Cook 加入华为热搜图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925301157_09.jpg" alt="芙莉莲朋友圈截图" width="220" /><br><sub>#09 芙莉莲朋友圈截图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925310552_10.jpg" alt="五条悟 X 账号主页" width="220" /><br><sub>#10 五条悟 X 账号主页</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925310152_11.jpg" alt="服装换装编辑界面" width="220" /><br><sub>#11 服装换装编辑界面</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925316827_12.png" alt="写真人像穿搭照" width="220" /><br><sub>#12 写真人像穿搭照</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925318940_13.png" alt="鸡毛掸子 Apple 风 Landing Page" width="220" /><br><sub>#13 鸡毛掸子 Apple 风 Landing Page</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925333171_14.png" alt="618 电商详情长图" width="220" /><br><sub>#14 618 电商详情长图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925334708_15.png" alt="GPT Image 2 科普信息图" width="220" /><br><sub>#15 GPT Image 2 科普信息图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925338855_16.png" alt="原神 Boss 战 UI" width="220" /><br><sub>#16 原神 Boss 战 UI</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925344987_17.png" alt="中文漫画分镜" width="220" /><br><sub>#17 中文漫画分镜</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925341940_18.jpg" alt="桌面周边随手拍" width="220" /><br><sub>#18 桌面周边随手拍</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925353853_19.png" alt="IP 角色设定图" width="220" /><br><sub>#19 IP 角色设定图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925357817_20.png" alt="星巴克联名设计" width="220" /><br><sub>#20 星巴克联名设计</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925357814_21.png" alt="泡泡玛特联名设计" width="220" /><br><sub>#21 泡泡玛特联名设计</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925357255_22.png" alt="中英双语菜单黑板" width="220" /><br><sub>#22 中英双语菜单黑板</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925368474_23.png" alt="上海旅行手账" width="220" /><br><sub>#23 上海旅行手账</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925378190_24.png" alt="多图参考输入拼图" width="220" /><br><sub>#24 多图参考输入拼图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925380623_25.png" alt="三人 vlog 成片" width="220" /><br><sub>#25 三人 vlog 成片</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925378939_26.png" alt="第二组人物参考图" width="220" /><br><sub>#26 第二组人物参考图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925385609_27.png" alt="麻将场景成片" width="220" /><br><sub>#27 麻将场景成片</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925387762_28.jpg" alt="猫咪武侠电影海报" width="220" /><br><sub>#28 猫咪武侠电影海报</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925397007_29.jpg" alt="追星直拍海报" width="220" /><br><sub>#29 追星直拍海报</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925401156_30.jpg" alt="专属漫画拼贴" width="220" /><br><sub>#30 专属漫画拼贴</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925402976_31.png" alt="Arena 榜单走势图" width="220" /><br><sub>#31 Arena 榜单走势图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925408233_32.png" alt="作者名片" width="220" /><br><sub>#32 作者名片</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925415365_33.png" alt="合作作者卡" width="220" /><br><sub>#33 合作作者卡</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925423994_34.png" alt="文末横幅 1" width="220" /><br><sub>#34 文末横幅 1</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925420251_35.png" alt="文末横幅 2" width="220" /><br><sub>#35 文末横幅 2</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925421997_36.jpg" alt="新榜矩阵通二维码" width="220" /><br><sub>#36 新榜矩阵通二维码</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776925432902_37.jpg" alt="新榜声量通二维码" width="220" /><br><sub>#37 新榜声量通二维码</sub></td>
<td></td>
<td></td>
</tr>
</table>

</details>

<details>
<summary>查看全部图床链接（37 张）</summary>

1. `https://upload.maynor1024.live/file/1776925266347_01.png`
2. `https://upload.maynor1024.live/file/1776925269246_02.png`
3. `https://upload.maynor1024.live/file/1776925279235_03.jpg`
4. `https://upload.maynor1024.live/file/1776925283819_04.png`
5. `https://upload.maynor1024.live/file/1776925286078_05.jpg`
6. `https://upload.maynor1024.live/file/1776925289291_06.jpg`
7. `https://upload.maynor1024.live/file/1776925296390_07.png`
8. `https://upload.maynor1024.live/file/1776925297066_08.png`
9. `https://upload.maynor1024.live/file/1776925301157_09.jpg`
10. `https://upload.maynor1024.live/file/1776925310552_10.jpg`
11. `https://upload.maynor1024.live/file/1776925310152_11.jpg`
12. `https://upload.maynor1024.live/file/1776925316827_12.png`
13. `https://upload.maynor1024.live/file/1776925318940_13.png`
14. `https://upload.maynor1024.live/file/1776925333171_14.png`
15. `https://upload.maynor1024.live/file/1776925334708_15.png`
16. `https://upload.maynor1024.live/file/1776925338855_16.png`
17. `https://upload.maynor1024.live/file/1776925344987_17.png`
18. `https://upload.maynor1024.live/file/1776925341940_18.jpg`
19. `https://upload.maynor1024.live/file/1776925353853_19.png`
20. `https://upload.maynor1024.live/file/1776925357817_20.png`
21. `https://upload.maynor1024.live/file/1776925357814_21.png`
22. `https://upload.maynor1024.live/file/1776925357255_22.png`
23. `https://upload.maynor1024.live/file/1776925368474_23.png`
24. `https://upload.maynor1024.live/file/1776925378190_24.png`
25. `https://upload.maynor1024.live/file/1776925380623_25.png`
26. `https://upload.maynor1024.live/file/1776925378939_26.png`
27. `https://upload.maynor1024.live/file/1776925385609_27.png`
28. `https://upload.maynor1024.live/file/1776925387762_28.jpg`
29. `https://upload.maynor1024.live/file/1776925397007_29.jpg`
30. `https://upload.maynor1024.live/file/1776925401156_30.jpg`
31. `https://upload.maynor1024.live/file/1776925402976_31.png`
32. `https://upload.maynor1024.live/file/1776925408233_32.png`
33. `https://upload.maynor1024.live/file/1776925415365_33.png`
34. `https://upload.maynor1024.live/file/1776925423994_34.png`
35. `https://upload.maynor1024.live/file/1776925420251_35.png`
36. `https://upload.maynor1024.live/file/1776925421997_36.jpg`
37. `https://upload.maynor1024.live/file/1776925432902_37.jpg`

</details>

### APPSO《刚刚，实测完 GPT-Image-2：设计师没完蛋，但我被 AI 骗麻了》

- 原文链接：https://mp.weixin.qq.com/s/sUAB-XiTTJF2MY8ghagUZg
- 公众号：APPSO
- 作者：发现明日产品的
- 本次补充提取：24 张正文图片
- 说明：这篇文章里没有像上文那样明确单列“提示词：”，下面只整理文中可直接复用的指令、描述和关键词，不补造不存在的 prompt

#### 可直接复用的指令/关键词摘录

1. macOS 浏览器中 ChatGPT 的截图。用户输入「draw me a dog」，ChatGPT 画了一只 ASCII 艺术风格的狗。前景窗口是 ChatGPT，桌面很乱，后台开着一堆随机窗口（比如终端）。
2. 一张写实风格的旅行抓拍：阴天清晨，一个人站在海边路旁的观景停车带，用35mm胶片拍摄。构图自然、略有瑕疵，颗粒感明显，环境光漫射，色调低饱和，衣物和发丝随风飘动，带着纪录片式的电影质感，像是某段真实生活留下的影像。
3. 用普通人的笔迹抄写《定风波·莫听穿林打叶声》
4. 关键词：`photorealistic`
5. 生成 OpenAI CEO Sam Altman 在微信朋友圈用中文介绍宣传 ChatGPT Images 2.0，底下马斯克评论发「？？？」，Demis Hassabis 评论称：「我觉得不如 Nano Banana Pro」，图片比例为 16:9

#### 根据图片反推的提示词（推测版）

> 下面这些不是 APPSO 原文逐字给出的 prompt，而是结合正文描述和成图效果整理出的可复用写法。

1. 桌面 UI 与产品界面（#05-#08）
   - 生成一张 macOS 桌面截图，前景窗口是 ChatGPT，用户输入 `draw me a dog`，输出是一只 ASCII 艺术风格的狗，后台开着终端和一堆杂乱窗口。
   - 生成一张对话截图或产品演示图，界面要像真实 SaaS / AI 工具，保留输入框、消息气泡、边栏和系统窗口细节。
   - 生成一张游戏实机画面或发布会现场演示图，突出界面 HUD、透视和真实屏摄感。
2. 写实摄影与知识信息图（#09-#11）
   - 生成一张 35mm 胶片旅行抓拍：阴天海边公路、人物回头、低饱和、颗粒感、纪录片质感。
   - 生成一张数学原理信息图或体育数据图，要求结构清晰、标题和标签准确、排版干净。
3. 角色一致性与中文文字（#12-#17）
   - 上传一张人物照片，生成多套穿搭和多个角度，保持人物脸部特征一致。
   - 用普通人的笔迹抄写《定风波·莫听穿林打叶声》，手写感自然，不要贴图感。
   - 生成一张多语言排版海报或中文玩梗视觉，要求小字号文字也尽量清晰稳定。
4. 真实质感与光影逻辑（#18-#21）
   - 关键词使用 `photorealistic`，要求保留真实摄影中的瑕疵、颗粒、阴影和轻微失焦。
   - 生成一张具有真实光影逻辑的场景图，例如月球 360 全景，太阳方向与地面阴影必须一致。
   - 生成一张教学信息图，例如鞋带系法教程，强调步骤清晰、箭头合理、布局像真实教材。
5. 社交媒体整活（#22）
   - 生成 OpenAI CEO Sam Altman 在微信朋友圈用中文宣传 ChatGPT Images 2.0，底下马斯克评论“？？？”，Demis Hassabis 评论“我觉得不如 Nano Banana Pro”，比例 16:9。
6. 说明
   - #01-#04 偏发布会、榜单和概览类图片，适合作为“发布会截图 / 榜单图 / OpenAI 团队圆桌”的说明图，不建议强行补复杂 prompt。
   - #23-#24 是二维码海报和编辑卡片，属于文末导流素材，不建议补 prompt。

#### 对应案例图

- 桌面 UI 与 ASCII 狗：#05
- 胶片抓拍与写实摄影：#09
- 数学信息图：#10、#11
- 角色一致性与穿搭延展：#12、#13
- 中文排版与手写文字：#14、#15、#16、#17
- photorealistic 与真实光影：#18、#19、#20
- 微信朋友圈整活图：#22

![APPSO案例-05-桌面UI](https://upload.maynor1024.live/file/1776927572727_05.other)
![APPSO案例-09-胶片抓拍](https://upload.maynor1024.live/file/1776927584894_09.other)
![APPSO案例-10-数学信息图](https://upload.maynor1024.live/file/1776927590918_10.webp)
![APPSO案例-12-角色一致性](https://upload.maynor1024.live/file/1776927598909_12.png)
![APPSO案例-14-中文手写](https://upload.maynor1024.live/file/1776927610651_14.png)
![APPSO案例-20-360光影](https://upload.maynor1024.live/file/1776927643952_20.png)
![APPSO案例-22-微信朋友圈](https://upload.maynor1024.live/file/1776927657894_22.png)

<details open>
<summary>查看全部图片（24 张，不省略）</summary>

<table>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927544187_01.png" alt="发布会主讲截图" width="220" /><br><sub>#01 发布会主讲截图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927556901_02.png" alt="AI 困境广告牌画面" width="220" /><br><sub>#02 AI 困境广告牌画面</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927556202_03.jpg" alt="Arena 排行榜" width="220" /><br><sub>#03 Arena 排行榜</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927562675_04.png" alt="OpenAI 团队圆桌" width="220" /><br><sub>#04 OpenAI 团队圆桌</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927572727_05.other" alt="macOS 桌面 ChatGPT ASCII 狗" width="220" /><br><sub>#05 macOS 桌面 ChatGPT ASCII 狗</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927576065_06.png" alt="Anthropic 对话截图" width="220" /><br><sub>#06 Anthropic 对话截图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927573344_07.png" alt="API 价格/参数表" width="220" /><br><sub>#07 API 价格/参数表</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927588440_08.jpg" alt="游戏实机画面" width="220" /><br><sub>#08 游戏实机画面</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927584894_09.other" alt="35mm 胶片旅行抓拍" width="220" /><br><sub>#09 35mm 胶片旅行抓拍</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927590918_10.webp" alt="康托尔对角线信息图" width="220" /><br><sub>#10 康托尔对角线信息图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927602380_11.jpg" alt="篮球信息图" width="220" /><br><sub>#11 篮球信息图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927598909_12.png" alt="角色一致性穿搭图" width="220" /><br><sub>#12 角色一致性穿搭图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927610992_13.png" alt="角色一致性延展图" width="220" /><br><sub>#13 角色一致性延展图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927610651_14.png" alt="中文手写诗词" width="220" /><br><sub>#14 中文手写诗词</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927619323_15.png" alt="多语言排版海报" width="220" /><br><sub>#15 多语言排版海报</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927624690_16.png" alt="中文玩梗视觉" width="220" /><br><sub>#16 中文玩梗视觉</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927623579_17.png" alt="极小文字演示" width="220" /><br><sub>#17 极小文字演示</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927634216_18.png" alt="真实人像风格" width="220" /><br><sub>#18 真实人像风格</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927637870_19.png" alt="真实质感摄影" width="220" /><br><sub>#19 真实质感摄影</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927643952_20.png" alt="月球 360 光影" width="220" /><br><sub>#20 月球 360 光影</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927655003_21.webp" alt="鞋带教学图" width="220" /><br><sub>#21 鞋带教学图</sub></td>
</tr>
<tr>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927657894_22.png" alt="微信朋友圈整活图" width="220" /><br><sub>#22 微信朋友圈整活图</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927661494_23.png" alt="二维码海报" width="220" /><br><sub>#23 二维码海报</sub></td>
<td align="center" valign="top"><img src="https://upload.maynor1024.live/file/1776927662893_24.other" alt="AI 方向编辑卡片" width="220" /><br><sub>#24 AI 方向编辑卡片</sub></td>
</tr>
</table>

</details>

<details>
<summary>查看全部图床链接（24 张）</summary>

1. `https://upload.maynor1024.live/file/1776927544187_01.png`
2. `https://upload.maynor1024.live/file/1776927556901_02.png`
3. `https://upload.maynor1024.live/file/1776927556202_03.jpg`
4. `https://upload.maynor1024.live/file/1776927562675_04.png`
5. `https://upload.maynor1024.live/file/1776927572727_05.other`
6. `https://upload.maynor1024.live/file/1776927576065_06.png`
7. `https://upload.maynor1024.live/file/1776927573344_07.png`
8. `https://upload.maynor1024.live/file/1776927588440_08.jpg`
9. `https://upload.maynor1024.live/file/1776927584894_09.other`
10. `https://upload.maynor1024.live/file/1776927590918_10.webp`
11. `https://upload.maynor1024.live/file/1776927602380_11.jpg`
12. `https://upload.maynor1024.live/file/1776927598909_12.png`
13. `https://upload.maynor1024.live/file/1776927610992_13.png`
14. `https://upload.maynor1024.live/file/1776927610651_14.png`
15. `https://upload.maynor1024.live/file/1776927619323_15.png`
16. `https://upload.maynor1024.live/file/1776927624690_16.png`
17. `https://upload.maynor1024.live/file/1776927623579_17.png`
18. `https://upload.maynor1024.live/file/1776927634216_18.png`
19. `https://upload.maynor1024.live/file/1776927637870_19.png`
20. `https://upload.maynor1024.live/file/1776927643952_20.png`
21. `https://upload.maynor1024.live/file/1776927655003_21.webp`
22. `https://upload.maynor1024.live/file/1776927657894_22.png`
23. `https://upload.maynor1024.live/file/1776927661494_23.png`
24. `https://upload.maynor1024.live/file/1776927662893_24.other`

</details>

## 免责声明

- GPT-Image-2 确实能生成以假乱真的内容，但这也意味着边界更重要
- 证件、试卷等高风险内容，请勿传播
- 很多人并不能分辨 AI 生成的内容，即便带有水印
- 请负责任地使用 AI 图像生成工具

---

## 参考来源

本文内容整合自以下 6 篇深度实测文章：

1. 蜡笔《熬夜跑了 16 组 GPT Image 2，这些提示词值得你直接拿走》
2. APPSO《刚刚，实测完 GPT-Image-2：设计师没完蛋，但我被 AI 骗麻了》
3. 数字生命卡兹克《实测 GPT-image-2，设计行业真的完蛋了吗？》
4. 《五大真实场景横测 GPT-image-2 和 Nano Banana2》
5. 量子位《GPT-Image-2 正式发布！设计师可以告别「古法设计」了》
6. 新智元《Images 2.0 登顶王座！大米刻字，生图跨入 GPT-5 时代》

---

## 使用方法

GPTImage2 模型五种使用方法：

- 官网使用: https://chatgpt.com/
- 国内使用地址：https://chatgpt-plus.top/list/#/home
- API 使用地址：https://apipro.maynor1024.live/
- Codex 使用：https://maynorai.jichiyun.sbs/buy/13
- 国外使用地址：https://gptimage2.asia/

---

<div align="center">

**如果觉得有用，给个 Star 吧！**

Made with GPT-Image-2 | Last updated: 2026-04-22

</div>
