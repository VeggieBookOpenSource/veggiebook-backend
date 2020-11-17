
These classes specify the table structure and relationships.

If a primary key is not explicitly stated, then there is a column "id" for that table that is a unique id, that a "ForeignKey" points to.

If there is a "ManyToManyField" it means there an additional table with that relationship,  for example, recipebook_selection and recipebook_selections.


class String(models.Model):
    en = models.TextField()
    es = models.TextField(default='needs translation')
    needsTranslation = models.BooleanField(default=True, db_index=True)

class Attribute(models.Model):
    name = models.CharField(max_length=24, primary_key=True)


class Annotation(models.Model):
    en_img = models.ForeignKey(StockPhoto, related_name='en_img', blank=True, null=True)
    es_img = models.ForeignKey(StockPhoto, related_name='es_img', blank=True, null=True)
    text = models.ForeignKey(String, related_name='annotation', default=1)
    color = models.CharField(max_length=6, default="ffffff")

class RecipeAnnotation(models.Model):
    name = models.CharField(max_length=24, primary_key=True)

class Recipe(models.Model):
    recipeId = models.AutoField(primary_key=True)
    title = models.ForeignKey(String, related_name="title")
    isActive = models.BooleanField(default=True)
    storyLine = models.ForeignKey(String, related_name="storyline", blank=True, null=True)
    timeToPrepare = models.ForeignKey(String, related_name="timeToPrepare")
    timeToCook = models.ForeignKey(String, related_name="timeToCook")
    servings = models.ForeignKey(String, related_name="servings")
    canBeMadeAhead = models.ForeignKey(String, related_name="canBeMadeAhead")
    canBeFrozen = models.ForeignKey(String, related_name="canBeFrozen")
    goodForLeftovers = models.ForeignKey(String, related_name="goodForLeftovers")
    rid = models.CharField(max_length=6, blank=True, null=True)
    foodStuff = models.ForeignKey(FoodStuff, db_index=True)
    requirements = models.ManyToManyField(OrRequirement, blank=True, null=True)
    annotations = models.ManyToManyField(Annotation, blank=True, null=True)


class FoodPantry(Address):
    name = models.CharField(max_length=256)
    printingAvailable = models.BooleanField(default=False)
    printerEmail = models.EmailField(default="tdi2048cynp656@print.epsonconnect.com")

class RecipeBookSelection(models.Model):
    recipe = models.ForeignKey(Recipe)
    selected = models.BooleanField(default=True)
    extras = models.IntegerField(default=0)
    scrolled = models.BooleanField(default=False)

class RecipeBook(models.Model):
    user = models.ForeignKey(User, db_index=True)
    attributes = models.ManyToManyField(Attribute)
    selections = models.ManyToManyField(RecipeBookSelection)
    coverPhoto = models.ForeignKey(CoverPhoto)
    pantry = models.ForeignKey(FoodPantry, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    foodStuff = models.ForeignKey(FoodStuff, null=True, blank=True, default=None)
    pdf_en = models.FileField(upload_to='pdfs', null=True, blank=True)
    pdf_es = models.FileField(upload_to='pdfs', null=True, blank=True)


class SecretCategory(models.Model):
    title = models.ForeignKey(String, related_name="secretCategory")
    image = models.ImageField(upload_to="secretCat", blank=True, null=True)
    color = models.CharField(max_length=6, default="69d0ee")
    positionIndex = models.IntegerField(default=100)


class ExternalLink(models.Model):
    secret = models.ForeignKey('Secret')
    linkString = models.ForeignKey(String)
    LANGUAGE_CHOICES = ((u'en', u'Inglés'), (u'es', u'Español'),)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    url = models.URLField(verify_exists=True)


class Secret(models.Model):
    title = models.ForeignKey(String, related_name="secretTitle")
    category = models.ForeignKey(SecretCategory)
    isActive = models.BooleanField(default=True)
    image = models.ImageField(upload_to="secrets", blank=True, null=True)
    coverImage = models.ForeignKey('CoverPhoto', blank=True, null=True)
    coverImage_es = models.ForeignKey('CoverPhoto', blank=True, null=True, related_name="coverImage_es")
    secret = models.ForeignKey(String, related_name="secretText")
    whyItWorks = models.ForeignKey(String, related_name="whyItWorks")
    attachment_en = models.FileField(upload_to="secret_attachments", null=True, blank=True)
    attachment_es = models.FileField(upload_to="secret_attachments", null=True, blank=True)

class SecretBookSelection(models.Model):
    secret = models.ForeignKey(Secret)
    selected = models.BooleanField(default=True)
    extras = models.IntegerField(default=0)
    scrolled = models.BooleanField(default=False)

class SecretBook(models.Model):
    user = models.ForeignKey(User, db_index=True)
    selections = models.ManyToManyField(SecretBookSelection)
    coverPhoto = models.ForeignKey(CoverPhoto)
    pantry = models.ForeignKey(FoodPantry, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(SecretCategory, null=True, blank=True, default=None)
    pdf_en = models.FileField(upload_to='pdfs', null=True, blank=True)
    pdf_es = models.FileField(upload_to='pdfs', null=True, blank=True)
    who_says_so_viewed = models.BooleanField(default=False)


class RecipeData(models.Model):
    recipe = models.ForeignKey('Recipe')
    timeStamp = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User)
    event_choices = (('Share', 'S'), ('Viewed for 10 seconds', 'V'),)
    event = models.CharField(max_length=1, choices=event_choices)
    data = models.TextField(blank=True, null=True)


class SecretData(models.Model):
    secret = models.ForeignKey('Secret')
    timeStamp = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User)
    event_choices = (('Share', 'S'), ('Viewed for 10 seconds', 'V'),)
    event = models.CharField(max_length=1, choices=event_choices)
    data = models.TextField(blank=True, null=True)
