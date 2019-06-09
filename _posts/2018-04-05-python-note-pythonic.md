---
layout: post
title: "Python筆記I：pythonic"
date: 2018-04-05
---

之前初學Python之後想找份相關的工作，在一次面試中被問到怎麼看pythonic以及being pythonic的好處<!-- more -->。我第一次接觸到這個詞，交卷後搜索才知道意思，和面試官卻沒有就此交流更多。看到有些中文翻譯為“Python風味”，於是理解為“地道”，類似學英語是熟悉語言之後的做法。

### 一部分pythonic
{: .subtitle}

Python中sequence有不少獨特之處，支持slice分片、負數值索引。初學時很不適應負數值索引，[這裡](https://www.liaoxuefeng.com/discuss/001409195742008d822b26cf3de46aea14f2b7378a1ba91000/001511101277134dbbdd0730c2c43b4af64a879be35fd3d000)利用負數值索引巧妙實現楊輝三角，印象深刻。在Python中所謂的sequence係實現了iterator protocol，即```__iter__()```和```next()```方法的objects。列表推導式「list comprehension」則提供了一種簡潔迭代sequence的方式。

Python中返回sequence還會自動解包從而實現返回多個值。不過接收自動解包的左值參數數量必須與返回的sequence長度一致，不似Lua會把超出範圍的左值參數設置為nil。所以Python返回多個值的函數每處```return```的sequence長度都必須一致，否則會在自動解包的過程中拋出異常。

迭代器係stateless遍歷容器的方式，在面向對象語言中通過interface或protocol實現，在Lua中通過函數閉包實現。Python也提供了類似的閉包實現：通過generator function。生成器generator也是pythonic之一，用於lazy loading大文件和streaming等場合，減小內存占用 [[PEP 255]](https://www.python.org/dev/peps/pep-0255/)。Python擴展了simple generator的用法，例如作為genexpr加入到listcomp提高其性能 [[PEP 289]](https://www.python.org/dev/peps/pep-0289/)、實現預定義上下文管理的with statement [[PEP 343]](https://www.python.org/dev/peps/pep-0343/)。

《Programming in Lua》中提到Python的generator屬於symmetric coroutine，區別在於```yield```係expression而非function：即generator必須存在```yield```（而非調用包含```yield```的函數） [[2]](#ref4)。首次使用coroutine前要先調用```next()```使之運行，是調用generator function進入函數體之後，後續的```next/send()```才能被```yield```響應 [[3]](#ref3)。

>"All of this makes generator functions quite similar to coroutines; they yield multiple times, they have more than one entry point and their execution can be suspended. The only difference is that a generator function cannot control where should the execution continue after it yields; the control is always transferred to the generator's caller."
>
> -- "The Python Language Reference"

在 [[PEP 288]](https://www.python.org/dev/peps/pep-0288/) 中提到其出發點是擴展作為函數的generator，相比class實現具有更高可讀性和性能。函數式編程也被我視為pythonic之一，其中函數的封裝解耦、重用就聯想到decorator。裝飾器作為高階函數是實現函數解耦、組合的方式，相當于FP實現的composite模式。

#### *Ref:*
[[1]](#ref1): [Charming Python](http://gnosis.cx/publish/programming/charming_python_b5.txt)

[[2]](#ref2): [Coroutines in Lua](http://www.inf.puc-rio.br/~roberto/docs/corosblp.pdf)

[[3]](#ref3): [Coroutine's resume and yield](https://stackoverflow.com/questions/38069751/confusion-about-lua-corountines-resume-and-yield-function)

### Being pythonic
{: .subtitle}

以語言特性為基礎建立起一套編程模式，實現易維護擴展、穩定安全、優化性能，作為一種思維方式，是如今我對pythonic的理解。類似用CAD作圖操作2D的點、線，使用Rhinoceros作圖操作3D的面、體，不同方案應用不同觀念。

通過比較不同編程語言的方式來思考pythonic，儘管不一定準確，也是有意思的事。據說Python參考了Lisp。Lisp的列表多一個指向剩餘列表的指針，Python到3.x才加入```car, *cdr = array```的解包方式，比較後想到列表生成式不能實現```reduce```的原因，也對Lisp的設計多了點理解。
