from django.db import models


class Elements(models.Model):
    symbol = models.CharField(max_length=30, verbose_name="元素符号")
    cn_name = models.CharField(max_length=30, verbose_name="中文名称", default='')
    atomic_number = models.IntegerField(verbose_name="原子序数")
    relative_atomic_mass = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name="相对原子质量")
    atomic_radius_type = models.IntegerField(default=1, verbose_name="原子半径类型")
    atomic_radius = models.CharField(max_length=100, verbose_name="原子半径大小")
    electronegativity = models.TextField(default='', verbose_name="电负性")
    electronic_affinity = models.CharField(default='', max_length=100, verbose_name="电子亲和能", blank=True)
    introduction = models.TextField(verbose_name="元素简介")
    extra = models.TextField(verbose_name="额外信息")
    color = models.CharField(default="", max_length=100, verbose_name="卡片颜色")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.symbol

    class Meta:
        verbose_name = "元素"
        verbose_name_plural = "元素列表"


class IonizationEnergy(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    energy = models.CharField(max_length=100, verbose_name="电离能")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.symbol + '电离能'

    class Meta:
        verbose_name = "电离能"


class VisitLog(models.Model):
    pages = models.CharField(max_length=100, verbose_name="访问页面")
    ip = models.GenericIPAddressField(verbose_name="访问IP")
    location = models.CharField(max_length=100, verbose_name="访问城市")
    time = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __unicode__(self):
        return self.ip + '访问' + self.pages

    class Meta:
        verbose_name = "访问记录"
        verbose_name_plural = "访问记录列表"


class HiElements(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    introduction = models.TextField(verbose_name="介绍")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '嗨元素'

    class Meta:
        verbose_name = "嗨元素"
        verbose_name_plural = "嗨元素列表"


class HiElementItems(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    img = models.CharField(max_length=100, verbose_name="图片")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '嗨元素条目'

    class Meta:
        verbose_name = "嗨元素条目"
        verbose_name_plural = "嗨元素条目列表"
