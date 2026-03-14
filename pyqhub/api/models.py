import io

from django.db import models
from django.core.validators import FileExtensionValidator
from pdf2image import convert_from_path
from django.core.files.base import ContentFile


class Semester(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Semester {self.number}"
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name
    
class Paper(models.Model):

    MIDSEM = 'MIDSEM'
    ENDSEM = 'ENDSEM'

    EXAM_TYPE_CHOICES = [
        (MIDSEM, 'Midsem'),
        (ENDSEM, 'Endsem'),
    ]


    year = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    pdf = models.FileField(upload_to='papers/', validators=[FileExtensionValidator(["pdf"])])

    preview = models.ImageField(upload_to='previews/', null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-exam_type']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pdf and not self.preview:

            images = convert_from_path(self.pdf.path, first_page=1, last_page=1, poppler_path=r"C:\poppler-24.07.0\Library\bin")

            image = images[0]

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")

            file_name = f"{self.pk}_preview.jpg"

            self.preview.save(file_name, ContentFile(buffer.getvalue()), save=False)

            super().save(update_fields=["preview"])

    def __str__(self):
        return f"{self.subject.name} - {self.get_exam_type_display()} {self.year}"


# Create your models here.
