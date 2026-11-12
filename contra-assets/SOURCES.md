# 魂斗罗素材与实现说明

以 HTML Canvas 和 JavaScript 实现移动、跳跃、射击、碰撞、敌人、双人操作和第一关 Boss。当前范围为丛林第一关，不是完整八关，也不运行 NES ROM。

## 素材来源

- 原作：KONAMI《Contra／魂斗罗》。原版美术及标识权利属于各自权利人。
- 关卡地图：VGMaps，Rick N. Bruns，[NES 地图索引](https://www.vgmaps.com/atlas/NES/index.htm)。
- 角色、敌人、标题、武器等像素图：[The Spriters Resource — Contra](https://www.spriters-resource.com/nes/contra/)。
- `*-original.png` 保存所用原始图；处理后的图已内嵌进 `contra.html`。网页中保留素材说明。

素材公开可获取不代表授予再分发或商用许可；本仓库不对原版素材另行授予开源许可。

## 本地整理与打包

`prepare-map.py` 和 `prepare-sprites.py` 使用 Python 3、Pillow 整理地图、碰撞信息和图集。`build-inline.py` 使用 Python 标准库将图像和 JSON 写回上级目录的 `contra.html`。直接打开 HTML 不需要安装依赖。

```sh
python3 contra-assets/prepare-map.py
python3 contra-assets/prepare-sprites.py
python3 contra-assets/build-inline.py
```
