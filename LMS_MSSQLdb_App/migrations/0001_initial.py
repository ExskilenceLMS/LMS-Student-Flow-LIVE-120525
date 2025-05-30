# Generated by Django 4.1.13 on 2025-05-12 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='batches',
            fields=[
                ('batch_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('batch_name', models.CharField(max_length=50)),
                ('delivery_type', models.CharField(choices=[('Online', 'Online'), ('In-person', 'In-person'), ('Hybrid', 'Hybrid')], max_length=50)),
                ('max_no_of_students', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('indicative_date', models.DateTimeField()),
                ('saturday_holiday', models.BooleanField(blank=True, default=False)),
                ('sunday_holiday', models.BooleanField(blank=True, default=False)),
                ('hours_per_day', models.IntegerField(default=0)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'batches',
            },
        ),
        migrations.CreateModel(
            name='college_details',
            fields=[
                ('college_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('college_name', models.CharField(max_length=50)),
                ('center_name', models.CharField(max_length=20)),
                ('college_code', models.CharField(max_length=20)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'college_details',
            },
        ),
        migrations.CreateModel(
            name='courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20, unique=True)),
                ('course_name', models.CharField(max_length=50)),
                ('course_description', models.TextField()),
                ('course_level', models.CharField(max_length=20)),
                ('Existing_Subjects', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_at', models.DateTimeField()),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('tracks', models.TextField(blank=True, default=None, null=True)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='questions',
            fields=[
                ('question_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('question_type', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=100)),
                ('creation_time', models.DateTimeField()),
                ('last_updated_time', models.DateTimeField()),
                ('last_updated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('reviewed_by', models.CharField(blank=True, max_length=20, null=True)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='students_info',
            fields=[
                ('student_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('student_firstname', models.CharField(max_length=100)),
                ('student_lastname', models.CharField(max_length=100)),
                ('student_email', models.EmailField(max_length=254, unique=True)),
                ('student_country', models.CharField(max_length=100)),
                ('student_state', models.CharField(max_length=100)),
                ('student_city', models.CharField(max_length=100)),
                ('student_gender', models.CharField(max_length=10)),
                ('student_course_starttime', models.DateTimeField(null=True)),
                ('student_pincode', models.CharField(max_length=20)),
                ('student_alt_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('student_dob', models.DateField(default=None, null=True)),
                ('student_qualification', models.CharField(max_length=100)),
                ('college', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('student_score', models.CharField(default=0, max_length=20)),
                ('student_total_score', models.CharField(default=0, max_length=20)),
                ('student_catogory', models.CharField(choices=[('SUN', 'SUN'), ('MOON', 'MOON'), ('STAR', 'STAR')], default='STAR', max_length=20)),
                ('student_college_rank', models.IntegerField(default=-1)),
                ('student_overall_rank', models.IntegerField(default=-1)),
                ('student_type', models.CharField(max_length=20)),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True)),
                ('leetcode', models.CharField(blank=True, max_length=100, null=True)),
                ('hackerrank', models.CharField(blank=True, max_length=100, null=True)),
                ('allocate', models.BooleanField(default=False)),
                ('del_row', models.BooleanField(default=False)),
                ('student_CGPA', models.FloatField(default=0.0)),
                ('batch_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.batches')),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.courses')),
            ],
            options={
                'db_table': 'students_info',
            },
        ),
        migrations.CreateModel(
            name='subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=20, unique=True)),
                ('subject_name', models.TextField()),
                ('subject_alt_name', models.TextField()),
                ('subject_description', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_at', models.DateTimeField()),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'subjects',
            },
        ),
        migrations.CreateModel(
            name='suite_login_details',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_first_name', models.CharField(max_length=100)),
                ('user_last_name', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('activity_status', models.CharField(max_length=20)),
                ('category', models.JSONField(blank=True, default=list)),
                ('reg_date', models.DateTimeField()),
                ('exp_date', models.DateTimeField(blank=True, null=True)),
                ('access', models.JSONField(blank=True, default=list)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'suite_login_details',
            },
        ),
        migrations.CreateModel(
            name='tracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(max_length=20, unique=True)),
                ('track_name', models.CharField(max_length=50)),
                ('track_name_searchable', models.CharField(max_length=50)),
                ('track_description', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_at', models.DateTimeField()),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tracks',
            },
        ),
        migrations.CreateModel(
            name='trainers',
            fields=[
                ('trainer_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('trainer_name', models.CharField(max_length=100)),
                ('trainer_email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('trainer_type', models.CharField(max_length=20)),
                ('linkedin', models.CharField(blank=True, max_length=100, null=True)),
                ('leetcode', models.CharField(blank=True, max_length=100, null=True)),
                ('hackerrank', models.CharField(blank=True, max_length=100, null=True)),
                ('del_row', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'trainers',
            },
        ),
        migrations.CreateModel(
            name='trainer_review_comments',
            fields=[
                ('comment_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('review_type', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=20)),
                ('comment', models.CharField(max_length=20)),
                ('date_time', models.DateTimeField()),
                ('del_row', models.BooleanField(default=False)),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.students_info')),
                ('trainer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.trainers')),
            ],
            options={
                'db_table': 'trainer_review_comments',
            },
        ),
        migrations.CreateModel(
            name='topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.CharField(max_length=20, unique=True)),
                ('topic_name', models.CharField(max_length=50)),
                ('topic_alt_name', models.CharField(blank=True, max_length=50, null=True)),
                ('topic_description', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_at', models.DateTimeField()),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('del_row', models.BooleanField(default=False)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.subjects')),
            ],
            options={
                'db_table': 'topics',
            },
        ),
        migrations.CreateModel(
            name='test_details',
            fields=[
                ('test_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('test_name', models.CharField(max_length=50)),
                ('test_duration', models.CharField(max_length=20)),
                ('test_marks', models.IntegerField()),
                ('test_type', models.CharField(max_length=20)),
                ('test_description', models.CharField(max_length=250)),
                ('test_created_by', models.EmailField(default=None, max_length=254, null=True)),
                ('topic_id', models.JSONField(blank=True, default=list)),
                ('level', models.CharField(max_length=20)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('test_date_and_time', models.DateTimeField(default=None, null=True)),
                ('test_created_date_time', models.DateTimeField(default=None, null=True)),
                ('del_row', models.BooleanField(default=False)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.courses')),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.subjects')),
                ('track_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.tracks')),
            ],
            options={
                'db_table': 'test_details',
            },
        ),
        migrations.AddField(
            model_name='subjects',
            name='track_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.tracks'),
        ),
        migrations.CreateModel(
            name='sub_topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_topic_id', models.CharField(max_length=20, unique=True)),
                ('sub_topic_name', models.CharField(max_length=50)),
                ('sub_topic_description', models.TextField()),
                ('sub_topic_alt_name', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.IntegerField(blank=True, null=True)),
                ('videos', models.IntegerField(blank=True, null=True)),
                ('mcq', models.IntegerField(blank=True, null=True)),
                ('coding', models.IntegerField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_at', models.DateTimeField()),
                ('action', models.CharField(blank=True, max_length=100, null=True)),
                ('del_row', models.BooleanField(default=False)),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.topics')),
            ],
            options={
                'db_table': 'sub_topics',
            },
        ),
        migrations.CreateModel(
            name='students_assessments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_type', models.CharField(max_length=20)),
                ('assessment_status', models.CharField(choices=[('Pending', 'Pending'), ('Started', 'Started'), ('Completed', 'Completed')], max_length=20)),
                ('assessment_score_secured', models.FloatField()),
                ('assessment_max_score', models.FloatField()),
                ('assessment_week_number', models.IntegerField(default=None, null=True)),
                ('assessment_completion_time', models.DateTimeField(default=None, null=True)),
                ('assessment_rank', models.IntegerField(default=None, null=True)),
                ('assessment_overall_rank', models.IntegerField(default=None, null=True)),
                ('student_duration', models.FloatField(default=0)),
                ('student_test_completion_time', models.DateTimeField(default=None, null=True)),
                ('student_test_start_time', models.DateTimeField(default=None, null=True)),
                ('del_row', models.BooleanField(default=False)),
                ('course_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.courses')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.students_info')),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.subjects')),
                ('test_id', models.ForeignKey(db_column='Test_id', on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.test_details')),
            ],
            options={
                'db_table': 'students_assessments',
            },
        ),
        migrations.CreateModel(
            name='student_test_questions_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=20)),
                ('score_secured', models.FloatField(default=0)),
                ('question_status', models.CharField(choices=[('Attempted', 'Attempted'), ('Pending', 'Pending'), ('Submitted', 'Submitted')], max_length=20)),
                ('max_score', models.FloatField(default=0)),
                ('week_number', models.IntegerField(default=0, null=True)),
                ('completion_time', models.DateTimeField(default=None, null=True)),
                ('student_answer', models.TextField(default=None, null=True)),
                ('del_row', models.BooleanField(default=False)),
                ('question_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.questions')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.students_info')),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.subjects')),
                ('test_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.test_details')),
            ],
            options={
                'db_table': 'student_test_questions_details',
            },
        ),
        migrations.CreateModel(
            name='student_app_usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logged_in', models.DateTimeField()),
                ('logged_out', models.DateTimeField()),
                ('del_row', models.BooleanField(default=False)),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.students_info')),
            ],
            options={
                'db_table': 'student_app_usage',
            },
        ),
        migrations.CreateModel(
            name='student_activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_end_time', models.DateTimeField()),
                ('activity_week', models.IntegerField()),
                ('activity_day', models.IntegerField()),
                ('del_row', models.BooleanField(default=False)),
                ('activity_subtopic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.sub_topics')),
                ('activity_topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.topics')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.students_info')),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.subjects')),
            ],
            options={
                'db_table': 'student_activities',
            },
        ),
        migrations.AddField(
            model_name='questions',
            name='sub_topic_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.sub_topics'),
        ),
        migrations.CreateModel(
            name='course_subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_in_days', models.CharField(max_length=20)),
                ('start_date', models.DateTimeField(default=None)),
                ('end_date', models.DateTimeField(default=None)),
                ('is_mandatory', models.BooleanField()),
                ('path', models.CharField(max_length=250)),
                ('del_row', models.BooleanField(default=False)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.courses')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.subjects')),
            ],
            options={
                'db_table': 'course_subjects',
            },
        ),
        migrations.CreateModel(
            name='course_plan_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('content_type', models.CharField(max_length=20)),
                ('week', models.IntegerField()),
                ('day_date', models.DateTimeField()),
                ('duration_in_hours', models.IntegerField()),
                ('del_row', models.BooleanField(default=False)),
                ('batch_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.batches')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.courses')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.subjects')),
            ],
            options={
                'db_table': 'course_plan_details',
            },
        ),
        migrations.CreateModel(
            name='branch_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_id', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=20)),
                ('del_row', models.BooleanField(default=False)),
                ('college_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.college_details')),
            ],
            options={
                'db_table': 'branch_details',
            },
        ),
        migrations.AddField(
            model_name='batches',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.courses'),
        ),
        migrations.CreateModel(
            name='test_sections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.IntegerField()),
                ('section_name', models.CharField(max_length=20)),
                ('del_row', models.BooleanField(default=False)),
                ('question_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.questions')),
                ('sub_topic_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.sub_topics')),
                ('test_id', models.ForeignKey(db_column='Test_id', on_delete=django.db.models.deletion.CASCADE, to='LMS_MSSQLdb_App.test_details')),
                ('topic_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='LMS_MSSQLdb_App.topics')),
            ],
            options={
                'db_table': 'test_sections',
                'unique_together': {('test_id', 'question_id')},
            },
        ),
    ]
