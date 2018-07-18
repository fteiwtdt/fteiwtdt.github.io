---
layout: post
title: "Python筆記II：OOP"
date: 2018-05-27
---

### Attributes
{: .subtitle}

Python使用字典類型實現namespace，任意類和實例都可以keep私有的namespace，使得類與實例的namespace存在互相覆蓋的情況。<!-- more -->首先遇到的問題是使用dot notation訪問屬性的「attribute lookup process」。所謂「attributes」包含實例屬性「instance attributes」和類屬性「class attributes」。訪問實例屬性時會查找```obj.__dict__```。那麼如何訪問到```obj.__dict__```？在2.3之後的new style classes中，調用dot notation都會觸發```__getattribute__```（包括metaclass實例即class object）。實例的```__dict__```屬於descriptor，由此進入invoke descriptor的過程。

[Data Model](https://docs.python.org/2/reference/datamodel.html)一章中說明查找屬性的一般順序：首先查找實例，然後查找MRO類簇。New style classes在應用這個規則前首先上溯MRO類簇查找data descriptor。重寫```__getattribute__```時注意函數體內訪問```self```可能出現的無限遞歸。

```py
class S(M, N):

    def __getattribute__(self, attr):
        for cls in type(self).mro():
            descr = cls.__dict__.get(attr)
            if descr:
                break

        if (hasattr(descr, '__set__') or hasattr(descr, '__delete__')) \
           and hasattr(descr, '__get__'):
            return descr.__get__(self, type(self))
			
        if attr in self.__dict__:
            v = self.__dict__.get(attr)
            # Or only return `v` as default implementation?
            if hasattr(v, '__get__'):
                return v.__get__(self, type(self))
            return v
			
        if not (hasattr(descr, '__set__') or hasattr(descr, '__delete__')) \
           and hasattr(descr, '__get__'):
            return descr.__get__(self, type(self))
        elif descr: return descr

        raise AttributeError('Lookup failed with "%s"' % attr)
```

### Descriptor
{: .subtitle}

調用內置的```property```類總返回data descriptor對象，其```__set__```和```__delete__```都是空函數只拋出異常使得缺省都是只讀的，這也是實現只讀data descriptor的方式。實踐中使用data descriptor分兩種，讀取保存在實例或類中的變量。Python 3.x的[descriptor howto](https://docs.python.org/3.6/howto/descriptor.html)比舊版本清楚不少，[這裡](http://nbviewer.jupyter.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb)也有個不錯的示範。

### Metaclass
{: .subtitle}

Metaclass是“面向類對象編程”，輿之相關的是構造類的過程和訪問類屬性，提供了實現面向對象特性的函數和描述類擁有的元素，譬如提供```cls.__mro__```來上溯類簇。Python reference中提到訪問屬性時上溯除metaclass之外的類簇，不過訪問類簇首先要訪問metaclass。相比之下Lua更直接了當一點，通過上溯metaclass來實現繼承，這樣的做法倒很好地解釋了metaclass的作用。```type```類似```object```的工廠類或helper類，故成為所有metaclass的基類。

調用dot notation訪問attribute存在3種情況：1）```__dict__```的k-v pairs，2）descriptor，3）special methods。通過內置函數調用special methods不會通過```__getattribute__```。Python reference解釋原因在於metaclass也實現了同樣的方法，如果不繞過```__getattribute__```直接返回類對象的實現，會因訪問metaclass而返回其中的實現。這違背了Python查找attribute不訪問metaclass的原則，或所謂的“metaclass confusion”。Lua也存在類似的設計繞過metaclass。

Python訪問屬性複雜如此的原因看來源於dot notation從沿用C struct訪問內存的方式遷移到對函數求值。Lua每一次訪問以查找並調用```__index```函數為終點，Lisp訪問列表元素只通過函數```car```、```cdr```：在《*ANSI Common Lisp*》中提到這是函數式編程的方式。Lua習慣上緩存常用函數或模塊，在Python的sre中也可見到這樣的應用。
