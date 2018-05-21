---
layout: post
title: "Init ghpages"
date: 2018-03-29
---

以前讀書的時候接觸到blog，選擇了免費的Octopress，當時Mac OS X還是10.6，內置Ruby 1.8.x<!-- more -->。經過一番折騰之後定製了一點樣式，後來卻沒有堅持下來。現在ghpages做了Jekyll的CI，連安裝配置rubygems都省了，方便了有系統潔癖的人。在本地配置環境則便於定製樣式。使用rbenv和rbenv-build編譯配置一個獨立版本ruby很方便，不安裝Homebrew更健康。然後安裝jekyll和jekyll-paginate，後者用在index.html中獲取博文列表。

### 佈局
{: .subtitle}

今時今日使用移動設備的場景更多、時長更長。為方便在手機上閱讀博文筆記，使用響應式佈局優先適配移動端瀏覽器。刪除傳統blog中的“Read more”按鈕，把首頁做成類似app的list，方便移動端觸摸打開鏈接。iOS 6上的舊版Safari對flexbox支持得不好，加上不熟悉CSS，只簡單通過media查詢適配桌面和移動端。

### CSS
{: .subtitle}

Jekyll默認的minima theme很不錯，不過想要護眼就要另外配置了。抄了[FT中文網](http://www.ftchinese.com)的護眼色調，代碼高亮選擇了深色主題的[Monokai](https://gist.github.com/wdullaer/e942cdd70d292e954166)。iOS缺少monospace字體而以sans顯示，需要在CSS中添加「font-face」link到等寬字體文件用於代碼顯示，使用支持較廣體積又小的woff格式。另按照《*Mastering Regular Expressions*》中提到的現代書信體格式設置段落間空一行。

```python
def fibonacci():
    i, j = 0, 1
    while True:
        yield i
        i, j = j, i+j
```

### MathJax
{: .subtitle}

Jekyll官網介紹了部分配置MathJax的方法，[CSDN極客頭條](http://geek.csdn.net)的設置也很詳細。大陸環境需要更換cdn，使用dns-prefetch加速讀取。MathJax默認上下margin了1em，重置樣式寫在js中才有效果。抄個「工业机器人的D-H矩阵」測試下：

$$^{i-1}T_i = \begin{bmatrix} \cos\theta_i & -\sin\theta_i\cos\alpha_{i,i+1} & \sin\theta_i\sin\alpha_{i,i+1} & \alpha_{i,i+1}\cos\theta_i \\ \sin\theta_i & \cos\theta_i\cos\alpha_{i,i+1} & -\cos\theta_i\sin\alpha_{i,i+1} & \alpha_{i,i+1}\sin\theta_i \\ 0 & \sin\alpha_{i,i+1} & \cos\alpha_{i,i+1} & d_i \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
