

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scraper", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="resume",
            old_name="job_title",
            new_name="title",
        ),
    ]
