from django.db import models


class Elements(models.Model):
    symbol = models.CharField(max_length=30, verbose_name=u"元素符号")
    cn_name = models.CharField(max_length=30, verbose_name=u"中文名称", default='')
    atomic_number = models.IntegerField(verbose_name=u"原子序数")
    relative_atomic_mass = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name=u"相对原子质量")
    atomic_radius = models.CharField(max_length=100, verbose_name=u"原子半径")
    electronegativity = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name=u"电负性")
    electronic_affinity = models.CharField(default='', max_length=100, verbose_name=u"电子亲和能", blank=True)
    introduction = models.TextField(verbose_name=u"元素简介")
    extra = models.TextField(verbose_name=u"额外信息")
    color = models.CharField(default="", max_length=100, verbose_name=u"卡片颜色")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")

    def __unicode__(self):
        return self.symbol

    class Meta:
        verbose_name = u"元素"
        verbose_name_plural = u"元素列表"


class IonizationEnergy(models.Model):
    ele = models.ForeignKey(Elements, verbose_name='对应元素', on_delete=None)
    energy = models.CharField(max_length=100, verbose_name=u"电离能")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")

    def __unicode__(self):
        return self.ele.symbol + '电离能'

    class Meta:
        verbose_name = u"电离能"


class VisitLog(models.Model):
    pages = models.CharField(max_length=100, verbose_name=u"访问页面")
    ip = models.GenericIPAddressField(verbose_name=u"访问IP")
    location = models.CharField(max_length=100, verbose_name=u"访问城市")
    time = models.DateTimeField(auto_now_add=True, verbose_name=u"访问时间")

    def __unicode__(self):
        return self.ip + '访问' + self.pages

    class Meta:
        verbose_name = u"访问记录"
        verbose_name_plural = u"访问记录列表"

