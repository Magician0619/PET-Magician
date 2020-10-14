> 在PET重建中所具有的系统矩阵为每个点所接收到电子的概率，从而判定该点应该有多少放射电子。 这里 *A(* *i* *, j)* 表示第 *j* 个像素发射的 光子对被第 *i* 个探测器接收的概率。   
> 根据PET的工作原理：实际的接收到的电子的数据（Y）=电子接受（发送）的概率矩阵（A）*人体内的放射性元素数量（向量X）；
> 即：
> $$
> Y=A*X
> $$
> 而将X根据各个点的放射性元素多少来分配明暗程度即可得到图像。因此求得X的过程即为求得图像过程。

# PET扫描泊松模型

## 1、ML-EM

极大似然最大期望法，Maximum-Likelihood Expectation-Maximization。通过已有的样本结果信息，反推最具有可能性导致这些样本结果出现的模型参数值。

> ML极大似然，假设先验概率分布式均匀的，我们根据已有的数据，对它属于某一类进行估计。估计的标准是，该参数或该类将令出现该数据的概率最大。EM最大期望，在所有隐变量未知的情况下，根据现有数据，估计出数据的分布参数（例如：混合高斯分布或者仅仅单一高斯分布），这是一种无监督聚类方法。其中包括了E步骤和M步骤

# ![image-20201014193648642](https://gitee.com/magician0619/picgo/raw/master/PET/20201014194105.png)

$$
Y_{i} \sim P\left(\sum_{j} A_{i j} X_{j}\right)
$$

其中，Y是线性响应率。系统响应矩阵$A$的元素$A_{ij}$表示在$LOR_{i}$处检测到像素点$j$发射的概率。



我们定义一个随机变量$C_{ij}$，它表示在$LOR_{i}$处$j$像素点检测放射物的计数。

$$
Z_{ij} \sim P\left(\sum_{j} A_{i j} X_{j}\right)
$$
并且，$ Y_{i} = \sum_{Z_{ij}}$				
					

## 2、ML

用似然函数构造目标函数（泊松分布概率公式）
$$
P\left(Z_{i j}=k\right)=\frac{\left(A_{i j} X_{j}\right)^{k} e^{-A_{i j} X_{j}}}{k !}
$$

假设已经知道$Z_{ij}$，并用$Z_{ij}$构造一个概率函数				
$$
L(X \mid Z)=\frac{\left(A_{i j} X_{j}\right)^{Z_{i j}} e^{-A_{i j} X_{j}}}{Z_{i j} !}
$$
取对数，并简化
$$
\ln (L(X \mid Z))=\sum_{i} \sum_{j}\left(-A_{i j} X_{j}+Z_{i j} \ln \left(A_{i j} X_{j}\right)\right)+\operatorname{const}
$$
由概率函数构建的泊松模型的目标函数
$$
\Phi(X)=\sum \sum\left(-A_{i j} X_{j}+Z_{i j} \ln \left(A_{i j} X_{j}\right)\right)
$$

## 3、EM

由于我们仍不知道概率$Z_{ij}$，使用EM算法可以求解目标函数。$Z_{ij}$的条件期望为：
$$
Z_{i j}=E\left(Z_{i j} \mid X^{k}\right)=Y_{i} \frac{A_{i j} X^{k}}{\sum_{j}  A_{i j} X^{k}}
$$

$X^{k}$是$k$次迭代的图像，$k+1$次的迭代为：
$$
X^{k+1}=X=X^{k} \frac{\sum_{i} A_{i j} \frac{Y_{i}}{\sum_{j} A_{i j} X_{j}^{k}}}{\sum_{i} A_{i j}}
$$

## 4、涉及到的系统响应的物理因素

几何结构、散射、随机偶然性、检测器性能

![QQ拼音截图20201014203449](https://gitee.com/magician0619/picgo/raw/master/PET/20201014203823.png)

# 

