# Yet most Elegant TeX

Elegant TeX script in YAML style

## Introduction

(Note: the below paragraph is opinionated, and so is this project)

Doubtless, documents typesetted with TeX are elegant from their beginning.
However, TeX script are usually not. That's why you need YeT.

* You Only Write Once: Just `environ:`. No more `\egin{environ}~\end{environ}`!
* Syntactical Definition: Works out-of-box for *any* TeX packages without configuration
* Easy Fallback: TeX script can be easily mixed into YeT script
* Intuitive: Reading the below example will be enough for you to get the most out of YeT

## Example

```yaml
# examples/front.yml
documentclass: article[a4paper]
usepackage: amsmath
usepackage: amssymb

title: YeT Example
author: BayMinimum

document:
  - \maketitle  # or maketitle: ""
  - Let's begin with some math.
  - equation:
    - F = \frac{1}{4 \pi \epsilon_0} \frac{q_1 q_2}{r^2}
  - enumerate:
      item: This is enumerate
      item: Write items in dict or list
  - some_custom_environment{arg}[optional]:
    - Key with dict or list value is interpreted as environment.
    - This works syntactically, without semantics.
```
