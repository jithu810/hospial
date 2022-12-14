# Generated by Django 3.2.7 on 2022-12-14 08:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_imprint', models.CharField(blank=True, max_length=6, null=True)),
                ('drug_name', models.CharField(blank=True, max_length=50, null=True)),
                ('drug_color', models.CharField(blank=True, max_length=50, null=True)),
                ('drug_shape', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('receive_quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('reorder_level', models.IntegerField(blank=True, default='0', null=True)),
                ('manufacture', models.CharField(blank=True, max_length=50, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('drug_strength', models.CharField(blank=True, max_length=10, null=True)),
                ('valid_from', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('valid_to', models.DateTimeField(null=True)),
                ('drug_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('drug_pic', models.ImageField(blank=True, default='images2.png', null=True, upload_to='')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.category')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('prescribe', models.CharField(max_length=100, null=True)),
                ('date_precribed', models.DateTimeField(auto_now_add=True)),
                ('patient_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.patient')),
            ],
        ),
        migrations.CreateModel(
            name='PatientFeedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField(null=True)),
                ('feedback_reply', models.TextField(null=True)),
                ('admin_created_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
                ('pharmacist_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.pharmacist')),
            ],
        ),
        migrations.CreateModel(
            name='Dispense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispense_quantity', models.PositiveIntegerField(default='1', null=True)),
                ('taken', models.CharField(blank=True, max_length=300, null=True)),
                ('stock_ref_no', models.CharField(blank=True, max_length=300, null=True)),
                ('instructions', models.TextField(max_length=300, null=True)),
                ('dispense_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('drug_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.stock')),
                ('patient_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hospital.patient')),
            ],
        ),
    ]
