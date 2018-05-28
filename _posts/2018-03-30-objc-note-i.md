---
layout: post
title: "ObjC筆記I：Misc"
date: 2018-03-30
---

### The “static”
{: .subtitle}

“A static function/variable is only 'seen' within translation unit.”<!-- more --> C語言中默認global，於是```static```被當成private使用。

### 常量定義
{: .subtitle}

在頭文件中聲明，在源文件中定義：

```objc
// config.h
FOUNDATION_EXTERN NSString * const GREETING;
// config.c
NSString * const GREETING = @"Hello, world";
```

在C中定義字符串常量的指針變量用```const char *```修飾。

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
typedef size_t (*pf)[10];
pf ugly_func;
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

不過在Xcode 4.6.3中```#pragma mark```緊跟@```implementation```沒有效果，可能因為舊版本Xcode自動indent類函數名顯示為次級列表而忽略掉首個notation，添加一個空block作為第一層次級列表條目間隔開就正常顯示了。

```objc
// No divider
@implementation Foo
#pragma mark -

// Got a divider
@implementation Foo {}
#pragma mark -
```

在註釋中使用```TODO:```、```FIXME:```和```MARK:```也可以在Xcode中顯示和跳轉。
