from django.db import migrations


def forwards(apps, schema_editor):
    Movie = apps.get_model('api', 'Movie')
    Movie.objects.filter(imdb_id='').update(imdb_id=None)


def backwards(apps, schema_editor):
    # No safe backwards mapping (NULL -> empty string), keep as-is.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0006_booking_price_movie_rating'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
