from django.core import management

management.call_command('import_category')
management.call_command('import_genre', )
management.call_command('import_users', )
management.call_command('import_titles', )
management.call_command('import_genre_title', )
management.call_command('import_review', )
management.call_command('import_comments', )
