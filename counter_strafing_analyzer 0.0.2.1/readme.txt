本软件不提供任何急停辅助功能，仅为左右急停操作进行计时！目前不支持除键盘及鼠标左键以外的输入检测。

可以在_internal\key_config.txt中对左右移动键位和窗口大小进行配置

0.0.2.1更新：将默认键位从cz改回ad

运行软件后，进行ad急停并左键射击时将在界面中输出：反方向键按键时长、ad同时按下的时间（或ad之间间隔的时间）、点击左键射击时反方向键已按下的时间。

根据视频 https://www.bilibili.com/video/BV1QzKmzXE7z/ 中的测试，即使使用宏以毫秒级完美的操作完成松开a的一瞬间按下d，也需要80ms的时间将地速降低至使ak精准的地速范围内。因此，训练时应当着重训练掌握这80ms的时间差，即按下反方向键后的80ms时点击左键。

按下P键，清空数据。

按下Enter键，进行最近20条数据的分析：
反方向键的按键时长平均值
与理想值（80ms）的差值
ad键按下松开之间的时间差
点击左键射击时反方向键已按下的平均时间
与理想值（80ms）的差值
例：
Analysis of latest statistics:
Average hold time of second pressed key: 0.098 seconds
Difference with 80ms: 0.018 seconds
Average time between keys: -0.013 seconds

Average mouse click timing: 0.059 seconds
Difference with 80ms (mouse click): -0.021 seconds

则反方向键按键时长略长，略有两个方向键同时按下的情况，左键射击时间太早。


