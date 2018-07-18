---
layout: post
title: "ObjC筆記I：Misc"
date: 2018-03-30
---

### Header files
{: .subtitle}

密歇根大學有一份[文檔](http://umich.edu/~eecs381/handouts/CHeaderFileGuidelines.pdf)詳細介紹了頭文件組織需要注意的規則，譬如在頭文件中聲明、源文件中定義<!-- more -->。通過這條規則來定義全局常量。定義C字符串常量的指針要用```const char *```修飾。

```objc
// config.h
FOUNDATION_EXTERN NSString * const kGreeting;
// config.c
NSString * const kGreeting = @"Hello, world!";
```

對應地定義file scope私有變量是在源文件中使用```static```，“A static function/variable is only 'seen' within translate unit”。ObjC定義私有property的方式是使用class extension，定義只讀property的方式是在class extension中重聲明為readwrite。

使用```#import```是為了防止重複包含，即所謂的「include guides」。傳統的做法是使用```#define```，其寫法也有幾種風格，BSD是把文件名大寫、前後帶下標。在文檔中解釋以下標開頭是C保留作內部實現的用法。另一種方法是使用```#pragma once```，優點是代碼更簡潔、預編譯更快，缺點是兼容性較差。譬如ARM就不推薦使用。此外在頭文件中減少不必要的```#import/include```、使用forward class declaration代替，可以使預編譯速度更快。

```c
// $FreeBSD: /usr/src/include/stdio.h
#ifndef _STDIO_H_
#define _STDIO_H_

#endif /* !_STDIO_H */
```

對於```#include```的文件名使用引號和尖括號的區別，通常的解釋是引號表示從當前目錄開始搜索，尖括號表示從系統目錄開始搜索。不過也可以看到使用尖括號包含源碼目錄中的頭文件。[這裡](https://stackoverflow.com/questions/4118376/what-are-the-rules-on-include-xxx-h-vs-include-xxx-h)解釋其實尖括號表示從編譯器指定的目錄開始搜索。

```c
// $FreeBSD: /usr/src/lib/libc/stdio/fgetc.c
#include <stdio.h>

// $FreeBSD: /usr/src/lib/libc/Makefile
CFLAGS+=-I${.CURDIR}/include  # /usr/src/include
```

### Macros
{: .subtitle}

這篇[宏定義的黑魔法](https://onevcat.com/2014/01/black-magic-in-macro/)很有意思地解釋了一些macro的寫法和實現細節，當中的要點在GNU的[文檔](https://gcc.gnu.org/onlinedocs/cpp/Macros.html)中都有詳細的介紹和分類，譬如把macros分為object-like和function-like。其中存在比較多pitfalls的是function-like macros。

```#ifdef/ifndef ```只測試單個object，```#if ```測試後面的表達式，適用於多個條件的組合。

```#pragma ```的意思是pragmatic，作用是與編譯器交互。Clang的[文檔](http://clang.llvm.org/docs/UsersManual.html#diagnostics_pragmas)列出了詳細的可選項。

### 指針變量
{: .subtitle}

按照優先級、左結合規則確定指針變量類型，去掉變量名即對應的指針類型：

```c
int *p[10]; // is an array of type "int *"
size_t (*p)[10]; // is a pointer of an array
size_t (*fp[3])(int); // is an array of function pointers
```

指針類型用來定義變量、強制類型轉換、函數參數。習慣上用```typedef```+指針類型簡化變量聲明：

```c
typedef size_t (*pf)(char);
pf oprations[10];
```

- 函數名(function designator)會被隱式轉換為函數指針；
- 函數不能返回function、array(C++ dcl.fct)；
- 函數聲明中不帶參數要顯式聲明為```void```；
- 賦值到函數指針變量會隱式轉換，但建議通過指針操作符實現；

```c
// 參數部分帶參數名，類型列表隻有類型
size_t (*pf(char)) (double, double);
size_t (*pf(char const op)) (double, double)
{
    if (op == '+') return &plus;
    else if (op == '-') return &minus;
    else return (size_t (*) (double, double))NULL;
}
```

由於函數名會隱式轉換成指針，所以複雜函數類似指針變量，通過去掉函數體聲明確定函數(指針)類型。函數體由變量名+參數列表組成。

在C標準中，type cast函數指針結果是undefined behavior。ObjC runtime中有個用來做變參函數適配的例子：

```c
id msg_Send(id, SEL, ...);
{ return ((id (*)(id, SEL))msg_Send)(self, sel); }
{ return ((id (*)(id, SEL, obj)msg_Send)(self, sel, obj); }
```

### Code organization
{: .subtitle}

使用```#pragma mark```在Xcode中添加分割線和註記，方便瀏覽和跳轉：

```objc
//添加分割線，不可跟空格
#pragma mark -
//添加註記
#pragma mark *LABEL*

// or
#pragma mark - *LABEL*
```

不過在Xcode 4.6.3中```#pragma mark```緊跟```@implementation```沒有效果，可能因為舊版本Xcode自動indent類函數名顯示為次級列表而忽略掉首個notation，添加一個空block作為第一層次級列表條目間隔開就正常顯示了。

```objc
// No divider
@implementation Foo
#pragma mark -

// Got a divider
@implementation Foo {}
#pragma mark -
```

在註釋中使用```TODO:```、```FIXME:```和```MARK:```也可以在navigation中顯示和跳轉。

### Building
{: .subtitle}

使用```xcodebuild```命令編譯時需要指定scheme、target、project和workspace，官方[文檔](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Targets.html)對此有詳細介紹。如其開篇所言，與編譯過程關係最密切的是target。通過設置targets之間的依賴關係來實現project內的分庫聯合編譯，projects之間的聯合編譯通過放入同一個workspace之中再設置其依賴關係來實現。

另外很多開源工程使用了GNU套件來管理project，這篇[The GNU configure and build system](https://airs.com/ian/configure/)是難得的佳作，詳細介紹了autoconf等工具的歷史和用法。使用對應的工具生成Makefile之後就可以用在Xcode中的編譯了。
