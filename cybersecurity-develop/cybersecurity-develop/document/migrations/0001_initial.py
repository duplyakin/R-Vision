# Generated by Django 3.1.5 on 2021-01-30 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Attribute name')),
                ('is_required', models.BooleanField(default=False, verbose_name='Is required')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_name', models.CharField(max_length=255, null=True, unique=True, verbose_name='Original name')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Description')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/', verbose_name='File path')),
                ('mime_type', models.CharField(max_length=50, null=True, verbose_name='Mime type')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Is processed')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type_name', models.CharField(max_length=255, null=True, verbose_name='Document type')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
            ],
            options={
                'db_table': 'document_document_type',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, unique=True, verbose_name='Status name')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Description')),
                ('color', models.CharField(blank=True, max_length=10, null=True, verbose_name='Color')),
                ('is_detail', models.BooleanField(default=True, verbose_name='Is detail')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Ocr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocr_text', models.TextField(blank=True, max_length=1000, null=True, verbose_name='OCR text')),
                ('user_text', models.TextField(blank=True, max_length=1000, null=True, verbose_name='User text')),
                ('status', models.SmallIntegerField(blank=True, default=2, null=True, verbose_name='Status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.document')),
            ],
        ),
        migrations.CreateModel(
            name='Nlp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=None, null=True, verbose_name='Position')),
                ('ocr_word_ids', models.JSONField(blank=True, default=None, null=True, verbose_name='OCR word IDs')),
                ('status', models.SmallIntegerField(choices=[(0, 'Not recognized'), (1, 'Recognized'), (2, 'Operator recognized'), (3, 'Operator add attribute with word ids'), (4, 'New attribute')], default=0, verbose_name='Status')),
                ('ocr_text', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Ocr text')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated date')),
                ('attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.attribute')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.documenttype'),
        ),
        migrations.AddField(
            model_name='document',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.status'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document.documenttype'),
        ),
    ]
