from django.db import migrations, models


def normalize_avatar_paths(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        raw = user.avatar
        # Pega valor string do campo (ImageFieldFile -> .name)
        if hasattr(raw, 'name'):
            value = raw.name or ''
        else:
            value = str(raw) if raw else ''

        if not value:
            continue

        original = value

        # Possíveis formatos antigos:
        # 1. /media/avatars/file.png
        # 2. avatars/file.png  (já ok)
        # 3. http(s)://host/media/avatars/file.png
        # 4. /media/avatars/default.png
        # 5. /media//avatars/file.png (duplicações ocasionais)

        # Remove prefixo / inicial redundante
        value = value.lstrip('/')

        # Se contiver 'media/avatars/' no início, remover 'media/'
        if value.startswith('media/avatars/'):
            value = value.replace('media/', '', 1)  # vira avatars/...

        # Se for URL completa
        if value.startswith('http://') or value.startswith('https://'):
            marker = '/media/avatars/'
            if marker in value:
                tail = value.split(marker, 1)[-1]
                value = f'avatars/{tail}' if not tail.startswith('avatars/') else tail
            # Caso não tenha marker, deixa como está (não sabemos estruturar) -> pula
            else:
                continue

        # Garante que começa por avatars/
        if 'avatars/' in value and not value.startswith('avatars/'):
            value = value[value.index('avatars/'):]

        if not value.startswith('avatars/'):
            # Não arriscamos sobrescrever com algo inesperado
            continue

        if value != original:
            user.avatar = value
            user.save(update_fields=['avatar'])


def reverse_normalize(apps, schema_editor):
    # Sem reverse exato (dados antigos já foram normalizados); operação idempotente
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/default.png', upload_to='avatars/'),
        ),
        migrations.RunPython(normalize_avatar_paths, reverse_normalize),
    ]
