from django.db import models


from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(max_length=100, verbose_name="昵称", null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name="手机", null=True, blank=True)
    modified_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = '用户表'

    def __str__(self):
        return self.user.__str__()


class Elements(models.Model):
    symbol = models.CharField(max_length=30, verbose_name="元素符号")
    cn_name = models.CharField(max_length=30, verbose_name="中文名称", default='')
    en_name = models.CharField(max_length=30, verbose_name="英文名称", default='')
    pinyin = models.CharField(max_length=30, verbose_name="拼音", null=True, blank=True)
    atomic_number = models.IntegerField(verbose_name="原子序数")
    relative_atomic_mass = models.CharField(default='0.00', max_length=20, verbose_name="相对原子质量")
    element_type = models.IntegerField(default=1, verbose_name="元素类型", null=True, blank=True)
    atomic_radius_type = models.IntegerField(default=1, verbose_name="原子半径类型", null=True, blank=True)
    atomic_radius = models.CharField(max_length=100, verbose_name="原子半径大小", null=True, blank=True)
    outer_electron = models.CharField(max_length=100, verbose_name="外层电子数", null=True, blank=True)
    electron_configuration = models.CharField(max_length=100, verbose_name="电子排布", null=True, blank=True)
    electronegativity = models.TextField(default='', verbose_name="电负性", null=True, blank=True)
    electronic_affinity = models.CharField(default='', max_length=100, verbose_name="电子亲和能", null=True, blank=True)
    introduction = models.TextField(verbose_name="元素简介", null=True, blank=True)
    extra = models.TextField(verbose_name="额外信息", null=True, blank=True)
    relate_video = models.TextField(verbose_name="相关视频", null=True, blank=True)
    relate_video_name = models.TextField(verbose_name="相关视频名称", null=True, blank=True)
    color = models.CharField(default="", max_length=100, verbose_name="卡片颜色", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    across = models.CharField(default="", max_length=20, verbose_name="横向位置", null=True, blank=True)
    vertical = models.CharField(default="", max_length=20, verbose_name="纵向位置", null=True, blank=True)
    discovery_year = models.CharField(default="", max_length=20, verbose_name="发现年份", null=True, blank=True)

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
    dark_color = models.CharField(default="", max_length=100, verbose_name="深颜色")
    light_color = models.CharField(default="", max_length=100, verbose_name="浅颜色")
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


class ElementHistory(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    year = models.CharField(max_length=100, verbose_name="年份")
    scientist = models.CharField(max_length=100, verbose_name="科学家")
    img = models.TextField(verbose_name="图片", blank=True, null=True)
    introduction = models.TextField(verbose_name="介绍")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    sort = models.IntegerField(verbose_name="排序", default=999)

    def __unicode__(self):
        return self.ele.cn_name + '元素发现史'

    class Meta:
        verbose_name = "元素发现史"
        verbose_name_plural = "元素发现史列表"


class ElementRepresentative(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    pro_name = models.CharField(max_length=50, verbose_name="教授名")
    university = models.CharField(max_length=50, verbose_name="大学")
    country = models.CharField(max_length=50, verbose_name="国家")
    duty = models.TextField(verbose_name="任职", null=True)
    top_color = models.CharField(max_length=50, verbose_name="导航栏颜色", null=True)
    main_color = models.CharField(max_length=50, verbose_name="主体颜色", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '元素代言人'

    class Meta:
        verbose_name = "元素代言人"
        verbose_name_plural = "元素代言人列表"


class ElementRepresentativeItem(models.Model):
    representative = models.ForeignKey(ElementRepresentative, verbose_name="对应代言人", on_delete=None)
    title = models.CharField(max_length=50, verbose_name="标题")
    img_info = models.TextField(verbose_name="图片信息")
    img_type = models.IntegerField(verbose_name="图片类别")
    introduction = models.TextField(verbose_name="介绍")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.representative.ele.cn_name + '元素代言人条目'

    class Meta:
        verbose_name = "元素代言人条目"
        verbose_name_plural = "元素代言人条目列表"


class ElementIsotope(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    stable_isotope = models.TextField(verbose_name="稳定同位素")
    guide = models.TextField(verbose_name="开头引导")
    introduction = models.TextField(verbose_name="介绍")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '同位素'

    class Meta:
        verbose_name = "同位素"
        verbose_name_plural = "同位素列表"


class ElementMaterial(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    other_name = models.CharField(max_length=50, verbose_name="别名")
    other_en_name = models.CharField(max_length=50, verbose_name="英文别名")
    has_allotrope = models.BooleanField(verbose_name="是否有同素异形体", default=False)
    allotrope = models.TextField(verbose_name="单质介绍或同素异形体")
    structure_img = models.TextField(verbose_name="结构图", null=True, blank=True)
    application = models.TextField(verbose_name="应用")
    introduction = models.TextField(verbose_name="单质介绍")
    experiment_video = models.TextField(verbose_name="实验视频", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    melting_point = models.CharField(default="", max_length=50, verbose_name="熔点", null=True, blank=True)
    boiling_point = models.CharField(default="", max_length=50, verbose_name="沸点", null=True, blank=True)
    density = models.CharField(default="", max_length=50, verbose_name="密度", null=True, blank=True)
    caloric = models.CharField(default="", max_length=50, verbose_name="热值", null=True, blank=True)
    chemical_formula = models.CharField(default="", max_length=50, verbose_name="化学式", null=True, blank=True)
    relative_molecular_mass = models.CharField(default="", max_length=50, verbose_name="化学式量", null=True, blank=True)
    compound = models.CharField(verbose_name="化合物名称", max_length=50, null=True, blank=True)
    is_compound = models.BooleanField(verbose_name="是否为化合物", default=False)

    def __unicode__(self):
        return self.ele.cn_name + '——物质'

    class Meta:
        verbose_name = "物质"
        verbose_name_plural = "物质列表"


class ElementPoem(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    poem = models.TextField(verbose_name="中文诗")
    en_poem = models.TextField(verbose_name="英文诗", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——三行诗'

    class Meta:
        verbose_name = "三行诗"
        verbose_name_plural = "三行诗列表"


class ElementLovePoem(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    poem = models.TextField(verbose_name="情诗")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——情诗'

    class Meta:
        verbose_name = "情诗"
        verbose_name_plural = "情诗列表"


class ElementIdiom(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    idiom = models.CharField(max_length=50, verbose_name="成语", null=True)
    pre_idiom = models.CharField(max_length=50, verbose_name="来源成语", null=True)
    introduction = models.TextField(verbose_name="简介", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——成语'

    class Meta:
        verbose_name = "成语"
        verbose_name_plural = "元素成语列表"


class ElementNameSource(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    category = models.IntegerField(verbose_name="分类", null=True)
    introduction = models.TextField(verbose_name="简介", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——命名来源'

    class Meta:
        verbose_name = "命名来源"
        verbose_name_plural = "元素命名来源列表"


class ElementCartoon(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    cn_introduction = models.TextField(verbose_name="中文简介", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——卡通'

    class Meta:
        verbose_name = "卡通"
        verbose_name_plural = "元素卡通列表"


class ElementCollection(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    introduction = models.TextField(verbose_name="简介", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——收藏'

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = "元素收藏列表"


class ElementJingle(models.Model):
    ele = models.ForeignKey(Elements, verbose_name="对应元素", on_delete=None)
    jingle = models.TextField(verbose_name="顺口溜", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.ele.cn_name + '——顺口溜'

    class Meta:
        verbose_name = "顺口溜"
        verbose_name_plural = "元素顺口溜列表"


class PageIndex(models.Model):
    index = models.IntegerField(verbose_name="排序", null=True)
    en_name = models.CharField(max_length=50, verbose_name="网页英文名")
    cn_name = models.CharField(max_length=50, verbose_name="网页中文名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.cn_name

    class Meta:
        verbose_name = "周期表排序"
        verbose_name_plural = "周期表排序列表"


class HiTheater(models.Model):
    hua = models.CharField(max_length=50, verbose_name="漫画话数")
    title = models.CharField(max_length=100, verbose_name="漫画标题")
    type = models.IntegerField(verbose_name="漫画类型", default=1)
    introduction = models.TextField(verbose_name="介绍", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "嗨元素长漫画"
        verbose_name_plural = "嗨元素长漫画列表"


class HiWallpaper(models.Model):
    sort = models.IntegerField(verbose_name="排序", null=True)
    file_name = models.CharField(max_length=200, verbose_name="文件名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.file_name

    class Meta:
        verbose_name = "嗨元素壁纸"
        verbose_name_plural = "嗨元素壁纸列表"


class IMG(models.Model):
    img = models.ImageField(upload_to='upload/')
    name = models.CharField(max_length=50, verbose_name="图片名")
    source = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.img.url

    class Meta:
        verbose_name = "上传图片"
        verbose_name_plural = "上传图片列表"
