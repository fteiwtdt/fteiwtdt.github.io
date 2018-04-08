---
layout: post
title: "由pythonic想到的"
date: 2018-04-05
---

之前初學python之後想找份相關的工作，在一次面試中被問到怎麼看pythonic以及being pythonic的好處<!-- more -->。我第一次接觸到這個詞，交卷後搜索才知道意思，和面試官卻沒有就此交流更多。看到有些中文翻譯為“python風味”，於是理解為“地道”，類似學英語是熟悉語言之後的做法。

### 一部分pythonic
{: .subtitle} 
Python中sequence有不少獨特之處，支持slice分片、負數值索引。初學時很不適應負數值索引，[這裡](https://www.liaoxuefeng.com/discuss/001409195742008d822b26cf3de46aea14f2b7378a1ba91000/001511101277134dbbdd0730c2c43b4af64a879be35fd3d000)利用負數值索引巧妙實現楊輝三角，印象深刻。另一個pythonic之處、生成式「list comprehension」也是常見的優化方式。所謂sequence係實現了python中的iterator protocol，即係實現了```__iter__()```和```next()```的objects。這2個方法以對應的Python/C API實現以優化迭代性能 [[1]](#ref1)，調用代價小於調用python function [[2]](#ref2)。所以布爾運算的生成式速度上優於以內建函數```map```、```filter```、```zip```遍歷sequence。不過也因為sequence的設計，生成式不能以內建函數```reduce```的方式遞歸sequence。

生成器generator也是pythonic之一，調用generator function時每運行一步到yield就掛起返回到caller，實現了lazy loading和更好的控制 [[PEP 255]](https://www.python.org/dev/peps/pep-0255/)。在此基礎上python通過擴展generator的交互 [[PEP 288]](https://www.python.org/dev/peps/pep-0288)，加入到listcomp作為genexpr在加載和運算listcomp時提高性能、節省內存 [[PEP 289]](https://www.python.org/dev/peps/pep-0289/)，加入內建屬性方法成為coroutine [[PEP 342]](https://www.python.org/dev/peps/pep-0342/)，加入支持exception handling成為with statement [[PEP 343]](https://www.python.org/dev/peps/pep-0343/)。

在 [[PEP 288]](https://www.python.org/dev/peps/pep-0288/) 中提到其出發點是擴展作為函數的generator，相比class實現具有更高可讀性和性能，加之自己積累的部分經驗，函數式編程也被我視為pythonic之一 [[3]](#ref3)。其中函數的封裝解耦、重用就聯想到decorator。裝飾器作為高階函數是實現函數解耦、組合的方式，相當于fp實現的composite模式。

#### *Ref:*
[[1]](#ref1): [Iterator Types](https://docs.python.org/2/library/stdtypes.html#iterator-types)

[[2]](#ref2): [Charming Python](http://gnosis.cx/publish/programming/charming_python_b5.txt)

[[3]](#ref3): [Functional Programming HOWTO](https://docs.python.org/2.7/howto/functional.html#iterators)

### Being pythonic
{: .subtitle}
以語言特性為基礎建立起一套編程模式，實現易維護擴展、穩定安全、優化性能，作為一種思維方式，是如今我對pythonic的理解。類似用CAD作圖操作2D的點、線，使用Rhinoceros作圖操作3D的面、體，不同方案不同觀念才是有效的應用方式。

通過比較不同編程語言的方式來思考pythonic，儘管不一定準確，也是有意思的事。據說python參考了lisp，lisp的列表多一個指向剩餘列表的指針，python到3.x才加入```car, *cdr = array```的解包方式，比較後想到列表生成式不能實現```reduce```的原因，也對lisp的設計多了點理解，還有ObjC的```@autoreleasepool```類似「with statement」等。比較異同、借鑑啟發也是有效的應用方式。
